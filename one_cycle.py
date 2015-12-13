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
        if '名詞' in morph['pos']:
            seed = morph
            break
    else:
        seed = morphs[0]
    return seed


def twitter_based(text):
    seed = preprocess(text) 

def reply_one(mention_id, user_name, text):
    reply_text = twitter_based(text)
    

if __name__ == '__main__':
    api = get_api()

    # メンションの取得
    result = api.get_reply()
    current_state = result['grade']
    replies = result['replies']
    
    # すべてのメンションに対して返信
    for reply in replies:
        reply_one(reply['mention_id'], reply['user_name'], reply['text'])


