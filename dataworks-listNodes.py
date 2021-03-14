# -*- coding: utf-8 -*-
import json
import sys
from util import App
from util import unicode_convert
import util

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getDataworksInstance()
str2 = util.readFile('projects.txt')
str2 = str2.strip('\n')
projectIds = util.explode(',', str2)
for projectId in projectIds:
    page = 1
    pageSize = 10
    flag = 1
    while flag == 1:
        ret = app.doAction('ListNodes', {'ProjectEnv': 'PROD', 'PageNumber': page, 'PageSize': pageSize, 'ProjectId': projectId})
        if ret['code'] == 0:
            data = json.loads(ret['data'])
            data = unicode_convert(data)
            if data['Data']['TotalCount'] > 0 and data['Data']['TotalCount'] < page * pageSize:
                flag = 0
            for item in data['Data']['Nodes']:
                print 'nodeId: {},name: {},projectId: {},Description:{},CronExpress: {}'.format(item['NodeId'], item['NodeName'], item['ProjectId'],item['Description'], item['CronExpress'])
            page = page + 1
        else:
            flag = 0
            print(ret['message'])
