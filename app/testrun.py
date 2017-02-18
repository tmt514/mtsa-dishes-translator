import urllib.request 
import urllib.parse
from secrets import GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_CX

import json

#result = search('pizza wiki 中文')

from bs4 import BeautifulSoup


def google_search(term="妙蛙種子"):
    v = "q=%s&key=%s&cx=%s" % (urllib.parse.quote_plus(term), GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_CX)
    url = "https://www.googleapis.com/customsearch/v1?" + v
    print(url)
    try:
        req = urllib.request.Request(url)
        f = urllib.request.urlopen(req)
        response = f.read()
        f.close()
        return response
    except Exception as e:
        print(e)
        return None
    

if __name__ == "__main__":
    f = open('testfile', 'r')
    lines = f.read()
    f.close()

    r = json.loads(lines)
    items = r['items']
    hp = [x['pagemap'] for x in items if 'pagemap' in x]

    print(json.dumps(hp, indent=4))
    


#cnt = 0
#for x in result:
#    print(x)
#    if 'wikipedia' in x:
#        x = str(x)
#        v = urllib.parse.unquote(x)
#        v = v.split('/')[-1]
#        url = "http://zh.wikipedia.org/zh-tw/" + urllib.parse.quote_plus(v)
#        print(url)
#        w = get_page(url)
#        soup = BeautifulSoup(w, 'lxml')
#        print(soup.title.string)
#        break
#
#    cnt += 1
#    if cnt>= 10:
#        break

#req = urllib.request.Request(url)
#f = urllib.request.urlopen(req)
#response = f.read()
#parser.feed(str(response))
#f.close()

