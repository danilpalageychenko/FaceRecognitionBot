import cv2
import telegram_send
import sys
from datetime import datetime
from threading import Thread
from time import sleep
from scipy.spatial import distance
import telebot
from dependence import token


bot = telebot.TeleBot(token)

class MyThread(Thread):
    def __init__(self, arg1, arg2, arg3, arg4, arg5):
        Thread.__init__(self)
        self.arg1 = arg1 
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4
        self.chatId = arg5
        self.ch = 0

    def run(self):
        # Сounters
        counterOfName=0
        isFaceFound=0
        for det in self.arg2['val']:
            titleName = self.arg2['name'][counterOfName].split('\\')[1].split('.')[0]
            counterOfName=counterOfName+1

            a = distance.euclidean(det, self.arg1)
            if a < 0.55:
                cv2.imwrite('find/' + titleName + '.jpg', self.arg4)
                #while self.ch < 2:
                #sleep(0.5)
                now = datetime.now()
                last_line = open("log/log.txt").readlines()[-1]
                str1 = last_line.rstrip().split(" ")

                try:
                    last_data = datetime.strptime(str1[1] + " " + str1[2],'%d-%m-%Y %H:%M')
                except Exception:
                    last_data = now

                if titleName == str1[-1] and (now - last_data).seconds < 60:
                    exit()
                else:
                    #print(t1[0] == str1[-1], "  ", (now - last_data).seconds < 60)
                    #print(t1[0], str1[-1], (now - last_data).seconds)
                    #print("qwe ", (now - last_data).seconds, t1[0] + " " + str1[-1] + "\n")
                    #with open("log/log.txt", "a") as my_file:
                        my_file = open("log/log.txt", "a")
                        my_file.write("ОБАНАРУЖЕННО:....Дата: " + now.strftime("%d-%m-%Y %H:%M") + " Призвище особи - " + titleName + "\n")
                        my_file.close()
                        print("ОБАНАРУЖЕННО:....Дата: " + now.strftime("%d-%m-%Y %H:%M") + " Призвище особи - " + titleName)
                        #self.find = "+"
                        foto = 0
                        #with open('find/' + titleName + ".jpg", "rb") as f:
                        #    telegram_send.send(messages=["Дата: "+now.strftime("%d-%m-%Y %H:%M")+" Призвище особи - "+ titleName], images=[f])
                        #    foto = f.read()


                        bot.send_photo(self.chatId, open('foto/' + titleName + ".jpg", "rb"), now.strftime("%d-%m-%Y %H:%M") + " Призвище особи - " + titleName )
                        #bot.send_photo(self.chatId, cv2.imread('foto/' + titleName + ".jpg"), now.strftime("%d-%m-%Y %H:%M") + " Призвище особи - " + titleName)



                        #bot.send_photo(self.chatId, foto, "Дата: " + now.strftime("%d-%m-%Y %H:%M") + " Призвище особи - " + titleName)
                        #self.ch=self.ch+1
                        isFaceFound = isFaceFound + 1
                        break
                        #global j
        if isFaceFound == 0:
            bot.send_message(self.chatId, "Лицо не найдено в базе")
            print("Лицо не найдено в базе")
