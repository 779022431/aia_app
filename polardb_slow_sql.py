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
readFile = app.config.env('polardb', 'polardbListFile')
str2 = util.readFile(dirPath + '/' + readFile)
ids = json.loads(str2)
now = util.time_unix() - 8 * 3600 - 60
startTime = util.time_date(now, "%Y-%m-%dT%H:%MZ")
endTime = startTime
for idItem in ids:
    id = idItem['id']
    name = idItem['name']
    page = 1
    flag = 1
    while flag == 1:
        ret = app.doAction('DescribeSlowLogRecords', {'StartTime': startTime, 'EndTime': endTime, 'DBClusterId': id, 'PageNumber': page, 'PageSize': pageSize})
        if ret['code'] != 0:
            break
        data = json.loads(ret['data'])
        if data['PageRecordCount'] <= 0:
            break
        if data['PageRecordCount'] < page * pageSize:
            flag = 0
        page = page + 1
        items = data['Items']['SQLSlowRecord']
        for item in items:
            if item['QueryTimes'] < int(app.config.env('polardb', 'slowSqlTime')):
                continue
            item['DBClusterId'] = id
            item['DBClusterDescription'] = name
            writeData.append(json.dumps(item))
# 数据写入文件
fileName = app.config.env('polardb', 'polardbSlowSqlFile')
util.write_file(dirPath, fileName, util.implode("\n", writeData))
