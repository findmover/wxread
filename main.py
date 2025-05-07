import asyncio
import os

from api.notifier import Notifier
from api.reader import WXReader

# 阅读次数 默认40次/20分钟
READ_NUM = int(os.getenv("READ_NUM") or 40)
# 需要推送时可选，可选pushplus、wxpusher、telegram
PUSH_METHOD = os.getenv("PUSH_METHOD")
# pushplus推送时需填
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN")
# telegram推送时需填
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# wxpusher推送时需填
WXPUSHER_SPT = os.getenv("WXPUSHER_SPT")
# read接口的bash命令，本地部署时可对应替换headers、cookies
curl_str = os.getenv("WXREAD_CURL_BASH")


# 新增：检查推送 token 是否存在
def has_valid_push_token(push_method):
    if push_method == "pushplus":
        return bool(PUSHPLUS_TOKEN)
    elif push_method == "telegram":
        return bool(TELEGRAM_BOT_TOKEN) and bool(TELEGRAM_CHAT_ID)
    elif push_method == "wxpusher":
        return bool(WXPUSHER_SPT)
    return False


config = WXReader.parse_curl(curl_str)
reader = WXReader(**config)

# 新增：根据推送 token 存在与否决定是否推送
if PUSH_METHOD and has_valid_push_token(PUSH_METHOD):
    notifier = Notifier(
        PUSH_METHOD,
        {
            "PUSHPLUS_TOKEN": PUSHPLUS_TOKEN,
            "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
            "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID,
            "WXPUSHER_SPT": WXPUSHER_SPT,
        },
    )
    notifier.onStart(f"📕 开始阅读，共{ READ_NUM/2 }分钟")
    asyncio.run(
        reader.sync_run(
            loop_num=READ_NUM,
            onFail=notifier.onFail,
            onFinish=notifier.onFinish,
        )
    )
else:
    # 如果没有有效的推送 token，则直接运行阅读逻辑
    asyncio.run(reader.sync_run(loop_num=READ_NUM))
