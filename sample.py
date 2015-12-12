# -*- coding: utf-8 -*-

import requests

class API:
    def __init__(self, url, usr, passwd):
        self.url = url
        self.auth = (usr, passwd)

    def __get(self, url, query):
        return requests.get(url, params=query, auth=self.auth, verify=False).json()

    def __post(self, url, query):
        return requests.post(url, params=query, auth=self.auth, verify=False).json()

## FROM HERE
    def trigger(self, filename ,morphs):
        url = self.url + '/tk/trigger'
        quary = {'rule': filename, 'morphs': morphs }
        return self.__post(url, query)

    def get_reply(self):
        url = self.url + '/tweet/get_reply'
        name = 'js_devbot04'
        query = {'bot_name': name}
        return self.__get(url, query)

    def send_tweet(self, message):
        url = self.url + '/tweet/simple'
        name = 'js_devbot04'
        query = {'bot_name': name, 'message': message}
        return self.__post(url, query)

    def send_reply(self, mention_id, user_name, message):
        url = self.url + '/tweet/send_reply'
        name = 'js_devbot04'
        query = {'bot_name': name, 'replies': [{ 'mention_id': mention_id, 'user_name': user_name, 'message': message } ] }
        return self.__post(url, query)

api = API('https://52.68.75.108', 'secret', 'js2015cps')
#s = '日本語文字列を文単位で分割する。複数文を渡すと、文ごとに区切ってくれる。'
#print api.sentences(s).text
#print api.morphs(s).text
#seed = {'norm_surface': "私", 'pos': "名詞"}
#print api.markov_chain(seed).text
print api.send_tweet("js_devbot04","this is test tweet.").text
