# -*- coding: utf-8 -*-

import requests

auth = ('secret', 'js2015cps')
url = 'https://52.68.75.108'

query = {'query': '日本語文字列を文単位で分割する。複数文を渡すと、文ごとに区切ってくれる。'}
res = requests.get(url + '/jmat/sentence', auth=auth, params=query, verify=False)
print res.text


query = {'query': '日本語文字列を形態素（単語）単位で分割する。複数文を渡すと、文ごとに区切ってくれる。'}
res = requests.get(url + '/jmat/morph', auth=auth, params=query, verify=False)
print res.text

