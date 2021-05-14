# -*- coding: utf-8 -*-
import json
import sys
from app import App
import util

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getMonitorInstance()
dirPath = app.config.env('app', 'dirpath')
pageSize = int(app.config.env('rds', 'pageSize'))
writeData = []
ret1 = app.doAction('DescribeMetricLast', {'Namespace': 'acs_rds_dashboard', 'MetricName': 'CpuUsage'})
ret2 = app.doAction('DescribeMetricLast', {'Namespace': 'acs_rds_dashboard', 'MetricName': 'MemoryUsage'})
ret3 = app.doAction('DescribeMetricLast', {'Namespace': 'acs_rds_dashboard', 'MetricName': 'DiskUsage'})
if ret1['code'] == 0:
   data = json.loads(ret1['data'])
   print data
exit()
# 数据写入文件
fileName = app.config.env('rds', 'rdsListFile')
util.write_file(dirPath, fileName, json.dumps(writeData))
