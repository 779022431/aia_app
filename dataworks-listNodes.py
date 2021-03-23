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
str2 = util.readFile(dirPath + '/projects.txt')
str2 = str2.strip('\n')
projectIds = util.explode(',', str2)
ids = []
for projectId in projectIds:
    page = 1
    pageSize = 10
    flag = 1
    while flag == 1:
        ret = app.doAction('ListNodes', {'ProjectEnv': 'PROD', 'PageNumber': page, 'PageSize': pageSize, 'ProjectId': projectId})
        if ret['code'] == 0:
            data = json.loads(ret['data'])
            data = unicode_convert(data)
            if 0 < data['Data']['TotalCount'] < page * pageSize:
                flag = 0
            for item in data['Data']['Nodes']:
                ids.append({'nodeId': item['NodeId'], 'projectId': item['ProjectId']})
                print 'nodeId: {},name: {},projectId: {},Description:{},CronExpress: {}'.format(item['NodeId'], item['NodeName'], item['ProjectId'], item['Description'], item['CronExpress'])
            page = page + 1
        else:
            flag = 0
            print(ret['message'])
dirPath = app.config.env('app', 'dirpath')
util.write_file(dirPath, 'nodes.txt', json.dumps(',', ids))
