# -*- coding: utf-8 -*-
import json
import sys
from app import App
import util

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getDataworksInstance()
dirPath = app.config.env('app', 'dirpath')
pageSize = int(app.config.env('dataworks', 'pageSize'))
projectIdsStr = app.config.env('dataworks', 'projectIds')
projectEnv = app.config.env('dataworks', 'projectEnv')
projectIds = util.explode(',', projectIdsStr)
writeData = []
for projectId in projectIds:
    if projectId == "":
        continue
    projectId = int(projectId)
    page = 1
    flag = 1
    while flag == 1:
        ret = app.doAction('ListNodes', {'ProjectEnv': projectEnv, 'PageNumber': page, 'PageSize': pageSize, 'ProjectId': projectId})
        if ret['code'] == 0:
            data = json.loads(ret['data'])
            if 0 <= data['Data']['TotalCount'] <= page * pageSize:
                flag = 0
            for item in data['Data']['Nodes']:
                item['timestamp'] = util.time_unix()
                writeData.append(item)
            page = page + 1
        else:
            flag = 0
            print(ret['message'])
writeFile = app.config.env('dataworks', 'nodesFile')
writeStr = ''
for i in writeData:
    writeStr = writeStr + json.dumps(i) + "\n"
util.write_file_append(dirPath, writeFile, writeStr)
