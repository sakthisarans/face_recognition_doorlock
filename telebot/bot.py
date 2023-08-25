import telebot
import time,sys,os
import sqlite3
import hashlib
import reset as re
import dateandtime as dtm


sys.path.insert(0,'/home/pi/cam/gpiocontrol')
import pincontrol

sys.path.insert(1,'/home/pi/cam/data')
import datagenerator as dg

sys.path.insert(2,'/home/pi/cam/recogniser/train')
import Dnn_train as dt
import lbp_trainer as lt

sys.path.insert(3,'/home/pi/cam')
import db_manager as dbm



API = '5748811622:AAFo4bq4Jn1D43TtD2FV3lf8UoOdxveTYsE'
bot = telebot.TeleBot(API)
name=''

@bot.message_handler(commands='start')
def bot_status(msg):

    txt = msg.from_user.first_name
    if(msg.from_user.id==5363178087):
        # print("start")
        bot.reply_to(msg, "welcome "+txt+"\n"
                     "bot is up and running")
    else:
        bot.reply_to(msg, "you have no access to the system")


@bot.message_handler(commands='help')
def help(msg):
    # print('helped')
    bot.reply_to(msg,"/lock to lock the door\n"
                     "/unlock to unlock the door\n"
                     "/start to chrck the status of the bot\n"
                     "/check_users to check the existant user\n"
                    "/add_user to add new user\n"
                    "/delete_user delete existing user\n"
                    "/pwd_update update default password\n"
                    "/factory_reset wipe entire system\n"
                    "/history to check the past 10 visitor records")


@bot.message_handler(commands='lock')
def lock_status(msg):

    if (msg.from_user.id == 5363178087):
        print("lock")
        pincontrol.relayoff()
        bot.reply_to(msg, "locked at "+dtm.find_time())
    else:
        bot.reply_to(msg, "you have no access to the system")


@bot.message_handler(commands='unlock')
def unlock_status(msg):
    if (msg.from_user.id == 5363178087):
        print("unlock")
        pincontrol.relayon()
        bot.reply_to(msg, "unlocked at "+dtm.find_time())
        time.sleep(20)
        print("locked")
        pincontrol.relayoff()
        bot.reply_to(msg, "locked at"+ dtm.find_time())
        dbm.updater('unknown', 'user-authenticated')
    else:
        bot.reply_to(msg, "you have no access to the system")

@bot.message_handler(commands='check_users')
def check_users(msg):
    if (msg.from_user.id == 5363178087):
        val=os.listdir('/home/pi/cam/data/images')
        out=""
        for i in val:
            out=out+i+'\n'
        bot.reply_to(msg, out+'are the existing users')
    else:
        bot.reply_to(msg, "you have no access to the system")

@bot.message_handler(commands='add_user')
def add_users(msg):
    if (msg.from_user.id == 5363178087):
        bot.reply_to(msg, "enter your name - password:")
        bot.register_next_step_handler(msg,add)
        
    else:
        bot.reply_to(msg, "you have no access to the system")

def add(msg):
    name=(msg.text).split('-')
    # print(name)
    conn = sqlite3.connect('/home/pi/cam/telebot/login.db')
    try:
        o=conn.execute(f"select password from login where password='{name[1]}'")
    except Exception as ex:
        print(ex)
    
    
    if(o.fetchone()):
        if(dg.datagenerator(name[0])):
            bot.reply_to(msg, "user added")
        else:
           bot.reply_to(msg, "something wrong") 
    else:
        bot.reply_to(msg, "enter valid credential")
    conn.close()

@bot.message_handler(commands='delete_user')
def delete_user(msg):
    if (msg.from_user.id == 5363178087):
        bot.reply_to(msg, "enter user name for deletion-password:")
        # print(msg.text)
        bot.register_next_step_handler(msg,delete)
    else:
        bot.reply_to(msg, "you have no access to the system")

def delete(msg):
    name=(msg.text).split('-')
    # print(name)
    conn = sqlite3.connect('/home/pi/cam/telebot/login.db')
    try:
        o=conn.execute(f"select password from login where password='{name[1]}'")
    except Exception as ex:
        print(ex)
    if(o.fetchone()):
        os.system(f'rm -r /home/pi/cam/data/images/{name[0]}')
        bot.reply_to(msg, "user removed successfully and system is recalibrating") 
        if(dt.train() and lt.train()):
            bot.send_message(msg.from_user.id, "system recalibrated")
        else:
            bot.send_message(msg.from_user.id, "something went wrong")
    else:
        bot.reply_to(msg, "enter valid credential")
    conn.close()


@bot.message_handler(commands='pwd_update')
def pwd_update(msg):
    if (msg.from_user.id == 5363178087):
        bot.reply_to(msg,"enter existing password and new password separated by hifen:")
        bot.register_next_step_handler(msg,updt)
    else:
        bot.reply_to(msg, "you have no access to the system")
def updt(msg):
    text=msg.text
    text=text.split('-')
    print(text)
    try:
        if(text[0]!=text[1]):
            #newpwd=hashlib.sha256(text[1].encode())
            #print(str(newpwd.hexdigest()))
            conn = sqlite3.connect('/home/pi/cam/telebot/login.db')
            # print()
            try:
                o=conn.execute(f"UPDATE login set password='{text[1]}' where password='{text[0]}'")
                conn.commit()
                if(o.rowcount==1):
                    bot.reply_to(msg,"updated successfully")
                else:
                    bot.reply_to(msg,"enter valid password")
                # print(o.rowcount)
            except Exception as ew:
                print(ew)
            conn.close()
        else:
            bot.reply_to(msg,"both pwd must be different")
    except Exception as ex:
        print(ex)

@bot.message_handler(commands='factory_reset')
def factory_reset(msg):
    if (msg.from_user.id == 5363178087):
        bot.reply_to(msg, "enter your confirm - password:")
        bot.register_next_step_handler(msg,rest)
    else:
        bot.reply_to(msg, "you have no access to the system")

def rest(msg):
    name=(msg.text).split('-')
    # print(name)
    
    try: 
        conn = sqlite3.connect('/home/pi/cam/telebot/login.db')
        o=conn.execute(f"select password from login where password='{name[1]}'")
        
    except Exception as ex:
        print(ex)

    bol=o.fetchone()
    conn.close()
    if(bol and name[0]=='confirm'):
        if(re.reset()):
            bot.reply_to(msg, "system completely wiped")
        else:
            bot.reply_to(msg, "something went wrong")
    else:
        bot.reply_to(msg, "enter valid credential")
    
@bot.message_handler(commands='history')
def history(msg):
    if (msg.from_user.id == 5363178087):
        conn=sqlite3.connect('/home/pi/cam/telebot/history.db')
        o=conn.execute('select * from history order by ROWID desc LIMIT 7')
        o=o.fetchall()
        out=''
        for i in o:
            out=out+f'{i[0]}    {i[1]}    {i[2]}    {i[3]}\n'
        conn.close()

        bot.reply_to(msg, out)
        
    else:
        bot.reply_to(msg, "you have no access to the system")






@bot.message_handler(func=lambda m: True)
def repeat(msg):
    if((msg.text).lower() == 'help'):
        help(msg)
    elif((msg.text).lower() == 'start'):
        bot_status(msg)
    elif ((msg.text).lower() == 'lock'):
        lock_status(msg)
    elif ((msg.text).lower() == 'unlock'):
        unlock_status(msg)
    elif ((msg.text).lower() == 'check_users'):
        check_users(msg)
    elif ((msg.text).lower() == 'add_user'):
        add_users(msg)
    elif ((msg.text).lower() == 'pwd_update'):
        pwd_update(msg)
    elif ((msg.text).lower() == 'delete_user'):
        delete_user(msg)
    elif ((msg.text).lower() == 'factory_reset'):
        factory_reset(msg)
    elif ((msg.text).lower() == 'history'):
        history(msg)
    elif ((msg.text).lower() == 'i love you'):
        bot.reply_to(msg,"love you to")
    else:
        bot.send_message(msg.chat.id,"invalid command i'm just a bot for access control please provide valid command linke\n\n"
                                     "/start\n"
                                     "/lock\n"
                                     "/unlock\n"
                                     "/help\n"
                                     "/check_users\n"
                                     "/add_user\n"
                                     "/delete_user\n"
                                     "/pwd_update\n"
                                     "/factory_reset\n"
                                     "/history")
try:
    bot.polling(none_stop=True)

except Exception as e:
    time.sleep(15)



