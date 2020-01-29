from datetime import datetime
from threading import Thread
from scipy.spatial import distance
import telebot
from dependence import token

bot = telebot.TeleBot(token)

class MyThread(Thread):
    def __init__(self, arg1, arg2, arg3, arg4, arg5, arg7):
        Thread.__init__(self)
        self.arg1 = arg1 
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4
        self.chatId = arg5
        if arg7 == 0: self.q = 'photo'
        else: self.q = arg7
        self.ch = 0

    def run(self):
        #Сounters
        counterOfName=0
        isFaceFound=0

        for det in self.arg2['val']:
            titleName = self.arg2['name'][counterOfName].split('\\')[1].split('.')[0]
            counterOfName=counterOfName+1
            a = distance.euclidean(det, self.arg1)
            if a < 0.55:
                if self.q == 'photo':
                    now = datetime.now()
                    print("ОБНАРУЖЕННО:....Дата: " + now.strftime("%d-%m-%Y %H:%M") + " Прiзвище особи - " + titleName)
                    bot.send_photo(self.chatId, open('foto/' + titleName + ".jpg", "rb"), now.strftime("%d-%m-%Y %H:%M") + " Прiзвище особи - " + titleName )
                    if isFaceFound == 0: isFaceFound = 1
                else:
                    self.q.put(titleName)
                break

        if isFaceFound == 0 and self.q == 'photo':
            bot.send_message(self.chatId, "Лицо не найдено в базе")
            print("Лицо не найдено в базе")

