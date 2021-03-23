# -*- coding: utf-8 -*-
import json
import sys
from util import App
from util import unicode_convert
import util

reload(sys)
sys.setdefaultencoding('utf8')
app = App().getDataworksInstance()
dirPath = app.config.env('app', 'dirpath')
str2 = util.readFile(dirPath + '/instances.txt')
str2 = str2.strip('\n')
ids = json.loads(str2)
outputData = []
for idItem in ids:
    if idItem['Status'] == 'FAILURE':
        ret = app.doAction('GetInstanceLog', {'InstanceId': idItem['InstanceId'], 'ProjectEnv': 'PROD'})
        if ret['code'] == 0:
            data = json.loads(ret['data'], 'utf-8')
            outputData.append({'instanceId':idItem['InstanceId'],'data':data['Data']})
        else:
            print(ret['message'])
util.write_file(dirPath, 'instances_logs.txt', json.dumps(outputData))