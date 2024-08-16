from flask import Flask, render_template, request, redirect, url_for
from database.sqliteClass import SqlitDB

app = Flask(__name__)

app.debug = True


# 首页路由
@app.route('/')
def index():
    # 前三
    sql = 'select * from movesInfo where pm = 1'
    yi = SqlitDB().querySql(sql)
    sql = 'select * from movesInfo where pm = 2'
    er = SqlitDB().querySql(sql)
    sql = 'select * from movesInfo where pm = 3'
    san = SqlitDB().querySql(sql)
    # 第三后十名
    sql = 'select * from movesInfo order by pm limit 3,10'
    movie = SqlitDB().querySql(sql)
    print(movie)
    return render_template('index.html', yi=yi, er=er, san=san, movie=movie)


# 排行榜路由
@app.route('/rank')
def rank():
    return render_template('rank.html')


# 异步获取排行数据
@app.route('/getRank', methods=['GET', 'POST'])
def getRank():
    # 获取参数
    start = request.values.get("start")
    pageSize = request.values.get("pageSize")
    # 获取记录
    sql = f"select * from movesInfo order by pm asc limit {pageSize} offset {start}"
    movesList = SqlitDB().querySql(sql)
    # 获取总记录数
    sql = 'select count(*) from movesInfo'
    total = SqlitDB().querySql(sql)
    # print(movesList)
    return [movesList, total[0][0]]


# 年份上榜数
@app.route('/brand')
def brand():
    num = []
    # 电影数量前十的年份
    sql = 'select count(nf) as sm,nf from movesInfo group by nf order by sm desc limit 10'
    request = SqlitDB().querySql(sql)
    # 1930年-1949年
    sql = 'select count(nf) from movesInfo where nf >= 1930 AND nf < 1950'
    ershiyi = SqlitDB().querySql(sql)
    dic = {
        "value": ershiyi[0][0],
        "name": '1930年-1949年',
    }
    num.append(dic)
    # 1950年-1969年
    sql = 'select count(nf) as sm from movesInfo where nf >= 1950 AND nf < 1970'
    ershier = SqlitDB().querySql(sql)
    dic = {
        "value": ershier[0][0],
        "name": '1950年-1969年',
    }
    num.append(dic)
    # 1970年-1989年
    sql = 'select count(nf) as sm from movesInfo where nf >= 1970 AND nf < 1990'
    ershisan = SqlitDB().querySql(sql)
    dic = {
        "value": ershisan[0][0],
        "name": '1970年-1989年',
    }
    num.append(dic)
    # 1990年-2019年
    sql = 'select count(nf) as sm from movesInfo where nf >= 1990 AND nf < 2010'
    ershisi = SqlitDB().querySql(sql)
    dic = {
        "value": ershisi[0][0],
        "name": '1990年-2019年',
    }
    num.append(dic)
    # 2010年-至今
    sql = 'select count(nf) as sm from movesInfo where nf >= 2010'
    ershiwu = SqlitDB().querySql(sql)
    dic = {
        "value": ershiwu[0][0],
        "name": '2010年-至今',
    }
    num.append(dic)

    def get_year(request):
        return request[1]

    request.sort(key=get_year)
    # print(request)
    xAxis = []
    seriesNum = []
    max = []
    min = []
    for i in request:
        seriesNum.append(i[0])
        xAxis.append(i[1])
        sql = f'select max(pf),min(pf),nf,name from movesInfo where nf = {i[1]}'
        pf = SqlitDB().querySql(sql)
        # print(pf)
        for a in pf:
            max.append(a[0])
            min.append(a[1])
        # print(max, min)
    return render_template('brand.html', xAxis=xAxis, seriesNum=seriesNum, max=max, min=min, num=num)  # 品牌销量路由


@app.route('/energy')
def energy():
    sql = 'select pc,name from movesInfo order by pc asc limit 10'
    request = SqlitDB().querySql(sql)
    print(request)
    requestData = []
    for i in request:
        dic = {
            "value": i[0],
            "name": i[1],
        }
        requestData.append(dic)
    sql = 'select pc,name from movesInfo order by pc desc limit 10'
    request1 = SqlitDB().querySql(sql)
    print(request1)
    requestData1 = []
    for i in request1:
        dic = {
            "value": i[0],
            "name": i[1],
        }
        requestData1.append(dic)
    sql = 'select count(dq) as cq,dq from movesInfo group by dq order by cq desc limit 5'
    request2 = SqlitDB().querySql(sql)
    # print(request2)
    requestData2 = []
    requestData21 = []
    for i in request2:
        dic = f'{i[0]}'
        dic1 = f'{i[1]}'
        requestData2.append(dic)
        requestData21.append(dic1)
    sql = 'select count(yy) as cq,yy from movesInfo group by yy order by cq desc limit 5'
    request3 = SqlitDB().querySql(sql)
    # print(request3)
    requestData3 = []
    requestData31 = []
    for i in request3:
        dic = f'{i[0]}'
        dic1 = f'{i[1]}'
        requestData3.append(dic)
        requestData31.append(dic1)
    # print(requestData3)
    # print(requestData31)
    return render_template('energy.html', requestData=requestData, requestData1=requestData1, requestData2=requestData2,
                           requestData21=requestData21, requestData3=requestData3, requestData31=requestData31)


if __name__ == '__main__':
    app.run(port=4001)
