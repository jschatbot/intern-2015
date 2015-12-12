# -*- coding: utf-8 -*-

import requests
import json

class API:
    def __init__(self, url, usr, passwd):
        self.url = url
        self.auth = (usr, passwd)

    def __get(self, url, query):
        return requests.get(url, params=query, auth=self.auth, verify=False).json()
    
    def __post(self, url, query):
        return requests.post(url, params=query, auth=self.auth, verify=False).json()

    def sentences(self, sentences):
        url = self.url + '/jmat/sentence'
        query = {'query': sentences}
        return self.__get(url, query)

    def morph(self, sentence):
        url = self.url + '/jmat/morph'
        query = {'query': sentences}
        return self.__get(url, query)

    def chunk(self, sentence):
        url = self.url + '/jmat/chunk'
        query = {'query': sentences}
        return self.__get(url, query)

    def synonym(self, sentence):
        url = self.url + '/jmat/synonym'
        query = {'query': sentences}
        return self.__get(url, query)

    def tweet(self, message):
        url = self.url + '/tweet/simple'
        name = 'js_devbot04'
        query = {'bot_name': name, 'message': message}
        return self.__post(url, query)

    def get_reply(self):
        url = self.url + '/tweet/get_reply'
        name = 'js_devbot04'
        query = {'bot_name': name}
        return self.__get(url, query)

    def search_tweets(self, query, limit=10):
        url = self.url + '/search/tweet'
        query = {'query': query, 'limit': limit}
        return self.__get(url, query)

    def markov_chain(self, seed):
        url = self.url + '/tk/markov'
        query = {'surface': seed['norm_surface'], 'pos': seed['pos']}
        return self.__get(url, query)

api = API('https://52.68.75.108', 'secret', 'js2015cps')

s = '日本語文字列を文単位で分割する。複数文を渡すと、文ごとに区切ってくれる。'
for sentence in api.sentences(s)['sentences']:
    print sentence

for text in api.search_tweets('検索')['texts']:
    print text

seed = {'norm_surface': "今日", 'pos': "名詞"}
for morph in  api.markov_chain(seed)['morphs']:
    print morph,

# エラーが出る。。。
#print api.tweet('ツイートテスト! ')
#print api.get_reply()
