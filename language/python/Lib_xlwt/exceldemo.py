
'''

excel
        - workbook
            - sheet
                -

'''

import xlwt

workbook=xlwt.Workbook(encoding='utf-8')
sheet=workbook.add_sheet("sheet")
sheet.write(1,1,"python使用excel")
workbook.save('xlwt.xls')


