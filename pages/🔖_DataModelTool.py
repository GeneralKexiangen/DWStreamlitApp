import streamlit as st
import pandas as pd
import meta_sql_config as sqlVar
import time
import streamlit.components.v1 as components


def get_hive_model_ddl_sql(modelDf, tableDf, tableName):
    tableComment = list(modelDf[modelDf['表名'] == tableName]['表描述'])[0]
    partitionStr = list(modelDf[modelDf['表名'] == tableName]['分区字段'])[0]
    sysType = list(modelDf[modelDf['表名'] == tableName]['数据域'])[0]

    maxColLen = max(tableDf['字段名'].str.len())
    for index, row in tableDf.iterrows():
        tableDf.loc[index, 'sql_str'] = row['字段名'] + ' '*(maxColLen+1-len(row['字段名'])) + row['字段数据类型'].upper() + " COMMENT '" + row['字段描述'] + "' "

    sqlStrList = list(tableDf['sql_str'])
    sqlStr = """\n    , """.join(str(i) for i in sqlStrList)
    # 生成建表语句
    createHiveDdlSql = sqlVar.createHiveDdlSql.format(
        column_info=sqlStr
        , table_name=tableName
        , table_comments=tableComment
        , current_date=time.strftime('%Y-%m-%d', time.localtime(time.time()))
        , partition_str=partitionStr
        , src_system_name=sysType
    )
    tableDf['加工逻辑'].fillna("{0}", inplace=True)
    tableDf['关联关系'].fillna("无", inplace=True)

    for index, row in tableDf.iterrows():
        tableDf.loc[index, 'col_str'] = str(row['加工逻辑']).format(str(row['来源表别名'] + '.' + row['来源字段'])) + ' AS ' + row[
            '字段名'] + ' '*(maxColLen+1-len(row['字段名']))+' --' + row['字段描述']
    tableDf['col_code_str'] = tableDf['col_str'].apply(lambda x: str(x).split(' AS')[0])
    maxLen = max(tableDf['col_code_str'].str.len())
    tableDf['col_str'] = tableDf['col_str'].apply(
        lambda x: str(x).replace(' AS', ' ' * (maxLen+1 - len(str(x).split(' AS')[0])) + 'AS'))
    colSqlStrList = list(tableDf['col_str'])
    colSqlStr = """\n    , """.join(str(i) for i in colSqlStrList)
    tableRelations = []
    tableDf['tableRelationStr'] = tableDf['来源表'] + ' ' + tableDf['来源表别名'] + ' ON ' + tableDf['关联关系']
    mainTable = str(tableDf['tableRelationStr'][0]).replace('ON 无', '')
    simpMainTable = mainTable.split(' ')[1]
    tableRelations.append(mainTable)
    for tr in list(tableDf['tableRelationStr']):
        if '无' not in tr and tr not in tableRelations:
            tableRelations.append(
                'LEFT JOIN ' + tr + ' AND ' + str(tr).split(' ')[1] + '.{0}={1}.{0}'.format(partitionStr,
                                                                                            simpMainTable))
    tableJoinStr = """\n""".join(str(i) for i in tableRelations)
    # 生成模型sql语句
    createHiveModelSql = sqlVar.modelJobSql.format(
        columnListStr=colSqlStr
        , tableJoinListStr=tableJoinStr
        , whereSqlStr="{2}.{0}='{1}'".format(partitionStr, '${yyyyMMdd,-1d}', simpMainTable)
        , tableName=tableName
        , tableComment=tableComment
        , currentDate=time.strftime('%Y-%m-%d', time.localtime(time.time()))
        , partitionStr=partitionStr + "='{0}'".format('${yyyyMMdd,-1d}')
        , srcSystemName=sysType
    )
    return createHiveDdlSql, createHiveModelSql


st.set_page_config(
    page_title="DATA.ER",
    page_icon="🐬",
    layout="wide",
    initial_sidebar_state= 'collapsed'
)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.sidebar.markdown("# Data Model Tool️")
st.title('Data Model')

session_state_list = ['upFile', 'upFileDf', 'tables']
for ss in session_state_list:
    if ss not in st.session_state:
        st.session_state[ss] = None

with st.expander("See Data Model Template And Download"):
    st.write("""
            Design the data model with this template and according to the rule within,
            then upload the data model file after design,
            finally standard ddl and sql code to be generated quickly.
        """)
    with open("./resource/模型设计.xlsx", "rb") as file:
        btn = st.download_button(
            label="Download",
            data=file,
            file_name="模型设计.xlsx",
            mime='xlsx/csv'
        )
upFile = st.file_uploader('Upload a data model file to generate ddl and sql code', ['xlsx', 'csv'])
if upFile:
    upFileDf = pd.read_excel(upFile)
    st.dataframe(upFileDf)
    tables = list(upFileDf['表名'])
    st.session_state.upFile = upFile
    st.session_state.upFileDf = upFileDf
    st.session_state.tables = tables
    table = st.selectbox('Select a Data Model', st.session_state.tables)
    if table:
        tdf = pd.read_excel(st.session_state.upFile, sheet_name=table, header=1)
        tdf["字段描述"].fillna("", inplace=True)
        st.dataframe(tdf)
        ddl, sql = get_hive_model_ddl_sql(st.session_state.upFileDf, tdf, table)
        c1, c2 = st.columns(2)
        with c1:
            st.code(ddl)
        with c2:
            st.code(sql)

