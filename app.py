import asyncio
import threading
from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3

import config
from config import settings
from browser_engine import OKXOrbitEngine


class OKXOrbitApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server, client_type="vue3")
        self.engine = OKXOrbitEngine()
        self._task_thread = None

        self.state.update(
            {
                "running": False,
                "status": "就绪",
                "logs": "",
                "comments_posted": 0,
                "template_type": "generic",
                "comment_count": 5,
                "min_delay": settings.MIN_DELAY,
                "max_delay": settings.MAX_DELAY,
                "headless": settings.BROWSER_HEADLESS,
                "template_types": ["generic", "bullish", "bearish", "neutral"],
                "selected_coins": [],
                "available_coins": [
                    f"{c['name']} ({c['symbol']})" for c in config.DEFAULT_COINS
                ],
            }
        )

        self.engine.set_callbacks(
            on_status=self._on_status,
            on_log=self._on_log,
        )

        self._build_ui()

    def _on_status(self, status: str):
        self.state.status = status

    def _on_log(self, message: str):
        current = self.state.logs
        self.state.logs = f"{message}\n{current}"[:5000]
        self.state.comments_posted = self.engine.comments_posted

    def _build_ui(self):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("OKX Orbit 自动评论机器人")
            self.ui.icon.hide()

            with self.ui.toolbar:
                v3.VSpacer()
                v3.VChip(
                    "{{ status }}",
                    color="primary",
                    variant="outlined",
                    size="small",
                )
                v3.VChip(
                    "已发布: {{ comments_posted }}",
                    color="success",
                    variant="flat",
                    size="small",
                    classes="ml-2",
                )

            with self.ui.content:
                with v3.VContainer(fluid=True):
                    with v3.VRow():
                        with v3.VCol(cols=6):
                            v3.VCard(
                                title="控制面板",
                                variant="outlined",
                            )
                            with v3.VCard():
                                with v3.VCardTitle() as title:
                                    title.set_text("控制面板")
                                    v3.VIcon("mdi-remote", classes="mr-2")

                                with v3.VCardText():
                                    with v3.VRow():
                                        with v3.VCol(cols=12):
                                            v3.VSelect(
                                                v_model=(
                                                    "template_type",
                                                    "generic",
                                                ),
                                                items=(
                                                    "template_types",
                                                    [
                                                        "generic",
                                                        "bullish",
                                                        "bearish",
                                                        "neutral",
                                                    ],
                                                ),
                                                label="评论模板类型",
                                                variant="outlined",
                                                density="compact",
                                            )

                                        with v3.VCol(cols=6):
                                            v3.VTextField(
                                                v_model_number=(
                                                    "comment_count",
                                                    5,
                                                ),
                                                label="评论数量",
                                                type="number",
                                                variant="outlined",
                                                density="compact",
                                                min=1,
                                                max=50,
                                            )

                                        with v3.VCol(cols=3):
                                            v3.VTextField(
                                                v_model_number=(
                                                    "min_delay",
                                                    30,
                                                ),
                                                label="最小延迟(秒)",
                                                type="number",
                                                variant="outlined",
                                                density="compact",
                                                min=5,
                                            )

                                        with v3.VCol(cols=3):
                                            v3.VTextField(
                                                v_model_number=(
                                                    "max_delay",
                                                    90,
                                                ),
                                                label="最大延迟(秒)",
                                                type="number",
                                                variant="outlined",
                                                density="compact",
                                                min=10,
                                            )

                                        with v3.VCol(cols=12):
                                            v3.VSwitch(
                                                v_model=(
                                                    "headless",
                                                    False,
                                                ),
                                                label="无头模式 (隐藏浏览器窗口)",
                                                color="primary",
                                                density="compact",
                                            )

                                    v3.VDivider(classes="my-4")

                                    with v3.VRow():
                                        with v3.VCol(cols=6):
                                            v3.VBtn(
                                                "启动并导航",
                                                color="primary",
                                                block=True,
                                                prepend_icon="mdi-play",
                                                click=self._start_browser,
                                                disabled=("running",),
                                            )

                                        with v3.VCol(cols=6):
                                            v3.VBtn(
                                                "停止",
                                                color="error",
                                                block=True,
                                                prepend_icon="mdi-stop",
                                                click=self._stop_browser,
                                                disabled=("!running",),
                                            )

                                    with v3.VRow(classes="mt-2"):
                                        with v3.VCol(cols=6):
                                            v3.VBtn(
                                                "检查登录状态",
                                                color="info",
                                                block=True,
                                                prepend_icon="mdi-account-check",
                                                click=self._check_login,
                                                disabled=("!running",),
                                            )

                                        with v3.VCol(cols=6):
                                            v3.VBtn(
                                                "开始自动评论",
                                                color="success",
                                                block=True,
                                                prepend_icon="mdi-comment-multiple",
                                                click=self._auto_comment,
                                                disabled=("!running",),
                                            )

                        with v3.VCol(cols=6):
                            with v3.VCard(variant="outlined"):
                                with v3.VCardTitle() as title:
                                    title.set_text("运行日志")
                                    v3.VIcon("mdi-text-box-multiple", classes="mr-2")

                                with v3.VCardText():
                                    v3.VTextarea(
                                        v_model=("logs", ""),
                                        readonly=True,
                                        variant="outlined",
                                        rows=20,
                                        auto_grow=False,
                                        density="compact",
                                    )

    def _run_async(self, coro):
        def _thread_target():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(coro)
            finally:
                loop.close()

        self._task_thread = threading.Thread(target=_thread_target, daemon=True)
        self._task_thread.start()

    def _start_browser(self):
        async def _do_start():
            await self.engine.start(headless=self.state.headless)
            await self.engine.navigate_to_feed()
            self.state.running = True

        self._run_async(_do_start())

    def _stop_browser(self):
        async def _do_stop():
            await self.engine.stop()
            self.state.running = False

        self._run_async(_do_stop())

    def _check_login(self):
        async def _do_check():
            if await self.engine.check_login_required():
                self.state.status = "需要登录，等待手动操作..."
                await self.engine.wait_for_manual_login()
            else:
                self.state.status = "已登录"

        self._run_async(_do_check())

    def _auto_comment(self):
        async def _do_comment():
            coins = config.DEFAULT_COINS
            if self.state.selected_coins:
                coins = [
                    config.DEFAULT_COINS[i]
                    for i, name in enumerate(self.state.available_coins)
                    if name in self.state.selected_coins
                ]

            await self.engine.auto_comment_loop(
                template_type=self.state.template_type,
                coins=coins,
                count=int(self.state.comment_count),
                delay_range=(
                    int(self.state.min_delay),
                    int(self.state.max_delay),
                ),
            )

        self._run_async(_do_comment())
