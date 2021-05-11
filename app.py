# -*- coding: utf-8 -*-
import ConfigParser
import os

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


class Config:
    cf = None

    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(os.path.split(os.path.realpath(__file__))[0] + "/config.ini")

    def env(self, section, key):
        return self.cf.get(section, key)


class App:
    client = None
    domain = None
    version = None
    config = None

    def __init__(self):
        self.config = Config()
        self.client = AcsClient(self.config.env('app', 'clientId'), self.config.env('app', 'clientSecret'), self.config.env('app', 'region'))

    def __build_request(self, action, param):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_method('POST')
        request.set_domain(self.domain)
        request.set_version(self.version)
        request.set_action_name(action)
        request.set_query_params(param)
        return request

    def __doAction(self, request):
        try:
            response = self.client.do_action_with_exception(request)
            return {"code": 0, "data": response}
        except Exception as e:
            return {"code": 1, "message": e.message}

    def setDomain(self, domain):
        self.domain = domain

    def setVersion(self, version):
        self.version = version

    def doAction(self, action, params=None):
        if params is None:
            params = {}
        request = self.__build_request(action, params)
        return self.__doAction(request)

    def getDataworksInstance(self):
        self.setDomain(self.config.env('dataworks', 'domain'))
        self.setVersion(self.config.env('dataworks', 'version'))
        return self

    def getRdsInstance(self):
        self.setDomain(self.config.env('rds', 'domain'))
        self.setVersion(self.config.env('rds', 'version'))
        return self
