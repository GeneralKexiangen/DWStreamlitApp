# -*- coding:utf-8 -*-
"""
    sql配置文件
"""
# -------------------------------------------自动盘点创建表结构----------------------------------------------------------
# 创建表元数据表
invCreateTableMeta = """
CREATE TABLE IF NOT EXISTS `{tableName}` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `system_name` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '系统名称',
  `table_schema` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '数据库SCHEMA',
  `table_name` varchar(200) COLLATE utf8_bin DEFAULT NULL COMMENT '数据表英文名',
  `table_type` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '表类型',
  `table_name_cn` text COLLATE utf8_bin COMMENT '数据表中文名',
  `generate_type` varchar(10) COLLATE utf8_bin DEFAULT NULL COMMENT '表数据生成方式（1.从外部同步；2.本系统业务操作产生；0.空表）',
  `is_used` varchar(10) COLLATE utf8_bin DEFAULT NULL COMMENT '业务是否使用',
  `is_core_table` varchar(10) COLLATE utf8_bin DEFAULT NULL COMMENT '是否核心表',
  `time_col` text COLLATE utf8_bin COMMENT '时间字段列表',
  `operate_type` varchar(10) COLLATE utf8_bin DEFAULT NULL COMMENT '数据操作类型包含：I, Insert；U，Update；D，Delete',
  `is_phy_del` varchar(1) COLLATE utf8_bin DEFAULT NULL COMMENT '是否有物理删除',
  `etl_time_col` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT 'ETL时间字段',
  `table_rows` bigint(20) DEFAULT NULL COMMENT '表总行数',
  `day_rows` bigint(20) DEFAULT NULL COMMENT '日增量行数',
  `primary_key` varchar(800) COLLATE utf8_bin DEFAULT NULL COMMENT '主键字段',
  `table_size_mb` double DEFAULT NULL COMMENT '表大小_MB',
  `index_size_mb` double DEFAULT NULL COMMENT '索引大小_MB',
  `db_type` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '数据库类型',
  `is_comment` varchar(1) COLLATE utf8_bin DEFAULT NULL COMMENT '是否有注释',
  `view_sql` text COLLATE utf8_bin COMMENT '视图定义',
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `drop_date` datetime DEFAULT NULL COMMENT '表删除时间',
  `is_valid` tinyint(4) DEFAULT '1' COMMENT '0：失效 1：生效',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_table` (`system_name`,`table_schema`,`table_name`,`db_type`) USING BTREE
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""
# 创建字段元数据表
invCreateColMeta = """
CREATE TABLE IF NOT EXISTS `{tableName}` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `system_name` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '系统名称',
  `table_schema` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '数据库SCHEMA',
  `table_name` varchar(200) COLLATE utf8_bin DEFAULT NULL COMMENT '数据表英文名',
  `table_comment` text COLLATE utf8_bin COMMENT '数据表中文名',
  `column_name` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '字段名',
  `column_comment` text COLLATE utf8_bin COMMENT '字段中文名',
  `column_type` text COLLATE utf8_bin COMMENT '字段类型',
  `data_type` text COLLATE utf8_bin COMMENT '数据类型',
  `is_pk` varchar(10) COLLATE utf8_bin DEFAULT NULL COMMENT '是否主键',
  `is_idx` varchar(10) COLLATE utf8_bin DEFAULT NULL COMMENT '是否索引',
  `is_null` varchar(10) COLLATE utf8_bin DEFAULT NULL COMMENT '是否为空',
  `column_desc` text COLLATE utf8_bin DEFAULT NULL COMMENT '字段描述',
  `simple_data` text COLLATE utf8_bin COMMENT '数据示例',
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `drop_date` datetime DEFAULT NULL COMMENT '字段删除时间',
  `is_valid` tinyint(4) DEFAULT '1' COMMENT '0：失效 1：生效',
  `simple_status` tinyint(4) DEFAULT '0' COMMENT '0: 未获取 1:获取成功 2  ：获取失败',
  `column_rank` int(11) DEFAULT NULL COMMENT '字段排序',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_column` (`system_name`,`table_schema`,`table_name`,`column_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""
# 初始化表元数据表
invTabMetaInit = """
INSERT INTO  {tableMetaTab} (
    system_name   
   , table_schema  
   , table_name    
   , table_type    
   , table_name_cn 
   , generate_type 
   , is_used       
   , is_core_table 
   , time_col      
   , operate_type  
   , is_phy_del    
   , etl_time_col  
   , table_rows    
   , day_rows      
   , primary_key   
   , table_size_mb 
   , index_size_mb 
   , db_type       
   , is_comment    
   , view_sql         
)
SELECT a.system_name   
   , a.table_schema  
   , a.table_name    
   , a.table_type    
   , a.table_name_cn 
   , a.generate_type 
   , a.is_used       
   , a.is_core_table 
   , a.time_col      
   , a.operate_type  
   , a.is_phy_del    
   , a.etl_time_col  
   , a.table_rows    
   , a.day_rows      
   , a.primary_key   
   , a.table_size_mb 
   , a.index_size_mb 
   , a.db_type       
   , a.is_comment    
   , a.view_sql
FROM  {tmpTableMetaTab} a 
LEFT JOIN
{tableMetaTab} b 
on
( 
    a.table_name = b.table_name 
    and a.table_schema = b.table_schema
    and a.system_name = b.system_name 
    and a.db_type = b.db_type
)
WHERE b.table_name is null 
"""
# 初始化字段元数据表
invColMetaInit = """
INSERT INTO  {colMetaTab}(
      system_name    
    , table_schema   
    , table_name     
    , table_comment  
    , column_name    
    , column_comment 
    , column_type    
    , data_type      
    , is_pk          
    , is_idx         
    , is_null        
    , column_desc    
    , simple_data    
    , create_date    
    , modify_date    
    , drop_date      
    , is_valid       
    , column_rank
)
SELECT  a.system_name    
    , a.table_schema   
    , a.table_name     
    , a.table_comment  
    , a.column_name    
    , a.column_comment 
    , a.column_type    
    , a.data_type      
    , a.is_pk          
    , a.is_idx         
    , a.is_null        
    , a.column_desc    
    , a.simple_data    
    , a.create_date    
    , a.modify_date    
    , a.drop_date      
    , a.is_valid      
    , a.column_rank
FROM  {tmpColMetaTab} a 
LEFT JOIN
{colMetaTab} b 
on
( 
    a.table_name = b.table_name 
    and a.table_schema = b.table_schema
    and a.column_name = b.column_name 
    and a.system_name = b.system_name
)
WHERE b.table_name is null 
"""
# 更新表元数据表,可能有的表会删除
updateTabMeta = """
UPDATE {table}   a 
LEFT JOIN
{tmpTable} b 
on
( 
    a.table_name = b.table_name 
    and a.table_schema = b.table_schema
    and a.system_name = b.system_name 
    and a.db_type = b.db_type
)
SET a.is_valid = (
                   CASE WHEN b.table_name is null THEN 0 
                        WHEN b.table_name is not null THEN b.is_valid
                     ELSE a.is_valid
                   END
                 )
   , a.drop_date = (
                   CASE WHEN b.table_name is null THEN CURRENT_TIMESTAMP()
                     ELSE a.drop_date
                   END
                 ) 
WHERE  lower(a.table_schema) in ({tableSchema})

"""
# 更新字段元数据表,可能有的字段会删除
updateColMeta = """
UPDATE  {table} a 
LEFT JOIN
{tmpTable} b 
on
( 
    a.table_name = b.table_name 
    and a.table_schema = b.table_schema
    and a.column_name = b.column_name 
    and a.system_name = b.system_name
)
SET a.is_valid = (
                   CASE WHEN b.table_name is null THEN 0 
                        WHEN b.table_name is not null THEN b.is_valid
                     ELSE a.is_valid
                   END
                 )
   , a.drop_date = (
                   CASE WHEN b.table_name is null THEN CURRENT_TIMESTAMP()
                     ELSE a.drop_date
                   END
                 ) 
WHERE  lower(a.table_schema) in ({tableSchema})
"""
# 删除数据
invDelTabMeta = """
DELETE FROM {tableName} 
WHERE system_name ='{systemName}' 
AND lower(table_schema) in ({tableSchema})
"""
# 删除数据
invDelColMeta = """
DELETE FROM {tableName} 
WHERE system_name ='{systemName}' 
AND lower(table_schema) in ({tableSchema})
"""
# 需要获取rowData表列表
rowDataTab = """
SELECT a.table_name
    , a.table_schema
    , a.system_name
FROM {colMetaTab} a 
LEFT JOIN 
{tableMetaTab} b 
ON 
(
    a.table_name = b.table_name 
    AND a.table_schema = b.table_schema 
    AND a.system_name = b.system_name
)
WHERE a.is_valid = 1 
AND a.simple_status <> 1
AND lower(a.table_schema) in ({tableSchema})
GROUP BY a.table_name
    , a.table_schema
    , a.system_name
"""
# 更新示例数据按字段
updateSimpleDataCol = """
UPDATE {colMetaTab}
SET simple_data = "{colValue}"
 , simple_status = {simpleStatus}
WHERE system_name = '{systemName}'
AND table_schema = '{tableSchema}'
AND table_name = '{tableName}'
AND upper(column_name) = '{columnName}'
AND is_valid = 1
"""
# 更新示例数据全表
updateSimpleDataTab = """
UPDATE {colMetaTab}
SET simple_data = "{colValue}"
 , simple_status = {simpleStatus}
WHERE system_name = '{systemName}'
AND table_schema = '{tableSchema}'
AND table_name = '{tableName}'
AND is_valid = 1
"""

# -------------------------------------------postgresql盘点SQL--------------------------------------------------------------
# pg表列表
invPgTab = """
SELECT '{systemName}' system_name
    , a.table_schema table_schema
    , a.table_name table_name
    , a.table_type table_type
    , e.table_comment  table_name_cn
    , null generate_type
    , null is_used 
    , null is_core_table
    , d.time_col time_col 
    , null operate_type
    , null is_phy_del
    , time_col etl_time_col
    , e.table_rows   table_rows
    , null day_rows
    , b.primary_key primary_key 
    , round(pg_table_size('"' || a.table_schema || '"."' || a.table_name || '"')/1024/1024,2) table_size_mb
    , round(pg_indexes_size('"' || a.table_schema || '"."' || a.table_name || '"')/1024/1024,2) index_size_mb
    , 'pg' db_type
    , CASE WHEN e.table_comment IS NULL THEN '是' 
        ELSE '否'
      END is_comment
    , c.view_DEFINITION view_sql
FROM information_schema.TABLES a
LEFT JOIN 
(
    select aa.table_name
        , aa.table_schema
        ,  array_to_string(array_agg(COLUMN_NAME),',') PRIMARY_KEY
    from information_schema.table_constraints aa 
    join information_schema.constraint_column_usage bb 
    on (aa.constraint_name  = bb.constraint_name and aa.constraint_schema = bb.constraint_schema)
    where constraint_type = 'PRIMARY KEY'
    group by aa.table_name
        , aa.table_schema
    )  b 
ON (a.table_name = b.table_name AND a.table_schema = b.table_schema)
LEFT JOIN  information_schema.VIEWS c 
ON (a.table_schema = c.table_schema AND a.table_name = c.table_name)
LEFT JOIN 
(
    SELECT table_schema
            , table_name
            , array_to_string(array_agg(COLUMN_NAME),',') time_col
    FROM  information_schema.columns
    WHERE data_type  like '%time%'
    GROUP BY  table_schema
            , table_name 
) d
ON (a.table_schema = d.table_schema AND a.table_name = d.table_name)
LEFT JOIN 
(
    SELECT nspname table_schema
        ,relname table_name 
        ,reltuples table_rows
        ,obj_description(relfilenode,'pg_class') TABLE_COMMENT
    FROM pg_class r 
    JOIN pg_namespace n
    ON (relnamespace = n.oid)
    WHERE relkind = 'r' 
) e 
ON (a.table_schema = e.table_schema AND a.table_name = e.table_name)
WHERE lower(a.table_schema) in ({tableSchema})
ORDER BY a.table_schema
"""
# pg字段列表
invPgColList = """
SELECT '{systemName}' system_name
    , a.table_schema table_schema
    , a.TABLE_NAME table_name 
    , a.TABLE_COMMENT table_comment 
    , a.COLUMN_NAME column_name 
    , a.COLUMN_COMMENT   column_comment 
    , a.COLUMN_TYPE column_type
    , a.COLUMN_TYPE data_type
    , CASE WHEN c.COLUMN_NAME IS NOT NULL THEN '是'
            ELSE '否'
        END is_pk
    , CASE WHEN d.COLUMN_NAME IS NOT NULL THEN '是'
            ELSE '否'
        END is_idx
    , null is_null
    , a.COLUMN_COMMENT   column_desc 
    , a.column_rank  column_rank
FROM 
(
    SELECT  b.table_name
        ,a.attname COLUMN_NAME
        ,obj_description(relfilenode,'pg_class') TABLE_COMMENT
        ,pg_catalog.format_type(a.atttypid, a.atttypmod) AS COLUMN_TYPE 
        ,col_description(a.attrelid,a.attnum) as COLUMN_COMMENT 
        ,table_schema
        ,a.attnum column_rank
     FROM  pg_attribute a,
     (
         SELECT  c.oid
                ,c.relname as table_name
                ,n.nspname  table_schema
                ,relfilenode  relfilenode
         FROM  pg_catalog.pg_class c 
         LEFT JOIN pg_catalog.pg_namespace n  ON n.oid = c.relnamespace  
         WHERE c.relkind = 'r'
     ) b 
     WHERE a.attrelid = b.oid 
         AND a.attnum > 0 
         AND NOT a.attisdropped 
) a 
LEFT JOIN information_schema.KEY_COLUMN_USAGE c 
ON (a.table_name = c.table_name AND a.table_schema = c.table_schema AND a.COLUMN_NAME=c.COLUMN_NAME AND c.CONSTRAINT_NAME='PRIMARY')
LEFT JOIN  
(
    select n.nspname table_schema,
            t.relname as table_name,
            a.attname as column_name
    from
            pg_class t,
            pg_class i,
            pg_index ix,
            pg_attribute a,
            pg_namespace n
    where
            t.oid = ix.indrelid
            and i.oid = ix.indexrelid
            and a.attrelid = t.oid
            and a.attnum = ANY(ix.indkey)
            and t.relkind = 'r'
            and t.relnamespace = n.oid
        group by  n.nspname ,
            t.relname ,
            a.attname 
) d  
ON (a.table_name = d.table_name AND a.table_schema = d.table_schema AND a.COLUMN_NAME = d.COLUMN_NAME)
WHERE a.table_schema  in ({tableSchema})
ORDER BY  a.table_schema
    , a.table_name
    , a.column_rank  
"""
# -------------------------------------------Hive盘点SQL--------------------------------------------------------------
# Hive表列表
invHiveTab = """
SELECT '{systemName}' system_name
        , c.name table_schema
        , a.tbl_name table_name
        , a.tbl_type table_type
        , IFNULL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(ifnull(d.PARAM_VALUE,''),CHAR(10),''),CHAR(13),''),CHAR(9),''),CHAR(39),''),CHAR(34),''),CHAR(92),''),'')   table_name_cn
        , null generate_type
        , null is_used 
        , null is_core_table
        , null time_col 
        , null operate_type
        , null is_phy_del
        , null etl_time_col
        , ifnull(e.PARAM_VALUE,null)   table_rows
        , null day_rows
        , null primary_key 
        , f.PARAM_VALUE  table_size_mb
        , null  index_size_mb
        , 'hive' db_type
        , CASE WHEN ifnull(d.PARAM_VALUE,'') IS NULL THEN '是' 
            ELSE '否'
          END is_comment
        , null view_sql
FROM TBLS a
LEFT JOIN DBS c
ON (a.db_id = c.db_id)
LEFT JOIN TABLE_PARAMS d 
on (a.tbl_id = d.tbl_id and d.PARAM_KEY = 'comment')
LEFT JOIN TABLE_PARAMS e 
on (a.tbl_id = e.tbl_id and e.PARAM_KEY = 'numRows')
LEFT JOIN TABLE_PARAMS f
on (a.tbl_id = f.tbl_id and f.PARAM_KEY = 'totalSize')
WHERE lower(c.name) in ({tableSchema})
ORDER BY c.name
"""
# Hive字段列表
invHiveColList = """
SELECT '{systemName}' system_name
    , d.name table_schema
    , a.tbl_name table_name 
    , e.PARAM_VALUE table_comment 
    , c.column_name column_name 
    , IFNULL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(c.COMMENT,CHAR(10),''),CHAR(13),''),CHAR(9),''),CHAR(39),''),CHAR(34),''),CHAR(92),''),'')   column_comment 
    , c.TYPE_NAME column_type
    , null is_pk
    , null is_idx
    , null is_null
    , IFNULL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(c.COMMENT,CHAR(10),''),CHAR(13),''),CHAR(9),''),CHAR(39),''),CHAR(34),''),CHAR(92),''),'')   column_desc 
    , c.INTEGER_IDX column_rank
FROM TBLS  a 
LEFT JOIN SDS   b
ON (a.SD_ID = b.SD_ID)
LEFT JOIN COLUMNS_V2 c 
ON (b.CD_ID = c.CD_ID)
LEFT JOIN DBS d
ON (a.db_id = d.db_id)
LEFT JOIN TABLE_PARAMS e 
ON (a.tbl_id = e.tbl_id AND e.PARAM_KEY = 'comment')
WHERE lower(d.name) in ({tableSchema})
ORDER BY d.name,a.tbl_name,c.INTEGER_IDX  
"""
# -------------------------------------------sqlserver盘点SQL--------------------------------------------------------------
# sqlserver表列表
invSqlserverTab = """
SELECT '{systemName}' system_name
    , g.name table_schema
    , a.NAME table_name
    , case when a.xtype ='U' then 'TABLE' else 'VIEW' END table_type
    , cast(b.VALUE AS varchar(100) ) table_name_cn
    , null generate_type
    , null is_used 
    , null is_core_table
    , f.data_col time_col 
    , null operate_type
    , null is_phy_del
    , null etl_time_col
    , d.rows   table_rows
    , null day_rows
    , PRIMARY_KEY primary_key 
    , rtrim(8*dpages/1024)  table_size_mb
    , null index_size_mb
    , 'sqlserver' db_type
    , CASE WHEN b.VALUE IS NOT NULL THEN '是' 
        ELSE '否'
      END is_comment
    , C.definition view_sql
FROM sys.sysobjects a
LEFT JOIN sys.extended_properties b 
ON ( a.id= b.major_id  and b.minor_id = 0)
LEFT JOIN SYS.sql_modules C 
ON (A.ID=C.OBJECT_ID)
LEFT JOIN sys.sysindexes d
ON (a.id = d.id and  d.indid <=1)
LEFT JOIN 
(
    SELECT idx.object_id
            , STUFF((
                    select ',' +col.name
                    from  sys.columns col 
                    join sys.index_columns idxCol 
                    ON 
                    (
                                    idx.object_id = idxCol.object_id 
                                    AND idx.index_id = idxCol.index_id 
                                    AND idx.object_id = col.object_id 
                                    AND idxCol.column_id = col.column_id  
                    )
                    FOR XML PATH('')), 1, 1, '') PRIMARY_KEY
    FROM sys.indexes idx
    WHERE  idx.is_primary_key = 1
) e
ON (a.id = e.object_id)
LEFT JOIN 
(
    SELECT table_name
        , STUFF((
                        SELECT ',' +b.column_name
                        FROM  INFORMATION_SCHEMA.COLUMNS  b  
                        WHERE (a.table_name = b.table_name )
                        AND data_type like '%date%'
                    FOR XML PATH('')), 1, 1, '') data_col
    FROM INFORMATION_SCHEMA.COLUMNS  a 
    WHERE data_type like '%date%'
    GROUP BY table_name
) f
ON (a.NAME = f.table_name)
LEFT JOIN sys.sysusers g
ON (a.uid = g.uid)
WHERE a.xtype IN ( 'U', 'V' )
AND lower(g.name) in ({tableSchema})
order by g.name asc
;
"""
# sqlserve字段列表
invSqlserverColList = """
SELECT  '{systemName}' system_name
    , h.name table_schema
    , d.name table_name 
    , CAST(e.VALUE AS varchar(200))  table_comment 
    , A.NAME column_name 
    , CAST(g.VALUE AS varchar(200))  column_comment 
    , b.name column_type
    , b.name data_type
    -- , a.length  字段长度 
    -- , ISNULL(COLUMNPROPERTY(a.id, a.name,'Scale'), 0) AS 小数位数 
    , CASE WHEN EXISTS
        (SELECT 1
          FROM sysobjects
         WHERE xtype = 'PK' AND name IN
         (SELECT name
            FROM sysindexes
           WHERE indid IN
           (SELECT indid
              FROM sysindexkeys
             WHERE id = a.id AND colid = a.colid)))
         THEN ' Y ' ELSE ''
        END  is_pk
    , CASE WHEN c.colid IS NULL
         THEN ''
        ELSE 'Y'
        END is_idx
    -- , CASE WHEN i.indid=1 THEN ' 聚集索引 '
    --        WHEN i.indid>1 AND i.indid<>255 THEN ' 非聚集索引 '
    --        WHEN i.indid IS NULL THEN ''
    --        ELSE ' 其他 '
    --   END AS 索引类型 
    , CASE WHEN isnullable = 1 THEN 'Y' ELSE '' END is_null
    -- , CASE WHEN COLUMNPROPERTY(a.id, a.name, 'IsIdentity')= 1 THEN ' Y ' ELSE ''
    --   END AS 递增字段 
    , CAST(g.VALUE AS varchar(200))    column_desc 
    , a.colorder  column_rank 
FROM sys.syscolumns a                     -- 数据表字段
LEFT JOIN sys.systypes b                  -- column_type
ON (a.xusertype= b.xusertype) 
LEFT  JOIN 
( 
	select id,colid from sysindexkeys 
	group by id,colid
) c               -- 索引中的键或列的信息
ON (c.id = a.id AND c.colid = a.colid)
-- LEFT  JOIN sysindexes  i                -- 数据库 索引表
-- ON (c.id =i.id  AND c.indid = i.indid)
JOIN sys.sysobjects d                     -- 数据对象
ON (a.id=d.id  AND d.xtype IN ( 'U', 'V' ))
LEFT JOIN sys.extended_properties e       -- 表属性信息
ON (a.id = e.major_id and e.minor_id = 0)
LEFT JOIN sys.extended_properties g       -- 字段属性信息
ON (a.id=g.major_id AND a.colid=g.minor_id)
LEFT JOIN sys.sysusers h
ON (d.uid = h.uid)
WHERE lower(h.name)  in ({tableSchema})
ORDER by h.name
    , d.name
    , a.colorder
"""
# -------------------------------------------Mysql自动盘点SQL--------------------------------------------------------------
# mysql表列表
invMysqlTab = """
    SELECT '{systemName}'  system_name
        , a.table_schema   table_schema
        , a.table_name     table_name
        , a.table_type     table_type
        , IFNULL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(a.TABLE_COMMENT,CHAR(10),''),CHAR(13),''),CHAR(9),''),CHAR(39),''),CHAR(34),''),CHAR(92),''),'')   table_name_cn
        , null generate_type
        , null is_used 
        , null is_core_table
        , d.time_col time_col 
        , null operate_type
        , null is_phy_del
        , null etl_time_col
        , a.TABLE_ROWS   table_rows
        , null day_rows
        , b.PRIMARY_KEY primary_key 
        , ROUND(a.data_length/1024/1024,2) table_size_mb
        , ROUND(a.index_length /1024/1024,2) index_size_mb
        , 'mysql' db_type
        , CASE WHEN a.TABLE_COMMENT IS NULL THEN '是' 
            ELSE '否'
          END is_comment
        , c.VIEW_DEFINITION view_sql
    FROM information_schema.TABLES a
    LEFT JOIN 
    (
        SELECT table_name
                ,table_schema
                ,GROUP_CONCAT(COLUMN_NAME)  PRIMARY_KEY
        FROM information_schema.KEY_COLUMN_USAGE
      WHERE CONSTRAINT_NAME = 'PRIMARY'
        GROUP BY table_name,table_schema
    )  b 
    ON (a.table_name = b.table_name AND a.table_schema = b.table_schema)
    LEFT JOIN  information_schema.VIEWS c 
    ON (a.table_schema = c.table_schema AND a.table_name = c.table_name)
    LEFT JOIN 
    (
        SELECT table_schema
            , table_name
            , GROUP_CONCAT(COLUMN_NAME) time_col
        FROM  information_schema.`COLUMNS`
        WHERE data_type in ('datetime','timestamp','time','date','year')
        GROUP BY  table_schema
            , table_name 
    ) d
    ON (a.table_schema = d.table_schema AND a.table_name = d.table_name)
    WHERE lower(a.table_schema) in ({tableSchema})
    ORDER BY a.table_schema
"""
# mysql字段列表
invMysqlColList = """
SELECT '{systemName}' system_name
    , a.TABLE_SCHEMA table_schema
    , a.TABLE_NAME table_name 
    , b.TABLE_COMMENT table_comment 
    , a.COLUMN_NAME column_name 
    , IFNULL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(a.COLUMN_COMMENT,CHAR(10),''),CHAR(13),''),CHAR(9),''),CHAR(39),''),CHAR(34),''),CHAR(92),''),'')   column_comment 
    , a.COLUMN_TYPE column_type
    , a.DATA_TYPE   data_type
    , CASE WHEN c.COLUMN_NAME IS NOT NULL THEN '是'
            ELSE '否'
        END is_pk
    , CASE WHEN d.COLUMN_NAME IS NOT NULL THEN '是'
            ELSE '否'
        END is_idx
    , CASE WHEN a.is_nullable ='NO' THEN '否'
        WHEN a.is_nullable ='YES' THEN '是'
        ELSE '未知'
      END is_null
    , IFNULL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(a.COLUMN_COMMENT,CHAR(10),''),CHAR(13),''),CHAR(9),''),CHAR(39),''),CHAR(34),''),CHAR(92),''),'')   column_desc 
    , a.ORDINAL_POSITION column_rank
FROM information_schema.`COLUMNS` a 
LEFT JOIN information_schema.TABLES b 
ON (a.table_name = b.table_name AND a.table_schema = b.table_schema)
LEFT JOIN information_schema.KEY_COLUMN_USAGE c 
ON (a.table_name = c.table_name AND a.table_schema = c.table_schema AND a.COLUMN_NAME=c.COLUMN_NAME AND c.CONSTRAINT_NAME='PRIMARY')
LEFT JOIN  
(
    SELECT table_schema
            ,table_name
            ,column_name 
    FROM information_schema.STATISTICS 
    GROUP BY table_schema,table_name ,column_name
) d  
ON (a.table_name = d.table_name AND a.table_schema = d.table_schema AND a.COLUMN_NAME = d.COLUMN_NAME)

WHERE lower(a.table_schema) in ({tableSchema})
ORDER BY a.TABLE_SCHEMA
    , a.TABLE_NAME
    , a.ORDINAL_POSITION
"""
# -------------------------------------------oracle盘点SQL--------------------------------------------------------------
# Oracle表列表
invOracleTab = """
    SELECT '{systemName}' system_name
        , a.owner table_schema
        , a.table_name table_name
        , a.table_type table_type
        , NVL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(a.comments,CHR(10),''),CHR(13),''),CHR(9),''),CHR(39),''),CHR(34),''),CHR(92),''),'')    table_name_cn
        , null generate_type
        , null is_used 
        , null is_core_table
        , g.time_col time_col 
        , null operate_type
        , null is_phy_del
        , null etl_time_col 
        , e.num_rows  table_rows
        , null day_rows
        , d.pk_key primary_key 
        , round(f.segment_size,2) table_size_mb
        , round(d.index_size,2)   index_size_mb
        , 'oracle' db_type
        , CASE WHEN a.comments IS NULL THEN '是' 
            ELSE '否'
          END is_comment
        -- , e.iot_type 索引组织
        , b.text view_sql
    FROM all_tab_comments a 
    LEFT JOIN all_views b 
    ON (a.table_name = b.view_name and a.owner = b.owner)
    LEFT JOIN all_constraints c 
    ON (a.table_name = c.table_name and a.owner = c.owner and c.constraint_type='P')
    LEFT JOIN 
    (
    --  表primary_key及索引大小
        SELECT t1.table_owner
            , t1.table_name
            , t1.index_name
            , t1.pk_key
            , SUM(t2.segment_size) OVER(PARTITION BY  table_name) / 1024 / 1024 index_size
        FROM 
            (
                SELECT a.table_owner
                    , a.table_name
                    , a.index_name
                    , listagg(column_name,',') within group(order by column_name desc) pk_key
                FROM all_ind_columns  a 
                GROUP BY a.table_owner
                    ,a.table_name
                    ,a.index_name
            ) t1 
            LEFT JOIN 
            (
                SELECT owner
                    , segment_name
                    , sum( bytes )   segment_size
                FROM dba_segments 
                GROUP BY owner
                    , segment_name
            ) t2 
            ON (t1.table_owner = t2.owner AND t1.index_name = t2.segment_name)
    ) d 
    ON (c.table_name = d.table_name AND c.owner = d.table_owner AND c.index_name = d.index_name)
    LEFT JOIN  all_tables  e 
    ON (a.owner = e.owner AND a.table_name = e.table_name)
    LEFT JOIN  
    (
    --  表大小
        SELECT owner
            , segment_name
            , sum( bytes ) / 1024 / 1024  segment_size
        FROM
            dba_segments 
        GROUP BY
            owner,
            segment_name
    ) f 
    ON (d.table_owner = f.owner AND a.table_name = f.segment_name) 
    LEFT JOIN  
    (
    --  日期格式字段
        SELECT owner
            , table_name
            , listagg(column_name,',') within group(order by column_name desc) time_col
        FROM  all_tab_columns
        WHERE data_type in ('DATE','TIMESTAMP')
        GROUP BY OWNER
            , TABLE_NAME
    ) g  
    ON (a.owner = g.owner AND a.TABLE_NAME = g.TABLE_NAME)  
    WHERE lower(a.owner)  IN  ({tableSchema})
    -- and a.table_name  in('GV_$HS_AGENT')
    ORDER BY a.owner
"""
# Oracle字段列表
invOracleColList = """
SELECT  '{systemName}' system_name
    , a.owner  table_schema
    , a.table_name table_name
    , c.comments  table_comment
    , a.column_name   column_name
    , NVL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(b.comments,CHR(10),''),CHR(13),''),CHR(9),''),CHR(39),''),CHR(34),''),CHR(92),''),'')     column_comment
    , (case
              when data_type='CHAR' then data_type||'('||data_length||')'
              when data_type='VARCHAR' then data_type||'('||data_length||')'
              when data_type='VARCHAR2' then data_type||'('||data_length||')'
              when data_type='NCHAR' then data_type||'('||data_length||')'
              when data_type='NVARCHAR' then data_type||'('||data_length||')'
              when data_type='NVARCHAR2' then data_type||'('||data_length||')'
              when data_type='RAW' then data_type||'('||data_length||')'
              when data_type='NUMBER' then
                 (
                    case
                       when data_scale is null and data_precision is null then 'NUMBER'
                       when data_scale <> 0  then 'NUMBER('||NVL(DATA_PRECISION,38)||','||DATA_SCALE||')'
                       else 'NUMBER('||NVL(DATA_PRECISION,38)||')'
                    end
                 )
              else
                (
                    case
                        when data_type_owner is not null then data_type_owner||'.'||data_type
                        else data_type
                    end
                 )
        end
        )  column_type
    , a.data_type   data_type
    , constraint_type is_pk
    , CASE WHEN e.column_name IS NOT NULL THEN '是'
        ELSE '否'
      END is_idx
    , NVL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(b.comments,CHR(10),''),CHR(13),''),CHR(9),''),CHR(39),''),CHR(34),''),CHR(92),''),'')  column_desc
    , a.NULLABLE is_null
    , a.column_id column_rank
FROM all_tab_columns a   --字段元数据
LEFT JOIN all_col_comments b   --字段注释元数据
ON (a.table_name =  b.table_name and a.column_name = b.column_name and a.owner = b.owner)
LEFT JOIN  all_tab_comments c   --表注释
ON (a.table_name =  c.table_name and a.owner = c.owner)
LEFT join
(
    select a.owner 
        ,a.table_name
        ,column_name
        ,constraint_type
    from  all_cons_columns  a
    join  all_constraints  b
    on (a.table_name=b.table_name and a.owner=b.owner and a.constraint_name=b.constraint_name)
    where b.constraint_type = 'P'
) d
ON (a.table_name =  d.table_name and a.owner = d.owner and a.column_name = d.column_name)
LEFT JOIN 
(
    SELECT table_owner
        , table_name
        , column_name
    FROM all_ind_columns
    GROUP BY table_owner
        , table_name
        , column_name
) e
ON (a.table_name =  e.table_name and a.owner = e.table_owner and a.column_name = e.column_name)
WHERE lower(a.owner)  IN  ({tableSchema})
ORDER bY  a.owner
    , a.table_name
    , a.column_id
"""
# ----------------------------------------------------质量盘点sql-----------------------------------------------------
# 创建数据质量metadata表名
dqCreateMetaTab = """
CREATE TABLE IF NOT EXISTS {tableName}
(
  `system_name` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '系统名称',
  `table_schema` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '数据库schema',
  `table_name` varchar(200) COLLATE utf8_bin NOT NULL COMMENT '表名',
  `column_name` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '字段名',
  `data_type` varchar(20) COLLATE utf8_bin NOT NULL COMMENT '字段类型',
  `db_type` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '数据库类型',
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建日期',
  `modify_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改日期',
  `is_valid` int(11) DEFAULT '1' COMMENT ' COMMENT ''0：失效 1：生效'',',
  `drop_date` datetime DEFAULT NULL COMMENT '删除日期',
  PRIMARY KEY (`table_schema`,`table_name`,`column_name`,`system_name`,`db_type`,`data_type`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""
# 创建数据质量metadata表名
dqCreateDataTab = """
CREATE TABLE IF NOT EXISTS  `{tableName}` (
  `system_name` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '系统名称',
  `table_schema` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '数据库schema',
  `table_name` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '表名',
  `column_name` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '字段名',
  `data_type` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '数据类型',
  `db_type` varchar(100) COLLATE utf8_bin NOT NULL COMMENT '数据库类型',
  `data_rows` bigint(20) DEFAULT NULL COMMENT '数据条数',
  `data_null_rows` bigint(20) DEFAULT NULL COMMENT '空值条数',
  `data_dist_rows` bigint(20) DEFAULT NULL COMMENT '去重条数',
  `data_dist_topn_json` text COLLATE utf8_bin COMMENT '去重json',
  `data_len_topn_json` text COLLATE utf8_bin COMMENT '长度json',
  `max_value` text COLLATE utf8_bin COMMENT '最大值',
  `min_value` text COLLATE utf8_bin COMMENT '最小值',
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建日期',
  `modify_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改日期',
  `drop_date` datetime DEFAULT NULL COMMENT '删除日期',
  PRIMARY KEY (`system_name`,`table_schema`,`table_name`,`column_name`,`db_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""
# 通过系统名和schema 删除表信息
invDelDpMeta = """
DELETE FROM {tableName} 
WHERE system_name ='{systemName}' 
AND lower(table_schema) in ({tableSchema})
"""
# 通过系统名和schema 删除表盘点数据
invDelDpData = """
DELETE FROM {tableName} 
WHERE system_name ='{systemName}' 
AND lower(table_schema) in ({tableSchema})
"""
# 初始化需要探查的字段列表
invDpColMetaInit = """
INSERT INTO  {table} (
    system_name    
    , table_schema   
    , table_name     
    , column_name    
    , data_type    
    , db_type
)
SELECT  a.system_name    
    , a.table_schema   
    , a.table_name     
    , a.column_name     
    , a.data_type      
    , a.db_type
FROM  {tmpTable} a 
LEFT JOIN
{table} b 
ON
( 
    a.table_name = b.table_name 
    and a.table_schema = b.table_schema
    and a.column_name = b.column_name 
    and a.system_name = b.system_name
    and a.db_type     = b.db_type
)
WHERE b.table_name is null 
"""
# 更新数据需要探查的字段列表
updateDpCol = """
UPDATE  {table} a 
LEFT JOIN
{tmpTable} b 
on
( 
    a.table_name = b.table_name 
    and a.table_schema = b.table_schema
    and a.column_name = b.column_name 
    and a.system_name = b.system_name
    and a.db_type     = b.db_type
)
SET a.is_valid = (
                   CASE WHEN b.table_name is null THEN 0 
                        WHEN b.table_name is not null THEN b.is_valid
                     ELSE a.is_valid
                   END
                 )
   , a.drop_date = (
                   CASE WHEN b.table_name is null THEN CURRENT_TIMESTAMP()
                     ELSE a.drop_date
                   END
                 ) 
WHERE  lower(a.table_schema) in ({tableSchema})
"""
# 获取要处理的字段列表
dqDataColList = """
SELECT a.table_schema
    , a.table_name 
    , a.column_name 
    , a.data_type
FROM {dpMetaTable} a 
LEFT JOIN {dpDataTable} b 
ON 
(   a.table_schema = b.table_schema 
    AND a.table_name = b.table_name 
    AND a.column_name = b.column_name
    AND a.db_type  = b.db_type
    AND a.system_name = b.system_name
)
WHERE b.column_name IS NULL
"""
# 获取Oracle需要盘点的字段列表
dqOracleColList = """
SELECT '{systemName}' system_name
    ,a.OWNER table_schema
    ,a.TABLE_NAME
    ,a.COLUMN_NAME
    ,a.DATA_TYPE
    ,'oracle' db_type
FROM all_tab_columns a  
WHERE a.data_type NOT IN ('LONG')
AND a.data_type NOT LIKE '%)%'
AND a.data_type NOT LIKE '%$%'
AND a.data_type NOT LIKE '%RAW%'
AND a.data_type NOT LIKE '%LOB%'
AND a.data_type not 
IN ('SCHEDULER_FILEWATCHER_RESULT'                
    , 'XMLTYPE'                                     
    , 'HSBLKNAMLST'                                                                 
    , 'ALERT_TYPE'                                   
    , 'HSBLKVALARY'                                  
    , 'UROWID'                                       
    , 'BINARY_DOUBLE'                                
    , 'SDO_NUMBER_ARRAY'                             
    , 'UNDEFINED'                                    
    , 'SDO_DIM_ARRAY'                                
    , 'DBMS_DBFS_CONTENT_PROPERTIES_T'               
    , 'ANYDATA'                                     
    , 'MLSLABEL'                                     
    , 'ROWID'                                        
    , 'SDO_GEOMETRY'                                 
    , 'SDO_TOPO_GEOMETRY_LAYER_ARRAY'       
    , 'INTERVAL DAY(3) TO SECOND(0)'   
    , 'CLOB'
    , 'ORDDOC'
    , 'MGMT'  
)
AND a.data_type not like 'KU%'
AND a.data_type not like '%LOB%'
AND a.data_type not like 'LONG%'
AND a.data_type not like 'AQ%'
AND a.data_type not like 'AQ%'
AND lower(a.owner) in ({tableSchema})
"""
# 获取Oracle 每个字段的结果数据
dqOracleColData = """
SELECT key_value  
    , col_cnt
    , col_null_cnt
    , col_dist_cnt
    , len_rank
    , cnt_rank
    , key_cnt
    , key_len
    , min_value
    , max_value
FROM 
(
    SELECT substr(colum_name,1,100) key_value
        , ROW_NUMBER() OVER(ORDER BY cnt DESC ) cnt_rank
        , ROW_NUMBER() OVER(ORDER BY LENGTH(colum_name) DESC ) len_rank
        , LENGTH(colum_name)  key_len
        , cnt  key_cnt
        , SUM(cnt) over() col_cnt 
        , COUNT(*) over() col_dist_cnt
        , SUM(case when length(colum_name) = 0 THEN cnt else 0 END) over() col_null_cnt
        , max(colum_name) over()  max_value
        , min(colum_name) over()  min_value
    FROM 
    (
        SELECT {columnName}  colum_name
            , count(*) cnt
        FROM {owner}."{tableName}"
        GROUP BY {columnName}
    ) t
) tt
WHERE cnt_rank <= {topN} or len_rank <= {topN}
"""

# dqMysqlColData = """
# SELECT key_value
#     , col_cnt
#     , col_null_cnt
#     , col_dist_cnt
#     , len_rank
#     , cnt_rank
#     , key_cnt
#     , key_len
#     , min_value
#     , max_value
# FROM
# (
#     SELECT colum_name key_value
#         , ROW_NUMBER() OVER(ORDER BY cnt DESC ) cnt_rank
#         , ROW_NUMBER() OVER(ORDER BY LENGTH(colum_name) DESC ) len_rank
#         , LENGTH(colum_name)  key_len
#         , cnt  key_cnt
#         , SUM(cnt) over() col_cnt
#         , COUNT(*) over() col_dist_cnt
#         , SUM(case when length(colum_name) = 0 THEN cnt else 0 END) over() col_null_cnt
#         , max(colum_name) over()  max_value
#         , min(colum_name) over()  min_value
#     FROM
#     (
#         SELECT {columnName}  colum_name
#             ,  LENGTH(colum_name)  colum_name_len
#             , count(*) cnt
#         FROM `{owner}`.`{tableName}`
#         GROUP BY {columnName}
#             ,  LENGTH(colum_name)
#     ) a

# ) tt
# WHERE cnt_rank <= {topN} or len_rank <= {topN}
# """


# ----------------------------------------------------生成ods hive语句 ------------------------------------------------
createHiveDdlSql = """
--********************************************************************--
--BelongToTheme: {src_system_name} 
--TableDescription: {table_comments}
--Creator:
--CreateDate:{current_date}
--ModifyDate  Modifier  ModifyContent
--yyyymmdd  name  comment
--********************************************************************--
--DROP TABLE IF  EXISTS {table_name};
CREATE TABLE IF NOT EXISTS {table_name} ( 
      {column_info} 
) COMMENT '{table_comments}' 
PARTITIONED BY ({partition_str}) 
STORED AS ORC;
"""

# ----------------------------------------------------通过excel 生成 job任务sql-----------------------------------------
modelJobSql = """
--********************************************************************--
--所属主题:{src_system_name} 
--功能描述: 
--创建者:
--创建日期:{current_date}
--修改日期  修改人  修改内容
--yyyymmdd  name  comment
--********************************************************************--
--DROP TABLE IF  EXISTS dwd_trd_ol_order_df;
INSERT OVERWRITE TABLE {tableName} PARTITION ({partitionListStr})
SELECT {columnListStr} 
FROM {tableJoinListStr}
"""

# ----------------------------------------------------增全量合并sql-----------------------------------------------------
# 增全量合并sql
mergeSql = """
--********************************************************************--
--所属主题:  
--功能描述:{tableComments}
--创建者:
--创建日期:2021-10-24
--修改日期 修改人 修改内容
--yyyymmdd name comment
--********************************************************************--
INSERT OVERWRITE TABLE {tableNameMerge} PARTITION ( ds = '${{bdp.system.bizdate}}')
SELECT {insertCol} 
FROM 
(
   SELECT {insertCol} 
    ,row_number()over(partition by {pkColumnStr} order by record_type desc) rn
   FROM 
   (
    SELECT {insertCol} 
        , 1 AS record_type 
    FROM {tableNameMerge} 
    WHERE ds = '${{last_day}}'
    UNION ALL 
    SELECT {insertCol}    
        , 2 AS record_type 
    FROM {tableNameDi} 
    WHERE ds='${{bdp.system.bizdate}}'
   ) a
) b
WHERE rn = 1
"""

# hive 表注释
gethiveTableCommentSql = """
SELECT tbl_name
    ,ifnull(PARAM_VALUE,'')     as comments
    ,ifnull(c.pkey_type,'')     as pkey_type
    ,ifnull(c.pkey_name,'')     as pkey_name
    ,ifnull(c.pkey_comment,'')  as pkey_comment
FROM TBLS a 
LEFT JOIN TABLE_PARAMS b 
ON (a.TBL_ID=b.TBL_ID AND b.PARAM_KEY = 'comment')
LEFT JOIN PARTITION_KEYS c 
ON (a.TBL_ID=c.TBL_ID)
LEFT JOIN DBS d
ON (a.db_id = d.db_id)
WHERE a.TBL_NAME = '{tableName}'
AND d.name ='{dbName}'
"""

##hive 字段列表
mergeHiveSqlColList = """
SELECT tbl_name
    , COLUMN_NAME column_name
    , TYPE_NAME type_name
    , INTEGER_IDX integer_idx
    , create_str
    , COLUMN_NAME_COMMENT column_name_comment
    , concat(RPAD(column_name_long,GREATEST(length(column_name_long)+1,100),'  '),'--',COMMENT) insert_str
FROM 
(
    SELECT a.tbl_name
       , COLUMN_NAME
       , IFNULL(COMMENT,'') COMMENT
       , upper(TYPE_NAME) TYPE_NAME
       , INTEGER_IDX
       , CONCAT( COLUMN_NAME ,'     --',IFNULL(COMMENT,'')) COLUMN_NAME_COMMENT
       , concat(RPAD(lower(column_name),GREATEST(length(column_name)+1,40),' '),upper(TYPE_NAME),' COMMENT ''',ifnull(COMMENT,''),'''') create_str
       , concat(RPAD(lower(column_name),GREATEST(length(column_name)+1,40),' '),'as   ',column_name) column_name_long  
    FROM TBLS  a 
    LEFT JOIN SDS   b
    ON (a.SD_ID = b.SD_ID)
    LEFT JOIN COLUMNS_V2 c 
    ON (b.CD_ID = c.CD_ID)
    LEFT JOIN DBS d
    ON (a.db_id = d.db_id)
    WHERE a.TBL_NAME = '{tableName}'
    AND d.name ='{dbName}'
    -- AND COLUMN_NAME  NOT LIKE '%\_qty\_%'
    ORDER BY integer_idx asc
)  AA 

"""
# ----------------------------------------------------拉链表sql-----------------------------------------------------
# 创建拉链表sql
createZipperTableSql = """
--********************************************************************--
--所属主题:  
--功能描述: {table_comments} 拉链表
--创建者:
--创建日期:{current_date}
--修改日期  修改人  修改内容
--yyyymmdd  name  comment
--********************************************************************--
DROP TABLE IF EXISTS {target_table};
CREATE TABLE IF NOT EXISTS {target_table} 
(
    {column_info}   
    ,start_date                    string COMMENT '记录生效时间'
    ,end_date                      string COMMENT '记录失效时间'
    ,etl_time                      string COMMENT '记录创建时间'
) COMMENT '{table_comments}' 
PARTITIONED BY
(end_mon STRING COMMENT '结束月份',start_mon STRING COMMENT '开始月份') 
STORED AS ORC;
"""
# 拉链表加工sql
zipperJobSql = """
--********************************************************************--
--所属主题:  
--功能描述:{tableComments}拉链表
--创建者:
--创建日期:{current_date}
--修改日期 修改人 修改内容
--yyyymmdd name comment
-- 步骤1：20211213 新增记录 id =1,10  
-- id  value   start_day   end_day 
-- 1     10    20211213   99991231
-- 步骤2：20211214 记录不变    
-- id  value   start_day   end_day 
-- 1     10    20211213   99991231
-- 步骤3：20211215 记录发生变更 11
--  id  value   start_day   end_day 
-- 1     10    20211213   20211214
-- 1     11    20211215   99991231
-- 步骤4：这个时候要重新跑14号的记录，写where start_day <= 20211214 的时候过滤出来的数据是这样的：
-- id  value   start_day   end_day 
-- 1     10    20211213   20211214
-- 并且14日新增表里面也没有这条记录的变更，插入数据库里面的记录就变成了：
-- id  value   start_day   end_day 
-- 1     10    20211213   20211214
-- 按道理应该和步骤2保持一致：
--  id  value   start_day   end_day 
--  1     10    20211213   99991231
-- 如果加上 when end_date >= '${{bdp.system.bizdate}}' then '99991231' 的话，这条记录就会变成：
--  id  value   start_day   end_day 
--  1     10    20211213   99991231
--  和步骤2保持一致
--********************************************************************--
set hive.exec.dynamic.partition.mode=nonstrict;
INSERT OVERWRITE TABLE {tableNameZipper} PARTITION (end_mon,start_mon)
SELECT {insertCol} 
    , a.start_date
    , case when b.{judgeNullStr} is not null and a.end_date >= '${{bdp.system.bizdate}}' then '${{yyyyMMdd,-2d}}'
           when end_date >= '${{bdp.system.bizdate}}' then '99991231'
           else end_date
      end end_date
    , current_timestamp()
    , substr(case when b.{judgeNullStr} is not null and a.end_date >= '${{bdp.system.bizdate}}' then '${{yyyyMMdd,-2d}}'
                when end_date >= '${{bdp.system.bizdate}}' then '99991231'
                else end_date 
           end,1,6) end_mon
    , substr(start_date,1,6) start_mon
FROM {tableNameZipper}  a 
LEFT JOIN 
(
    SELECT {pkColumnStr}
    FROM {tableNameDi}
    WHERE ds = '${{bdp.system.bizdate}}'
)  b 
ON ({onString})
WHERE start_date < '${{bdp.system.bizdate}}'
AND start_date <= end_date
UNION ALL
SELECT {insertCol} 
    , '${{bdp.system.bizdate}}' start_date
    , '99991231' end_date   
    , current_timestamp()
    , '999912'  end_mon
    , substr('${{bdp.system.bizdate}}',1,6) start_mon     
FROM  {tableNameDi} a
WHERE ds = '${{bdp.system.bizdate}}'
"""
# 拉链表初始化sql
zipperInitSql = """
--********************************************************************--
--所属主题:  
--功能描述:{tableComments}拉链表
--创建者:
--创建日期:{current_date}
--修改日期 修改人 修改内容
--yyyymmdd name comment
--********************************************************************--
set hive.exec.dynamic.partition.mode=nonstrict;
INSERT OVERWRITE TABLE {tableNameZipper} PARTITION (end_mon,start_mon)
SELECT {insertCol} 
    , '${{bdp.system.bizdate}}' start_date
    , '99991231' end_date
    , current_timestamp()
    , '999912' end_mon
    , substr('${{bdp.system.bizdate}}' ,1,6) start_mon
FROM {tableNameDf}  a 
WHERE ds = '${{bdp.system.bizdate}}'
"""

# ------------------------------------------------------自动从源库生成hive ddl sql---------------------------------
mysqlColList = """
SELECT TRAGET_COLUMN_NAME traget_column_name
    , SRC_COLUMN_NAME src_column_name
    , COLUMN_COMMENT column_comment
    , DATA_TYPE data_type
    , HIVE_DATA_TYPE hive_data_type
    , COLUMN_ID column_id
    , CONCAT(RPAD(LOWER(TRAGET_COLUMN_NAME),GREATEST(LENGTH(TRAGET_COLUMN_NAME)+1,50),' '),' ',HIVE_DATA_TYPE,' COMMENT ','''',column_comment,'''') create_str
FROM 
(
    SELECT  column_name AS TRAGET_COLUMN_NAME
        , column_name   AS SRC_COLUMN_NAME
        , REPLACE(REPLACE(IFNULL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(column_comment,CHAR(10),''),CHAR(13),''),CHAR(9),''),CHAR(39),''),CHAR(34),''),CHAR(92),''),''),';',''),'--','') as column_comment
        , data_type     AS DATA_TYPE
        , CASE WHEN data_type LIKE 'int%' OR data_type  LIKE '%int'  OR data_type IN ('integer')  THEN 'BIGINT'
            WHEN data_type IN  ('decimal','double','float') THEN 'DOUBLE'
            WHEN data_type IN  ('bit','bool') THEN 'STRING'
            WHEN DATA_TYPE IN  ('timestamp','datetime') THEN 'STRING'
            ELSE 'STRING'
          END          AS HIVE_DATA_TYPE
        , ordinal_position  AS COLUMN_ID
    FROM information_schema.columns
    WHERE table_schema = lower('{tableSchema}')
    AND table_name = lower('{tableName}')
) T1
ORDER BY COLUMN_ID ASC 
"""

###oracle字段列表
oracleColList = """
SELECT TRAGET_COLUMN_NAME traget_column_name
    , SRC_COLUMN_NAME src_column_name
    , COLUMN_COMMENT column_comment
    , DATA_TYPE data_type
    , HIVE_DATA_TYPE hive_data_type
    , COLUMN_ID column_id
    , RPAD(LOWER(TRAGET_COLUMN_NAME),GREATEST(LENGTH(TRAGET_COLUMN_NAME)+1 ,30),'   ')||' '|| upper(HIVE_DATA_TYPE)||' COMMENT '''||column_comment||''''  create_str
FROM 
(
    SELECT a.column_name TRAGET_COLUMN_NAME
        , a.column_name SRC_COLUMN_NAME
        , DATA_TYPE
        , CASE WHEN data_type='NUMBER' AND (DATA_SCALE <> 0  AND DATA_SCALE IS NOT NULL ) THEN 'DOUBLE'
                 WHEN data_type='NUMBER' THEN 'BIGINT'
                ELSE 'STRING'
          END HIVE_DATA_TYPE
        , REPLACE(REPLACE(NVL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(b.comments,CHR(10),''),CHR(13),''),CHR(9),''),CHR(39),''),CHR(34),''),CHR(92),''),''),';',''),'--','') as  COLUMN_COMMENT
        , COLUMN_ID
    FROM all_tab_columns a
    LEFT JOIN all_col_comments b 
    ON ( a.owner = b.owner  AND a.table_name = b.table_name AND a.column_name = b.column_name) 
    WHERE a.table_name = upper('{tableName}')
    AND a.owner = upper('{tableSchema}')
) 
ORDER BY COLUMN_ID ASC
"""

###sqlserver 的字段列表
sqlserverColList = """
SELECT TRAGET_COLUMN_NAME traget_column_name
    , SRC_COLUMN_NAME src_column_name
    , COLUMN_COMMENT column_comment
    , DATA_TYPE data_type
    , HIVE_DATA_TYPE hive_data_type
    , COLUMN_ID column_id
    , CONCAT(LOWER(TRAGET_COLUMN_NAME),' ',HIVE_DATA_TYPE,' COMMENT ','''',column_comment,'''') create_str
FROM 
(
    SELECT  a.NAME AS TRAGET_COLUMN_NAME
        , a.NAME   AS SRC_COLUMN_NAME
        , REPLACE(REPLACE(ISNULL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(CAST(g.VALUE AS varchar(200)),CHAR(10),''),CHAR(13),''),CHAR(9),''),CHAR(39),''),CHAR(34),''),CHAR(92),''),''),';',''),'--','') as COLUMN_COMMENT
        , b.name     AS DATA_TYPE
        , CASE WHEN b.name  like 'int%' or b.name  like '%int'  THEN 'BIGINT'
                WHEN b.name  IN  ('decimal','double','float') THEN 'DOUBLE'
                ELSE 'STRING'
            END        AS HIVE_DATA_TYPE
        , a.colorder AS COLUMN_ID
    FROM sys.syscolumns a                     -- 数据表字段
    LEFT JOIN sys.systypes b                  -- 数据类型
    ON (a.xusertype= b.xusertype) 
    JOIN sys.sysobjects d                     -- 数据对象
    ON (a.id=d.id  AND d.xtype IN ( 'U', 'V' ))
    LEFT JOIN sys.extended_properties g       -- 字段属性信息
    ON (a.id=g.major_id AND a.colid=g.minor_id)
    LEFT JOIN sys.sysusers h
    ON (d.uid = h.uid)
    WHERE d.name ='{tableName}'
    AND h.name = '{tableSchema}'
) t1 
ORDER BY COLUMN_ID asc 
"""

# mysql表注释
mysqlTableComment = """
    select IFNULL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(TABLE_COMMENT,CHAR(10),''),CHAR(13),''),CHAR(9),''),CHAR(39),''),CHAR(34),''),CHAR(92),''),'')  as comments
    from information_schema.tables
    where upper(table_name) = upper('{tableName}')
    and  upper(table_schema) = upper('{tableSchema}')
"""

#  oracle表注释
oracleTableComment = """
    SELECT NVL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(comments,CHR(10),''),CHR(13),''),CHR(9),''),CHR(39),''),CHR(34),''),CHR(92),''),'') AS comments
    FROM ALL_TAB_COMMENTS
    WHERE table_name = UPPER('{tableName}')
    AND  owner = UPPER('{tableSchema}')
"""

# sqlserver 表注释
sqlserverTableComment = """
    SELECT ISNULL(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(cast(b.VALUE AS varchar(100) ),CHAR(10),''),CHAR(13),''),CHAR(9),''),CHAR(39),''),CHAR(34),''),CHAR(92),''),'') comments
    FROM sys.sysobjects a
    LEFT JOIN sys.extended_properties b 
    ON (a.id= b.major_id  and b.minor_id = 0)
    LEFT JOIN sys.sysusers g
    ON (a.uid = g.uid)
    WHERE a.xtype IN ( 'U', 'V' )
    AND upper(a.name) = upper('{tableName}')
    AND upper(g.name) = upper('{tableSchema}')
"""
