# -*- coding: utf-8 -*-
import json
import sys
from util import App
from util import unicode_convert

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getDataworksInstance()
ret = app.doAction('GetInstanceLog', {'InstanceId': 9716662351, 'ProjectEnv': 'PROD'})
if ret['code'] == 0:
    data = json.loads(ret['data'], 'utf-8')
    data = unicode_convert(data)
    print 'InstanceId: {},ErrorCode: {}, ErrorMessage: {}'.format(data['InstanceId'], data['Status'], data['ErrorMessage'])
else:
    print(ret['message'])
