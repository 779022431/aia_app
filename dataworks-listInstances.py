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
str2 = util.readFile(dirPath + '/nodes.txt')
str2 = str2.strip('\n')
ids = json.loads(str2)
page = 1
pageSize = 10
flag = 1
outputData = []
outputData = []
for idItem in ids:
    while flag == 1:
        ret = app.doAction('ListInstances', {'NodeId': idItem['nodeId'], 'ProjectEnv': 'PROD', 'PageNumber': page, 'PageSize': pageSize, 'ProjectId': idItem['projectId']})
        if ret['code'] == 0:
            data = json.loads(ret['data'], 'utf-8')
            data = unicode_convert(data)
            if 0 <= data['Data']['TotalCount'] < page * pageSize:
                flag = 0
            for item in data['Data']['Instances']:
                outputData.append(item)
            page = page + 1
        else:
            flag = 0
            print(ret['message'])
dirPath = app.config.env('app', 'dirpath')
write_file(dirPath, 'instances.txt', json.dumps(outputData))
