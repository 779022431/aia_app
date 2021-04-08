# -*- coding: utf-8 -*-
import json
import os
import sys
import time


def write_file_append(dir_path, file, data):
    if sys.platform == "win32":
        dir_path = dir_path + '\\'
    else:
        dir_path = dir_path + '/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    filepath = dir_path + file
    fp = open(filepath, "a+")
    fp.write(data + "\n")
    fp.close()


def write_file(dir_path, file, data):
    if sys.platform == "win32":
        dir_path = dir_path + '\\'
    else:
        dir_path = dir_path + '/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    filepath = dir_path + file
    fp = open(filepath, "w")
    fp.write(data)
    fp.close()


def bytes_to_json(bytes_):
    data = str(bytes_)
    return json.loads(data)


def bytes_to_str(bytes_):
    return str(bytes_)


def str_split(str_):
    return str_.split(',')


def dict_to_str(dict_):
    return str(dict_)


def get_dict_value(dict_, key, value=""):
    if key in dict_:
        return dict_[key]
    else:
        return value


def time_unix(date="", format_="%Y-%m-%d %H:%M:%S"):
    if date == "":
        return int(time.time())
    else:
        return int(time.mktime(time.strptime(date, format_)))


def time_date(timestamp=0, format_="%Y-%m-%d %H:%M:%S"):
    if timestamp == 0:
        return time.strftime(format_, time.localtime())
    else:
        return time.strftime(format_, time.localtime(timestamp))


def utc_time_date(timestamp=0, format_="%Y-%m-%dT%H:%M:%S+0800"):
    if timestamp == 0:
        return time.strftime(format_, time.localtime())
    else:
        return time.strftime(format_, time.localtime(timestamp))


def unicode_convert(input_data):
    if isinstance(input_data, dict):
        return {unicode_convert(key): unicode_convert(value) for key, value in input_data.iteritems()}
    elif isinstance(input_data, list):
        return [unicode_convert(element) for element in input_data]
    elif isinstance(input_data, unicode):
        return input_data.encode('utf-8')
    else:
        return input_data


def implode(char, data):
    return char.join(str(i) for i in data)


def explode(char, data):
    return data.split(char)


def readFile(filePath):
    fileObj = open(filePath)
    try:
        txt = fileObj.read()
    finally:
        fileObj.close()
    return txt
