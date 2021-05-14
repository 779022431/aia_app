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
readFile = app.config.env('rds', 'rdsListFile')
str2 = util.readFile(dirPath + '/' + readFile)
ids = json.loads(str2)
startTime = util.time_date(util.time_unix(), "%Y-%m-%d") + "Z"
endTime = startTime
for id in ids:
    ret = app.doAction('DescribeSlowLogs', {'StartTime': startTime, 'EndTime': endTime, 'DBInstanceId': id, 'PageNumber': 1, 'PageSize': 30})
    if ret['code'] != 0:
        continue
    data = json.loads(ret['data'])
    if data['PageRecordCount'] <= 0:
        continue
    items = data['Items']['SQLSlowLog']
    count = 1
    for item in items:
        if count > 10:
            continue
        item['DBInstanceId'] = id
        writeData.append(json.dumps(item))
        count = count + 1
# 数据写入文件
fileName = app.config.env('rds', 'rdsSlowSqlFile')
util.write_file(dirPath, fileName, util.implode("\n", writeData))
