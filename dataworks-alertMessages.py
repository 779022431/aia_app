# -*- coding: utf-8 -*-
import json
import sys
from util import App
from util import unicode_convert
from util import time_unix
from util import utc_time_date
import util

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getDataworksInstance()
now = time_unix()
beginTime = utc_time_date(now - 48 * 3600)
endTime = utc_time_date(now)
page = 1
pageSize = 10
flag = 1
outputData = []
while flag == 1:
    ret = app.doAction('ListAlertMessages',{'AlertMethods': 'SMS', 'PageNumber': page, 'PageSize': pageSize, 'BeginTime': beginTime, 'EndTime': endTime})
    if ret['code'] == 0:
        data = json.loads(ret['data'], 'utf-8')
        data = unicode_convert(data)
        if data['Data']['TotalCount'] > 0 and data['Data']['TotalCount'] < page * pageSize:
            flag = 0
        for alertMessage in data['Data']['AlertMessages']:
            outputData.append(alertMessage)
        page = page + 1
    else:
        flag = 0
        print(ret['message'])
dirPath = app.config.env('app', 'dirpath')
util.write_file(dirPath, 'alert_messages.txt', json.dumps(outputData))