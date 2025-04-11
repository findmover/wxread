# config.py 自定义配置,包括阅读次数、推送token的填写
import os
import re

"""
可修改区域
默认使用本地值如果不存在从环境变量中获取值
"""

# 阅读次数 默认120次/60分钟
READ_NUM = int(os.getenv('READ_NUM') or 120)
# 需要推送时可选，可选pushplus、wxpusher、telegram
PUSH_METHOD = "" or os.getenv('PUSH_METHOD')
# pushplus推送时需填
PUSHPLUS_TOKEN = "" or os.getenv("PUSHPLUS_TOKEN")
# telegram推送时需填
TELEGRAM_BOT_TOKEN = "" or os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "" or os.getenv("TELEGRAM_CHAT_ID")
# wxpusher推送时需填
WXPUSHER_SPT = "" or os.getenv("WXPUSHER_SPT")
# read接口的bash命令，本地部署时可对应替换headers、cookies
curl_str = os.getenv('WXREAD_CURL_BASH')

# headers、cookies是一个省略模版，本地或者docker部署时对应替换
cookies = {
    'wr_gid': '292311143',
    'wr_vid': '18916453',
    'wr_rt': 'web%40TSjdRuJBTm6xn572iXC_AL',
    'wr_localvid': '549320307120a46554968f5',
    'wr_name': 'Johnny',
    'wr_gender': '1',
    'wr_theme': 'dark',
    'wr_avatar': 'https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FT56yGfB99fRO6J8KxRG7I68EuWibrPiav8RhCicYjaGwc5uasWhacGpNAfCNeK1B5sV1EvpJZ6WkWXXJndXdV8saw%2F132',
    'wr_pf': 'NaN',
    'wr_skey': 'hAKwacx6',
    'wr_fp': '1469692579',
    'mp_49719c4dbff298b1e6c9adca527948b5_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A195db96d3ce75c-0fd623595e5fb5-1b525636-384000-195db96d3cf75d%22%2C%22%24device_id%22%3A%20%22195db96d3ce75c-0fd623595e5fb5-1b525636-384000-195db96d3cf75d%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-AU,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'baggage': 'sentry-environment=production,sentry-release=dev-1743523268690,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=e77196018bde478180011b6135742d06',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://weread.qq.com',
    'priority': 'u=1, i',
    'referer': 'https://weread.qq.com/web/reader/ce032b305a9bc1ce0b0dd2ak1c932da029c1c9ac015999a',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'e77196018bde478180011b6135742d06-b6d750f0f6cfc313',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'wr_gid=292311143; wr_vid=18916453; wr_rt=web%40TSjdRuJBTm6xn572iXC_AL; wr_localvid=549320307120a46554968f5; wr_name=Johnny; wr_gender=1; wr_theme=dark; wr_avatar=https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FT56yGfB99fRO6J8KxRG7I68EuWibrPiav8RhCicYjaGwc5uasWhacGpNAfCNeK1B5sV1EvpJZ6WkWXXJndXdV8saw%2F132; wr_pf=NaN; wr_skey=hAKwacx6; wr_fp=1469692579; mp_49719c4dbff298b1e6c9adca527948b5_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A195db96d3ce75c-0fd623595e5fb5-1b525636-384000-195db96d3cf75d%22%2C%22%24device_id%22%3A%20%22195db96d3ce75c-0fd623595e5fb5-1b525636-384000-195db96d3cf75d%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D',
}

"""
建议保留区域|默认读三体，其它书籍自行测试时间是否增加
"""
data = {
    'appId': 'wb115321887466h725297694',
    'b': 'ce032b305a9bc1ce0b0dd2a',
    'c': '1c932da029c1c9ac015999a',
    'ci': 71,
    'co': 389,
    'sm': '危机纪元4年云天明今天张医生来病房查诊，',
    'pr': 74,
    'rt': 5,
    'ts': 1744197384707,
    'rn': 776,
    'sg': '29e4c427e1d2675ba9913c245e1e2b2c75f664019ad9a5d1bf061602484d02b5',
    'ct': 1744197384,
    'ps': 'cdc320407a656f19g017cbf',
    'pc': '5ba32ed07a656f19g0187e1'
}


def convert(curl_command):
    """提取bash接口中的headers与cookies
    支持 -H 'Cookie: xxx' 和 -b 'xxx' 两种方式的cookie提取
    """
    # 提取 headers
    headers_temp = {}
    for match in re.findall(r"-H '([^:]+): ([^']+)'", curl_command):
        headers_temp[match[0]] = match[1]

    # 提取 cookies
    cookies = {}
    
    # 从 -H 'Cookie: xxx' 提取
    cookie_header = next((v for k, v in headers_temp.items() 
                         if k.lower() == 'cookie'), '')
    
    # 从 -b 'xxx' 提取
    cookie_b = re.search(r"-b '([^']+)'", curl_command)
    cookie_string = cookie_b.group(1) if cookie_b else cookie_header
    
    # 解析 cookie 字符串
    if cookie_string:
        for cookie in cookie_string.split('; '):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
    
    # 移除 headers 中的 Cookie/cookie
    headers = {k: v for k, v in headers_temp.items() 
              if k.lower() != 'cookie'}

    return headers, cookies


headers, cookies = convert(curl_str) if curl_str else (headers, cookies)
