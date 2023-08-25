import telebot

API = '5748811622:AAFo4bq4Jn1D43TtD2FV3lf8UoOdxveTYsE'
bot = telebot.TeleBot(API)

def warning_sender(warning,img_list):
    for i in img_list:
        bot.send_photo(chat_id, open(i,'rb'))
    bot.send_message('5363178087', warning)
    
