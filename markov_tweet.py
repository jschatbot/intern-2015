# -*- coding: utf-8 -*-

__doc__ = """{f}
exec one cycle of chatbot
Usage:
    markov_tweet.py [--dev]
Option:
    -h, --help
        Show this screen
    -v, --version
        Show version
    --dev
        use development environment
""".format(f=__file__)

import api
from docopt import docopt
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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

def generate_seed(text):
    #TODO とりあえず最初の文の最初の名詞を利用, なければ最初の形態素
    sentences = api.sentences(text)['sentences']
    morphs = api.morph(sentences[0])['morphs']
    for morph in morphs:
        if '固有名詞' in morph['pos']:
            seed = morph
            break
    else:
        seed = morphs[1]
    return seed

def preprocess(text):
    #TODO とりあえず最初の文の最初の名詞を利用, なければ最初の形態素
    sentences = api.sentences(text)['sentences']
    morphs = api.morph(sentences[0])['morphs']
    for morph in morphs:
        if '名詞' in morph['pos']:
            seed = morph
            break
    else:
        seed = morphs[1]
    return seed

def twitter_based(text):
    seed = preprocess(text)
    # TODO とりあえずツイート検索結果の最初のツイートを利用
    tweet_example = api.search_tweets(seed['norm_surface'], limit=1)
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
    for morph in morphs[1:-1]:
        reply_text += u':'.join(morph.split(u':')[:-1])
    return reply_text

def markov_based(text):
    seed =  generate_seed(text)
    sentence = ''
    for morph in api.markov_chain(seed)['morphs'][1:-1]:
        sentence += ':'.join(morph.split(':')[:-1])#morph.split(':')[0]
    return sentence

def reply_one(mention_id, user_name, text):
    reply_text = twitter_based(text)
    api.send_reply(mention_id, user_name, reply_text)

if __name__ == '__main__':
    #api = get_api()
    api = api.API('https://52.68.75.108', 'secret', 'js2015cps')
    #rewrite_rule = 'team2_rewrite_{}.txt'.format(current_state)
    rewrite_rule = 'rule_test.txt'
    text = "スペースシャトルはすごい"
    print markov_based(text)
    print twitter_based("今日")

#result = api.get_reply()
#current_state = result['grade']
#replies = result['replies']
#for sentence in api.sentences('おはよう。こんにちは。')['sentences']:
#    print sentence

#for tweet in api.get_reply()['replies']:
#    print tweet['mention_id']
#    print tweet['user_name']
#    print tweet['text']

#print '=' * 20
#for text in api.search_reply('おはよう',100)['texts']:
#    print text
#print

#print '=' * 20
#for text in api.search_tweets('おはよう',10)['texts']:
#    print text
#print
