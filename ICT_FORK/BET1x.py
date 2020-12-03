# turnir team1 team2 data uakyty p1 p2   C:\Users\user\AppData\Local\Programs\Python\Python38\Scripts\
import requests
import urllib3
import json
from bs4 import BeautifulSoup
import time
import re
urllib3.disable_warnings()
def go():
    xurl = "https://m.1xbet.kz/line/Esports/"

    xr = requests.get(xurl, verify = False)
    xhtml = xr.text
    xsoup = BeautifulSoup(xhtml, "html.parser")
    BETturnir = xsoup.select('.events__item')
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    stopwords = ['team', 'esports', 'e-sports', "Gaming"]

    xiterable = []
    for item in BETturnir:
        item = str(item).replace('\n', '').strip()
        if str(item).count('<div class="coef__item coef__name">') == 2 and str(item).count('<div class="events__team">') == 2 and str(item).find('X') == -1 and item.find('<div class="events__team">') != -1 and item.find('</div><div class="events__divider">') != -1:
            l1 = item.find('<div class="events__team">')
            r1 = item.find('</div><div class="events__divider">')
            # print(l1, r1)
            opp1 = item[l1+26:r1].strip()
            l2 = item.rfind('<div class="events__team">')
            r2 = item.find('</div></div></div></div><div class="events__cell_line events__cell_right">')
            opp2 = item[l2+26:r2].strip()
            l3 = item.find('<div class="events__time events__time_sec events__text events__text_small events__text_shade">')
            r3 = item.find('</div><div class="events__time events__time_sec events__text events__text_small events__text_shade"></div>')
            data = item[l3+94:r3]
            # kun = data.split(' ')[0]
            # uakyt = data.split(' ')[1]
            m = re.findall(":[0-5][0-9]", str(data))
            mm = re.findall("[0-5][0-9]", str(m))
            h = re.findall("[0-5][0-9]:", str(data))
            hh = re.findall("[0-5][0-9]", str(h))
            d = re.findall("[0-5][0-9].", str(data))
            dd = re.findall("[0-5][0-9]", str(d))
            n = re.findall(".[0-5][0-9]", str(data))
            nn = re.findall("[0-5][0-9]", str(n))
            # print(hh[0])
            mmm = (int(mm[0]))
            ddd = (int(dd[0]))
            hhh = (int(hh[0]) + 6)
            nnn = int(nn[0])
            if hhh >= 24:
                hhh = (hhh) % 24
                ddd = ddd + 1
            else:
                hhh = hhh
                ddd = ddd 
            #print(ddd,nnn,hhh,mmm)
            if mmm < 10:
                minut = "0" + str(mmm)
            else:
                minut = str(mmm)
            if ddd < 10:
                day = "0" + str(ddd)
            else:
                day = str(ddd)  
            if hhh < 10:
                hour = "0" + str(hhh)
            else:
                hour = str(hhh)        
            if nnn < 10:
                month = "0" + str(nnn)
            else:
                month = str(nnn)      
            kun = str(day) + '.' + str(month)
            uakyt = str(hour) + ':' + str(minut)
            l4 = item.find('<div class="coef__item coef__name">П1</div><a class="coef__item coef__num" href="javascript:void(0)">')
            r4 = item.find('</a></div><div class="js-coef coef" data-betname="П2"')
            l5 = item.find('<div class="coef__item coef__name">П2</div><a class="coef__item coef__num" href="javascript:void(0)">')
            r5 = item.find('</a></div> </div></li>')
            coef1 = item[l4 + 101:r4]
            coef2 = item[l5 + 101:r5]
            if isfloat(coef1) and isfloat(coef2):
                # for i in stopwords:
                #     opp1.replace(i, '').strip()
                #     opp2.replace(i, '').strip()
                xiterable.append([kun.strip(), uakyt.strip(), 'Cybersport', opp1.strip(), opp2.strip(), 'П1', coef1.strip(), 'П2', coef2.strip()])

    import csv
    with open('1xBET.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(xiterable)


    import sqlite3

    conn = sqlite3.connect('FOR.db')
    c = conn.cursor()
    c.execute('delete from BET1x')

    for a in xiterable:
        c.execute('''INSERT INTO BET1x (date,time,ligues,opp1,opp2,coef1,coef2) VALUES(?,?,?,?,?,?,?)''',(a[0],a[1],a[2],a[3],a[4],a[6],a[8]))
        conn.commit()