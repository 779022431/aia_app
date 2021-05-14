# -*- coding: utf-8 -*-
import json
import sys
from app import App
import util

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getMonitorInstance()
dirPath = app.config.env('app', 'dirpath')
# cpu
ret1 = app.doAction('DescribeMetricLast', {'Namespace': 'acs_rds_dashboard', 'MetricName': 'CpuUsage'})
data = json.loads(ret1['data'])
datapoints = json.loads(data['Datapoints'])
fileName1 = app.config.env('rds', 'rdsCpuFile')
writeData1 = []
for i in datapoints:
    writeData1.append(json.dumps(i))
util.write_file(dirPath, fileName1, util.implode("\n", writeData1))
# memory
ret1 = app.doAction('DescribeMetricLast', {'Namespace': 'acs_rds_dashboard', 'MetricName': 'MemoryUsage'})
data = json.loads(ret1['data'])
datapoints = json.loads(data['Datapoints'])
fileName1 = app.config.env('rds', 'rdsMemoryFile')
writeData1 = []
for i in datapoints:
    writeData1.append(json.dumps(i))
util.write_file(dirPath, fileName1, util.implode("\n", writeData1))
# DiskUsage
ret1 = app.doAction('DescribeMetricLast', {'Namespace': 'acs_rds_dashboard', 'MetricName': 'DiskUsage'})
data = json.loads(ret1['data'])
datapoints = json.loads(data['Datapoints'])
fileName1 = app.config.env('rds', 'rdsDiskFile')
writeData1 = []
for i in datapoints:
    writeData1.append(json.dumps(i))
util.write_file(dirPath, fileName1, util.implode("\n", writeData1))
