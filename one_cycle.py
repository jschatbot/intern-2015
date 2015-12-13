# -*- coding: utf-8 -*-
"""
exec one cycle of chatbot

Usage:
    one_cycle.py [--dev]

Option:
    -h, --help
        Show this screen
    -v, --version
        Show version
    --dev
        use development environment
"""

from docopt import docopt
import api


def get_api():
    args = docopt(__doc__)

    if args['--dev']:
        url = 'https://52.68.75.108'
        usr = 'secret'
        paswd = 'js2015cps'
    else:
        url = 'http://10.243.251.70'
        usr = None
        paswd = None

    return api.API(url, usr, paswd)


def preprocess(text):
    #TODO とりあえず最初の文の最初の名詞を利用, なければ最初の形態素
    sentences = api.sentences(text)['sentences']
    morphs = api.morph(sentences[0])['morphs']
    for morph in morphs:
        if u'名詞' in morph['pos']:
            seed = morph
            break
    else:
        seed = morphs[1]
    return seed['norm_surface']


def twitter_based(text):
    seed = preprocess(text) 
    
    # TODO とりあえずツイート検索結果の最初のツイートを利用
    tweet_example = api.search_tweets(seed, limit=1)
    # 空ならNoneを返す
    if tweet_example['count'] == 0:
        return None
    
    # TODO とりあえず先頭の文を利用
    # 形態素列書き換え
    sent = api.sentences(tweet_example['texts'][0])['sentences'][0]
    morphs = api.morph(sent)['morphs']
    query = list()
    for morph in morphs:
        query.append(u'{}:{}'.format(morph['norm_surface'], morph['pos']))
    morphs = api.rewrite_morph(rewrite_rule, query)['morphs']
    
    reply_text = u''
    for morph in morphs:
        reply_text += u':'.join(morph.split(u':')[:-1])
    return reply_text
    

def reply_one(mention_id, user_name, text):
    reply_text = twitter_based(text)
    api.send_reply(mention_id, user_name, reply_text)
    

if __name__ == '__main__':
    api = get_api()

    # メンションの取得
    result = api.get_reply()
    current_state = result['grade']
    replies = result['replies']

    rewrite_rule = 'team2_rewrite_{}.txt'.format(current_state)
    rewrite_rule = 'rule_test.txt'

    # すべてのメンションに対して返信
    for reply in replies:
        reply_one(reply['mention_id'], reply['user_name'], reply['text'])

    if len(replies) == 0:
        print twitter_based(u'こんにちは')

