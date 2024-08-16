import jieba
from matplotlib import pyplot
from wordcloud import wordcloud, WordCloud
from PIL import Image
import numpy as np
from database.sqliteClass import SqlitDB


# 读取数据
sql = 'select name from movesInfo'
data = SqlitDB().querySql(sql)
# 将data拼接成字符串
text = ''
for i in data:
    text += str(i[0])

# 分词
cutWord = jieba.cut(text)
string = ' '.join(cutWord)

# 加载图片
img = Image.open('static/img/123.jpg')
img_array = np.array(img)


# 生成词云
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path='static/fonts/simsun.ttc',
)
# 加载词云文本
wc.generate_from_text(string)
# 绘制图片
pyplot.imshow(wc)
pyplot.axis('off')
# pyplot.show()
# 保存图片
pyplot.savefig('static/img/wordcloud.png', dpi=500)