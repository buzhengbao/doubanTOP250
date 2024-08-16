import requests
from time import sleep
from random import randint

baseUrl = 'https://movie.douban.com/top250'
# 延迟3-5秒
sleep(randint(3, 5))
#  请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 '
                  'Safari/537.36 Edg/125.0.0.0'
}
try:
    res = requests.get(baseUrl, headers=headers, timeout=10)
    print(res.text)
except Exception as e:
    print(f'爬取错误：{e}')

