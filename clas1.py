import os
import dlib
import datetime
import glob
from threading import Thread
import pickle
import sqlite3

class MyThread1(Thread):
    def __init__(self, arg1, arg2, arg3, arg4, arg5):
        Thread.__init__(self)
        print("Запуск инициализации базы")
        self.predictor_path = arg1
        self.face_rec_model_path = arg2
        self.detector = arg3
        self.sp = arg4
        self.facerec = arg5
        self.dict = {}

    def run(self):
        if not os.path.exists('db/mydatabase.db'):
            conn = sqlite3.connect("db/mydatabase.db")  # или :memory: чтобы сохранить в RAM
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE Faces
                              (id INTEGER PRIMARY KEY AUTOINCREMENT, title text, photoPath text)
                           """)
            conn.commit()
            conn.close()
        if os.path.exists('db/data_file.pkl'):
            self.dict = pickle.load(open('db/data_file.pkl', 'rb'))
            exit()
        else:
            face_descriptor_it = []
            face_descriptor_name = []
            now1 = datetime.datetime.now()
            my_file = open("log/log.txt", "a")
            my_file.write("Начало работы: "+now1.strftime("%d-%m-%Y %H:%M")+"\n")
            print("Начало работы: "+now1.strftime("%d-%m-%Y %H:%M"))
            conn = sqlite3.connect("db/mydatabase.db")  # или :memory: чтобы сохранить в RAM
            cursor = conn.cursor()
            for fil in glob.iglob('foto/**/*.jpg', recursive=True):
                img = dlib.load_rgb_image(fil)
                my_file.write("В обработке файлы цели: "+fil+"\n")
                print("В обработке файлы цели: "+fil)
                try:
                    dets = self.detector(img)
                    for k, d in enumerate(dets):
                        shape = self.sp(img, d)
                        try:
                            increment = self.dict.get('name')[-1] + 1
                        except:
                            increment = 0
                        face_descriptor_it.append(self.facerec.compute_face_descriptor(img, shape))
                        face_descriptor_name.append(increment)
                        self.dict = {'name': face_descriptor_name, 'val': face_descriptor_it}
                        try:
                            titleName = fil.split('/')[1].split('.')[0]
                        except:
                            titleName = fil
                        cursor.execute("INSERT INTO Faces VALUES(?, ?, ?)", [(increment), (titleName), (fil)])
                        conn.commit()
                except:
                    pass
            conn.close()
            my_file.close()
            pickle.dump(self.dict, open('db/data_file.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)




    def add(self, img, text):
        if not self.dict == {}:
            face_descriptor_name = self.dict.get('name')
            face_descriptor_it = self.dict.get('val')
        else:
            face_descriptor_name = []
            face_descriptor_it = []
        dets = self.detector(img)
        if len(dets) <= 0:
            return False
        for k, d in enumerate(dets):
            shape = self.sp(img, d)
            try:
                increment = self.dict.get('name')[-1] + 1
            except:
                increment = 0
            #
            self.dict = {'name': face_descriptor_name, 'val': face_descriptor_it}
            #
            face_descriptor_name.append(increment)
            face_descriptor_it.append(self.facerec.compute_face_descriptor(img, shape))
        conn = sqlite3.connect("db/mydatabase.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        photoPath = "foto/" + str(increment) + ".jpg"
        cursor.execute("INSERT INTO Faces (id, title, photoPath) VALUES(?, ?, ?)", [(increment), (text), (photoPath)])
        conn.commit()
        conn.close()
        pickle.dump(self.dict, open('db/data_file.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        return photoPath


'''
        face_descriptor_name = self.dict.get('name')
        face_descriptor_it = self.dict.get('val')
        img = dlib.load_rgb_image(foto)
        dets = self.detector(img)
        if len(dets) <= 0:
            return 0
        for k, d in enumerate(dets):
            shape = self.sp(img, d)
            face_descriptor_it.append(self.facerec.compute_face_descriptor(img, shape))
            face_descriptor_name.append(foto)
        pickle.dump(self.dict, open('db/data_file.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
'''