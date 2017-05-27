import pymysql.cursors


class OutputMysql(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_mysql(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='password',
                                     db='test',
                                     charset='utf8')
        try:
            #获取会话指针
            with connection.cursor() as cursor:
                #先将原有的数据删除再添加数据
                cursor.execute("DELETE FROM `newspaper`")
                #创建sql语句
                sql = "INSERT INTO `newspaper`(`title`, `time`, `content`, `page`) "\
                      "VALUES (%s, %s, %s, %s)"
                for data in self.datas:
                    #执行sql语句
                    cursor.execute(sql, (data['title'], data['time'], data['content'],
                                         data['page']))
                #提交
                connection.commit()
        finally:
            connection.close()



