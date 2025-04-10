import logging

import requests
from apprise.decorators import notify

logger = logging.getLogger(__name__)


@notify(on='wxpusherspt', name='WxPusher SPT')
def notify_wxpusher_spt(body: str, title: str, notify_type: str, meta: dict, *args, **kwargs):
    """WxPusher消息推送（极简方式）"""
    spt = meta.get('host', '')
    wxpusher_simple_url = f"https://wxpusher.zjiecode.com/api/send/message/{spt}/{body}"
    response = requests.get(wxpusher_simple_url, timeout=10)
    response.raise_for_status()
    logger.info("✅ WxPusher响应: %s", response.text)
