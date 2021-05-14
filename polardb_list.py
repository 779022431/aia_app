# -*- coding: utf-8 -*-
import json
import sys
from app import App
import util

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getPolardbInstance()
dirPath = app.config.env('app', 'dirpath')
pageSize = int(app.config.env('polardb', 'pageSize'))
writeData = []
page = 1
flag = 1
while flag == 1:
    ret = app.doAction('DescribeDBClusters', {'PageNumber': page, 'PageSize': pageSize})
    if ret['code'] != 0:
        flag = 0
        continue
    data = json.loads(ret['data'])
    if 0 <= data['TotalRecordCount'] <= page * pageSize:
        flag = 0
    for item in data['Items']['DBCluster']:
        writeData.append(item['DBClusterId'])
    page = page + 1
# 数据写入文件
fileName = app.config.env('polardb', 'polardbListFile')
util.write_file(dirPath, fileName, json.dumps(writeData))
