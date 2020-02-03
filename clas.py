from datetime import datetime
from threading import Thread
from scipy.spatial import distance
import telebot
import cv2
import sqlite3
from dependence import token

bot = telebot.TeleBot(token)

class MyThread(Thread):
    def __init__(self, arg1, arg2, arg3, arg4, arg5, arg6):
        Thread.__init__(self)
        self.arg1 = arg1 
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4
        self.chatId = arg5
        if arg6 == 0: self.q = 'photo'
        else: self.q = arg6
        self.ch = 0

    def run(self):
        #Сounters
        counterOfName=0
        isFaceFound=0
        for det in self.arg2['val']:
            try:
                titleName = self.arg2['name'][counterOfName].split('\\')[1].split('.')[0]
            except:
                titleName = self.arg2['name'][counterOfName]
            counterOfName=counterOfName+1
            a = distance.euclidean(det, self.arg1)
            if a < 0.55:
                conn = sqlite3.connect("db/mydatabase.db")  # или :memory: чтобы сохранить в RAM
                cursor = conn.cursor()
                photoPatn = cursor.execute("SELECT photoPath FROM Faces WHERE id = ?", [(titleName)]).fetchone()[0]
                info = cursor.execute("SELECT title FROM Faces WHERE id = ?", [(titleName)]).fetchone()[0]
                conn.close()
                if self.q == 'photo':
                    now = datetime.now()
                    print("ВИЯВЛЕНО:....Дата: " + now.strftime("%d-%m-%Y %H:%M") + " Прiзвище особи -", info)
                    bot.send_photo(self.chatId, open(photoPatn, "rb"), now.strftime("%d-%m-%Y %H:%M") + " Прiзвище особи - " + info)
                    cv2.imwrite('find\\' + now.strftime("%d-%m-%Y %H.%M") + " Name-" + photoPatn.split('\\')[1], self.arg4)
                    if isFaceFound == 0: isFaceFound = 1
                else:
                    self.q.put([info, photoPatn])
                break
        if isFaceFound == 0 and self.q == 'photo':
            bot.send_message(self.chatId, "Обличчя не знайдено в базі")
            print("Обличчя не знайдено в базі")

