# -*- coding: utf-8 -*-
"""
exec one cycle of chatbot

Usage:
    on_cycle.py [--dev] [--term]

Option:
    -h, --help
        Show this screen
    -v, --version
        Show version
    --dev
        use development environment
    --term
        chatbot on your terminal
"""

import sys
import random
from docopt import docopt
import api


def get_api():
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
    for sentence in api.sentences(text)['sentences']:
        morphs = api.morph(sentence)['morphs']
        for morph in morphs:
            if u'名詞' in morph['pos']:
                seed = morph
                break
        else:
            seed = morphs[1]
    return seed


# 形態素列書き換え, こっちは文を受け取る
def postprocess(sent):
    morphs = api.morph(sent)['morphs']
    query = list()
    for morph in morphs:
        query.append(u'{}:{}'.format(morph['norm_surface'], morph['pos']))
    morphs = api.rewrite_morph(rewrite_rule, query)['morphs']
    
    sent = u''
    for morph in morphs[1:-1]:
        sent += u':'.join(morph.split(u':')[:-1])
    return sent


def twitter_based(text):
    seed = preprocess(text)['norm_surface']
    
    # TODO とりあえずツイート検索結果の最初のツイートを利用
    tweet_example = api.search_tweets(seed, limit=1)
    # 空ならNoneを返す
    if tweet_example['count'] == 0:
        return None
    
    # TODO とりあえず先頭の文を利用
    sent = api.sentences(tweet_example['texts'][0])['sentences'][0]
    return postprocess(sent)
    

def markov_based(text):
    seed =  preprocess(text)
    reply_text = u''
    for morph in api.markov_chain(seed)['morphs'][1:-1]:
        reply_text += u':'.join(morph.split(u':')[:-1])#morph.split(':')[0]
    return postprocess(reply_text)


def scenario_based(text):
    sent = api.sentences(text)
    text = []
    for s in sent['sentences']:
        morphs = api.morph(s)
        query = list()
        for morph in morphs['morphs']:
            query.append(u'{}:{}'.format(morph['surface'], morph['pos']))
    texts = api.trigger(scenario_file,query)
    for t in texts['texts']:
        text.append(t)
    if len(text)>0:
        r = random.randint(0,len(text)-1)
        return text[r]
    return ''


def reply_one(mention_id, user_name, text):
    reply_text1 = twitter_based(text)
    reply_text2 = markov_based(text)
    reply_text3 = scenario_based(text)
    api.send_reply(mention_id, user_name, 'tw:' + reply_text1)
    api.send_reply(mention_id, user_name, 'mv:' + reply_text2)
    api.send_reply(mention_id, user_name, 'sc:' + reply_text3)
    

if __name__ == '__main__':
    args = docopt(__doc__)
    api = get_api()

    # メンションの取得
    result = api.get_reply()
    current_state = result['grade']
    replies = result['replies']

    rewrite_rule = u'4_rewrite_grade{}.txt'.format(current_state)
    scenario_file = u'4_scenario_grade{}.txt'.format(current_state)
#    rewrite_rule = 'rewrite_c00.txt'
#    query = ['BOS:BOS', '私:代名詞', 'EOS:EOS']
#    print api.rewrite_morph(rewrite_rule, query, True).text

    if args['--term']:
        print 'chatbot on this terminal'
        print 'input your message'
        for line in iter(sys.stdin.readline, '\n'):
            line = line.strip()
            print 'twitter'
            print twitter_based(line.decode('utf-8'))
            print 'markov'
            print markov_based(line.decode('utf-8'))
            print 'scenario'
            print scenario_based(line.decode('utf-8'))
    else:
        # すべてのメンションに対して返信
        for reply in replies:
            reply_one(reply['mention_id'], reply['user_name'], reply['text'].strip())
