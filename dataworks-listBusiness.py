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
projectIds = util.explode(',', projectIdsStr)
writeData = []
for projectId in projectIds:
    page = 1
    flag = 1
    while flag == 1:
        ret1 = app.doAction('ListBusiness', {'PageNumber': page, 'PageSize': pageSize, 'ProjectId': projectId})
        if ret1['code'] == 0:
            data1 = json.loads(ret1['data'])
            if 0 <= data1['Data']['TotalCount'] <= page * pageSize:
                flag = 0
            for item1 in data1['Data']['Business']:
                writeData.append(item1)
            page = page + 1
        else:
            flag1 = 0
            print(ret1['message'])
writeFile = app.config.env('dataworks', 'businessFile')
util.write_file(dirPath, writeFile, json.dumps(writeData))
