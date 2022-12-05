import traceback
from meta_conn_db import connDb


class dbMetaConfirm(object):
    def __init__(self, srcDbInfo):
        supportList = ['oracle', 'sqlserver', 'hive', 'pg', 'mysql']
        if srcDbInfo['db_type'].lower() not in supportList:
            print('暂时支持{supportList},输入的metaType为:{src_db_type}'.format(supportList=supportList
                                                                        , src_db_type=srcDbInfo['db_type']))
            exit()
        self.__srcDbInfo = srcDbInfo
        self.__metaType = srcDbInfo['db_type']
        self.__srcDb = connDb(srcDbInfo)

    def dbMetaSchema(self):
        '''获取数据库schema'''
        try:
            if self.__metaType.lower() == 'mysql':
                sql = """select table_schema as table_schema FROM information_schema.TABLES group by table_schema"""
            elif self.__metaType.lower() == 'oracle':
                sql = """select owner as table_schema FROM all_tab_comments group by owner"""
            elif self.__metaType.lower() == 'sqlserver':
                sql = """select name as table_schema FROM sys.sysusers group by name"""
            elif self.__metaType.lower() == 'pg':
                sql = """select table_schema as table_schema FROM information_schema.TABLES group by table_schema"""
            elif self.__metaType.lower() == 'hive':
                sql = """select name as table_schema FROM DBS group by name"""
            else:
                sql = """"""

            if len(sql) > 0:
                sqlResult = self.__srcDb.select(sql)
                if sqlResult and sqlResult != '-99999':
                    schemas = [re['table_schema'] for re in sqlResult]
                    rowData = schemas
                elif sqlResult == '-99999':
                    rowData = []
                    self.__srcDb = connDb(self.__srcDbInfo)  # 创建源数据库链接
                else:
                    rowData =[]
            else:
                rowData = []
        except Exception as e:
            errors = traceback.format_exc()
            print(errors)
            rowData = []
        return rowData


if __name__ == '__main__':
    conf = {'db_type': 'mysql', 'host': 'localhost', 'port': '3306', 'user': 'root', 'pwd': 'root1234',
            'charset': 'utf8',
            'db_name': 'test'}
    dbMetaConfirmTest = dbMetaConfirm(conf)
    result = dbMetaConfirmTest.dbMetaSchema()
    print(result)
