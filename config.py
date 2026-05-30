from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    BROWSER_HEADLESS: bool = False
    BROWSER_SLOW_MO: int = 100
    BROWSER_TIMEOUT: int = 60000

    OKX_ORBIT_URL: str = "https://www.okx.com/zh-hans/orbit/feed"
    OKX_LOGIN_URL: str = "https://www.okx.com/login"

    MIN_DELAY: int = 30
    MAX_DELAY: int = 90
    PAGE_LOAD_WAIT: int = 5000

    @property
    def session_dir(self) -> Path:
        path = Path(__file__).parent / "sessions"
        path.mkdir(exist_ok=True)
        return path

    @property
    def session_file(self) -> Path:
        return self.session_dir / "okx_session.json"

    @property
    def log_file(self) -> Path:
        return Path(__file__).parent / "bot.log"


settings = Settings()


COMMENT_TEMPLATES = {
    "bullish": [
        "{coin} ({symbol}) 看起来要起飞了！技术面突破关键阻力位，目标价看到更高！🚀",
        "刚加仓了 {coin}，周线形态非常好，期待后续表现！💪",
        "{coin} 今天涨了 {change}，牛市的味道越来越浓了！🐂",
        "一直在关注 {coin}，基本面扎实，长期看好！💎🙌",
        "{coin} 社区越来越活跃了，生态发展势头强劲！",
        "ICE携手OKX达成深度合作，{coin} 这波行情含金量拉满！🔥",
        "传统金融正式杀入币圈！{coin} 作为核心资产，配置价值凸显！",
        "监管风口在转，{coin} 这个位置磨得越久，后续爆发力越强！",
        "布林带收窄是变盘前兆，{coin} 单边行情即将出现，坐稳扶好！",
        "MACD金叉确认，{coin} 短期多头动能开始凝聚，目标看前高！",
    ],
    "bearish": [
        "{coin} ({symbol}) 短期回调是正常现象，逢低布局的好机会。",
        "市场调整中，{coin} 的支撑位在关键位置，耐心等待企稳。",
        "{coin} 跌了 {change}，但长期趋势不变，继续持有。",
        "日线仍在下跌通道，{coin} 反弹为弱势修复，注意仓位管理。",
        "缩量反弹持续性存疑，{coin} 关键分水岭位置，跌破则下探支撑。",
        "行情波动幅度更大，{coin} 上方压力明显，建议保持谨慎思路。",
    ],
    "neutral": [
        "{coin} ({symbol}) 最近走势比较震荡，建议观望为主。",
        "研究了一下 {coin} 的白皮书，项目理念很有意思。",
        "大家怎么看 {coin} 后续的走势？欢迎讨论！",
        "{coin} 的技术更新进展如何？有了解的朋友吗？",
        "今天学习了 {coin} 的机制，涨知识了！📚",
        "关键位分析：{coin} 短线支撑在当前价位附近，强压位需放量突破。",
        "地缘局势不断变化，{coin} 作为当下热门赛道，随时能进场对冲。",
        "市场增量资金匮乏，{coin} 联动大盘来回震荡，反弹空间有限。",
    ],
    "generic": [
        "好文分享！学习了 🔥",
        "感谢分享，很有见地！👏",
        "涨知识了，收藏！📌",
        "分析得很到位，感谢楼主！💯",
        "继续关注后续发展 👀",
        "这个角度很独特，受教了！🙏",
        "市场瞬息万变，保持学习最重要 📖",
        "共识越来越强了！🤝",
        "期待更多这样的分析！⭐",
        "入圈以来学到很多，感谢社区！🌟",
        "世界变得太快，原来'准备好'也有保质期，保持学习最重要！",
        "不是市场没有钱，是缺乏让传统大钱放心进入的合规契机。",
        "监管集体'认错'！传统金融的巨鲸们，这次真的要扑进加密来了？",
        "用数据和事实拆解市场，这种硬核干货不多了，懂的都懂。",
        "风控比技术更重要，趋势面前所有理智和技术全都是废纸。",
        "多一点点耐心，等水开了再下饺子。🥟",
        "保持好奇、保持思考，永远对变化说一句：KEEP ASKING🔥",
        "币圈边界正在被打破，用我们习惯的交易方式，就能参与全球顶级资产博弈。",
        "监管从'一棒子打死'转向惩罚真实欺诈，这是好事！",
        "当百年金融巨头开始真金白银押注，很多疑虑可能真的只是浪花。",
    ],
    "technical": [
        "从技术面看，{coin} RSI6在强弱分界线附近，短期方向不明。",
        "{coin} MACD方面，DIF逐步向上接近DEA，已经出现收窄迹象。",
        "布林带通道在不断收窄，{coin} 典型的变盘前兆，注意风险。",
        "{coin} 关键阻力在当前价位附近，向下要看支撑强度。",
        "15分钟RSI一度飙到90以上，{coin} 严重超买后回踩，注意风险。",
        "MACD高位形成死叉，{coin} 需要注意回调风险。",
    ],
    "macro": [
        "霍尔木兹海峡局势紧张，油价预期反复摇摆，{coin} 短期可能继续跟随外部情绪波动。",
        "特朗普政府思路清晰：CFTC和SEC正在全面退出拜登时期的过激执法，利好 {coin}。",
        "《CLARITY法案》参议院那边还有阻力，目前通过概率约56%，{coin} 需关注进展。",
        "万事达卡拿下BitLicense，稳定币轨道加速，{coin} 生态受益。",
        "渣打银行完成首笔机构加密托管，传统金融入场信号明确，{coin} 长期看好。",
    ],
}

HOT_TOPICS = [
    "#纽交所母公司授权OKX推出原油合约",
    "#HYPE回调：空头退场与机构接力同步",
    "#美股洞察：戴尔超预期26%，好市多消费疲软",
    "#CFTC翻案：加密监管格局重塑",
    "#FOMC前瞻：BTC多头大举建仓",
    "#Anthropic率先盈利，联创发AI失业预警",
    "#CLARITY法案：60票门槛，最快8月签署",
    "#美伊谈判：伊朗宣称掌控霍尔木兹",
]

DEFAULT_COINS = [
    {"name": "Bitcoin", "symbol": "BTC", "price": "$73,780", "change": "+1.16%"},
    {"name": "Ethereum", "symbol": "ETH", "price": "$2,019", "change": "+1.40%"},
    {"name": "Solana", "symbol": "SOL", "price": "$145", "change": "+5.2%"},
    {"name": "UNI", "symbol": "UNI", "price": "$3.07", "change": "+1.93%"},
    {"name": "BNB", "symbol": "BNB", "price": "$580", "change": "+0.8%"},
    {"name": "XRP", "symbol": "XRP", "price": "$0.52", "change": "-0.5%"},
    {"name": "Dogecoin", "symbol": "DOGE", "price": "$0.15", "change": "+3.1%"},
    {"name": "OKB", "symbol": "OKB", "price": "$45", "change": "+2.3%"},
    {"name": "ALLO", "symbol": "ALLO", "price": "$0.20", "change": "+121%"},
    {"name": "HYPE", "symbol": "HYPE", "price": "$18", "change": "-5.2%"},
]
