# -*- coding: utf-8 -*-
import json
import sys
from app import App
import util

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getMonitorInstance()
dirPath = app.config.env('app', 'dirpath')
pageSize = int(app.config.env('monitor', 'pageSize'))
writeData = []
ret1 = app.doAction('DescribeMetricLast', {'Namespace': 'acs_polardb', 'MetricName': 'cluster_cpu_utilization'})
# ret2 = app.doAction('DescribeMetricLast', {'Namespace': 'acs_polardb', 'MetricName': 'cluster_memory_utilization'})
if ret1['code'] == 0:
    data = json.loads(ret1['data'])
    datapoints = json.loads(data['Datapoints'])
    for item in datapoints:
        writeData.append(json.dumps(item))
# 数据写入文件
fileName = app.config.env('monitor', 'monitorListFile')
util.write_file(dirPath, fileName, util.implode("\n", writeData))
