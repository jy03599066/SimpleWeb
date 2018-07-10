# -*- coding: utf-8 -*-

# @Time     : 2018/4/11
# @Author   : WangL
# @File     : data_factory.py

import requests
import json
import imghdr
import random
import string
import socketserver
from urllib.parse import urlencode
from json.decoder import JSONDecodeError
from tools import ThreadPool


class DataFactory(object):
    def __init__(self):
        self.Sess = requests.session()
        self.img_list = []
        self.Pool = ThreadPool(4)

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
        self._save_imgs()
        
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

    @staticmethod
    def download_img(url):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                # 判断文件格式，并随机生成文件名
                content = res.content
                img_type = imghdr.what('', content)
                name = ''.join(random.choice(string.ascii_letters) for _ in range(24))
                path = 'img/{}.{}'.format(name, img_type)
                with open(path, 'wb') as file:
                    file.write(content)
            else:
                print('{} failed'.format(url))
        except Exception as e:
            pass

    def _save_imgs(self):
        print('there is {} imgs'.format(len(self.img_list)))
        for e in self.img_list:
            self.Pool.add_task(self.download_img, e)
        self.Pool.terminate()
