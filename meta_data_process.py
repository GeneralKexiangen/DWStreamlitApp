# -*- coding: utf-8 -*-
import traceback
import re
import os
import pymysql
import pandas as pd
import sys
import meta_sql_config as sqlVar
from meta_conn_db import connDb
from meta_excel_method import writeExcel
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))));
pymysql.install_as_MySQLdb()
pythonFileName = os.path.basename(__file__)


class dbMeta(object):
    def __init__(self, srcDbInfo, systemName, metaType, schemaList):
        supportList = ['oracle', 'sqlserver', 'hive', 'pg', 'mysql']
        if metaType.lower() == 'hive' and srcDbInfo['db_type'].lower() != 'mysql':
            print('hiveMetaStore对应的数据库类型为mysq,源数据库类型:{srcDbType}'.format(srcDbType=srcDbInfo['db_type']))
            exit()
        elif metaType.lower() != 'hive' and srcDbInfo['db_type'].lower() != metaType.lower():
            print('数据类型不匹配:元数据库类型:{metaType},源数据库类型:{src_db_type}'.format(metaType=metaType,
                                                                          src_db_type=srcDbInfo['db_type']))
            exit()
        elif metaType.lower() not in supportList:
            print('暂时支持{supportList},输入的metaType为:{src_db_type}'.format(supportList=supportList,
                                                                        src_db_type=srcDbInfo['db_type']))
            exit()
        self.__srcDbInfo = srcDbInfo
        self.__systemName = systemName
        self.__metaType = metaType[0:1].upper() + metaType[1:]
        self.__tableSchema = '\'' + """\',\'""".join(schemaList).lower() + '\''

    def xstr(self, s):
        try:
            if isinstance(s, bytes):
                s = bytes.decode(
                    s
                    , 'utf-8'
                    , 'ignore'
                )
            if s is None:
                return ''
            else:
                return str(s)
        except Exception as e:
            errors = traceback.format_exc()
            print(errors)
            print(" {fileName}--->{name}--报错--------------".format(
                name=sys._getframe().f_code.co_name
                , fileName=pythonFileName
            )
            )
            for x in (sys._getframe().f_code.co_varnames):
                print(x)
                print(eval(x))

    def get_simple_data(self, tableInfo):
        '''获取数据样例'''
        sql = """"""
        try:
            print('正在获取样例数据:' + tableInfo['table_schema'] + '.' + tableInfo['table_name'])
            if self.__metaType.lower() == 'mysql':
                sql = """
                    select * from `{tableSchema}`.`{tableName}` limit 1
                """.format(tableName=tableInfo['table_name'], tableSchema=tableInfo['table_schema'])
            elif self.__metaType.lower() == 'oracle':
                sql = """
                    select * from {tableSchema}."{tableName}" WHERE ROWNUM<=1
                """.format(tableName=tableInfo['table_name'], tableSchema=tableInfo['table_schema'])
            elif self.__metaType.lower() == 'sqlserver':
                sql = """
                    select top 1 * from {tableSchema}.{tableName} 
                """.format(tableName=tableInfo['table_name'], tableSchema=tableInfo['table_schema'])
            elif self.__metaType.lower() == 'pg':
                sql = """
                    select  * from "{tableSchema}"."{tableName}"  limit 1
                """.format(tableName=tableInfo['table_name'], tableSchema=tableInfo['table_schema'])
            elif self.__metaType.lower() == 'hive':
                sql = """"""

            if len(sql) > 0:
                sqlResult = self.__srcDb.select(sql)
                if sqlResult and sqlResult != '-99999':
                    rowData = {'codes': 1, 'code_text': '有数据', 'data': sqlResult[0]}
                elif sqlResult == '-99999':
                    rowData = {'codes': 4, 'code_text': '获取数据报错', 'data': {}}
                    self.__srcDb = connDb(self.__srcDbInfo)  # 创建源数据库链接
                else:
                    rowData = {'codes': 2, 'code_text': '空表', 'data': {}}
            else:
                rowData = {'codes': 3, 'code_text': '暂不探查', 'data': {}}
        except Exception as e:
            errors = traceback.format_exc()
            print(errors)
            print(" {fileName}--->{name}--报错--------------".format(
                name=sys._getframe().f_code.co_name
                , fileName=pythonFileName
            )
            )
            for x in (sys._getframe().f_code.co_varnames):
                print(x)
                print(eval(x))
            rowData = {'codes': 4, 'code_text': '获取数据报错', 'data': {}}
        return rowData

    def metadata_to_excel(self, filePath):
        try:
            self.__writerExcel = writeExcel(filePath)  ##创建excel写入对象
            # 不同源数据系统获取表信息SQL
            sql = getattr(sqlVar, 'inv{metaType}Tab'.format(metaType=self.__metaType)).format(
                systemName=self.__systemName, tableSchema=self.__tableSchema)
            tableList = self.__srcDb.select(sql)  ##获取表列表
            # print('>>>>>>>>>>',tableList)
            columns = {'system_name': '业务系统名称'
                , 'table_schema': '数据库SCHEMA'
                , 'table_name': '表名'
                , 'table_type': '表类型'
                , 'table_name_cn': '表描述'
                , 'generate_type': '表数据生成方式(1.从外部同步;2.本系统业务操作产生;0.空表）'
                , 'is_used': '业务是否使用(手工填)'
                , 'is_core_table': '是否核心表(手工填)'
                , 'time_col': '时间字段列表'
                , 'operate_type': '数据操作类型包含:I, Insert;U,Update;D,Delete(手工填)'
                , 'is_phy_del': '是否有物理删除(手工填)'
                , 'etl_time_col': 'ETL时间字段(手工填)'
                , 'table_rows': '表总行数'
                , 'day_rows': '日增量行数'
                , 'primary_key': '主键字段'
                , 'table_size_mb': '表大小_MB'
                , 'index_size_mb': '索引大小_MB'
                , 'db_type': '数据库类型'
                , 'is_comment': '是否有注释'
                , 'view_sql': '视图定义'
                       }
            tableInfoDf = pd.DataFrame(list(tableList))
            tableInfoDf.rename(columns=columns, inplace=True)
            tableInfoDf = tableInfoDf.apply(pd.to_numeric, errors='ignore')
            self.__writerExcel.write_excel(tableInfoDf, sheet_name='数据目录', header_row_position=0)  ##表目录写入excel中
            tableColDfs = self.metadata_col_to_excel(tableList)  # 字段写入到excel
            metaDfResult = {'tableInfoDf': tableInfoDf, 'tableColDf': tableColDfs}
            self.__writerExcel.save_excel()  # 保存zexcel文件
            return metaDfResult
        except Exception as e:
            errors = traceback.format_exc()
            print(errors)
            print(" {fileName}--->{name}--报错--------------".format(
                name=sys._getframe().f_code.co_name
                , fileName=pythonFileName
            )
            )
            for x in (sys._getframe().f_code.co_varnames):
                print(x)
                print(eval(x))
            self.__writerExcel.save_excel()  # 保存excel文件
            return {}

    def metadata_col_to_excel(self, tableList):
        '''
            功能描述: 获取源数据库的表目录及字段信息,写入excel中
        '''
        try:
            i = 2  # excel 从第二行开始写数据,第一行是
            sql = getattr(sqlVar, 'inv{metaType}ColList'.format(metaType=self.__metaType)).format(
                systemName=self.__systemName, tableSchema=self.__tableSchema)
            schemaColList = self.__srcDb.select(sql)
            schemaColDf = pd.DataFrame(list(schemaColList))  # 获取schema下所有的字段列表
            sheetNameList = []  # 用来判断在不同schema下面重复的表名
            tableColDfResult = {}
            for tableInfo in tableList:
                filterTable = schemaColDf['table_name'] == tableInfo['table_name']
                filterSchame = schemaColDf['table_schema'] == tableInfo['table_schema']
                filterSystem = schemaColDf['system_name'] == tableInfo['system_name']
                tableColDf = schemaColDf.loc[filterTable & filterSchame & filterSystem].copy()  # 筛选单个表字段
                rowData = self.get_simple_data(tableInfo)  # 获取样例数据
                if rowData['codes'] == 1:
                    # 查询到了数据
                    rowDataValue = list(rowData['data'].values())
                else:
                    # 查询不到数据
                    rowDataValue = rowData['code_text']
                tableColDf['simple_data'] = rowDataValue  # 样例数据写入到dataframe中
                columns = {'system_name': '业务系统名称'
                    , 'table_schema': '数据库SCHEMA'
                    , 'table_name': '表名'
                    , 'column_name': '字段名'
                    , 'table_comment': '表描述'
                    , 'column_comment': '字段描述'
                    , 'column_type': '字段类型'
                    , 'is_pk': '是否主键'
                    , 'is_idx': '是否索引'
                    , 'is_null': '是否为空'
                    , 'column_desc': '字段详细描述(手工填)'
                    , 'column_rank': '字段排序'
                    , 'simple_data': '数据样例'
                           }
                tableColDf.rename(columns=columns, inplace=True)
                tableColDfResult[tableInfo['table_schema'] + '.' + tableInfo['table_name']] = tableColDf
                sheetName = re.sub(r'[\\:*\[\]\'/?$]*', '',
                                   tableInfo['table_name'])  # 替换excel 中sheet不允许出现的特殊字符串: / ? * [ ]
                # excel只能使用31个字符作为sheetName
                if len(sheetName) > 31:
                    sheetName = sheetName[0:26] + sheetName[-5:]
                else:
                    sheetName = sheetName[0:31]
                if sheetName.upper() in sheetNameList:
                    sheetName = 'o' + sheetName[1:30] + 'k'
                '''
                    写excel 
                    :parm  tableColDf           单个表字段数据
                    :parm  sheet_name           写到哪个sheet
                    :parm  header_row_position  从第几行开始写

                '''
                self.__writerExcel.write_excel(tableColDf, sheet_name=self.xstr(sheetName), header_row_position=1)
                '''
                    写excel Url 链接
                    :parm  src_sheet_name       哪个sheet需要写url
                    :parm  target_sheet_name    跳转到哪个sheet
                    :parm  col                  url写在第几列
                    :parm  line                 url写在第几行
                    :parm  col_text             链接名称
                    :parm  targetCol            跳转到第几列
                    :parm  targetLine           跳转大第几行
                '''
                self.__writerExcel.write_url(src_sheet_name='数据目录', target_sheet_name=sheetName, line=i, col='C',
                                             col_text=tableInfo['table_name'], targetCol='A', targetLine=1)  # 目录链接到表
                self.__writerExcel.write_url(src_sheet_name=sheetName, target_sheet_name='数据目录', line=1, col='A',
                                             col_text='返回', targetCol='C', targetLine=i)  # 返回url
                sheetNameList.append(sheetName.upper())  # 用来判断在不同schema下面重复的表名
                i = i + 1
            return tableColDfResult
        except Exception as e:
            errors = traceback.format_exc()
            print(errors)
            print(" {fileName}--->{name}--报错--------------".format(
                name=sys._getframe().f_code.co_name
                , fileName=pythonFileName
            )
            )
            for x in (sys._getframe().f_code.co_varnames):
                print(x)
                print(eval(x))
            return {}

    def metadata_inv_to_excel(self, excelPath, excelName):
        self.__srcDb = connDb(self.__srcDbInfo)  # 创建源数据库链接
        filePath = '{excelPath}/{excelName}'.format(excelName=excelName, excelPath=excelPath)
        if not os.path.exists(excelPath):  # 如果目录不存在创建目录
            os.makedirs(excelPath)
        if os.path.exists(filePath):  # 如果文件存在删除文件
            os.remove(filePath)
        DfResult = self.metadata_to_excel(filePath)
        self.__srcDb.close()  # 关闭数据库链接
        return DfResult

    def metadata_init_target_table(self, tableMetaTab, colMetaTab, impType):
        try:
            '''
                功能描述:创建元数据表,并初始化数据
                :parm   tableMetaTab    表元数据表名称 
                :parm   colMetaTab      字段元数据表名称 
                :parm   impType         导入类型 1:删除数据后重导 2:断点续传,并添加新的元数据信息 
            '''
            tmpTableMetaTab = tableMetaTab + '_tmp'
            tmpColMetaTab = colMetaTab + '_tmp'
            # 创建表
            sql = sqlVar.invCreateTableMeta.format(tableName=tableMetaTab)
            self.__targetDb.ddl(sql)  # 创建表元数据表
            sql = sqlVar.invCreateColMeta.format(tableName=colMetaTab)
            self.__targetDb.ddl(sql)  # 创建字段元数据表

            # 创建临时表
            sql = sqlVar.invCreateTableMeta.format(tableName=tmpTableMetaTab)
            self.__targetDb.ddl(sql)  # 创建表元数据表
            sql = sqlVar.invCreateColMeta.format(tableName=tmpColMetaTab)
            self.__targetDb.ddl(sql)  # 创建字段元数据表

            # 清空临时表
            sql = """truncate table {tableMetaTab}""".format(tableMetaTab=tmpTableMetaTab)
            self.__targetDb.ddl(sql)
            sql = """truncate table {colMetaTab}""".format(colMetaTab=tmpColMetaTab)
            self.__targetDb.ddl(sql)
            # ----------------------------获取表元数据并导入临时表
            # 不同源数据系统获取表信息SQL
            sql = getattr(sqlVar, 'inv{metaType}Tab'.format(metaType=self.__metaType)).format(
                systemName=self.__systemName, tableSchema=self.__tableSchema)
            # 获表取元数据
            tableList = self.__srcDb.select(sql)
            tableInfoDf = pd.DataFrame(tableList)
            # 表元据导入临时表
            tableInfoDf.to_sql(tmpTableMetaTab, self.__engine, if_exists='append', index=False)

            # ----------------------------获字段元数据并导入临时表
            # 不同源数据系统获取字段信息SQL
            sql = getattr(sqlVar, 'inv{metaType}ColList'.format(metaType=self.__metaType)).format(
                systemName=self.__systemName, tableSchema=self.__tableSchema)
            # 获取元数据
            colList = self.__srcDb.select(sql.format(systemName=self.__systemName, tableSchema=self.__tableSchema))
            colInfoDF = pd.DataFrame(colList)
            # 表元据导入临时表
            colInfoDF.to_sql(tmpColMetaTab, self.__engine, if_exists='append', index=False)

            if impType == '1':
                # 删除数据
                sql = sqlVar.invDelTabMeta.format(tableName=tableMetaTab, tableSchema=self.__tableSchema,
                                                  systemName=self.__systemName)
                self.__targetDb.dml(sql)
                # 删除数据
                sql = sqlVar.invDelColMeta.format(tableName=colMetaTab, tableSchema=self.__tableSchema,
                                                  systemName=self.__systemName)
                self.__targetDb.dml(sql)
            elif impType == '2':
                # 清空表
                sql = """truncate table {tableMetaTab}""".format(tableMetaTab=tableMetaTab)
                self.__targetDb.ddl(sql)
                sql = """truncate table {colMetaTab}""".format(colMetaTab=colMetaTab)
                self.__targetDb.ddl(sql)

                # 临时表插入正式表,增量更新
            sql = sqlVar.invTabMetaInit.format(tableMetaTab=tableMetaTab, tmpTableMetaTab=tmpTableMetaTab)
            self.__targetDb.dml(sql)
            # 临时表插入正式表,增量更新
            sql = sqlVar.invColMetaInit.format(colMetaTab=colMetaTab, tmpColMetaTab=tmpColMetaTab)
            self.__targetDb.dml(sql)

            # 更新表数据,可能会删除修改字段
            sql = sqlVar.updateTabMeta.format(table=tableMetaTab, tmpTable=tmpTableMetaTab,
                                              tableSchema=self.__tableSchema)
            self.__targetDb.dml(sql)

            # 更新字段数据,可能会删除修改字段
            sql = sqlVar.updateColMeta.format(table=colMetaTab, tmpTable=tmpColMetaTab, tableSchema=self.__tableSchema)
            self.__targetDb.dml(sql)

            # 删除临时表
            sql = """drop table {tableNmae}""".format(tableNmae=tmpTableMetaTab)  # 创建元数据表
            self.__targetDb.ddl(sql)

            # 删除临时表
            sql = """drop table {tableNmae}""".format(tableNmae=tmpColMetaTab)  # 创建元数据表
            self.__targetDb.ddl(sql)

        except Exception as e:
            errors = traceback.format_exc()
            print(errors)

    def metadata_row_data(self, colMetaTab, tableMetaTab):
        '''
            功能描述: 更新每个表的示例数据
        '''
        try:
            sql = sqlVar.rowDataTab.format(tableMetaTab=tableMetaTab, colMetaTab=colMetaTab,
                                           tableSchema=self.__tableSchema)
            tableList = self.__targetDb.select(sql)  # 获取需要获取rowData表列表
            for tableInfo in tableList:
                rowData = self.get_simple_data(tableInfo)  # 获取样例数据
                if rowData['codes'] == 1:
                    # 如果正常获取到数据更新每个字段
                    for colName, colValue in rowData['data'].items():
                        sql = sqlVar.updateSimpleDataCol.format(
                            colMetaTab=colMetaTab
                            , tableSchema=tableInfo['table_schema']
                            , tableName=tableInfo['table_name']
                            , columnName=colName.upper()  # oracle 要大写
                            , systemName=tableInfo['system_name']
                            , colValue=self.xstr(colValue).replace('"', '\\"')
                            , simpleStatus=rowData['codes']
                        )
                        self.__targetDb.dml(sql)
                else:
                    # 如果正常获取到数据更新每个字段
                    sql = sqlVar.updateSimpleDataTab.format(
                        colMetaTab=colMetaTab
                        , tableSchema=tableInfo['table_schema']
                        , tableName=tableInfo['table_name']
                        , systemName=tableInfo['system_name']
                        , colValue=rowData['code_text']
                        , simpleStatus=rowData['codes']
                    )
                    self.__targetDb.dml(sql)
        except Exception as e:
            errors = traceback.format_exc()
            print(errors)
            print(" {fileName}--->{name}--报错--------------".format(
                name=sys._getframe().f_code.co_name
                , fileName=pythonFileName
            )
            )
            for x in (sys._getframe().f_code.co_varnames):
                print(x)
                print(eval(x))

    def metadata_inv_to_db(self, targetDbInfo, tableMetaTab, colMetaTab, impType):
        if targetDbInfo['db_type'].lower() != 'mysql':
            print('目前只支持盘点数据写入Mysql')
            exit()
        self.__targetDbInfo = targetDbInfo  # 获取目标数据库链接信息
        self.__srcDb = connDb(self.__srcDbInfo)  # 创建源数据库链接
        self.__targetDb = connDb(targetDbInfo)  # 创建目标数据库链接
        self.__engine = create_engine(
            """mysql://{user}:{pwd}@{host}:{port}/{dbName}?charset={charset}""".format(
                host=self.__targetDbInfo['host']
                , user=self.__targetDbInfo['user']
                , pwd=self.__targetDbInfo['pwd']
                , dbType=self.__targetDbInfo['db_type']
                , port=self.__targetDbInfo['port']
                , charset=self.__targetDbInfo['charset']
                , dbName=self.__targetDbInfo['db_name']
            )
        )
        tableList = self.metadata_init_target_table(tableMetaTab, colMetaTab, impType)  # 创建表,并初始化数据
        self.metadata_row_data(colMetaTab=colMetaTab, tableMetaTab=tableMetaTab)  # 示例数据更新到表
        self.__srcDb.close()  # 关闭数据库链接


if __name__ == '__main__':
    conf = {'db_type': 'mysql', 'host': 'localhost', 'port': '3306', 'user': 'root', 'pwd': 'root1234',
            'charset': 'utf8',
            'db_name': 'test'}
    dbInvTool = dbMeta(
        srcDbInfo=conf  # 需要盘点的数据库配置信息
        , systemName='mysql'  # 需要盘点业务系统名称
        , metaType='mysql'  # 需要盘点数据库类型(hive,mysql,oracle,sqlserver,pg)
        , schemaList=['test']  # 需要导出的 schema 列表
    )
    dbInvTool.metadata_inv_to_excel(
        excelPath='./tmp/meta'  # excel生成目录
        , excelName='sqlserver.xlsx'  # excel文件名
    )  # 盘点数据写入excel
    # dbInvTool.metadata_inv_to_db(
    #     targetDbInfo=conf['mysql']  # 目标数据库
    #     , tableMetaTab='jdy___inv_meta_db_table'  # 表元数据表
    #     , colMetaTab='jdy___inv_meta_db_column'  # 字段元数据表
    #     , impType='2'  # 1:delete schema列表后重导    2:truncate 后重导  3:2:断点续传
    # )  # 盘点数据写入Mysql
