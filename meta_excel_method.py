import traceback, pymysql
import pandas as pd


class writeExcel(object):

    def __init__(self, filePath):
        self.__writer = pd.ExcelWriter(filePath, engine='xlsxwriter')

    def write_url(self, src_sheet_name, target_sheet_name, line, col, col_text, targetCol, targetLine):
        worksheet = self.__writer.sheets[src_sheet_name]
        worksheet.write_url(
            '{col}{row}'.format(col=col, row=line)
            , 'internal:{sheet_name}!{targetCol}{targetLine}'.format(sheet_name=target_sheet_name, targetCol=targetCol,
                                                                     targetLine=targetLine)
            , string=col_text
        )

        # worksheet = self.__writer.sheets[target_sheet_name]
        # worksheet.write_url('A1','internal:{src_sheet_name}!A{row}'.format(src_sheet_name=src_sheet_name,row = line),string='返回')

    def excel_col_sign(self, col_int):
        # 数字转换为excel对应列
        list1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        col_str = ''
        if (col_int <= 26):
            col_str = list1[col_int - 1]
        elif (col_int < 702):
            col_int = col_int - 27
            col_str = list1[int(col_int / 26)] + list1[int(col_int % 26)]
        elif (col_int == 702):
            col_str = 'ZZ'
        else:
            col_int = col_int - 703
            col_str = list1[int(col_int / 676)] + list1[int(col_int / 26) % 26] + list1[col_int % 26]
        return (col_str)

    def save_excel(self):
        self.__writer.save()

    def write_excel(self, df, sheet_name, header_row_position):
        writer = self.__writer
        workbook = writer.book
        # 通用格式
        fmt = workbook.add_format({"font_name": u"微软雅黑", 'align': 'center', 'font_size': 9, 'valign': 'vcenter'})
        # 边框
        border_format = workbook.add_format({'border': 1})
        # 列头格式
        head_fmt = workbook.add_format(
            {
                'bold': False, 'font_size': 11, 'font_name': '微软雅黑', 'num_format': 'yyyy-mm-dd',
                'bg_color': '#9bc2e6', 'valign': 'vcenter', 'align': 'center', 'border': 1
            }
        )

        # 写入excel
        excel_rows = len(df.index) + header_row_position + 1
        df.to_excel(writer, sheet_name=sheet_name, encoding='utf8', header=True, index=False, startcol=0,
                    startrow=header_row_position)
        worksheet = writer.sheets[sheet_name]
        # 写入列头
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(header_row_position, col_num, value, head_fmt)  # 生成列头
        col_sign = self.excel_col_sign(len(df.columns))  # 生成列标签

        worksheet.conditional_format(
            'A{row_position}:{col_sign}{row_position}'.format(row_position=header_row_position + 1, col_sign=col_sign),
            {'type': 'no_blanks', 'format': head_fmt})

        # 设置列宽
        worksheet.set_column('A:{col_sign}'.format(col_sign=col_sign), 15, fmt)
        # 加边框
        worksheet.conditional_format(
            'A{header_row_position}:{col_sign}{excel_rows}'.format(col_sign=col_sign, excel_rows=excel_rows,
                                                                   header_row_position=header_row_position + 1),
            {'type': 'no_blanks', 'format': border_format})
        worksheet.conditional_format(
            'A{header_row_position}:{col_sign}{excel_rows}'.format(col_sign=col_sign, excel_rows=excel_rows,
                                                                   header_row_position=header_row_position + 1),
            {'type': 'blanks', 'format': border_format})

