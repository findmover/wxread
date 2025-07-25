import asyncio  # 添加 asyncio 导入
import configparser
import datetime
from pathlib import Path

from loguru import logger

from api.notifier import WxPusherNotifier
from api.reader import WXReader


def load_share_payload(curl_path):
    wx = WXReader.from_curl_bash(curl_path)
    return wx.payload


async def process_curl_path(curl_path, read_num, share_payload):
    FILE_NAME = Path(curl_path).stem
    if WXPUSHER_SPT:
        pusher = WxPusherNotifier(WXPUSHER_SPT)

    def onStart(msg):
        logger.info(f"{FILE_NAME}---{msg}")

    def onSuccess(msg):
        logger.success(f"{FILE_NAME}---{msg}")

    def onDebug(msg):
        logger.debug(f"{FILE_NAME}---{msg}")

    def onFail(msg):
        logger.error(f"{FILE_NAME}---{msg}")

    def onFinish(msg):
        logger.info(f"{FILE_NAME}---{msg}")
        if WXPUSHER_SPT:
            pusher.push(f"🎉 {FILE_NAME} 阅读脚本已完成！")

    wx = WXReader.from_curl_bash(curl_path)
    wx.payload = share_payload  # 修改 payload 属性
    await wx.sync_run(
        loop_num=read_num * 2,
        onStart=onStart,
        onSuccess=onSuccess,
        onDebug=onDebug,
        onFail=onFail,
        onFinish=onFinish,
    )


def setup_logger():
    today = datetime.date.today()
    log_file = f"logs/{today}.log"
    logger.add(log_file, rotation="1 day", retention="7 days", encoding="utf-8")


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config.get("WXPUSHER", "SPT")


async def main():
    share_payload = load_share_payload(CURL_PATH / "curl_config.sh")
    print("共享负载: ", share_payload)
    tasks = (
        process_curl_path(curl_path, READ_NUM, share_payload)
        for curl_path in CURL_PATH.glob("*.sh")
    )
    # 修改为异步运行
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    # config 文件夹下所有.sh
    CURL_PATH = Path("./config")
    CONFIG_PATH = Path("./config/key.ini")
    READ_NUM = 60

    setup_logger()
    # WXPUSHER_SPT = load_config() if CONFIG_PATH.exists() else None
    WXPUSHER_SPT = None

    asyncio.run(main())
