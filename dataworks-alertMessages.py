# -*- coding: utf-8 -*-
import json
import sys
from util import App
from util import unicode_convert
from util import time_unix
from util import utc_time_date

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getDataworksInstance()
now = time_unix()
beginTime = utc_time_date(now - 40 * 3600)
endTime = utc_time_date(now)
page = 1
pageSize = 10
flag = 1
while flag == 1:
    ret = app.doAction('ListAlertMessages',{'AlertMethods': 'SMS', 'PageNumber': page, 'PageSize': pageSize, 'BeginTime': beginTime, 'EndTime': endTime})
    if ret['code'] == 0:
        data = json.loads(ret['data'], 'utf-8')
        data = unicode_convert(data)
        if data['Data']['TotalCount'] > 0 and data['Data']['TotalCount'] < page * pageSize:
            flag = 0
        for alertMessage in data['Data']['AlertMessages']:
            # print get_dict_value(alertMessage,'AlertId')
            # print get_dict_value(alertMessage,'Nodes')
            # print get_dict_value(alertMessage,'Instances')
            print 'AlertId: {}, Content: {}, Nodes: {}'.format(alertMessage['AlertId'], alertMessage['Content'],alertMessage['Nodes'])
            # write_file('./', bytes(alertMessage['AlertId']) + '.html', alertMessage['Content'])
        page = page + 1
    else:
        flag = 0
        print(ret['message'])
