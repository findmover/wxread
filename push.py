import requests


def push(content):
    url = "https://www.pushplus.plus/send"
    params = {
        "token": "a3d80d84ff434ee79b5db33fc45b6d1d",
        "content": content
    }
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
    }

    response = requests.get(url, headers=headers, params=params)
    print(response.text)


