from datetime import datetime
from dependence import token
import telebot
import cv2
import dlib
import clas
import clas1
import numpy as np
from queue import Queue
bot = telebot.TeleBot(token)

print("Запуск распознователя")
#cam = cv2.VideoCapture(0)
#cam.open('rtsp://admin:admin12345678@192.168.83.1:554/cam/realmonitor?channel=5&subtype=1')
#cam.open('http://192.168.133.235:8080/videofeed')

predictor_path = "shape_predictor_68_face_landmarks.dat"
#predictor_path = "shape_predictor_5_face_landmarks.dat"
face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
#color_green = (0,255,0)
#line_width = 3

f=clas1.MyThread1(predictor_path, face_rec_model_path, detector, sp, facerec)
f.start()
f.join()

def addFace(foto, text):
    nparr = np.fromstring(foto, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    resName = f.add(img, text)
    if not resName == False:
        cv2.imwrite(resName, img)
    else:
        return resName


def findFace(foto, messageChatId):
    nparr = np.fromstring(foto, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    dets = detector(rgb_image, 1)
    if len(dets) <= 0:
        return 0
    for k, d in enumerate(dets):
        print("find face")
        shape = sp(rgb_image, d)
        face_descriptor_fram = facerec.compute_face_descriptor(rgb_image, shape)
        c = clas.MyThread(face_descriptor_fram, f.dict, rgb_image, img, messageChatId, 0)
        c.start()


def findFaceOnVideo(Video, messageChatId):
    cam = cv2.VideoCapture(Video)

    #Сounters
    masFace = {}
    isFindFaceOnFideo = 0
    q = Queue()
    while (cam.isOpened()):
        ret_val, img = cam.read()
        try:
            rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except:
            if isFindFaceOnFideo == 0: return 0
            else: return masFace
        ####
        dets = detector(rgb_image, 1)
        ####
        for k, d in enumerate(dets):
            print("find face")
            if isFindFaceOnFideo == 0: isFindFaceOnFideo = 1
            shape = sp(rgb_image, d)
            ####
            face_descriptor_fram = facerec.compute_face_descriptor(rgb_image, shape)
            ####
            clas.MyThread(face_descriptor_fram, f.dict, rgb_image, img, messageChatId, q).start()
        while q.empty() == False:
            item = q.get()
            if item[0] not in masFace.keys():
                now = datetime.now()
                print("ВИЯВЛЕНО:....Дата: " + now.strftime("%d-%m-%Y %H:%M") + " Прізвище особи - ", item[0])
                bot.send_photo(messageChatId, open(item[1], "rb"), now.strftime("%d-%m-%Y %H:%M") + " Прізвище особи - " + item[0])
            masFace[item[0]] = (int(masFace.get(item[0]) or 0)) + 1

