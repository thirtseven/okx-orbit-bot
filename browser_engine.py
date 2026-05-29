import asyncio
import random
import logging
from pathlib import Path
from typing import Callable, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class OKXOrbitEngine:
    def __init__(self):
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._running = False
        self._on_status: Optional[Callable] = None
        self._on_log: Optional[Callable] = None
        self._comments_posted = 0

    def set_callbacks(self, on_status: Callable = None, on_log: Callable = None):
        self._on_status = on_status
        self._on_log = on_log

    def _emit_status(self, status: str):
        logger.info(f"Status: {status}")
        if self._on_status:
            self._on_status(status)

    def _emit_log(self, message: str):
        logger.info(message)
        if self._on_log:
            self._on_log(message)

    async def start(self, headless: bool = False):
        self._emit_status("启动浏览器...")
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=headless,
            slow_mo=config.BROWSER_SLOW_MO,
        )

        if config.SESSION_FILE.exists():
            self._emit_log("检测到已保存的会话，正在恢复...")
            self._context = await self._browser.new_context(
                storage_state=str(config.SESSION_FILE),
                viewport={"width": 1280, "height": 800},
            )
        else:
            self._context = await self._browser.new_context(
                viewport={"width": 1280, "height": 800},
            )

        self._page = await self._context.new_page()
        self._page.set_default_timeout(config.BROWSER_TIMEOUT)
        self._running = True
        self._emit_status("浏览器已启动")

    async def stop(self):
        self._running = False
        if self._context:
            await self._context.storage_state(path=str(config.SESSION_FILE))
            self._emit_log("会话已保存")
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        self._emit_status("浏览器已关闭")

    async def navigate_to_feed(self):
        self._emit_status(f"正在导航到 OKX Orbit...")
        await self._page.goto(config.OKX_ORBIT_URL, wait_until="networkidle")
        await self._page.wait_for_timeout(config.PAGE_LOAD_WAIT)
        self._emit_status("已到达 OKX Orbit 页面")

    async def check_login_required(self) -> bool:
        login_selectors = [
            'button:has-text("登录")',
            'button:has-text("Log in")',
            'a[href*="login"]',
            '[data-testid="login-button"]',
        ]
        for selector in login_selectors:
            try:
                element = await self._page.query_selector(selector)
                if element and await element.is_visible():
                    return True
            except Exception:
                continue
        return False

    async def wait_for_manual_login(self, timeout_seconds: int = 300):
        self._emit_status("等待手动登录... (请在浏览器中完成登录)")
        self._emit_log("请在弹出的浏览器窗口中登录您的 OKX 账户")

        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < timeout_seconds:
            if not await self.check_login_required():
                await self._context.storage_state(path=str(config.SESSION_FILE))
                self._emit_status("登录成功！会话已保存")
                self._emit_log("登录成功，后续运行将自动恢复会话")
                return True
            await asyncio.sleep(2)

        self._emit_status("登录超时")
        return False

    async def find_comment_boxes(self) -> list:
        selectors = [
            '[data-testid="comment-input"]',
            'textarea[placeholder*="评论"]',
            'textarea[placeholder*="comment"]',
            'div[contenteditable="true"]',
            '.comment-input',
            'textarea',
        ]
        for selector in selectors:
            try:
                elements = await self._page.query_selector_all(selector)
                visible = [e for e in elements if await e.is_visible()]
                if visible:
                    return visible
            except Exception:
                continue
        return []

    async def post_comment(self, text: str) -> bool:
        try:
            comment_boxes = await self.find_comment_boxes()
            if not comment_boxes:
                self._emit_log("未找到评论框，尝试滚动页面...")
                await self._page.evaluate("window.scrollBy(0, 500)")
                await self._page.wait_for_timeout(1000)
                comment_boxes = await self.find_comment_boxes()

            if not comment_boxes:
                self._emit_log("无法找到评论框")
                return False

            box = comment_boxes[0]
            await box.click()
            await self._page.wait_for_timeout(500)
            await box.fill(text)
            await self._page.wait_for_timeout(500)

            submit_selectors = [
                'button:has-text("发布")',
                'button:has-text("发送")',
                'button:has-text("Post")',
                'button:has-text("Submit")',
                'button[type="submit"]',
                '[data-testid="comment-submit"]',
            ]

            for selector in submit_selectors:
                try:
                    btn = await self._page.query_selector(selector)
                    if btn and await btn.is_visible():
                        await btn.click()
                        self._comments_posted += 1
                        self._emit_log(f"评论发布成功: {text[:30]}...")
                        return True
                except Exception:
                    continue

            await self._page.keyboard.press("Enter")
            self._comments_posted += 1
            self._emit_log(f"评论发布成功 (Enter): {text[:30]}...")
            return True

        except Exception as e:
            self._emit_log(f"评论发布失败: {str(e)}")
            return False

    async def post_template_comment(
        self, template_type: str, coin: dict
    ) -> bool:
        templates = config.COMMENT_TEMPLATES.get(template_type, [])
        if not templates:
            self._emit_log(f"未找到模板类型: {template_type}")
            return False

        template = random.choice(templates)
        comment = template.format(
            coin=coin.get("name", ""),
            symbol=coin.get("symbol", ""),
            price=coin.get("price", ""),
            change=coin.get("change", ""),
        )
        return await self.post_comment(comment)

    async def auto_comment_loop(
        self,
        template_type: str = "generic",
        coins: list = None,
        count: int = 5,
        delay_range: tuple = None,
    ):
        if coins is None:
            coins = config.DEFAULT_COINS
        if delay_range is None:
            delay_range = (
                config.MIN_DELAY_BETWEEN_COMMENTS,
                config.MAX_DELAY_BETWEEN_COMMENTS,
            )

        self._emit_status(f"开始自动评论 (目标: {count} 条)")

        posted = 0
        attempts = 0
        max_attempts = count * 3

        while posted < count and self._running and attempts < max_attempts:
            attempts += 1
            coin = random.choice(coins)

            success = await self.post_template_comment(template_type, coin)
            if success:
                posted += 1
                self._emit_status(
                    f"进度: {posted}/{count} | 总计: {self._comments_posted}"
                )

            if posted < count:
                delay = random.uniform(*delay_range)
                self._emit_log(f"等待 {delay:.0f} 秒后继续...")
                await asyncio.sleep(delay)
                await self._page.evaluate("window.scrollBy(0, 300)")
                await self._page.wait_for_timeout(1000)

        self._emit_status(f"自动评论完成! 本次发布 {posted} 条")
        return posted

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def comments_posted(self) -> int:
        return self._comments_posted

    @property
    def page(self) -> Optional[Page]:
        return self._page
