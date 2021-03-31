# -*- coding: utf-8 -*-
import json
import sys
from util import App
import util

reload(sys)
sys.setdefaultencoding('utf8')
app = App().getDataworksInstance()
dirPath = app.config.env('app', 'dirpath')
readFile = app.config.env('dataworks', 'instancesNoSuccessFile')
str2 = util.readFile(dirPath + '/' + readFile)
ids = json.loads(str2)
outputData = []
for idItem in ids:
    ret = app.doAction('GetInstanceLog', {'InstanceId': idItem['InstanceId'], 'ProjectEnv': 'PROD'})
    if ret['code'] == 0:
        data = json.loads(ret['data'], 'utf-8')
        outputData.append({'instanceId': idItem['InstanceId'], 'logData': data['Data']})
    else:
        print(ret['message'])
writeFile2 = app.config.env('dataworks', 'instanceLog')
util.write_file_append(dirPath, writeFile2, json.dumps(outputData))
