# -*- coding: utf-8 -*-
import json
import sys
from app import App
import util

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getPolardbInstance()
dirPath = app.config.env('app', 'dirpath')
readFile = app.config.env('polardb', 'polardbListFile')
str2 = util.readFile(dirPath + '/' + readFile)
ids = json.loads(str2)
now = util.time_unix() - 8 * 3600
performanceInterval = int(app.config.env('polardb', 'performanceInterval'))
startTime = util.time_date(now - performanceInterval, "%Y-%m-%dT%H:%MZ")
endTime = util.time_date(now, "%Y-%m-%dT%H:%MZ")
writeMem = []
writeCpu = []
writeData = []
for idItem in ids:
    id = idItem['id']
    name = idItem['name']
    ret1 = app.doAction('DescribeDBClusterPerformance', {'DBClusterId': id, 'Key': 'PolarDBDiskUsage', 'StartTime': startTime, 'EndTime': endTime})
    other = 0
    total = 0
    data = json.loads(ret1['data'])
    for item in data['PerformanceKeys']['PerformanceItem']:
        itemValue = item['Points']['PerformanceItemValue'][0]
        if item['MetricName'] == 'mean_data_size':
            other = float(itemValue['Value'])
            total += other
        else:
            total += float(itemValue['Value'])
    writeData.append(json.dumps({
        'Average': round(other / total, 3),
        'DBClusterId': id,
        'timestamp': (util.time_unix(startTime, "%Y-%m-%dT%H:%MZ") + 8 * 3600) * 1000,
    }))
# DiskUsage
fileName1 = app.config.env('polardb', 'polardbDiskFile')
util.write_file(dirPath, fileName1, util.implode("\n", writeData))
