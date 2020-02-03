import telebot
import trnsl
import os
import uuid
from dependence import token
from dependence import telegramID

print("Запуск распознователя (Можно работать)")
bot = telebot.TeleBot(token)

#Сounters
isAddFaceOrFindFace = 0
downloaded_file = 0

@bot.message_handler(commands=['start'])
def start_message(message):
    if str(message.from_user.id) not in telegramID:
        bot.send_message(message.chat.id, 'False')
        exit()
    keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
    keyboard1.row('Додати обличчя', 'Знайти обличчя')
    bot.send_message(message.chat.id, 'Вiтаю', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if str(message.from_user.id) not in telegramID:
        bot.send_message(message.chat.id, 'False')
        exit()
    global isAddFaceOrFindFace, downloaded_file
    if message.text and isAddFaceOrFindFace == 3 and message.text != ('Додати обличчя' or 'Знайти обличчя'):
        isAddFaceOrFindFace = 0
        if trnsl.addFace(downloaded_file, message.text) == False:
            bot.send_message(message.chat.id, 'На фото не знайдено обличчя')
        else:
            bot.send_message(message.chat.id, 'Додано')
    elif message.text == 'Додати обличчя':
        bot.send_message(message.chat.id, 'Надішліть фото для завантаження')
        isAddFaceOrFindFace = 1
    elif message.text == 'Знайти обличчя':
        bot.send_message(message.chat.id, 'Надішліть Фото або Відео для пошуку')
        isAddFaceOrFindFace = 2
    elif message.text == 'qwe':
        bot.send_message(message.chat.id, trnsl.f.dict.items() )
    elif message:
        print(isAddFaceOrFindFace)
        bot.send_message(message.chat.id, 'Невірне введення')

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    global isAddFaceOrFindFace, downloaded_file
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    if isAddFaceOrFindFace == 1:
        bot.send_message(message.chat.id, 'Введіть ім\'я')
        isAddFaceOrFindFace = 3
    elif isAddFaceOrFindFace == 2:
        isAddFaceOrFindFace = 0
        if trnsl.findFace(downloaded_file, message.chat.id) == 0:
            bot.send_message(message.chat.id, 'На фото не знайдено обличчя')
        else:
            bot.send_message(message.chat.id, 'Пошук запущений!')
    else:
        isAddFaceOrFindFace = 0

@bot.message_handler(content_types=['video'])
def handle_docs_video(message):
    global isAddFaceOrFindFace
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    if isAddFaceOrFindFace == 2:
        photoPathAndName = 'inTheProcess\\' + str(uuid.uuid1()) + '.mp4'
        with open(photoPathAndName, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, 'Пошук запущений!')
        print('Пошук запущений!')
        res = trnsl.findFaceOnVideo(photoPathAndName, message.chat.id)
        if res == 0:
            bot.send_message(message.chat.id, 'На відео не знайдено облич')
        else:
            print("Пошук завершений!")
            resFul = ""
            for i in res.keys():
                resFul += "Особа: " + str(i) + ", "  + str(res.get(i)) + " разів\n"
            bot.send_message(message.chat.id, 'Пошук завершений!\n' + "Знайдено:\n" + resFul)
        os.remove(photoPathAndName)
        isAddFaceOrFindFace = 0

bot.polling()