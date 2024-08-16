import re

from bs4 import BeautifulSoup

file = open('index.html', 'rb')
htm = file.read()

bs = BeautifulSoup(htm, 'html.parser')
# print(bs)

# 获取页面标题
# print(bs.head.title.string)
# print(bs.title.string)

# 获取第一个出现的IMG
# print(bs.img)
# print(bs.img.attrs)
# print(bs.img.attrs['src'])
# print(bs.img.get('src'))
# print(bs.img['src'])

# 获取所有img
# imgs = bs.find_all('img')
# # print(imgs)
# for t in imgs:
#     print('img标签的src属性', t.get('src'))

# print(bs.find_all('li'))
# 正则re.compile
# print(bs.find_all(re.compile('a')))

# 标签属性查询
# print(bs.find_all(id='books1'))
# print(bs.find_all(class_='boo'))
# b = bs.find_all(class_='boo')
# for i in b:
#     print(i.string)
# print(bs.find_all(src=re.compile('www')))
# limit限制提取数量
# print(bs.find_all('span', limit=2))
# print(bs.find_all('img', border='1')[0].get('src'))

# 选择器
# print(bs.find_all(class_='boo'))
# print(bs.select('.boo'))
# print(bs.select('p > span.redText'))
#content > div > div.article > ol > li:nth-child(1) > div > div.info > div.hd > a > span:nth-child(1)
# print(bs.select('#books1'))
print(bs.select('div#yellowDiv > ol#books1 > li:nth-child(2)'))
print(bs.select('span[style="color: blue;"]'))