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
page = 1
pageSize = 10
flag = 1
projectIds = []
while flag == 1:
    ret = app.doAction('ListProjects', {'PageNumber': page, 'PageSize': pageSize})
    if ret['code'] == 0:
        data = json.loads(ret['data'])
        data = unicode_convert(data)
        if data['PageResult']['TotalCount'] > 0 and data['PageResult']['TotalCount'] < page * pageSize:
            flag = 0
        for item in data['PageResult']['ProjectList']:
            projectIds.append(item['ProjectId'])
            print item
        page = page + 1
    else:
        flag = 0
        print(ret['message'])

dirPath = app.config.env('app', 'dirpath')
write_file(dirPath, 'projects.txt', util.implode(',', projectIds))