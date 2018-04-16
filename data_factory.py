# -*- coding: utf-8 -*-

# @Time     : 2018/4/11
# @Author   : WangL
# @File     : data_factory.py

import requests
import json
from urllib.parse import urlencode
from json.decoder import JSONDecodeError



class DataFactory(object):
    def __init__(self):
        self.Sess = requests.session()
        self.img_list = []

    def _get_img_from_sogou(self, key):
        """
        获取图片信息
        :param key: 搜索的关键字
        :return:
        """
        para_dict = {'query': key,
                     'mode': '1',
                     'start': '48',
                     'reqType': 'ajax',
                     'reqFrom': 'result',
                     'tn': '0'}
        
        param_str = urlencode(para_dict)
        url = 'http://pic.sogou.com/pics?' + param_str
        res = self.Sess.get(url)
        if res.status_code != 200:
            return False
        self._parse_and_download(res.text)
        
    def _parse_and_download(self, text):
        if len(text) == 0:
            return False
        try:
            result = json.loads(text.strip())
        except JSONDecodeError as e:
            return False
        if 'items' in result.keys():
            self._save_img_links(result['items'])
        
    def _save_img_links(self, info_list):
        if not isinstance(info_list, list):
            return False
        for elem in info_list:
            if not isinstance(elem, dict):
                continue
            if 'pic_url' in elem.keys():
                self.img_list.append(elem['pic_url'])

    def query_img(self, key):
        """
        查询了图片
        :return:
        """
        self._get_img_from_sogou(key)
