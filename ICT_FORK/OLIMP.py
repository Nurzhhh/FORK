# turnir team1 team2 data uakyty p1 p2   C:\Users\user\AppData\Local\Programs\Python\Python38\Scripts\
import requests
import urllib3
import json
from bs4 import BeautifulSoup
import time
urllib3.disable_warnings()
def go():
    url = "https://olimpbet.kz/mobile/index.php?page=line&action=1&time=0&line_nums=0&sel[]=6"
    r = requests.get(url, verify = False)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    OLIMPturnir = soup.select('.row2')
    HTTPOLIMP = 'https://olimpbet.kz/mobile/'

    stopwords = ['team', 'esports', 'e-sports', "Gaming"]

    OLIMP = []

    for item in OLIMPturnir:
        if len(item.text.strip()) > 0:
            league = item.text.strip()
        if item.get('href').strip() == '':
            continue
        turnirurl = HTTPOLIMP + item.get('href').strip()
        req = requests.get(turnirurl, verify = False)
        html1 = req.text
        tur = BeautifulSoup(html1, "html.parser")
        opp = tur.select('.col-xs-10')
        for oyin in opp:
            href = oyin['href']
            if oyin.get('href').strip() == '':
                continue
            oyinurl = HTTPOLIMP + href.strip()
            requ = requests.get(oyinurl, verify = False)
            html2 = requ.text
            karsylas = BeautifulSoup(html2, "html.parser")
            if karsylas.select('.small') != None and len(karsylas.select('.small')) > 0:
                data = karsylas.select('.small')[0].text
            if karsylas.select('.matchName') != None and len(karsylas.select('.matchName')) > 0:
                komanda = karsylas.select('.matchName')[0].text
            opp1 = komanda.split(' - ')[0].strip()
            opp2 = komanda.split(' - ')[1].strip()
            if len(data) > 0 and data.find(' ') != -1:
                uakity = data.split(' ')[1].strip()
            if len(data) > 0 and data.find(' ') != -1:
                data = data.split(' ')[0].strip()
            obet = data + uakity + opp1 + opp2
            print(obet)
            koef = karsylas.select('.odd')
            p = []
            ok = 0
            for i in koef:
                if i.get('data-event') == 'Ничья' or i.get('data-event') == 'П1 с форой (-1.5)':
                    ok = 1
                    p = []
                    break
                p.append(str(i.get('data-odd')))
                if len(p) == 2:
                    break
            if(komanda != 'Победитель 2019' and len(p) > 1 and ok == 0):
                if p[0] == 'None':
                    continue
                    p[0] = 1
                    opp1 = 'OLIMPBET'
                if p[1] == 'None':
                    continue
                    p[1] = 1
                    opp2 = 'OLIMPBET'
                # for i in stopwords:
                #     opp1.replace(i, '').strip()
                #     opp2.replace(i, '').strip()
                OLIMP.append([data[0:5], uakity, league, opp1, opp2, 'П1', p[0], 'П2', p[1]])
        # if(len(OLIMP) > 20):
        #     break
            # time.sleep(1)
        time.sleep(1)

    import csv
    with open('OLIMP.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(OLIMP)


    import sqlite3

    conn = sqlite3.connect('FOR.db')
    c = conn.cursor()
    c.execute('delete from OLIMPBET')
    for a in OLIMP:
        c.execute('''INSERT INTO OLIMPBET (date,time,ligues,opp1,opp2,coef1,coef2) VALUES(?,?,?,?,?,?,?)''',(a[0],a[1],a[2],a[3],a[4],a[6],a[8]))
        conn.commit()