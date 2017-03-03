import requests
from bs4 import BeautifulSoup
import re
import json



class Tag:
    def __init__(self, pair):
        self.pair = pair

    def __lt__(self, other):
        if self.pair.word != other.pair.word:
            return self.pair.word < other.pair.word
        if self.pair.flag != other.pair.flag:
            return self.pair.flag < other.pair.flag
        return False



# from app.app import redis_store
import math
from collections import defaultdict
import pickle


def get_all_names():
    r = requests.get('https://wiki.52poke.com/zh-hant/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89/%E7%AE%80%E5%8D%95%E7%89%88')
    # return r

    soup = BeautifulSoup(r.text, 'lxml')
    x = soup.find_all('table', 'a-c')
    y = x[0].find_all('tr')
    #f = open('pokemon_data', 'a')
    
    ret = {}
    for i in range(3, len(y)):
        z = y[i].find_all('td')
        if len(z) == 4:
            # is pokemon
            seq = z[0].text.strip() #1
            chinese = z[1].text.strip() #2 
            japanese = z[2].text.strip() #3
            english = z[3].text.strip().lower() #4
            ret[int(seq[1:])] = english


    #blahlafile = open('app/data/pokemon_names_mapping', 'wb')
    #pickle.dump(ret, blahlafile)
    #blahlafile.close()
    return ret



def tfidf():
    nt = defaultdict(int)
    tfidf = defaultdict(float)
    tlist = defaultdict(list)
    darklist = defaultdict(list)
    N = 0
    for i in range(1, 802+1):
        N += 1
        f = open('app/data/pokemon_dir/%03d.out' %i, 'r')
        print("first pass, i=%d" % i)
        for line in f:
            v = line.split(",")
            freq = int(v[0])
            term = v[1].strip()
            # log normalization
            tfidf[(i, term)] = 1.0 + math.log(freq)
            nt[term] += 1
        f.close()


    pkmnnames = get_all_names()

    for i in range(1, 802+1):
        f = open('app/data/pokemon_dir/%03d.out' %i, 'r')
        print("second pass, i=%d" % i)
        doclist = []
        for line in f:
            v = line.split(",")
            freq = int(v[0])
            term = v[1].strip()
            # inverse document frequency
            tfidf[(i, term)] *= math.log(N / float(nt[term]))
            tlist[term].append((i, tfidf[(i, term)]))
            doclist.append((tfidf[(i, term)], term))
            
            #redis_store.set('pkmn:%03d:%s' % (i, term), str(freq))
        doclist.sort(reverse=True)
        doclist = doclist[0:10]
        darklist[pkmnnames[i]] = doclist

    
    darklistfile = open('app/data/pokemon_doc_freq', 'wb')
    pickle.dump(darklist, darklistfile)
    darklistfile.close()

    reverseindex = open('app/data/pokemon_reverse_index', 'wb')
    pickle.dump(tlist, reverseindex)
    reverseindex.close()


    print("tlist size = %d" % len(tlist))
    #for term, v in tlist.items():
        #pass
        #redis_store.set('pkmn:inverse_document_count:%s' %(term), str(nt[term]))
        #redis_store.set('pkmn:term:%s' % (term), pickle.dumps(v))

    


import jieba
import jieba.posseg as pseg
jieba.set_dictionary("app/data/dict.txt.big")

import zhon.hanzi
import string
def bag_of_words():
    stopwords = [" ", "\n", "，", "。", "的", "\t"]
    for i in range(1, 802+1):
        # for i in range(1, 802+1):
        f = open('app/data/pokemon_dir/%03d' % i, 'r')
        text = f.read()
        soup = BeautifulSoup(text, 'lxml')
        tags = list(pseg.cut(soup.text))
        tags = list(filter(lambda x: x.word not in zhon.hanzi.punctuation and \
                x.word not in stopwords and \
                x.word not in string.punctuation, tags))
        #print("\n".join(map(lambda x: x.__repr__(), tags)))
        
        term_freq = defaultdict(int)
        for x in tags:
            term_freq[x.word] += 1
       
        term_freq = [(v, k) for k, v in term_freq.items()]
        term_freq.sort(reverse=True)
        output = map(lambda x: "%d, %s" % (x[0], x[1]), term_freq)
        #output = map(lambda x: "%s: %d" % (x[0], int(x[1])), list(term_freq))
        w = "\n".join(output)
        fout = open('app/data/pokemon_dir/%03d.out' % i, 'w')
        fout.write(w)
        fout.write('\n')
        fout.close()
        f.close()
        print("#%03d OK... %d Terms" % (i, len(term_freq)))
        





def get_page():
    r = requests.get('https://wiki.52poke.com/zh-hant/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89/%E7%AE%80%E5%8D%95%E7%89%88')
    # return r

    soup = BeautifulSoup(r.text, 'lxml')
    x = soup.find_all('table', 'a-c')
    y = x[0].find_all('tr')
    #f = open('pokemon_data', 'a')
    
    for i in range(3, len(y)):
        z = y[i].find_all('td')
        if len(z) == 4:
            # is pokemon
            seq = z[0].text.strip() #1
            chinese = z[1].text.strip() #2 
            japanese = z[2].text.strip() #3
            english = z[3].text.strip().lower() #4
            print("Parsing %s: %s ... " % (seq, chinese))
            pic_url = None

            try:
                req = requests.get("https://wiki.52poke.com/zh-hant/File:%s%s.png" % (seq[1:], z[3].text.strip()))
                s2 = BeautifulSoup(req.text, 'lxml')
                pic = list(filter(lambda x: 'png' in x.attrs.get('title', ''), s2.find_all('a')))
                pic_url = pic[0].attrs.get('href') #5
            except:
                pass

            
            desc = None
            try:
                req = requests.get("https://wiki.52poke.com/zh-hant/%s" % (chinese))
                thefile = open("app/data/pokemon_dir/%s" % seq[1:], 'w')
                thefile.write(req.text)
                thefile.write("\n")
                thefile.close()

                s2 = BeautifulSoup(req.text, 'lxml')
                tmp = s2.find_all('span', class_='mw-headline', string=re.compile('(外貌)'))
                desc = tmp[0].parent.find_next('p').text #6
            except Exception as e:
                print("\033[0;31m%s\033[m" % e)

            v = json.dumps({
                'seq': seq,
                'chinese': chinese,
                'japanese': japanese,
                'english': english,
                'image': pic_url,
                'desc': desc
                })
            print("\033[1;30m%s\033[m" % desc)

            #f.write(v)
            #f.write('\n')

    #f.close()
