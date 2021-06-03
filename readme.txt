from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

client = AcsClient('', '', 'cn-shenzhen')
request = CommonRequest()
request.set_accept_format('json')
request.set_method('POST')
request.set_domain('polardb.aliyuncs.com')
request.set_version('2017-08-01')
request.set_action_name('DescribeDBClusters')
request.set_query_params({'RegionId': 'cn-shanghai-finance-1', 'PageNumber': 1, 'PageSize': 50})
try:
    response = client.do_action_with_exception(request)
    print response
except Exception as e:
    print e
