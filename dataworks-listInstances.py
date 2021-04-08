# -*- coding: utf-8 -*-
import json
import sys
from app import App
from util import unicode_convert
from util import write_file
import util

reload(sys)
sys.setdefaultencoding('utf8')
app = App().getDataworksInstance()
dirPath = app.config.env('app', 'dirpath')
pageSize = int(app.config.env('dataworks', 'pageSize'))
projectEnv = app.config.env('dataworks', 'projectEnv')
nodeProgramTypeFile = app.config.env('dataworks', 'nodeProgramTypeFile')
str2 = util.readFile(dirPath + '/' + nodeProgramTypeFile)
nodeProgramType = json.loads(str2)
businessStr = util.readFile(dirPath + '/' +  app.config.env('dataworks', 'businessFile'))
ids = json.loads(businessStr)
outputData = []
noSuccessData = []
now = util.time_unix()
BeginBizdate = util.time_date(now - 20 * 60)
EndBizdate = util.time_date(now)
for idItem in ids:
    if idItem == "":
        continue
    page = 1
    flag = 1
    while flag == 1:
        ret = app.doAction('ListInstances', {'BizName': idItem['BusinessName'], 'ProjectEnv': projectEnv, 'PageNumber': page, 'PageSize': pageSize, 'ProjectId': idItem['ProjectId']})
        if ret['code'] == 0:
            data = json.loads(ret['data'], 'utf-8')
            totalCount = util.get_dict_value(data['Data'], 'TotalCount', 0)
            if 0 <= totalCount < page * pageSize:
                flag = 0
            items = util.get_dict_value(data['Data'], 'Instances', 0)
            for item in items:
                item['ProgramType'] = util.get_dict_value(nodeProgramType, str(item['NodeId']), '')
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
writeStr = ''
for i in outputData:
    writeStr = writeStr + json.dumps(i) + "\n"
util.write_file_append(dirPath, writeFile1, writeStr)

writeFile2 = app.config.env('dataworks', 'instancesNoSuccessFile')
util.write_file(dirPath, writeFile2, json.dumps(noSuccessData))
