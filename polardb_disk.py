# -*- coding: utf-8 -*-
import json
import sys
from app import App
import util

reload(sys)
sys.setdefaultencoding('utf8')

app = App().getPolardbInstance()
dirPath = app.config.env('app', 'dirpath')
readFile = app.config.env('polardb', 'polardbListFile')
str2 = util.readFile(dirPath + '/' + readFile)
ids = json.loads(str2)
now = util.time_unix()
writeData = []
for idItem in ids:
    id = idItem['id']
    name = idItem['name']
    ret2 = app.doAction('DescribeDBClusterAttribute', {'DBClusterId': id})
    data2 = json.loads(ret2['data'])
    storageMax = round(data2['StorageMax'] / 1024 / 1024, 2)
    storageUsed = round(data2['StorageUsed'] / 1024 / 1024, 2)
    average = round(storageUsed * 100 / storageMax, 2)
    writeData.append(json.dumps({
        'Average': format(average, '.2f') + '%',
        'DBClusterId': id,
        'DBClusterDescription': name,
        'timestamp': now * 1000,
    }))
# DiskUsage
fileName1 = app.config.env('polardb', 'polardbDiskFile')
util.write_file(dirPath, fileName1, util.implode("\n", writeData))
