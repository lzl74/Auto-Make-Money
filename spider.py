# -*- encoding: utf-8 -*-
"""
爬取来自东方财富网的最新可转债信息：http://data.eastmoney.com/kzz/default.html
接口示例：http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB2.0&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=1&ps=6
"""
import re

from config import headers
import abc
import requests
import json
import time


class BaseSpider(abc.ABC):
    def __init__(self, url=None):
        pass

    def _get_token(self) -> str:
        pass

    def get_today_list(self) -> list:
        pass


class EastSpider(BaseSpider):
    def __init__(self, ps='10', url='http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get'):
        super(EastSpider, self).__init__()
        self.url = url
        self.params = {
            'type': 'KZZ_LB2.0',
            'token': '',
            'cmd': '',
            'st': 'STARTDATE',
            'sr': '-1',
            'p': '1',
            'ps': ps  # page_size
        }

    def get_list(self):
        self.params['token'] = self._get_token()
        r = requests.get(self.url, params=self.params, headers=headers)
        return json.loads(r.text)

    def get_today_list(self) -> list:
        r_list = self.get_list()
        today_str = time.strftime("%Y-%m-%d", time.localtime())
        today_list = []
        for stock in r_list:
            if stock['STARTDATE'].split('T')[0] == today_str:
                today_list.append([stock['BONDCODE'], stock['SNAME']])
        return today_list

    def _get_token(self) -> str:
        token_url = 'http://data.eastmoney.com/kzz/default.html'
        r = requests.get(token_url, headers=headers)
        token_list = re.findall('&token=(.+?)&', r.text)
        if len(token_list) != 1:
            raise ValueError("Token获取出错！")
        return token_list[0]
