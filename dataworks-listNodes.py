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


def listBusiness(projectId1):
    businessData1 = []
    page1 = 1
    flag1 = 1
    while flag1 == 1:
        ret1 = app.doAction('ListBusiness', {'PageNumber': page1, 'PageSize': pageSize, 'ProjectId': projectId1})
        if ret1['code'] == 0:
            data1 = json.loads(ret1['data'])
            if 0 <= data1['Data']['TotalCount'] <= page1 * pageSize:
                flag1 = 0
            for item1 in data['Data']['Nodes']:
                businessData1.append(item1)
            page1 = page1 + 1
        else:
            flag1 = 0
            print(ret1['message'])
    return businessData1


writeData = []
for projectId in projectIds:
    if projectId == "":
        continue
    projectId = int(projectId)
    businessData = listBusiness(projectId)
    print businessData
    for businessItem in businessData:
        page = 1
        flag = 1
        while flag == 1:
            ret = app.doAction('ListNodes', {'BizName': businessItem['BusinessName'], 'ProjectEnv': projectEnv, 'PageNumber': page, 'PageSize': pageSize, 'ProjectId': projectId})
            if ret['code'] == 0:
                data = json.loads(ret['data'])
                if 0 <= data['Data']['TotalCount'] <= page * pageSize:
                    flag = 0
                for item in data['Data']['Business']:
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
util.write_file(dirPath, 'org_' + writeFile, json.dumps(writeData))
