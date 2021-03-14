# -*- coding: utf-8 -*-
import json
import sys
from util import App
from util import unicode_convert

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getDataworksInstance()
page = 1
pageSize = 10
flag = 1
while flag == 1:
    ret = app.doAction('ListInstances', {'NodeId': 13582, 'ProjectEnv': 'PROD', 'PageNumber': page, 'PageSize': pageSize, 'ProjectId': 157})
    if ret['code'] == 0:
        data = json.loads(ret['data'], 'utf-8')
        data = unicode_convert(data)
        if 0 <= data['Data']['TotalCount'] < page * pageSize:
            flag = 0
        for item in data['Data']['Instances']:
            print 'InstanceId: {},Status: {}, ErrorMessage: {}'.format(item['InstanceId'], item['Status'], item['ErrorMessage'])
        page = page + 1
    else:
        flag = 0
        print(ret['message'])