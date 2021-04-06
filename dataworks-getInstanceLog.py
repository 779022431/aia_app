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
timestamp=util.time_unix()
for idItem in ids:
    ret = app.doAction('GetInstanceLog', {'InstanceId': idItem['InstanceId'], 'ProjectEnv': projectEnv})
    if ret['code'] == 0:
        data = json.loads(ret['data'], 'utf-8')
        outputData.append({'instanceId': idItem['InstanceId'], 'logData': data['Data'],'timestamp':timestamp})
    else:
        print(ret['message'])
writeFile = app.config.env('dataworks', 'instanceLog')
writeStr = ''
for i in outputData:
    writeStr = writeStr + json.dumps(i) + "\n"
util.write_file_append(dirPath, writeFile, writeStr)
