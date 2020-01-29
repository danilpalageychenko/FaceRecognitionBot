from datetime import datetime
from dependence import token
import telebot
import cv2
import dlib
import clas
import clas1
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

def addFace(fil):
    face_descriptor_name = f.dict.get('name')
    face_descriptor_it = f.dict.get('val')
    img = dlib.load_rgb_image(fil)
    dets = detector(img)
    if len(dets) <= 0:
        return 0
    for k, d in enumerate(dets):
        shape = sp(img, d)
        face_descriptor_name.append(fil)
        face_descriptor_it.append(facerec.compute_face_descriptor(img, shape))
        print('Добавлено в базу')
        #newFaces = {'name': face_descriptor_name, 'val': face_descriptor_it}
        #print(f.dict)
        #f.dict.update({'name': face_descriptor_name, 'val': face_descriptor_it})

        #print(f.dict.get('name'))
        #f.dict.update(newFaces)
    #print(f.dict.get('name'))



def findFace(foto, messageChatId):
    img = cv2.imread(foto)
    #cv2.imshow("Original image", image)
    #cv2.waitKey(0)

    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    dets = detector(rgb_image, 1)
    if len(dets) <= 0:
        return 0
    for k, d in enumerate(dets):
        print("find face")
        #cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), color_green, line_width)
        shape = sp(rgb_image, d)
        face_descriptor_fram = facerec.compute_face_descriptor(rgb_image, shape)
        c = clas.MyThread(face_descriptor_fram, f.dict, rgb_image, img, messageChatId, 0)
        c.start()
        #c.join()

        # sleep(0.5)

    #cv2.imshow('my webcam', img)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break



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
        dets = detector(rgb_image, 1)
        for k, d in enumerate(dets):
            print("find face")
            if isFindFaceOnFideo == 0: isFindFaceOnFideo = 1
            shape = sp(rgb_image, d)
            face_descriptor_fram = facerec.compute_face_descriptor(rgb_image, shape)
            clas.MyThread(face_descriptor_fram, f.dict, rgb_image, img, messageChatId, q).start()
        while q.empty() == False:
            item = q.get()
            if item not in masFace.keys():
                now = datetime.now()
                print("ОБНАРУЖЕННО:....Дата: " + now.strftime("%d-%m-%Y %H:%M") + " Прiзвище особи - " + item)
                bot.send_photo(messageChatId, open('foto/' + item + ".jpg", "rb"), now.strftime("%d-%m-%Y %H:%M") + " Прiзвище особи - " + item)
            masFace[item] = (int(masFace.get(item) or 0)) + 1
    #if isFindFaceOnFideo == 0:
    #    return 0
