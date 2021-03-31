# -*- coding: utf-8 -*-
import json
import sys
from util import App
from util import unicode_convert
from util import write_file
import util

reload(sys)
sys.setdefaultencoding('utf8')
app = App().getDataworksInstance()
dirPath = app.config.env('app', 'dirpath')
pageSize = int(app.config.env('dataworks', 'pageSize'))
nodesFile = app.config.env('dataworks', 'nodesFile')
projectEnv = app.config.env('dataworks', 'projectEnv')
str2 = util.readFile(dirPath + '/' + nodesFile)
ids = json.loads(str2)
outputData = []
noSuccessData = []
for idItem in ids:
    if idItem == "":
        continue
    page = 1
    flag = 1
    while flag == 1:
        ret = app.doAction('ListInstances', {'NodeId': idItem['NodeId'], 'ProjectEnv': projectEnv, 'PageNumber': page, 'PageSize': pageSize, 'ProjectId': idItem['ProjectId']})
        if ret['code'] == 0:
            data = json.loads(ret['data'], 'utf-8')
            data = unicode_convert(data)
            if 0 <= data['Data']['TotalCount'] < page * pageSize:
                flag = 0
            for item in data['Data']['Instances']:
                item['ProgramType'] = idItem['ProgramType']
                if item['Status'] != 'SUCCESS':
                    noSuccessData.append(item)
                else:
                    item['UseTime'] = item['FinishTime'] - item['BeginRunningTime']
                outputData.append(item)
            page = page + 1
        else:
            flag = 0
            print(ret['message'])
writeFile1 = app.config.env('dataworks', 'instancesFile')
write_file(dirPath, writeFile1, json.dumps(outputData))
writeFile2 = app.config.env('dataworks', 'instancesNoSuccessFile')
write_file(dirPath, writeFile2, json.dumps(noSuccessData))
