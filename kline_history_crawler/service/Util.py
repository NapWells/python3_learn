import pymysql


class DBUtil:
    def __init__(self):
        self.insert_sql = 'INSERT INTO `exchange_data`.`kline_history` (`exchange`,`symbol`,`amount`,`count`,`open`,`close`,`low`,`high`,`vlo`,`buy_amount`,`buy_count`,`buy_vlo`,`sell_amount`,`sell_count`,`sell_vlo`,`time`) VALUES (%(exchange)d,\'%(symbol)s\',%(amount).10f,%(count).10f,%(open).10f,%(close).10f,%(low).10f,%(high).10f,%(vlo).10f,%(buy_amount).10f,%(buy_count).10f,%(buy_vlo).10f,%(sell_amount).10f,%(sell_count).10f,%(sell_vlo).10f,\'%(time)s\');'
        self.connection = self.connect()

    @staticmethod
    def connect():
        return pymysql.connect(host="localhost", user="root", password="123456", db="exchange_data", port=3306)

    def open(self):
        return self.connection.open

    def insert(self, params):
        if self.open() is False:
            self.connection = self.connect
        try:
            self.connection.begin()
            cur = self.connection.cursor()
            sql = self.insert_sql % params
            print(sql)
            cur.execute(self.insert_sql % params)
            # 提交
            self.connection.commit()
        except Exception as e:
            # 错误回滚
            self.connection.rollback()
            self.connection = self.connect()
            print('insert exception :', e)
        finally:
            pass


db = DBUtil()
