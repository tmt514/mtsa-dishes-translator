import urllib.request 
import urllib.parse
from html.parser import HTMLParser
from google import search, get_page

class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        print("Data     :", data)



parser = MyHTMLParser()
result = search('pizza wiki 中文')

from bs4 import BeautifulSoup

cnt = 0
for x in result:
    print(x)
    if 'wikipedia' in x:
        x = str(x)
        v = urllib.parse.unquote(x)
        v = v.split('/')[-1]
        url = "http://zh.wikipedia.org/zh-tw/" + urllib.parse.quote_plus(v)
        print(url)
        w = get_page(url)
        soup = BeautifulSoup(w, 'lxml')
        print(soup.title.string)
        break

    cnt += 1
    if cnt>= 10:
        break

#req = urllib.request.Request(url)
#f = urllib.request.urlopen(req)
#response = f.read()
#parser.feed(str(response))
#f.close()

