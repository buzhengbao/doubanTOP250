from flask import Flask, render_template

# 创建Flask实例
app = Flask(__name__)
app.debug = True


# 创建路由
@app.route('/')
def home():
    name = '张三'
    age = 45
    my = ['14', '44', '44']
    return render_template('index.html', name=name, age=age, my=my)


# 启动flask网站
if __name__ == '__main__':
    app.run(port=4000)
