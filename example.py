# -*- coding: utf-8 -*-

import requests

class API:
    def __init__(self, url, usr, passwd):
        self.url = url
        self.auth = (usr, passwd)

    def sentences(self, sentences):
        url = '/jmat/sentence'
        query = {'query': sentences}
        return requests.get(self.url + url, params=query, auth=self.auth, verify=False)

api = API('https://52.68.75.108', 'secret', 'js2015cps')
s = '日本語文字列を文単位で分割する。複数文を渡すと、文ごとに区切ってくれる。'
print api.sentences(s).text

