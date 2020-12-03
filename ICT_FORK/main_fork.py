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
import BET

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



#l=[a[0],a[1],a[2],bet1,op1,coef1,p11,proff1,bet2,op2,coef2,p22,proff2]
def strict_table(l):
    date=l[0]
    time=l[1]
    league=l[2]
    bet1=l[3]
    op1=l[4]
    coef1=l[5]
    p11=l[6]
    proff1=l[7]
    bet2=l[8]
    op2=l[9]
    coef2=l[10]
    p22=l[11]
    proff2=l[12]
    full_len=0
    len_col1=0
    len_col1=0
    text='''
Date: {date}.20 - {time}

{opp1} vs {opp2}
league: {leag}
<pre>
|    |'''.format(date=date,time=time,opp1=op1,opp2=op2,leag=league)


    if len(bet1)>len(op1):
        text+=bet1+'|'
        len_col1=len(bet1)
    else:
        
        for i in range(len(op1)-len(bet1)):
            text+=' '
        text+='<i>'+bet1+'</i>'
        text+='|'
        len_col1=len(op1)

    if len(bet2)>len(op2):
        text+='<i>'+bet2+'</i>|'
        len_col2=len(bet2)
    else:
        
        for i in range(len(op2)-len(bet2)):
            text+=' '
        text+=bet2
        text+='|\n|'
        len_col2=len(op2)

    full_len=8+len_col1+len_col2+2
    for i in range(full_len-4):
        text+='-'
    text+='|\n'
        
    text+='|<i>Team</i>|'

    
    for i in range(len_col1-len(op1)):
        text+=' '
    text+=op1
    text+='|'

    
    for i in range(len_col2-len(op2)):
        text+=' '
    text+=op2
    text+='|'

    text+='\n|'
    for i in range(full_len-4):
        text+='-'
    text+='|\n'



    text+='|<i>coef</i>|'

    
    for i in range(len_col1-len(coef1)):
        text+=' '
    text+=coef1
    text+='|'

    
    for i in range(len_col2-len(coef2)):
        text+=' '
    text+=coef2
    text+='|'

    text+='\n|'

    for i in range(full_len-4):
        text+='-'
    text+='|\n'

    text+='|<i>cash</i>|'

    
    for i in range(len_col1-len(p11)-1):
        text+=' '
    text+=p11
    text+='%|'

    
    for i in range(len_col2-len(p22)-1):
        text+=' '
    text+=p22
    text+='%|'
    text+='\n|'
    for i in range(full_len-4):
        text+='-'
    text+='|\n'

    '''text+='|<i>profit</i>|'

    
    for i in range(len_col1-len(proff1)):
        text+=' '
    text+=proff1
    text+='|'

    
    for i in range(len_col2-len(proff2)):
        text+=' '
    text+=proff2
    text+='|'

    text+=' ''' #\n

    text+='</pre>'

    return text

while True:
    try:
        if (datetime.datetime.now().minute * 0 == 0):
            conn = sqlite3.connect('FOR.db')
            c = conn.cursor()
            c.execute('delete from FIND')
            conn.commit()
            
            BET.bets()
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

                l=[a[0],a[1],a[2],bet1,op1,coef1,p11,proff1,bet2,op2,coef2,p22,proff2]

                voice_msg_id=creating_and_sending_audio(l)
                deleting_audio(l)

                text = getting_emoji(round(float(proff1)))+'% profit\n........................................\n'
                if (len(op1)+len(op2))>0:
                    print(len(op1)+len(op2))
                    text+='''
Date: {date}.20 - {time}

{opp1} vs {opp2}
league: {leag}

*Bet1:* _{b1}_
*Team1:* _{opp1}_
*coef1:* _{c1}_
*cash:* _{p1}%_
*profit:*_{prof1}%_

*Bet2:* _{b2}_
*Team2:* _{opp2}_
*coef2:* _{c2}_
*cash:* _{p2}%_
*profit:* _{prof2}%_ '''.format(leag=a[2],date=a[0],time=a[1],b1=bet1,
                                            opp1=op1,p1=p11,b2=bet2,opp2=op2,p2=p22,
                                            prof1=proff1,prof2=proff2,c1=coef1,c2=coef2)
                    tb.send_message(chat_id='@BET_BUSTERS', text = text,reply_markup=make_keyboard(bet1,bet2),parse_mode='Markdown')
                else:
                    print(len(op1)+len(op2))
                    text += strict_table(l)
                    tb.send_message(chat_id='@BET_BUSTERS', text = text,reply_markup=make_keyboard(bet1,bet2),parse_mode='HTML')
                print(text)
                print(l)
                csvfile.append(l)
            conn.commit()
            conn.close()
        
        import csv
        with open('csvfile.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(csvfile)

        print('DONE!')
        #break
    except:
        #break
        print('Something goes wrong')

