import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, Manager
import csv

from lxml import etree

from database.sqliteClass import SqlitDB


# 爬虫类
class Spider:
    # 构造函数
    def __init__(self):
        # 爬取的页面的地址
        self.url = (
            'https://movie.douban.com/top250?')  # start=0

        #  请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/125.0.0.0'
                          'Safari/537.36 Edg/125.0.0.0'
        }

    # 创造csv文件
    def createCsv(self):
        with open('temp.csv', 'w', newline='', encoding='utf-8') as f:
            # 创建csv写入对象
            w = csv.writer(f)
            # 向csv文件写入标题
            w.writerow(
                ["name", "pf", "pm", "img", "js", "dy", "bj", "zy", "nf", "dq", "lx",
                 "yy", "pc"])

    # 保存爬取的数据至CSV文件
    def saveToCsv(self, data):
        with open('temp.csv', 'a', newline='', encoding='utf-8') as f:
            # 创建csv写入对象
            w = csv.writer(f)
            # 写入数据
            w.writerows(data)

    # 爬取二级页面
    def subSpider(self, series_id):
        # 爬取地址
        # 开始爬取
        subPage = requests.get(series_id, headers=self.headers).text
        # 解析数据
        soup = BeautifulSoup(subPage, 'html.parser')
        # print(soup)
        params = []
        # 导演
        try:
            dy = soup.select('#info > span:nth-child(1) > span.attrs > a')[0].text
            # print(dy)
            params.append(dy)
        except:
            print('导演爬取失败')
            params.append('')
        # 编剧
        try:
            bj = soup.select('#info > span:nth-child(3) > span.attrs')[0].text
            # print(bj)
            params.append(bj)
        except:
            print('编剧爬取失败')
            params.append('')
        # 主演
        try:
            zy = soup.select('#info > span:nth-child(5) > span.attrs')[0].text
            # print(zy)
            params.append(zy)
        except:
            print('主演爬取失败')
            params.append('')
        # 年份
        try:
            pattern = '<span class="year">\\((.+?)\\)</span>'
            yf = re.findall(pattern, f'{soup}')
            # print(yf[0])
            params.append(yf[0])
        except:
            print('年份爬取失败')
            params.append('')
        # 地区
        try:
            pattern = '<span class="pl">制片国家/地区:</span> (.+)<br/>'
            dq = re.findall(pattern, f'{soup}')
            # print(dq[0])
            dq1 = dq[0].find(' ')
            dq2 = ''
            if dq1 != -1:  # 如果找到斜杠
                # 返回斜杠之前的子字符串
                dq2 = dq[0][:dq1]
            else:
                # 如果没有找到斜杠，则返回原始字符串
                dq2 = dq[0]
            params.append(dq2)
        except:
            print('地区爬取失败')
            params.append('')
        # 类型
        try:
            pattern = '<span class="pl">类型:</span>(.+)<br/>'
            pattern1 = '<span property="v:genre">(.+?)</span>'
            lx = re.findall(pattern, f'{soup}')
            lx1 = re.findall(pattern1, lx[0])
            lx2 = '/'.join(lx1)
            # print(lx2)
            params.append(lx2)
        except:
            print('类型爬取失败')
            params.append('')
        # 语言
        try:
            pattern = '<span class="pl">语言:</span> (.+)<br/>'
            yy = re.findall(pattern, f'{soup}')
            # print(yy[0])
            yy1 = yy[0].find(' ')
            yy2 = ''
            if yy1 != -1:  # 如果找到斜杠
                # 返回斜杠之前的子字符串
                yy2 = yy[0][:yy1]
            else:
                # 如果没有找到斜杠，则返回原始字符串
                yy2 = yy[0]
            # print(yy2)
            params.append(yy2)
        except:
            print('语言爬取失败')
            params.append('')
        # 片长
        try:
            pattern = '<span class="pl">片长:</span>(.+)<br/>'
            pattern1 = '<span.*>(.*)分钟.*</span>'
            pc = re.findall(pattern, f'{soup}')
            pc1 = re.findall(pattern1, pc[0])
            # print(pc1[0])
            params.append(pc1[0])
        except:
            print('片长爬取失败')
            params.append('')
        # print(params)
        return params

    # 爬取排行榜页面 offset 控制分页
    def mainSpider(self, start, q_task):
        print(f'数据从第{start}开始爬取....')
        # 创建参数字典
        params = {
            'start': start
        }
        pageText = requests.get(self.url, headers=self.headers, params=params, timeout=20).text
        # print(pageText)
        # 解析数据
        page = BeautifulSoup(pageText, 'html.parser')
        # print(page)
        # q_task.get()
        name1 = page.select(f'#content > div > div.article > ol > li:nth-child({1}) > div > div.info > '
                            f'div.hd > a > span:nth-child(1)')[0].text
        movieRows = []
        movieRow = []
        # 判断爬虫是否爬取到数据
        if not name1:
            print(f'数据从第{start}条开始没有数据了')
        else:
            # 爬取成功任务完成，从任务队列中删除任务
            q_task.get()
            i = 1
            if i <= 25:
                # 电影排名
                try:
                    name = page.select(f'#content > div > div.article > ol > li:nth-child({i}) > div > div.info > '
                                       f'div.hd > a > span:nth-child(1)')[0].text
                    # print(name)
                    movieRow.append(name)
                except:
                    print('电影名称爬取失败')
                    movieRow.append('')
                # 电影评分
                try:
                    pf = page.select(
                        f'#content > div > div.article > ol > li:nth-child({i}) > div > div.info > div.bd > div > '
                        f'span.rating_num')[0].text
                    # print(pf)
                    movieRow.append(pf)
                except:
                    print('电影评分爬取失败')
                    movieRow.append('')
                # 电影排名
                try:
                    pm = page.select(
                        f'#content > div > div.article > ol > li:nth-child({i}) > div > div.pic > em')[0].text
                    # print(pm)
                    movieRow.append(pm)
                except:
                    print('电影排名爬取失败')
                    movieRow.append('')
                # 电影海报
                try:
                    img = page.select(
                        f'#content > div > div.article > ol > li:nth-child({i}) > div > div.pic > a > img')[0].attrs[
                        'src']
                    # print(img)
                    movieRow.append(img)
                except:
                    print('电影海报爬取失败')
                    movieRow.append('')
                # 电影简介
                try:
                    js = page.select(
                        f'#content > div > div.article > ol > li:nth-child({i}) > div > div.info > div.bd > p.quote > '
                        f'span')[0].text
                    # print(js)
                    movieRow.append(js)
                except:
                    print('电影简介爬取失败')
                    movieRow.append('')
                # 二级页面
                try:
                    url = page.select(
                        f'#content > div > div.article > ol > li:nth-child({i}) > div > div.pic > a')[
                        0].attrs['href']
                    sublist = self.subSpider(url)
                    movieRow.extend(sublist)
                except:
                    print('二级页面爬取失败')
                    movieRow.append('')
                movieRows.append(movieRow)
                print(movieRows)
                i += 1
            else:
                i = 1
        print(movieRows)
        # 写入csv文件
        self.saveToCsv(movieRows)

    # 主函数
    def main(self):
        # 创建csv文件
        self.createCsv()
        # 进程池可以运行10个进程
        max_pool = 10
        p = Pool(max_pool)
        # 设置爬虫的起点位置
        start = 0
        # 创建任务队列
        q_task = Manager().Queue(max_pool)
        while start <= 300:
            try:
                q_task.put('task', timeout=20)
                # self.mainSpider(offset, q_task)
                p.apply_async(self.mainSpider, args=(start, q_task))
                start += 1
            except:
                p.close()
                p.join()
                print('爬取完毕')
                break

    # 数据清晰
    def cleanCsv(self):
        # 使用pandas库
        df = pd.read_csv('temp.csv')
        # 清除空行
        # df.dropna(inplace=True)
        # 清除重复行
        df.drop_duplicates(inplace=True)
        # 处理pandas返回的列表类型数据，转换为元组列表
        data = []
        for row in df.values:
            data.append(tuple(row))
        return data

    # 出入数据库
    def saveDB(self):
        # 清晰数据
        data = self.cleanCsv()
        # 插入数据库
        sql = 'insert into movesInfo(name,pf,pm,img,js,dy,bj,zy,nf,dq,lx,yy,pc) values (?,?,?,?,?,?,?,?,?,?,?,?,?)'
        SqlitDB().doSql(sql, data)


if __name__ == '__main__':
    Spider().main()
    # Spider().saveDB()
    # while True:
    #     print('1.开始爬取 2.保存数据库 3. 退出')
    #     num = int(input('请输入数字:'))
    #     if num == 1:
    #         Spider().main()
    #     elif num == 2:
    #         Spider().saveDB()
    #     else:
    #         break
