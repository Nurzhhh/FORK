import datetime
import sqlite3
import requests
import urllib3
import re 
from bs4 import BeautifulSoup
import textdistance
import time
urllib3.disable_warnings()
from gtts import gTTS 
import os 
import csv
import telebot
tb = telebot.TeleBot('1025277727:AAGKOX9qGF0mw_Cry--3ufdMQ3RGq50Qv3Y')
#import BET

def for_in_every_element(a):
    b=c.execute('select * from FORK')
    for i in b.fetchall():
        cnt=0
        for x in range(16):
            if a[x]==i[x]:
                cnt+=1
        if cnt>7:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Already exist')
            return False
    return True

def compare(ans,a):
        print('comparing started!')
        b=c.execute('select * from FORK')
        f = True
        f = for_in_every_element(a)
        return f
        
def compare_and_insert(ans):
    for a in ans:
        f = compare(ans,a)
        print('comparing succesfull!')

        print('inserting started!')
        if f == True:
            c.execute('''INSERT INTO FORK (data, time,league, opp1, opp2, bet1, coef1_bet1, coef2_bet1, bet2, coef1_bet2, coef2_bet2, win_opp1, percent_of_your_money_for_win_opp1, profit1, win_opp2, percent_of_your_money_for_win_opp2, profit2) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13], a[14], a[15],a[16]))  
            conn.commit()
            c.execute('''INSERT INTO FIND (data, time,league, opp1, opp2, bet1, coef1_bet1, coef2_bet1, bet2, coef1_bet2, coef2_bet2, win_opp1, percent_of_your_money_for_win_opp1, profit1, win_opp2, percent_of_your_money_for_win_opp2, profit2) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13], a[14], a[15],a[16]))
        conn.commit()
        print(" ")
        print('inserting succesfull!')

def get_coefficients(a,bet1,op1):
    coef1 = ''
    coef2 = ''
    if bet1 == a[5]:
        print('bet1==a[5]:')
        if op1 == (a[3]+' '):
            print('op1==a[3]')
            coef1 += a[6]
            coef2 += a[10]
        elif op1 == (a[4]+' '):
            print('op1==a[4]')
            coef1 += a[7]
            coef2 += a[9]
    elif bet1 == a[8]:
        print('bet2==a[8]:')
        if op1 == (a[3]+' '):
            print('op1==a[3]')
            coef1 += a[9]
            coef2 += a[7]
        elif op1 == (a[4]+' '):
            print('op1==a[4]')
            coef1 += a[10]
            coef2 += a[6]   
    return coef1,coef2 

def float_of_degree_three(a):
    a = format(float(a.replace('%','')),'.3f')
    return a

import mutagen
from mutagen.mp3 import MP3
def creating_and_sending_audio(l):
    
    text = '''На букмекере {b1}, надо ставить на команду - {opp1} под каэффицентом {c1}, ставить строго {p1} процентов от твоих общих денег,
     а затем На букмекере {b2}, надо ставить на команду - {opp2} под каэффицентом {c2}, ставить строго {p2} процентов от твоих общих денег'''.format(b1=bet1,opp1=op1,p1=p11,b2=bet2,
                                                                                                                        opp2=op2,p2=p22,c1=coef1,c2=coef2)
    language = 'ru'
    myobj = gTTS(text = text, lang=language, slow=False) 
    myobj.save(os.getcwd()+"\\audio\{date}_{time}_{opp1}_{opp2}_{c1}_{c2}.mp3".format(date=a[0],time=a[1].replace(':','-'),
                                                                        opp1=op1.strip(),opp2=op2.strip(),p2=p22,c1=coef1,c2=coef2))
    voice = open(os.getcwd()+'\\audio\\{date}_{time}_{opp1}_{opp2}_{c1}_{c2}.mp3'.format(date=a[0],time=a[1].replace(':','-'),
                                                                        opp1=op1.strip(),opp2=op2.strip(),p2=p22,c1=coef1,c2=coef2), 'rb')
    audio = MP3(os.getcwd()+'\\audio\\{date}_{time}_{opp1}_{opp2}_{c1}_{c2}.mp3'.format(date=a[0],time=a[1].replace(':','-'),
                                                                        opp1=op1.strip(),opp2=op2.strip(),p2=p22,c1=coef1,c2=coef2))
    audio_info = audio.info    
    length_in_secs = int(audio_info.length)
    import json

    c=tb.send_voice(chat_id='@BET_BUSTERS', voice=voice,duration=length_in_secs)
    return c.message_id

def deleting_audio(l):
    os.remove(os.getcwd()+'\\audio\\{date}_{time}_{opp1}_{opp2}_{c1}_{c2}.mp3'.format(date=a[0],time=a[1].replace(':','-'),
                                                                        opp1=op1.strip(),opp2=op2.strip(),p2=p22,c1=coef1,c2=coef2))

def getting_emoji(c):
    from emoji import emojize
    zero = emojize(":zero:", use_aliases=True)
    one = emojize(":one:", use_aliases=True)
    two = emojize(":two:", use_aliases=True)
    three = emojize(":three:", use_aliases=True)
    four = emojize(":four:", use_aliases=True)
    five = emojize(":five:", use_aliases=True)
    six = emojize(":six:", use_aliases=True)
    seven = emojize(":seven:", use_aliases=True)
    eight = emojize(":eight:", use_aliases=True)
    nine = emojize(":nine:", use_aliases=True)
    trophy = emojize(":trophy:", use_aliases=True)
    if 0 <= c < 1:
        text = zero
    if 1 <= c < 2:
        text = one
    if 2 <= c < 3:
        text = two
    if 3 <= c < 4:
        text = three
    if 4 <= c < 5:
        text = four
    if 5 <= c < 6:
        text = five
    if 6 <= c < 7:
        text = six
    if 7 <= c < 8:
        text = seven
    if 8 <= c < 9:
        text = eight
    if 9 <= c < 10:
        text = nine
    if 10 <= c:
        text = trophy
    
    return text

global csvfile
csvfile = []

from telebot import types
def make_keyboard(bet1,bet2):
    markup = types.InlineKeyboardMarkup()

    if bet1=='1xBET':
        link1='https://m.1xbet.kz/line/Esports/'
    elif bet1=='OLIMPBET':
        link1='https://olimpbet.kz/betting/cybersport'
    elif bet1=='FONBET':
        link1='https://www.fonbet.kz/esports/disciplines/all'

    if bet2=='1xBET':
        link2='https://m.1xbet.kz/line/Esports/'
    elif bet2=='OLIMPBET':
        link2='https://olimpbet.kz/betting/cybersport'
    elif bet2=='FONBET':
        link2='https://www.fonbet.kz/esports/disciplines/all'
    
    markup.add(types.InlineKeyboardButton(text=bet1,
                                                url=link1),
               types.InlineKeyboardButton(text=bet2,
                                                url=link2))

    return markup

while True:
    try:
        if (datetime.datetime.now().minute * 0 == 0):
            conn = sqlite3.connect('FOR.db')
            c = conn.cursor()
            c.execute('delete from FIND')
            conn.commit()
            import BET
            ans = BET.find()
            compare_and_insert(ans)
            
            text = None
            token = "1025277727:AAGKOX9qGF0mw_Cry--3ufdMQ3RGq50Qv3Y"
            url = "https://api.telegram.org/bot%s/sendMessage" % token
            op1 = ''
            op2 = ''
            b=c.execute('select * from FIND')

            for a in b.fetchall():
                m=a[11].split()        
                n=a[14].split()
                bet1=m[0]
                bet2=n[0]
                op1=''
                op2=''

                p11 =    float_of_degree_three(a[12])
                p22 =    float_of_degree_three(a[15])
                proff1 = float_of_degree_three(a[13])
                proff2 = float_of_degree_three(a[16])

                for i in range(1,len(m)):
                    op1+=m[i]
                    op1+=' '
                for i in range(1,len(n)):
                    op2+=n[i]
                    op2+=' '

                coef1, coef2 = get_coefficients(a,bet1,op1)

                print()
                text = getting_emoji(round(float(proff1)))+'% profit\n'
                text+='''
........................................\n
Date: {date}.20 - {time}
    {opp1} vs {opp2}
    league: {leag}

                Bet1: {b1}
                Team1: {opp1}
                coef1: {c1}
                cash: {p1}%
                profit:{prof1}%

                Bet2: {b2}
                Team2: {opp2}
                coef2: {c2}
                cash: {p2}%
                profit: {prof2}% '''.format(leag=a[2],date=a[0],time=a[1],b1=bet1,
                                            opp1=op1,p1=p11,b2=bet2,opp2=op2,p2=p22,
                                            prof1=proff1,prof2=proff2,c1=coef1,c2=coef2)

                l=[a[0],a[1],a[2],bet1,op1,coef1,p11,proff1,bet2,op2,coef2,p22,proff2]
                print(l)
                csvfile.append(l)

                voice_msg_id=creating_and_sending_audio(l)
                deleting_audio(l)
                
                tb.send_message(chat_id='@BET_BUSTERS', text = text,reply_to_message_id=voice_msg_id,reply_markup=make_keyboard(bet1,bet2))

                getting_emoji(round(float(proff1)))
            conn.commit()
            conn.close()
        
        import csv
        with open('csvfile.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(csvfile)

        print('DONE!')
    except:
        print('something goes wrong')

