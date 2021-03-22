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
str2 = util.readFile(dirPath + '/instances.txt')
str2 = str2.strip('\n')
ids = util.explode(',', str2)
for id in ids:
    ret = app.doAction('GetInstanceLog', {'InstanceId': id, 'ProjectEnv': 'PROD'})
    if ret['code'] == 0:
        data = json.loads(ret['data'], 'utf-8')
        data = unicode_convert(data)
        print 'InstanceId: {},ErrorCode: {}, ErrorMessage: {}, Data: {}'.format(id, data['ErrorCode'], data['ErrorMessage'], data['Data'])
    else:
        print(ret['message'])
