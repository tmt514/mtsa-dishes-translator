import requests
from bs4 import BeautifulSoup
import re
import json

def get_page():
    r = requests.get('https://wiki.52poke.com/zh-hant/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89/%E7%AE%80%E5%8D%95%E7%89%88')
    # return r

    soup = BeautifulSoup(r.text, 'lxml')
    x = soup.find_all('table', 'a-c')
    y = x[0].find_all('tr')
    f = open('pokemon_data', 'a')
    
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
                s2 = BeautifulSoup(req.text, 'lxml')
                tmp = s2.find_all('span', class_='mw-headline', string=re.compile('((習性)|(性情))'))
                desc = tmp[0].parent.find_next('p').text #6
            except:
                pass

            v = json.dumps({
                'seq': seq,
                'chinese': chinese,
                'japanese': japanese,
                'english': english,
                'image': pic_url,
                'desc': desc
                })
            print("\033[1;30m%s\033[m" % desc)

            f.write(v)
            f.write('\n')

    f.close()
