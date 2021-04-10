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
projectEnv = app.config.env('dataworks', 'projectEnv')
businessStr = util.readFile(dirPath + '/' + app.config.env('dataworks', 'businessFile'))
ids = json.loads(businessStr)
writeData = []
nodeProgramType = {}
for idItem in ids:
    page = 1
    flag = 1
    while flag == 1:
        ret = app.doAction('ListNodes', {'BizName': idItem['BusinessName'], 'ProjectEnv': projectEnv, 'PageNumber': page, 'PageSize': pageSize, 'ProjectId': idItem['ProjectId']})
        if ret['code'] == 0:
            data = json.loads(ret['data'])
            totalCount = util.get_dict_value(data['Data'], 'TotalCount', 0)
            if 0 <= totalCount <= page * pageSize:
                flag = 0
            items = util.get_dict_value(data['Data'], 'Nodes', [])
            for item in items:
                nodeProgramType[item['NodeId']] = item['ProgramType']
                writeData.append(json.dumps(item))
            page = page + 1
        else:
            flag = 0
            print(ret['message'])
writeFile = app.config.env('dataworks', 'nodesFile')
util.write_file(dirPath, writeFile, util.implode("\n", writeData))

writeFile = app.config.env('dataworks', 'nodeProgramTypeFile')
util.write_file(dirPath, writeFile, json.dumps(nodeProgramType))
