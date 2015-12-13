# -*- coding: utf-8 -*-

import api

api = api.API('https://52.68.75.108', 'secret', 'js2015cps')

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
