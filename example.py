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
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.post(url, data=json.dumps(query), auth=self.auth, verify=False, headers=headers).json()

    def sentences(self, sentences):
        url = self.url + '/jmat/sentence'
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

    def search_tweets(self, query, limit=10):
        url = self.url + '/search/tweet'
        query = {'query': query, 'limit': limit}
        return self.__get(url, query)
    
    def search_reply(self, query, limit=10):
        url = self.url + '/search/reply'
        query = {'query': query, 'limit': limit}
        return self.__get(url, query)

    def markov_chain(self, seed):
        url = self.url + '/tk/markov'
        query = {'surface': seed['norm_surface'], 'pos': seed['pos']}
        return self.__get(url, query)
    
    def rewrite_morph(self, file_name, morphs):
        url = self.url + '/tk/rewrite'
        query = {'rule': file_name, 'morphs': morphs}
        return self.__post(url, query)

api = API('https://52.68.75.108', 'secret', 'js2015cps')

print
print '文分割'
s = '日本語文字列を文単位で分割する。複数文を渡すと、文ごとに区切ってくれる。'
for sentence in  api.sentences(s)['sentences']:
    print sentence


print
print 'ツイート検索'
print '=' * 20
for text in api.search_tweets('検索')['texts']:
    print text

print
print 'リプライ検索'
print '=' * 20
for text in api.search_reply('検索')['texts']:
    print text

print
print 'マルコフ連鎖'
print '=' * 20
seed = {'norm_surface': "今日", 'pos': "名詞"}
for morph in  api.markov_chain(seed)['morphs']:
    print morph,

# エラーが出る。。
print
print '書き換え'
print '=' * 20
morphs = ['BOS:BOS', '私:代名詞', 'EOS:EOS']
for morph in api.rewrite_morph('rule_test.txt', morphs)['morphs']:
    print morph

# エラーが出る。。。
print api.tweet('ツイートテスト! ')
print api.get_reply()
