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
writeData = []
page = 1
flag = 1
while flag == 1:
    ret = app.doAction('ListProjects', {'PageNumber': 1, 'PageSize': pageSize})
    if ret['code'] == 0:
        data = json.loads(ret['data'])
        if 0 <= data['PageResult']['TotalCount'] <= page * pageSize:
            flag = 0
        for item in data['PageResult']['ProjectList']:
            writeData.append(item)
        page = page + 1
    else:
        flag = 0
        print(ret['message'])
util.write_file(dirPath, 'projects.txt', json.dumps(writeData))