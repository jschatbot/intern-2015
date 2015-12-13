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

import random
import json

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

if __name__ == '__main__':
    api = get_api()

    reps = api.get_reply()
    print json.dumps(reps, ensure_ascii=False, indent = 4)

    

    for rep in reps['replies']:
        print '======================================================'
        if reps['grade'] == 0:
            scenario_file = 'scenario_c09.txt'
        elif reps['grade'] == 1:
            scenario_file = 'scenario_c09.txt'
        else :
            scenario_file = 'scenario_c09.txt'
        sent = api.sentences(rep['text'])
        text = []
        for s in sent['sentences']:
            print '-------------------------------------------------------'
            print s
            morphs = api.morph(s)
            print json.dumps(morphs, ensure_ascii=False, indent = 4)
            query = list()
            for morph in morphs['morphs']:
                query.append(u'{}:{}'.format(morph['surface'], morph['pos']))
            print json.dumps(query, ensure_ascii=False, indent = 4)
            texts = api.trigger(scenario_file,query)
            print json.dumps(texts, ensure_ascii=False, indent = 4)
            for t in texts['texts']:
                text.append(t)
                print t
        if len(text)>0:
            r = random.randint(0,len(text)-1)
            print '++++++++++++++++++++++++++++++++++++++'
            print str(len(text))
            print text[r]
            api.send_reply(rep['mention_id'],rep['user_name'],text[r])