# push.py 支持 Apprise、PushPlus 、wxpusher spt 的消息推送模块
import logging
import os
import random
import time

from apprise import Apprise, AppriseAsset

from config import (APPRISE_URLS, PUSH_METHOD, PUSHPLUS_TOKEN,
                    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, WXPUSHER_SPT)

logger = logging.getLogger(__name__)


def push_one(content: str, url: str, apprise_obj: Apprise):
    attempts = 5
    result = False
    for attempt in range(attempts):
        result = apprise_obj.notify(body=content, title='微信阅读推送...')
        if result:
            logger.info(f"✅ 推送成功：{url}")
            return True
        else:
            logger.error(f"❌ 推送失败：{url}")
            if attempt < attempts - 1:
                sleep_time = random.randint(180, 360)
                logger.info(f"将在 {sleep_time} 秒后重试...")
                time.sleep(sleep_time)
    return False


"""外部调用"""


def push(content: str):
    """统一推送接口，通过Apprise实现，额外支持 PushPlus 和 WxPusher 极简方式"""
    urls = APPRISE_URLS
    apprise_obj = Apprise(asset=AppriseAsset(
        plugin_paths=os.path.join(__file__, '../apprise_plugins')
    ))
    if PUSH_METHOD == 'pushplus':
        urls = [f'pushplus://{PUSHPLUS_TOKEN}']
    elif PUSH_METHOD == 'wxpusher':
        urls = [f'wxpusherspt://{WXPUSHER_SPT}']
    elif PUSH_METHOD == 'telegram':
        urls = [f'tgram://{TELEGRAM_BOT_TOKEN}/{TELEGRAM_CHAT_ID}']
    if urls:
        logging.info("⏱️ 开始推送...")
    for url in urls:
        # 由于Apprise不支持返回各个url成功与否的结果，故单独处理各个url
        if not apprise_obj.add(url):
            logger.error(f"❌ 通知渠道无效：{url}")
            continue
        if not push_one(content, url, apprise_obj):
            old_no_proxy = os.getenv('no_proxy')
            os.environ['no_proxy'] = '*'
            push_one(content, url, apprise_obj)
            if old_no_proxy:
                os.environ['no_proxy'] = old_no_proxy
            else:
                os.environ.pop('no_proxy', None)
        apprise_obj.clear()
