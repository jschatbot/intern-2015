# -*- coding: utf-8 -*-

import requests

class API:
    def __init__(self, url, usr, passwd):
        self.url = url
        self.auth = (usr, passwd)

    def sentences(self, sentences):
        url = '/jmat/sentence'
        query = {'query': sentences}
        return requests.get(self.url + url, params=query, auth=self.auth, verify=False).json()

    def tweet(self, message):
        url = '/tweet/simple'
        name = 'js_devbot04'
        query = {'bot_name': name, 'message': message}
        return requests.post(self.url + url, params=query, auth=self.auth, verify=False).json()

    def get_reply(self):
        url = '/tweet/get_reply'
        name = 'js_devbot04'
        query = {'bot_name': name}
        return requests.get(self.url + url, params=query, auth=self.auth, verify=False).json()

    def search_tweets(self, query, limit=10):
        url = '/search/tweet'
        query = {'query': query, 'limit': limit}
        return requests.get(self.url + url, params=query, auth=self.auth, verify=False).json()


api = API('https://52.68.75.108', 'secret', 'js2015cps')

s = '日本語文字列を文単位で分割する。複数文を渡すと、文ごとに区切ってくれる。'
for sentence in  api.sentences(s)['sentences']:
    print sentence

for text in api.search_tweets('検索')['texts']:
    print text

# エラーが出る。。。
#print api.tweet('ツイートテスト! ')
#print api.get_reply()
