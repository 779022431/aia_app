# -*- coding: utf-8 -*-
import json
import sys
from app import App
import util

reload(sys)
sys.setdefaultencoding('utf8')
app = App().getDataworksInstance()
dirPath = app.config.env('app', 'dirpath')
readFile = app.config.env('dataworks', 'instancesNoSuccessFile')
projectEnv = app.config.env('dataworks', 'projectEnv')
str2 = util.readFile(dirPath + '/' + readFile)
ids = json.loads(str2)
outputData = []
for idItem in ids:
    ret = app.doAction('GetInstanceLog', {'InstanceId': idItem['InstanceId'], 'ProjectEnv': projectEnv})
    if ret['code'] == 0:
        data = json.loads(ret['data'], 'utf-8')
        outputData.append(json.dumps({'instanceId': idItem['InstanceId'], 'logData': data['Data']}))
    else:
        print(ret['message'])
if len(outputData) > 0:
    writeFile = app.config.env('dataworks', 'instanceLog')
    util.write_file(dirPath, writeFile, util.implode("\n", outputData))
