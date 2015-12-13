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
    max_length = 0
    for sentence in api.sentences(text)['sentences']:
        morphs = api.morph(sentence)['morphs']
        for morph in morphs:
            if u'固有' in morph['pos'] or u'名詞' in morph['pos']:
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
    seed = generate_seed(text)
    # TODO とりあえずツイート検索結果の最初のツイートを利用
    tweet_example = api.search_tweets(seed['norm_surface'], limit=1)
    # 空ならNoneを返す
    if tweet_example['count'] == 0:
        return None
    # TODO とりあえず先頭の文を利用
    # 形態素列書き換え
    sent = api.sentences(tweet_example['texts'][0])['sentences'][0]
    return postprocess(sent)

def markov_based(text):
    seed =  generate_seed(text)
    reply_text = u''
    for morph in api.markov_chain(seed)['morphs'][1:-1]:
        reply_text += u':'.join(morph.split(u':')[:-1])#morph.split(':')[0]
    return postprocess(reply_text)

def reply_one(mention_id, user_name, text):
    reply_text = twitter_based(text)
    api.send_reply(mention_id, user_name, reply_text)

if __name__ == '__main__':
    #api = get_api()
    api = api.API('https://52.68.75.108', 'secret', 'js2015cps')
    #rewrite_rule = 'team2_rewrite_{}.txt'.format(current_state)
    rewrite_rule = 'rule_test.txt'
    text = "どうして人間は魂の在処にこだわるの？"
    for morph in api.morph(text)['morphs']:
        print morph['norm_surface'] + "\t" + morph['pos']
    print markov_based(text)
    print twitter_based(text)

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
