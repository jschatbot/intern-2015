# -*- coding: utf-8 -*-

import requests
import json


class API:
    def __init__(self, url, usr, passwd):
        self.url = url
        self.auth = (usr, passwd)
        if usr is None:
            self.auth = None

    def __get(self, url, query, raw=False):
        result = requests.get(url, params=query, auth=self.auth, verify=False)
        if raw:
            return result
        return result.json()

    def __post(self, url, query, raw=False):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        result = requests.post(url, data=json.dumps(query), auth=self.auth, verify=False, headers=headers)
        if raw:
            return result
        return result.json()

    def sentences(self, sentences):
        url = self.url + '/jmat/sentence'
        query = {'query': sentences}
        return self.__get(url, query)

    def morph(self, sentence):
        url = self.url + '/jmat/morph'
        query = {'query': sentence}
        return self.__get(url, query)

    def chunk(self, sentence):
        url = self.url + '/jmat/chunk'
        query = {'query': sentence}
        return self.__get(url, query)

    def synonym(self, sentence):
        url = self.url + '/jmat/synonym'
        query = {'query': sentence}
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

    def search_reply(self, query, limit=10):
        url = self.url + '/search/reply'
        query = {'query': query, 'limit': limit}
        return self.__get(url, query)

    def markov_chain(self, seed):
        url = self.url + '/tk/markov'
        query = {'surface': seed['norm_surface'], 'pos': seed['pos']}
        return self.__get(url, query)

    def rewrite_morph(self, file_name, morphs, raw=False):
        url = self.url + '/tk/rewrite'
        query = {'rule': file_name, 'morphs': morphs}
        return self.__post(url, query, raw)

    def trigger(self, filename ,morphs):
        url = self.url + '/tk/trigger'
        query = {'rule': filename, 'morphs': morphs }
        return self.__post(url, query)

    def send_reply(self, mention_id, user_name, message):
        url = self.url + '/tweet/send_reply'
        name = 'js_devbot04'
        morphs = self.morph(message)
        s = ''
        for morph in morphs['morphs']:
            if morph['pos']=='BOS':
                continue
            if morph['pos']=='EOS':
                continue
            if len(s + morph['surface'])>120:
                query = {'bot_name': name, 'replies': [{ 'mention_id': mention_id, 'user_name': user_name, 'message': s } ] }
                self.__post(url, query)
                s = morph['surface']
        query = {'bot_name': name, 'replies': [{ 'mention_id': mention_id, 'user_name': user_name, 'message': s } ] }
        return self.__post(url, query)
