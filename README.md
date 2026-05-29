# OKX Orbit 自动评论机器人

基于 Trame + Playwright 的交互式自动化软件，用于在 OKX Orbit 社区自动发表模板化评论。

## 功能特性

- **交互式控制面板**：基于 Trame/Vuetify3 的现代化 Web UI
- **浏览器自动化**：Playwright 驱动，模拟真实用户操作
- **会话持久化**：登录状态自动保存，无需重复登录
- **模板化评论**：支持多种情绪模板（看涨/看跌/中性/通用）
- **随机延迟**：模拟人类行为，避免被检测
- **实时日志**：运行状态实时反馈

## 快速开始

### 1. 安装依赖

```bash
cd okx-orbit-bot
pip install -r requirements.txt
playwright install chromium
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件调整参数
```

### 3. 运行程序

```bash
python main.py
```

浏览器将自动打开，访问 `http://localhost:8080` 查看控制面板。

## 使用流程

1. 点击 **"启动并导航"** 打开 OKX Orbit 页面
2. 首次运行需手动登录 OKX 账户（后续自动恢复会话）
3. 选择评论模板类型和数量
4. 点击 **"开始自动评论"** 启动自动化

## 评论模板类型

| 类型 | 说明 |
|------|------|
| generic | 通用评论，适用于各种帖子 |
| bullish | 看涨情绪，适合热门上涨币种 |
| bearish | 看跌情绪，适合回调行情 |
| neutral | 中性讨论，引发互动 |

## 配置说明

在 `.env` 文件中可调整：

- `BROWSER_HEADLESS`：是否隐藏浏览器窗口（默认 false）
- `BROWSER_SLOW_MO`：操作间隔毫秒数（默认 100）
- `MIN_DELAY` / `MAX_DELAY`：评论间隔秒数（默认 30-90）
- `PAGE_LOAD_WAIT`：页面加载等待时间（默认 5000ms）

## 项目结构

```
okx-orbit-bot/
├── app.py              # Trame UI 应用
├── browser_engine.py   # Playwright 自动化引擎
├── config.py           # 配置和模板管理
├── main.py             # 入口文件
├── requirements.txt    # 依赖列表
├── .env.example        # 环境变量模板
└── sessions/           # 会话存储目录（自动创建）
```

## 依赖库

- **trame** - Python Web 应用框架
- **playwright** - 浏览器自动化
- **python-dotenv** - 环境变量管理

## 注意事项

- 请遵守 OKX 社区规范，合理使用自动化功能
- 建议设置合理的评论间隔，避免频繁操作
- 首次使用需手动登录，后续自动恢复会话
- 会话文件保存在 `sessions/` 目录，请勿泄露
