#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from urllib import request
from urllib import parse


# ======================================================
# 通过百度天气API，获取天气信息
# API请求参数：
# city = 城市名称
# ak = 用户认证key，需要注册才能获得
# ======================================================
class Weather(object):
    def __init__(self, city=''):
        self.__weather = {}
        self.__url_weather = 'http://api.map.baidu.com/telematics/v3/weather'
        self.__key = '1fb0f26807b883c97ba10d3ce7ad8c38'
        self.__city = city

    @staticmethod  # 静态方法
    def handle_request(url):
        req = request.Request(url)
        with request.urlopen(req) as response:
            print('Status: ', response.status, response.reason)
            return response.read().decode('utf-8')

    def get_weather(self, city=''):
        if city is not None:
            self.__city = city
        url = '%s?location=%s&output=json&ak=%s' % (
            self.__url_weather, parse.quote(self.__city), self.__key)
        print("%s" % url)
        #return
        self.__weather = self.handle_request(url)

        data_json = json.loads(self.__weather)
        if data_json['error'] != 0:
            print('检查城市输入是否有误')
            return
        print("%s:%s" %
              (data_json['results'][0]['currentCity'], data_json['date']))

        for t in data_json['results'][0]['weather_data']:
            print(t['date'])
            print(t['temperature'])
            print(t['weather'])
            print(t['wind'])
            print("")

        for t in data_json['results'][0]['index']:
            print(t['tipt'] + ':' + t['zs'])
            print(t['title'] + ':' + t['des'])
            print('')
        return self.__weather


if __name__ == '__main__':
    weather = Weather()
    weather.get_weather('杭州')
