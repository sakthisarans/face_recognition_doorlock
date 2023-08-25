from threading import Thread
import os,time

class myClass():

    def recogniser(self):
        os.system('python /home/pi/cam/cam_manager.py ')
    def bot(self):
        os.system('python3 /home/pi/cam/telebot/bot.py ')
        print('bot')


if __name__=='__main__':
    Yep = myClass()
    thread1 = Thread(target = Yep.recogniser)
    thread2 = Thread(target = Yep.bot)
    thread1.start()
    thread2.start()
  
    time.sleep(10)
        
