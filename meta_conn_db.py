import traceback
import sys, os


class connDb(object):
    def __init__(self, DbInfo):
        self.__dbInfo = DbInfo
        self.__host = self.__dbInfo['host']
        self.__port = int(self.__dbInfo['port'])
        self.__userName = self.__dbInfo['user']
        self.__passWord = self.__dbInfo['pwd']
        self.__dbType = self.__dbInfo['db_type']
        self.__dbName = self.__dbInfo['db_name']
        self.__conn()

    def __conn(self):
        """链接数据库"""
        try:
            if self.__dbType == 'oracle':
                self.__connectType = self.__dbInfo['connect_type']
                self.__connectName = self.__dbInfo['connect_name']
                self.__conn = self.__getOracleConnet()
            elif self.__dbType == 'hive':
                self.__conn = self.__getHiveConnet()
            elif self.__dbType == 'mysql':
                self.__charset = self.__dbInfo['charset']
                self.__conn = self.__getMysqlConnet()
            elif self.__dbType == 'sqlserver':
                self.__charset = self.__dbInfo['charset']
                self.__conn = self.__getSqlserverConnet()
            elif self.__dbType == 'pg':
                self.__conn = self.__getPostgresqlConnet()
            return True
        except:
            return False

    # def __reconndb(self, num=10, stime=3):
    #     '''重链数据库'''
    #     __number = 0
    #     __status = True
    #     while _status and __number <= num:
    #         try:
    #             self.__conn.isClosed() # cping 校验连接是否异常
    #             __status = False
    #         except:
    #             if self._conn() == True:  # 重新连接,成功退出
    #                 __status = False
    #                 break
    #             __number += 1
    #             time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束

    @property
    def get_db_type(self):
        return self.__dbType

    @property
    def get_db_conn_status(self):
        return self.__conn._closed

    def select(self, sql):
        result = "-99999"
        try:
            if self.__dbType == 'mysql':
                import pymysql
                cursor = self.__conn.cursor(pymysql.cursors.DictCursor)
                # cursor = self.__conn.cursor()
                cursor.execute('SET session group_concat_max_len=15000;')
                cursor.execute(sql)
                result = cursor.fetchall()

            elif self.__dbType == 'oracle' or self.__dbType == 'hive' or self.__dbType == 'sqlserver' or self.__dbType == 'pg':
                cursor = self.__conn.cursor()
                cursor.execute(sql)
                columnNamesList = [d[0].lower() for d in cursor.description]  # 获取字段列表
                rowDataTupleList = list(cursor.fetchall())  # 把获取到的数据元组转换成list列表
                cursor.close()
                rowDataDicList = []
                for rowDataTuple in rowDataTupleList:
                    rowDataDic = {}
                    for i in range(len(columnNamesList)):
                        rowDataDic[columnNamesList[i]] = rowDataTuple[i]
                    rowDataDicList.append(rowDataDic)
                result = rowDataDicList
            return result
        except:
            print('db-{db_type}-[select]---> is errors'.format(db_type=self.__dbType))
            print(sql)
            errors = traceback.format_exc()
            print(errors)
            return result

    def dml(self, sql):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.__conn.commit()
            return "0"
        except:
            errors = traceback.format_exc()
            print(sql)
            print('db-{db_type}-[dml]---> is errors'.format(db_type=self.__dbType))
            print(errors)
            return "-99999"

    def ddl(self, sql):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
            return "0"
        except:
            errors = traceback.format_exc()
            print(sql)
            print('db-{db_type}-[ddl]---> is errors'.format(db_type=self.__dbType))
            print(errors)
            return "-99999"

    def close(self):
        try:
            self.__conn.close()
        except:
            errors = traceback.format_exc()
            print('db[close]---> is errors')
            print(errors)
            return "-99999"

    def __getOracleConnet(self):
        import jaydebeapi
        try:
            jarFile = os.path.dirname(__file__) + '/ojdbc6.jar'
            if self.__connectType == 'service_name':
                jdbcUrl = 'jdbc:oracle:thin:@//{dbHost}:{port}/{connectName}'.format(port=self.__port,
                                                                                     dbHost=self.__host,
                                                                                     connectName=self.__connectName)
            else:
                jdbcUrl = 'jdbc:oracle:thin:@{dbHost}:{port}:{connectName}'.format(port=self.__port, dbHost=self.__host,
                                                                                   connectName=self.__connectName)
            conn = jaydebeapi.connect('oracle.jdbc.driver.OracleDriver', jdbcUrl, [self.__userName, self.__passWord],
                                      jarFile)
            return conn
        except:
            errors = traceback.format_exc()
            print('oracle[getConnet]---> is errors')
            print(errors)
            return "-99999"

    def __getPostgresqlConnet(self):
        import psycopg2
        try:
            conn = psycopg2.connect(host=self.__host, user=self.__userName, password=self.__passWord,
                                    database=self.__dbName, port=self.__port)
            return conn
        except:
            errors = traceback.format_exc()
            print('postgreSql[getConnet]---> is errors')
            print(errors)
            return "-99999"

    def __getSqlserverConnet(self):
        import pymssql
        try:
            conn = pymssql.connect(host=self.__host, user=self.__userName, password=self.__passWord,
                                   database=self.__dbName, charset=self.__charset, port=self.__port)  # 建立连接
            return conn
        except:
            errors = traceback.format_exc()
            print('SQLServer[getConnet]---> is errors')
            print(errors)
            return "-99999"

    def __getMysqlConnet(self):
        import pymysql
        try:
            conn = pymysql.connect(db=self.__dbName, host=self.__host, port=self.__port, user=self.__userName,
                                   passwd=self.__passWord, charset=self.__charset)
            return conn
        except:
            errors = traceback.format_exc()
            print('hive[getConnet]---> is errors')
            print(errors)
            return "-99999"

    def __getHiveConnet(self):
        from pyhive import hive
        try:
            conn = hive.Connection(host=self.__host, port=self.__port, username=self.__userName, database=self.__dbName)
            return conn
        except:
            errors = traceback.format_exc()
            print('hive[getConnet]---> is errors')
            print(errors)
            return "-99999"



