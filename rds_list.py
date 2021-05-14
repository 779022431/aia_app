# -*- coding: utf-8 -*-
import json
import sys
from app import App
import util

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getRdsInstance()
dirPath = app.config.env('app', 'dirpath')
pageSize = int(app.config.env('rds', 'pageSize'))
writeData = []
page = 1
flag = 1
while flag == 1:
    ret = app.doAction('DescribeDBInstances', {'PageNumber': page, 'PageSize': pageSize})
    if ret['code'] != 0:
        flag = 0
        continue
    data = json.loads(ret['data'])
    if 0 <= data['TotalRecordCount'] <= page * pageSize:
        flag = 0
        continue
    for item in data['Items']['DBInstance']:
        writeData.append(item['DBInstanceId'])
    page = page + 1
# 数据写入文件
fileName = app.config.env('rds', 'rdsListFile')
util.write_file(dirPath, fileName, json.dumps(writeData))
