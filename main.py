import os
import json
import time
import random
import logging
import hashlib
import requests
import urllib.parse
from push import push
from capture import headers as local_headers, cookies as local_cookies, data

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-8s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 常量
# 加密盐及其它默认值
KEY = "3c5c8717f3daf09iop3423zafeqoi"
COOKIE_DATA = {"rq": "%2Fweb%2Fbook%2Fread"}
READ_URL = "https://weread.qq.com/web/book/read"
RENEW_URL = "https://weread.qq.com/web/login/renewal"

# github action部署用
# 从环境变量获取 headers、cookies等值(如果不存在使用默认本地值)
# 每一次代表30秒，比如你想刷1个小时这里填120，你只需要签到这里填2次
env_num = os.getenv('READ_NUM')
env_method = os.getenv('PUSH_METHOD')
env_headers = os.getenv('WXREAD_HEADERS')
env_cookies = os.getenv('WXREAD_COOKIES')

number = int(env_num) if env_num not in (None, '') else 120
headers = json.loads(json.dumps(eval(env_headers))) if env_headers else local_headers
cookies = json.loads(json.dumps(eval(env_cookies))) if env_cookies else local_cookies

def encode_data(data):
    """
    将数据字典转为排序后的 URL 编码字符串
    """
    return '&'.join(f"{k}={urllib.parse.quote(str(data[k]), safe='')}" for k in sorted(data.keys()))


def cal_hash(input_string):
    """
    按照特定规则计算 hash
    """
    _7032f5 = 0x15051505
    _cc1055 = _7032f5
    length = len(input_string)
    _19094e = length - 1

    while _19094e > 0:
        _7032f5 = 0x7fffffff & (_7032f5 ^ ord(input_string[_19094e]) << (length - _19094e) % 30)
        _cc1055 = 0x7fffffff & (_cc1055 ^ ord(input_string[_19094e - 1]) << _19094e % 30)
        _19094e -= 2

    return hex(_7032f5 + _cc1055)[2:].lower()


def get_wr_skey():
    """
    刷新 cookies 中的 wr_skey
    """
    try:
        response = requests.post(RENEW_URL, headers=headers, cookies=cookies,
                                 data=json.dumps(COOKIE_DATA, separators=(',', ':')))
        response.raise_for_status()
        for cookie in response.headers.get('Set-Cookie', '').split(';'):
            if "wr_skey" in cookie:
                return cookie.split('=')[-1][:8]
    except requests.RequestException as e:
        logger.error(f"❌ 请求刷新 wr_skey 失败: {e}")
    return None

def log_and_push_error(message):
    """
    记录错误日志并推送消息，同时终止脚本
    """
    logger.error(message)  # 记录错误日志
    if env_method:
        push(message, env_method)  # 推送错误信息
    raise Exception(message)  # 触发异常终止脚本



# 开始阅读脚本
logger.info(f"🔔 阅读脚本启动，目标次数：{number}次")

index = 1
while index <= number:
    try:
        # 更新动态数据
        data['ct'] = int(time.time())
        data['ts'] = int(time.time() * 1000)
        data['rn'] = random.randint(0, 1000)
        data['sg'] = hashlib.sha256(f"{data['ts']}{data['rn']}{KEY}".encode()).hexdigest()
        data['s'] = cal_hash(encode_data(data))

        logger.info(f"⏱️ 尝试第 {index} 次阅读...")
        response = requests.post(READ_URL, headers=headers, cookies=cookies,
                                 data=json.dumps(data, separators=(',', ':')))
        response.raise_for_status()  # 如果请求失败会直接抛出异常
        res_data = response.json()

        if 'succ' in res_data:
            logger.info(f"✅ 阅读成功，累计阅读时间：{index * 0.5} 分钟")
            index += 1
            time.sleep(30)
        else:
            logger.warning("❌ Cookie 已过期，尝试刷新...")
            new_skey = get_wr_skey()
            if new_skey:
                cookies['wr_skey'] = new_skey
                logger.info(f"✅ 密钥刷新成功，新密钥：{new_skey}")
            else:
                log_and_push_error("❌ 无法获取新密钥，终止运行。")
    except requests.RequestException as e:
        log_and_push_error(f"❌ 请求失败: {e}")  # 直接调用统一的错误处理函数
    finally:
        data.pop('s', None)  # 清除动态数据

# 完成阅读脚本
logger.info("🎉 阅读脚本已完成！")

if env_method:
    completed = index - 1  # 实际完成的次数
    total_time = completed * 0.5  # 阅读时长（分钟）
    completion_rate = (completed / number) * 100  # 完成率

    message = (
        "微信读书自动阅读完成！\n"
        f"📚 目标次数：{number}次\n"
        f"✅ 成功次数：{completed}次\n"
        f"💯 完成率：{completion_rate:.1f}%\n"
        f"⏱️ 阅读时长：{total_time}分钟"
    )

    logger.info(f"⏱️ 开始推送: {message}")
    push(message, env_method)