import streamlit as st
from meta_data_process import dbMeta
from meta_data_confirm import dbMetaConfirm
import time
import traceback
import meta_sql_config as sqlVar


def get_hive_ddl_sql(tdf, sysType):
    tableName = 'ods_' + sysType + '_' + list(set(tdf['表名']))[0]
    tableComment = list(set(tdf['表描述']))[0]

    def trans_data_type(x):
        x = str(x)
        if 'int' in x:
            return ' BIGINT COMMENT '
        elif x in ('decimal', 'double', 'float'):
            return ' DOUBLE COMMENT '
        else:
            return ' STRING COMMENT '

    tdf['hive_data_type'] = tdf['data_type'].apply(lambda x: trans_data_type(x))
    maxColLen = max(tdf['字段名'].str.len())
    for index, row in tdf.iterrows():
        tdf.loc[index, 'sql_str'] = row['字段名'] + ' '*(maxColLen+1-len(row['字段名'])) + row['hive_data_type'] + "'" + row['字段描述'] + "'"
    sqlStrList = list(tdf['sql_str'])
    sqlStr = """\n    , """.join(str(i) for i in sqlStrList)
    # 生成建表语句
    createHiveDdlSql = sqlVar.createHiveDdlSql.format(
        column_info=sqlStr
        , table_name=tableName
        , table_comments=tableComment
        , current_date=time.strftime('%Y-%m-%d', time.localtime(time.time()))
        , partition_str='ds'
        , src_system_name=sysType
    )
    return createHiveDdlSql


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

session_state_list = ['schemas', 'abstract_df', 'all_tables', 'table_df']
for ss in session_state_list:
    if ss not in st.session_state:
        if ss == 'schemas':
            st.session_state[ss] = []
        else:
            st.session_state[ss] = ''

st.title('Data Inventorying')

db_connect_info = st.sidebar.text_input('Database Connect Information', 'mysql/localhost/3306/root/root1234/test')
sys_type = st.sidebar.text_input('Business System Type', 'local')

db_connect_info_ = []
conf = {}

if (len(db_connect_info.split('/')) == 6 or len(db_connect_info.split('/')) == 8) and len(sys_type) > 0:
    db_connect_info_ = db_connect_info.split('/')
    connect_type = ''
    connect_name = ''
    if len(db_connect_info_) == 6:
        db_connect_info_.append(connect_type)
        db_connect_info_.append(connect_name)
    conf = {'db_type': db_connect_info_[0], 'host': db_connect_info_[1], 'port': db_connect_info_[2],
            'user': db_connect_info_[3], 'pwd': db_connect_info_[4], 'charset': 'utf8',
            'db_name': db_connect_info_[5], 'connect_type': db_connect_info_[6], 'connect_name': db_connect_info_[7]}
    schemas_check = st.sidebar.button('Submit')
    if schemas_check:
        dbSchemasFun = dbMetaConfirm(srcDbInfo=conf)
        schema_list = dbSchemasFun.dbMetaSchema()
        if len(schema_list) == 0:
            st.sidebar.warning('Connection Failed')
        st.session_state.schemas = schema_list
    schemas_choose = st.sidebar.multiselect('Select Schemas', st.session_state.schemas)
    query = st.sidebar.button('Start Inventorying')
    print('>>>>>>>>>>>>', schemas_choose)
    metaDfJson = {}
    if query and len(schemas_choose) > 0:
        st.balloons()
        try:
            dbInvTool = dbMeta(
                srcDbInfo=conf  # 需要盘点的数据库配置信息
                , systemName=sys_type  # 需要盘点业务系统名称
                , metaType=db_connect_info_[0]  # 需要盘点数据库类型(hive,mysql,oracle,sqlserver,pg)
                , schemaList=schemas_choose  # 需要导出的 schema 列表
            )
            metaDfJson = dbInvTool.metadata_inv_to_excel(
                excelPath='./tmp/meta' # excel生成目录
                , excelName='{filename}.xlsx'.format(filename=sys_type + 'DataInventory')  # excel文件名
            )
        except:
            errors = traceback.format_exc()
            print(errors)
        abstract_df = metaDfJson['tableInfoDf']
        abstract_df = abstract_df.astype(str)
        table_df = metaDfJson['tableColDf']
        st.session_state.table_df = table_df
        st.session_state.abstract_df = abstract_df
        st.session_state.all_tables = list(metaDfJson['tableColDf'].keys())
    elif len(schemas_choose) == 0:
        st.sidebar.warning('No Schema')
        st.session_state.table_df = ''
        st.session_state.abstract_df = ''
        st.session_state.all_tables = ''
    st.subheader('Overview Of Inventorying')
    st.write(st.session_state.abstract_df)
    st.subheader('Detail Of Inventorying')
    c1, c2 = st.columns([8, 2])
    with c1:
        table = st.selectbox('Select A Table', st.session_state.all_tables)
    with c2:
        if len(st.session_state.abstract_df) > 0:
            with open("./tmp/meta/{filename}.xlsx".format(filename=sys_type + 'DataInventory'), "rb") as file:
                btn = st.download_button(
                    label="Download all data inventory as CSV",
                    data=file,
                    file_name="{filename}.xlsx".format(filename=sys_type + 'DataInventory'),
                    mime='xlsx/csv'
                )
    if table:
        td = st.session_state.table_df[table]
        td = td.astype(str)
        st.dataframe(td)
        ddlSql = get_hive_ddl_sql(td, sys_type)
        st.code(ddlSql)
else:
    st.sidebar.warning('Wrong Information')
