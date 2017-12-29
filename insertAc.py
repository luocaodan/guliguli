# -*- coding: utf-8 -*-

import requests

def test():
    data = {}
    data['cont'] = u'二次元萌什么?'
    data['d_release'] = '2018-1-1'
    data['img'] = '/static/image/596loyx0vk.png'
    r = requests.post('http://127.0.0.1:5000/api/insertActivity', data=data)
    print r.text

if __name__ == '__main__':
    test()