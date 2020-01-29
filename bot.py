import telebot
import trnsl
from dependence import token
'''
class MyThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
'''

print("Запуск распознователя (Можно работать)")
#token = '1071090511:AAHQh4ACl--lIVXhJjxLk6lfYnt8LT5OT_g'
bot = telebot.TeleBot(token)

#Сounters
isAddFaceOrFindFace = 0
downloaded_file = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
    keyboard1.row('Добавить Лицо', 'Найти Лицо')
    bot.send_message(message.chat.id, 'Hi', reply_markup=keyboard1)

    #keyboard = telebot.types.InlineKeyboardMarkup()
    #first_btn = telebot.types.InlineKeyboardButton(text='Добавить Лицо', callback_data='first_cb')
    #second_btn = telebot.types.InlineKeyboardButton(text='Найти Лицо', callback_data='second_cb')
    #keyboard.add(first_btn, second_btn)
    #bot.send_message(message.chat.id, text='Hi', reply_markup=keyboard)

#downloaded_file = 0

@bot.message_handler(content_types=['text'])
def send_text(message):
    global isAddFaceOrFindFace, downloaded_file
    if message.text and isAddFaceOrFindFace == 3:
        isAddFaceOrFindFace = 0
        photoPathAndName = 'foto\\' + message.text + '.jpg'
        with open(photoPathAndName, 'wb') as new_file:
            new_file.write(downloaded_file)
        # downloaded_file = 0
        # bot.reply_to(message, "Фото добавлено")
        if trnsl.addFace(photoPathAndName) == 0:
            bot.send_message(message.chat.id, 'На фото не найдено лица')
        else:
            bot.send_message(message.chat.id, 'Добавлено')

    elif message.text == 'Добавить Лицо':
        bot.send_message(message.chat.id, 'Отправте Фото для загрузки')
        isAddFaceOrFindFace = 1
        #exit()
    elif message.text == 'Найти Лицо':
        bot.send_message(message.chat.id, 'Отправте Фото или Видео для поиска')
        isAddFaceOrFindFace = 2
        #exit()
    elif message.text == 'qwe':
        bot.send_message(message.chat.id, trnsl.f.dict)
    elif message:
        print(isAddFaceOrFindFace)
        bot.send_message(message.chat.id, 'Неправильный ввод')

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    global isAddFaceOrFindFace, downloaded_file

    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    if isAddFaceOrFindFace == 1:
        bot.send_message(message.chat.id, 'Введите имя')
        isAddFaceOrFindFace = 3
    elif isAddFaceOrFindFace == 2:
        isAddFaceOrFindFace = 0
        with open('test/test.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
        if trnsl.findFace('test/test.jpg', message.chat.id) == 0:
            bot.send_message(message.chat.id, 'На фото не найдено лица')
        else:
            bot.send_message(message.chat.id, 'Поиск запущен!')
    else:
        isAddFaceOrFindFace = 0

@bot.message_handler(content_types=['video'])
def handle_docs_video(message):
    global isAddFaceOrFindFace

    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)


    if isAddFaceOrFindFace == 2:
        with open('test/test.mp4', 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, 'Поиск запущен!')
        print('Поиск запущен!')
        res = trnsl.findFaceOnVideo('test/test.mp4', message.chat.id)
        if res == 0:
            bot.send_message(message.chat.id, 'На Видео не найдено лиц')
        else:
            print(res)
            print("Поиск завершон!")
            bot.send_message(message.chat.id, str(res) + '\n' + 'Поиск завершон!')
    isAddFaceOrFindFace = 0










    #global downloaded_file
    '''if message.text == 'Добавить Лицо':
        bot.send_message(message.chat.id, 'Отправте Фото')
        @bot.message_handler(content_types=['photo'])
        def handle_docs_photo(message):

            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            global downloaded_file
            downloaded_file = bot.download_file(file_info.file_path)
            bot.send_message(message.chat.id, 'Введите имя')'''

    '''elif message.text == 'Найти Лицо':
        bot.send_message(message.chat.id, 'Отправте Фото для поиска')
        @bot.message_handler(content_types=['photo'])
        def handle_docs_photo(message):
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('test/test.jpg', 'wb') as new_file:
                new_file.write(downloaded_file)

            trnsl.find('test/test.jpg')'''



    '''elif message and downloaded_file != 0 :
        bot.send_message(message.chat.id, 'добавлено')
        with open('foto/' + message.text + '.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
        downloaded_file = 0
        #bot.reply_to(message, "Фото добавлено")
        trnsl.addFace('photos\Danil.jpg')'''

    '''elif message:
        print(downloaded_file)
        bot.send_message(message.chat.id, 'gggggggggggggggggg')
    '''
'''
#@bot.callback_query_handler(func=lambda call: call.data == 'first_cb')
@bot.callback_query_handler(func=lambda call: True)
def add_photo(call):
    global i
    global j
    if call.data == 'first_cb':
        bot.send_message(call.message.chat.id, 'Отправте Фото для загрузки')
        i = 1
        #exit()
    if call.data == 'second_cb':
        bot.send_message(call.message.chat.id, 'Отправте Фото для поиска')
        i = 2
        #exit()
'''

bot.polling()