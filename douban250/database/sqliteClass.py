import sqlite3
import os


class SqlitDB:
    # 类私有变量
    __dbName = 'moveInfo.db'
    # 构造函数
    def __init__(self):
        # 获取当前类的绝对路径
        # print(os.path.abspath(__file__))
        file_path = os.path.abspath(__file__)
        db_path = os.path.dirname(file_path) + '\\' + SqlitDB.__dbName
        # 连接数据库
        self.conn = sqlite3.connect(db_path)
        # 创建游标
        self.cur = self.conn.cursor()

    # 构造表
    def createTable(self):
        sql = '''
            create table if not exists movesInfo(
            id integer primary key autoincrement,
            name text,
            pf text,
            pm integer,
            dy integer,
            bj text,
            zy text,
            nf integer,
            dq integer,
            lx text,
            yy text,
            pc integer,
            img text,
            js text NULL
            )
        '''
        self.cur.execute(sql)

    # 查询表
    def querySql(self,sql):
        if not sql:
            return
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print('查询出错', e)

    # 增删改
    def doSql(self, sql, params):
        try:
            if isinstance(params, list):
                # 批量修改时，params  [(name=1),(name=2)]
                self.cur.executemany(sql, params)
            else:
                self.cur.execute(sql, params)
            self.conn.commit()
            print(f'执行成功，影响了{self.cur.rowcount}条数据')
        except Exception as e:
            print('执行出错', e)


if __name__ == '__main__':
    SqlitDB().createTable()