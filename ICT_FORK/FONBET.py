import requests
import urllib3
import json
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def go():
    fonurl ='https://line01.kz-resources.com/line/mobile/showEvents?lineType=line&lang=ru&skId=29086&skId=40479&skId=40480&skId=40481&skId=44943&skId=45827'
    fonr = requests.get(fonurl,verify=False)
    data = fonr.json()

    stopwords = ['team', 'esports', 'e-sports', "Gaming"]

    FONBET=[]
    for i in data['events']:
        if i.get('skName') == 'Киберспорт' and i.get('kind') == 1 and i.get('rootKind') == 1 and i.get('skId') == 29086 and i.get('parentId') == 0 and i.get('team1') != 'Первый фраг в 1 раунде' and i.get('team1') != 'Будет ли овертайм' and i.get('team1') != 'Тип победы в 1 раунде' and i.get('team1') != 'Тотал фрагов':
            opp1 = i.get('team1')
            opp2 = i.get('team2')
            data = i.get('startTime')
            league = str(i.get('sportName'))
            league = league[12:len(league) - 13]
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
            hhh = (int(hh[0]) + 3)
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
            x = i.get('subcategories')
            if x == None:
                continue
            for j in x:
                if j['num'] == 1 and len(j['quotes']) == 2:
                    coef1 = j['quotes'][0]['value']
                    coef2 = j['quotes'][1]['value']
            print(kun, end=' ')
            print(uakyt, end=' ')
            print(opp1, end=' ')
            print(opp2, end=' ')
            print(coef1, end=' ')
            print(coef2)
            # for i in stopwords:
            #     opp1.replace(i, '').strip()
            #     opp2.replace(i, '').strip()
            FONBET.append([kun, uakyt, league, opp1, opp2, 'П1', coef1, 'П2', coef2])

    import csv
    with open('FONBET.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(FONBET)


    import sqlite3

    conn = sqlite3.connect('FOR.db')
    c = conn.cursor()
    c.execute('delete from FONBET')
    for a in FONBET:
        c.execute('''INSERT INTO FONBET (date,time,ligues,opp1,opp2,coef1,coef2) VALUES(?,?,?,?,?,?,?)''',(a[0],a[1],a[2],a[3],a[4],a[6],a[8]))
        conn.commit()