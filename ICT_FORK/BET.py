import requests
import urllib3
import re 
import json
from bs4 import BeautifulSoup
import textdistance
import time
urllib3.disable_warnings()
import sqlite3
import BET1x
import FONBET
import OLIMP
def bets():
    BET1x.go()
    FONBET.go()
    OLIMP.go()

def find():
    ans = []

    conn = sqlite3.connect('FOR.db')
    c = conn.cursor()
    #c.execute('delete from FORK')
    conn.commit()

    BET1x = c.execute('select * from BET1x')

    for i in BET1x.fetchall():
        # print('ok')
        xdata = i[0]
        xuakity = i[1]
        xopp1 = i[3]
        xopp2 = i[4]
        xbet = xdata + ',' + xuakity + ',' + xopp1 + ',' + xopp2
        xp1 = i[5]
        xp2 = i[6]
        OLIMP = c.execute('select * from OLIMPBET')
        for o in OLIMP.fetchall():
            odata = o[0]
            otime = o[1]
            league = o[2]
            oopp1 = o[3]
            oopp2 = o[4]
            obet = odata + ',' + otime + ',' + oopp1 + ',' + oopp2
            obet2 = odata + ',' + otime + ',' + oopp2 + ',' + oopp1
            op1 = o[5]
            op2 = o[6]
            uksastik = textdistance.jaro_winkler(xbet.lower().strip(), obet.lower().strip())
            uksastik2 = textdistance.jaro_winkler(xbet.lower().strip(), obet2.lower().strip())
            if uksastik >= 0.97 and uksastik > uksastik2:
                print('1xBET - OLIMPBET', end=' ')
                print(xbet, end=' ')
                print(obet, end=' ')
                print(uksastik, end=' ')
                print(uksastik2, end=' ')
                orta1 = 1/float(xp1) + 1/float(op2)
                orta2 = 1/float(op1) + 1/float(xp2) 
                if (1/float(xp1) + 1/float(op2) < 1.0) or (1/float(op1) + 1/float(xp2) < 1.0):
                    print("Yes", end=' ')
                    print(obet)
                    print('--------------------------------------------')
                    if (1/float(xp1) + 1/float(op2) < 1.0) and (1/float(xp1) + 1/float(op2) < (1/float(xp2) + 1/float(op1))):
                        A1 = (1 / float(xp1) / orta1) * 100
                        A1 = int(float(A1) * 1000) / 1000
                        ans.append([odata, otime, league, oopp1, oopp2, '1xBET', xp1, xp2, 'OLIMPBET', op1, op2, '1xBET ' + xopp1, str(A1) + '%', str(float(A1) * float(xp1) - 100) + '%', 'OLIMPBET ' + oopp2, str(100 - A1) + '%', str(float(100 - A1) * float(op2) - 100) + '%'])
                    elif (1/float(xp2) + 1/float(op1) < 1.0) and (1/float(xp2) + 1/float(op1) < (1/float(xp1) + 1/float(op2))):
                        A2 = (1 / float(op1) / orta2) * 100
                        A2 = int(float(A2) * 1000) / 1000
                        ans.append([odata, otime, league, oopp1, oopp2, '1xBET', xp1, xp2, 'OLIMPBET', op1, op2, 'OLIMPBET ' + oopp1, str(A2) + '%', str(float(A2) * float(op1) - 100) + '%', '1xBET ' + xopp2, str(100 - A2) + '%', str(float(100 - A2) * float(xp2) - 100) + '%'])
                else:
                    print("No")    
            elif uksastik < uksastik2 and uksastik2 >= 0.97:
                print('1xBET - OLIMPBET', end=' ')
                print(xbet, end=' ')
                print(obet, end=' ')
                print(uksastik, end=' ')
                print(uksastik2, end=' ')
                orta1 = 1/float(xp1) + 1/float(op1)
                orta2 = 1/float(op2) + 1/float(xp2) 
                if (1/float(xp1) + 1/float(op1) < 1.0) or (1/float(op2) + 1/float(xp2) < 1.0):
                    print("Yes", end=' ')
                    print(obet2)
                    print('--------------------------------------------')
                    if (1/float(xp1) + 1/float(op1) < 1.0) and (1/float(xp1) + 1/float(op1) < (1/float(xp2) + 1/float(op2))):
                        A1 = (1 / float(xp1) / orta1) * 100
                        A1 = int(float(A1) * 1000) / 1000
                        ans.append([odata, otime, league, oopp1, oopp2, '1xBET', xp1, xp2, 'OLIMPBET', op1, op2, '1xBET ' + xopp1, str(A1) + '%', str(float(A1) * float(xp1) - 100) + '%', 'OLIMPBET ' + oopp1, str(100 - A1) + '%', str(float(100 - A1) * float(op1) - 100) + '%'])
                    elif (1/float(xp2) + 1/float(op2) < 1.0) and (1/float(xp2) + 1/float(op2) < (1/float(xp1) + 1/float(op1))):
                        A2 = (1 / float(op2) / orta2) * 100
                        A2 = int(float(A2) * 1000) / 1000
                        ans.append([odata, otime, league, oopp1, oopp2, '1xBET', xp1, xp2, 'OLIMPBET', op1, op2, 'OLIMPBET ' + oopp2, str(A2) + '%', str(float(A2) * float(op2) - 100) + '%', '1xBET ' + xopp2, str(100 - A2) + '%', str(float(100 - A2) * float(xp2) - 100) + '%'])
                else:
                    print("No") 
            else:
                continue


    BET1x = c.execute('select * from BET1x')
    for i in BET1x.fetchall():
        xdata = i[0]
        xuakity = i[1]
        xopp1 = i[3]
        xopp2 = i[4]
        xbet = xdata + ',' + xuakity + ',' + xopp1 + ',' + xopp2
        xp1 = i[5]
        xp2 = i[6]
        # print('ok')
        FONBET = c.execute('select * from FONBET') 
        for o in FONBET.fetchall():
            odata = o[0]
            otime = o[1]
            league = o[2]
            oopp1 = o[3]
            oopp2 = o[4]
            obet = odata + ',' + otime + ',' + oopp1 + ',' + oopp2
            obet2 = odata + ',' + otime + ',' + oopp2 + ',' + oopp1
            op1 = o[5]
            op2 = o[6]
            uksastik = textdistance.jaro_winkler(xbet.lower().strip(), obet.lower().strip())
            uksastik2 = textdistance.jaro_winkler(xbet.lower().strip(), obet2.lower().strip())
            if uksastik > uksastik2 and uksastik >= 0.97:
                print('1xBET - FONBET', end=' ')
                print(xbet, end=' ')
                print(obet, end=' ')
                print(uksastik, end=' ')
                print(uksastik2, end=' ')
                orta1 = 1/float(xp1) + 1/float(op2)
                orta2 = 1/float(op1) + 1/float(xp2) 
                if (1/float(xp1) + 1/float(op2) < 1.0) or (1/float(op1) + 1/float(xp2) < 1.0):
                    print("Yes", end=' ')
                    print(obet)
                    print('--------------------------------------------')
                    if (1/float(xp1) + 1/float(op2) < 1.0) and (1/float(xp1) + 1/float(op2) < (1/float(xp2) + 1/float(op1))):
                        A1 = (1 / float(xp1) / orta1) * 100
                        A1 = int(float(A1) * 1000) / 1000
                        ans.append([odata, otime, league, oopp1, oopp2, '1xBET', xp1, xp2, 'FONBET', op1, op2, '1xBET ' + xopp1, str(A1) + '%', str(float(A1) * float(xp1) - 100) + '%', 'FONBET ' + oopp2, str(100 - A1) + '%', str(float(100 - A1) * float(op2) - 100) + '%'])
                    elif (1/float(xp2) + 1/float(op1) < 1.0) and (1/float(xp2) + 1/float(op1) < (1/float(xp1) + 1/float(op2))):
                        A2 = (1 / float(op1) / orta2) * 100
                        A2 = int(float(A2) * 1000) / 1000
                        ans.append([odata, otime, league, oopp1, oopp2, '1xBET', xp1, xp2, 'FONBET', op1, op2, 'FONBET ' + oopp1, str(A2) + '%', str(float(A2) * float(op1) - 100) + '%', '1xBET ' + xopp2, str(100 - A2) + '%', str(float(100 - A2) * float(xp2) - 100) + '%'])
                    print("Yes")
                else:
                    print(xbet, end=' ')
                    print(obet, end=' ')
                    print("No")    
            else:
                if uksastik < uksastik2 and uksastik2 >= 0.97:
                    print('1xBET - FONBET', end=' ')
                    print(xbet, end=' ')
                    print(obet, end=' ')
                    print(uksastik, end=' ')
                    print(uksastik2, end=' ')
                    orta1 = 1/float(xp1) + 1/float(op1)
                    orta2 = 1/float(op2) + 1/float(xp2) 
                    if (1/float(xp1) + 1/float(op1) < 1.0) or (1/float(op2) + 1/float(xp2) < 1.0):
                        print("Yes", end=' ')
                        print(obet2)
                        print('--------------------------------------------')
                        if (1/float(xp1) + 1/float(op1) < 1.0) and (1/float(xp1) + 1/float(op1) < (1/float(xp2) + 1/float(op2))):
                            A1 = (1 / float(xp1) / orta1) * 100
                            A1 = int(float(A1) * 1000) / 1000
                            ans.append([odata, otime, league, xopp1, xopp2, '1xBET', xp1, xp2, 'FONBET', op1, op2, '1xBET ' + xopp1, str(A1) + '%', str(float(A1) * float(xp1) - 100) + '%', 'FONBET ' + oopp1, str(100 - A1) + '%', str(float(100 - A1) * float(op1) - 100) + '%'])
                        elif (1/float(xp2) + 1/float(op2) < 1.0) and (1/float(xp2) + 1/float(op2) < (1/float(xp1) + 1/float(op1))):
                            A2 = (1 / float(op2) / orta2) * 100
                            A2 = int(float(A2) * 1000) / 1000
                            ans.append([odata, otime, league, xopp1, xopp2, '1xBET', xp1, xp2, 'FONBET', op1, op2, 'FONBET ' + oopp2, str(A2) + '%', str(float(A2) * float(op2) - 100) + '%', '1xBET ' + xopp2, str(100 - A2) + '%', str(float(100 - A2) * float(xp2) - 100) + '%'])
                    else:
                        print("No")    
                else:
                    continue

    FONBET = c.execute('select * from FONBET')
    for i in FONBET.fetchall():
        xdata = i[0]
        xuakity = i[1]
        xopp1 = i[3]
        xopp2 = i[4]
        xbet = xdata + ',' + xuakity + ',' + xopp1 + ',' + xopp2
        xp1 = i[5]
        xp2 = i[6]
        OLIMP = c.execute('select * from OLIMPBET')
        for o in OLIMP.fetchall():
            # print('ok')
            odata = o[0]
            otime = o[1]
            league = o[2]
            oopp1 = o[3]
            oopp2 = o[4]
            obet = odata + ',' + otime + ',' + oopp1 + ',' + oopp2
            obet2 = odata + ',' + otime + ',' + oopp2 + ',' + oopp1
            op1 = o[5]
            op2 = o[6]
            uksastik = textdistance.jaro_winkler(xbet.lower().strip(), obet.lower().strip())
            uksastik2 = textdistance.jaro_winkler(xbet.lower().strip(), obet2.lower().strip())
            if uksastik > uksastik2 and uksastik >= 0.97:
                print('FONBET - OLIMPBET', end=' ')
                print(xbet, end=' ')
                print(obet, end=' ')
                print(uksastik, end=' ')
                print(uksastik2, end=' ')
                orta1 = 1/float(xp1) + 1/float(op2)
                orta2 = 1/float(op1) + 1/float(xp2) 
                if (1/float(xp1) + 1/float(op2) < 1.0) or (1/float(op1) + 1/float(xp2) < 1.0):
                    print("Yes", end=' ')
                    print(obet)
                    print('--------------------------------------------')
                    if (1/float(xp1) + 1/float(op2) < 1.0) and (1/float(xp1) + 1/float(op2) < (1/float(xp2) + 1/float(op1))):
                        A1 = (1 / float(xp1) / orta1) * 100
                        A1 = int(float(A1) * 1000) / 1000
                        ans.append([odata, otime, league, oopp1, oopp2, 'FONBET', xp1, xp2, 'OLIMPBET', op1, op2, 'FONBET ' + xopp1, str(A1) + '%', str(float(A1) * float(xp1) - 100) + '%', 'OLIMPBET ' + oopp2, str(100 - A1) + '%', str(float(100 - A1) * float(op2) - 100) + '%'])
                    elif (1/float(xp2) + 1/float(op1) < 1.0) and (1/float(xp2) + 1/float(op1) < (1/float(xp1) + 1/float(op2))):
                        A2 = (1 / float(op1) / orta2) * 100
                        A2 = int(float(A2) * 1000) / 1000
                        ans.append([odata, otime, league, oopp1, oopp2, 'FONBET', xp1, xp2, 'OLIMPBET', op1, op2, 'OLIMPBET ' + oopp1, str(A2) + '%', str(float(A2) * float(op1) - 100) + '%', 'FONBET ' + xopp2, str(100 - A2) + '%', str(float(100 - A2) * float(xp2) - 100) + '%'])
                else:
                    print("No")    
            if uksastik < uksastik2 and uksastik2 >= 0.97:
                print('FONBET - OLIMPBET', end=' ')
                print(xbet, end=' ')
                print(obet, end=' ')
                print(uksastik, end=' ')
                print(uksastik2, end=' ')
                orta1 = 1/float(xp1) + 1/float(op1)
                orta2 = 1/float(op2) + 1/float(xp2) 
                if (1/float(xp1) + 1/float(op1) < 1.0) or (1/float(op2) + 1/float(xp2) < 1.0):
                    print("Yes", end=' ')
                    print(obet2)
                    print('--------------------------------------------')
                    if (1/float(xp1) + 1/float(op1) < 1.0) and (1/float(xp1) + 1/float(op1) < (1/float(xp2) + 1/float(op2))):
                        A1 = (1 / float(xp1) / orta1) * 100
                        A1 = int(float(A1) * 1000) / 1000
                        ans.append([odata, otime, league, oopp1, oopp2, 'FONBET', xp1, xp2, 'OLIMPBET', op1, op2, 'FONBET ' + xopp1, str(A1) + '%', str(float(A1) * float(xp1) - 100) + '%', 'OLIMPBET ' + oopp1, str(100 - A1) + '%', str(float(100 - A1) * float(op1) - 100) + '%'])
                    elif (1/float(xp2) + 1/float(op2) < 1.0) and (1/float(xp2) + 1/float(op2) < (1/float(xp1) + 1/float(op1))):
                        A2 = (1 / float(op2) / orta2) * 100
                        A2 = int(float(A2) * 1000) / 1000
                        ans.append([odata, otime, league, oopp1, oopp2, 'FONBET', xp1, xp2, 'OLIMPBET', op1, op2, 'FONBET ' + xopp2, str(A2) + '%', str(float(A2) * float(xp2) - 100) + '%', 'OLIMPBET ' + oopp2, str(100 - A2) + '%', str(float(100 - A2) * float(op2) - 100) + '%'])
                else:
                    print("No")    
            else:
                continue
        # time.sleep(1)

    print(ans)
    import csv
    with open('FORK.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(ans)
    
    return ans


# for a in ans:
#     c.execute('''INSERT INTO FORK (data, time, league, opp1, opp2, bet1, coef1_bet1, coef2_bet1, bet2, coef1_bet2, coef2_bet2, win_opp1, percent_of_your_money_for_win_opp1, profit1, win_opp2, percent_of_your_money_for_win_opp2, profit2) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13], a[14], a[15], a[16]))
#     conn.commit()
# conn.close()
# print('ok')