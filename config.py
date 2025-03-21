# config.py 自定义配置,包括阅读次数、推送token的填写
import os
import re
import random

"""
可修改区域
默认使用本地值如果不存在从环境变量中获取值
"""
random_num = random.randint(120, 150)
# 阅读次数 默认120次/60分钟
READ_NUM = int(os.getenv('READ_NUM') or random_num)
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
    'iip': '0',
    '_qimei_q36': '',
    '_qimei_h38': 'bafb76fc23de31a2a092cec40300000cc18217',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22191b16bd60a55c-0fb2646ef7ec56-17525637-2073600-191b16bd60b322%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxYjE2YmQ2MGE1NWMtMGZiMjY0NmVmN2VjNTYtMTc1MjU2MzctMjA3MzYwMC0xOTFiMTZiZDYwYjMyMiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22191b16bd60a55c-0fb2646ef7ec56-17525637-2073600-191b16bd60b322%22%7D',
    '_ga': 'GA1.2.1724625815.1725258521',
    'pac_uid': '0_Dhzxz48ZNTWh6',
    'suid': 'user_0_Dhzxz48ZNTWh6',
    'pgv_pvid': '8249101234',
    'wr_localvid': '3eb328d0746357953ebfdac',
    'wr_name': '%E5%BC%A0%E6%B4%8B',
    'wr_avatar': 'https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FQ0j4TwGTfTKpZehZfaoicvXZ6FZialWjs2AIQQ6raqTOgpYmPYiabjyZibKGUGicF0FvQ5uMynD6W8wZO9EmSPHVXQw%2F132',
    'wr_gender': '1',
    '_qimei_fingerprint': '5cfd92629ca389803c4cf6d883b6b292',
    '_clck': 'fsx6kg|1|fty|0',
    'wr_gid': '253935748',
    'wr_vid': '73619349',
    'wr_rt': 'web%40mA2YLHsfEHO0IiZO0CP_AL',
    'wr_fp': '3692135753',
    'wr_pf': 'NaN',
    'wr_skey': 'oIV3aYFT',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'baggage': 'sentry-environment=production,sentry-release=dev-1742474690576,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=6e88abafcc05491291ce07a16090960f',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://weread.qq.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://weread.qq.com/web/reader/ce032b305a9bc1ce0b0dd2a',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '6e88abafcc05491291ce07a16090960f-8e2270fd93ea930f',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'iip=0; _qimei_q36=; _qimei_h38=bafb76fc23de31a2a092cec40300000cc18217; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22191b16bd60a55c-0fb2646ef7ec56-17525637-2073600-191b16bd60b322%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxYjE2YmQ2MGE1NWMtMGZiMjY0NmVmN2VjNTYtMTc1MjU2MzctMjA3MzYwMC0xOTFiMTZiZDYwYjMyMiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22191b16bd60a55c-0fb2646ef7ec56-17525637-2073600-191b16bd60b322%22%7D; _ga=GA1.2.1724625815.1725258521; pac_uid=0_Dhzxz48ZNTWh6; suid=user_0_Dhzxz48ZNTWh6; pgv_pvid=8249101234; wr_localvid=3eb328d0746357953ebfdac; wr_name=%E5%BC%A0%E6%B4%8B; wr_avatar=https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FQ0j4TwGTfTKpZehZfaoicvXZ6FZialWjs2AIQQ6raqTOgpYmPYiabjyZibKGUGicF0FvQ5uMynD6W8wZO9EmSPHVXQw%2F132; wr_gender=1; _qimei_fingerprint=5cfd92629ca389803c4cf6d883b6b292; _clck=fsx6kg|1|fty|0; wr_gid=253935748; wr_vid=73619349; wr_rt=web%40mA2YLHsfEHO0IiZO0CP_AL; wr_fp=3692135753; wr_pf=NaN; wr_skey=oIV3aYFT',
}

"""
建议保留区域|默认读三体，其它书籍自行测试时间是否增加
"""
data = {
    "appId": "wb182564874663h152492176",
    "b": "ce032b305a9bc1ce0b0dd2a",
    "c": "7cb321502467cbbc409e62d",
    "ci": 70,
    "co": 0,
    "sm": "[插图]第三部广播纪元7年，程心艾AA说",
    "pr": 74,
    "rt": 30,
    "ts": 1727660516749,
    "rn": 31,
    "sg": "991118cc229871a5442993ecb08b5d2844d7f001dbad9a9bc7b2ecf73dc8db7e",
    "ct": 1727660516,
    "ps": "b1d32a307a4c3259g016b67",
    "pc": "080327b07a4c3259g018787",
}


# def convert(curl_command):
#     """提取bash接口中的headers与cookies"""
#     # 提取 headers
#     for match in re.findall(r"-H '([^:]+): ([^']+)'", curl_command):
#         headers[match[0]] = match[1]
#     print(headers)
#     # 提取 cookies
#     cookies = {}
#     cookie_string = headers.pop('cookie', '')
#     print(cookie_string)
#     # for cookie in cookie_string.split('; '):
#     #     key, value = cookie.split('=', 1)
#     #     cookies[key] = value
#
#     return headers, cookies
#
# #
# convert(temp)

