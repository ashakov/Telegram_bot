import os
from background import keep_alive #импорт функции для поддержки работоспособности
import pip
pip.main(['install', 'python-telegram-bot', 'pytelegrambotapi'])
import telebot
import telegram
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import openpyxl
from telegram import ReplyKeyboardRemove

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from datetime import datetime




# create a new Excel workbook and select the active sheet
workbook = openpyxl.Workbook()
sheet = workbook.active

# set the headers for the Excel file
sheet["A1"] = "TimeStamp"
sheet["B1"] = "User ID"
sheet["C1"] = "User Name"
sheet["D1"] = "Question"
sheet["E1"] = "Response"

bot = telebot.TeleBot('6100483283:AAGAXER5F5lEn7f_vZaRc0Ofsik_UoPZ8H4')
#bot.delete_webhook()


# функция для записи ответа пользователя в Excel файл
def log_response(timestamp, user_id, first_name, question, response):
    row = (timestamp, user_id, first_name, question, response)
    sheet.append(row)
    workbook.save("user_responses.xlsx")


@bot.message_handler(commands = ['start'])
def start(message):
    # Создаем клавиатуру Да/Нет
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Да, продолжить'))
    #keyboard.add(KeyboardButton('Нет'))

    # Отправляем приветственное сообщение с клавиатурой Да/Нет
    bot.send_message(message.chat.id, f"<code>Привет, {message.from_user.first_name}! Мы очень рады видеть тебя здесь! "
                                      f"Чтобы скорее начать работу, пройди несколько несложных шагов. Готов начать?</code>", parse_mode='HTML' ,
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_email)

@bot.message_handler(content_types=['text'])
def ask_email(message):
    # Отправляем вопрос "Какая у вас почта?" и ждем ответа
    remove_keyboard = telebot.types.ReplyKeyboardRemove()
    # Отправляем вопрос "Какая у вас почта?" и ждем ответа
    bot.send_message(message.chat.id, "<code>Укажите почту, под которой вы регистрировались.</code>", parse_mode='HTML',
                     reply_markup=remove_keyboard)
    #bot.send_message(message.chat.id, "<code>Укажите почту, под которой вы регистрировались.</code>", parse_mode='HTML')
    log_response(datetime.now(),message.chat.id, message.from_user.first_name, "Готовность", message.text)
    bot.register_next_step_handler(message, ask_traffic_source)
    #save_to_excel(message) # add this line

def ask_traffic_source(message):
    # Создаем клавиатуру с вариантами ответов
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("SEO", callback_data="seo"))
    keyboard.add(InlineKeyboardButton("ASO", callback_data="aso"))
    keyboard.add(InlineKeyboardButton("Контекстная реклама", callback_data="context ad"))
    keyboard.add(InlineKeyboardButton("Социальные сети", callback_data="social"))
    keyboard.add(InlineKeyboardButton("Стримминг", callback_data="streaming"))
    keyboard.add(InlineKeyboardButton("Youtube трафик", callback_data="youtube"))
    keyboard.add(InlineKeyboardButton("Другое", callback_data="others"))
    keyboard.add(InlineKeyboardButton("Нет активных источников", callback_data="no_active"))

    # Отправляем вопрос "Выберите источник трафика" с клавиатурой
    bot.send_message(message.chat.id, "<code>Укажите источники трафика, с которыми планируете работать. Также, информируем вас о ряде запрещенных источников, которые не сможем согласовать:\n "
                                      "- трафик с порнографических сайтов, контекстная реклама с указанием бренда Рекламодателя,\n"
                                      "- мотивированный трафик,\n"
                                      "- спам-рассылка в личных сообщениях в аккаунтах социальных сетей,\n "
                                      "- трафик из Фейсбук, Инстаграм, Тик Ток.</code>", reply_markup=keyboard, parse_mode='HTML')
    log_response(datetime.now(), message.chat.id, message.from_user.first_name, "Укажите почту, на которую вы регистрировались", message.text)
    bot.register_callback_query_handler(message, handle_callback_query)

    #Ответы кнопок:
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Получаем ID чата, из которого пришел запрос
    chat_id = call.message.chat.id if call.message else call.chat.id
    message_id = call.message.id if call.message else call.message_id

    # Проверяем, какую кнопку нажал пользователь
    if call.data == 'seo':
        bot.send_message(chat_id, "- Укажите ссылку на сайт,\n "
                                  "- прикрепите статистику по посещаемости сайта, \n"
                                  "- опишите, как планируете рекламировать БК «Лига Ставок»: баннер, рейтинг и т.д.")
    elif call.data == 'aso':
        bot.send_message(chat_id, "- Укажите ссылку на приложение, место в рейтинге.\n "
                                  "- Если планируете делать брендовое приложение - опишите его вид, механику и т.д., \n"
                                  "- примерно сроки реализации")
    elif call.data == "context ad":
        bot.send_message(chat_id, "Укажите, по каким ключам планируете запускать рекламу, где? При запуске через ЯД, пришлите статистику из ЛК ЯД")
    elif call.data == "social":
        bot.send_message(chat_id, "Укажите, являетесь ли вы владельцем сообщества/ планируете закупать рекламу. Прикрепите ссылки. Если это группа ВК - пришлите статистику по охватам")
    elif call.data == "streaming":
        bot.send_message(chat_id, "Укажите ссылки на стримы, прикрепите портфолио с опытом в сфере стрим-индустрии")
    elif call.data == "youtube":
        bot.send_message(chat_id, "Укажите ссылку на ютуб канал/каналы, пришлите статистику по охватам")
    elif call.data == "others":
        bot.send_message(chat_id, "Укажите источник самостоятельно")
    elif call.data == "no_active":
        bot.send_message(chat_id, "Жаль, что у вас нет активных источников. В данный момент мы не можем с вами сотрудничать.")
        bot.stop_bot()

    log_response(datetime.now(), chat_id, call.from_user.first_name, "Источник трафика", call.data)
    bot.register_next_step_handler(call.message, ask_experience)


# Обработчик отправки видео
@bot.message_handler(content_types=['video'])
def forward_video(message):
    chat_id = message.chat.id
    video_id = message.video.file_id
    file_info = bot.get_file(video_id)
    downloaded_file = bot.download_file(file_info.file_path)
    # определяем путь для сохранения видео
    file_name = message.video.file_name
    file_path = os.path.join('videos', file_name)
    # сохраняем файл на сервере
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    # пересылаем видео пользователю
    bot.forward_message(62667001, chat_id, message.chat.id, message.message_id)
    log_response(datetime.now(), chat_id, message.from_user.first_name, "Отправлено видео пользователю", file_name)

@bot.message_handler(content_types=['document'])
def save_document(message):
    document = message.document
    file_info = bot.get_file(document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    chat_id = message.chat.id
    user_id = message.from_user.id
# сохраняем файл на сервере
    file_name = document.file_name
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
# Пересылаем документ другому пользователю
    target_user_id = 62667001  # замените на ID целевого пользователя
    bot.send_document(chat_id=target_user_id, data=downloaded_file, caption=f"Получено от пользователя {user_id}")
    log_response(datetime.now(), chat_id, message.from_user.first_name, "Отправлен документ пользователю", file_name)

@bot.message_handler(content_types=['photo'])
def save_image(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id
    file_name = f"photo_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    # сохраняем файл на сервере
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    # отправляем фото другому пользователю
    target_user_id = 62667001  # замените на ID целевого пользователя
    caption = f"Получено от пользователя {user_id}"
    with open(file_name, 'rb') as photo:
        bot.send_photo(chat_id=target_user_id, photo=photo, caption=caption)

    # удаляем локальный файл
    #os.remove(file_name)
    log_response(datetime.now(), chat_id, message.from_user.first_name, "Отправлено изображение пользователю", file_name)


@bot.message_handler(content_types=['text'])
def ask_experience(message):
    # Сохраняем ответ на вопрос "Выберите источник трафика"
    #traffic_source = call.data

    # Создаем клавиатуру Да/Нет
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Да'))
    keyboard.add(KeyboardButton('Нет'))

    # Отправляем вопрос "Был ли у вас опыт в сфере арбитража трафика?" с клавиатурой Да/Нет
    bot.send_message(message.chat.id, "Был ли у вас опыт в сфере арбитража трафика?", reply_markup=keyboard)
    bot.register_next_step_handler(message, send_statistics)
    log_response(datetime.now(), message.chat.id, message.from_user.first_name, "Запрос информации по источникам", message.text)

@bot.message_handler(content_types=['text'])
def send_statistics(message):
    if message.text == "Да":
        # Отправляем вопрос "Какая у вас почта?" и ждем ответа
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Беттинг'))
        keyboard.add(KeyboardButton('Гемблинг'))
        keyboard.add(KeyboardButton('Фин. офферы'))
        keyboard.add(KeyboardButton('Другие'))

        bot.send_message(message.chat.id, "По работе в какой вертикали арбитража трафика имеется статистика?", reply_markup=keyboard)
        bot.register_next_step_handler(message, prev_payments)

    #    save_to_excel(message)
        #bot.register_next_step_handler(message, ask_traffic_source)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "<code>Если ваша заявка пройдет модерацию, с вами свяжется "
                                          "менеджер в течение 1-3 дней в зависимости от загруженности.\n\n"
                                          " Если менеджер с вами не связался, ваша заявка не была апрувлена по трем причинам: \n"
                                          "- низкое качество траффика по предоставленным данным; \n"
                                          "- нарушение шаблона подачи заявки: какая-то информация из требуемого списка отсутствует;\n "
                                          "- нет активных источников на руках: если вы в процессе создания источника, свяжитесь с нами по готовности (ИСКЛЮЧЕНИЕ: ваш источник трафика ASO, и вы планируете делать приложение под БК Лига Ставок. \n"
                                          "Просим быть внимательными и не оставлять вопросы без ответа. Это очень важно при принятии решения! :)</code>",
                         parse_mode='HTML')
     #   save_to_excel(message)
        #bot.stop_polling()
      #bot.stop_bot()
    # Сохраняем данные пользователя в файл# Сохраняем данные пользователя в файл

    log_response(datetime.now(), message.chat.id, message.from_user.first_name, "Был ли у вас опыт в сфере арбитража трафика?", message.text)


@bot.message_handler(content_types=['text'])
def prev_payments(message):
    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Партнерская программа'))
    keyboard.add(KeyboardButton('Фикс. оплата'))

    if message.text == "Другие":
        remove_keyboard = telebot.types.ReplyKeyboardRemove()


        bot.send_message(message.chat.id, "<code>Введите название вертикали, по которой есть статистика:</code>", parse_mode='HTML', reply_markup=remove_keyboard)
        bot.register_next_step_handler(message, send_other, keyboard)
        log_response(datetime.now(), message.chat.id, message.from_user.first_name,
                     "По работе в какой вертикали арбитража трафика имеется статистика?", message.text)
    else:
        bot.send_message(message.chat.id, "Вы работали по партнерской программе/по фиксированной оплате?",
                         reply_markup=keyboard)
        log_response(datetime.now(), message.chat.id, message.from_user.first_name,
                     "По работе в какой вертикали арбитража трафика имеется статистика?", message.text)
        bot.register_next_step_handler(message, stat_requester)

    #log_response(datetime.now(), message.chat.id, message.from_user.first_name,
              #   "По работе в какой вертикали арбитража трафика имеется статистика?", message.text)

def send_other(message, prev_keyboard):
    # Сохраняем ответ на вопрос "Другие"
    other = message.text
    # Отправляем ответ пользователю
    bot.send_message(message.chat.id,"Вы работали по партнерской программе/по фиксированной оплате?", reply_markup=prev_keyboard)
    log_response(datetime.now(), message.chat.id, message.from_user.first_name,
                     "Ответ на вопрос 'По работе в какой вертикали арбитража трафика имеется статистика?'", message.text)
    bot.register_next_step_handler(message, stat_requester)



@bot.message_handler(content_types=['text'])
def stat_requester(message):
    remove_keyboard = telebot.types.ReplyKeyboardRemove()
    if message.text == 'Партнерская программа':
        bot.send_message(message.chat.id, "<code>Необходимо прислать статистику в формате видео по следующей инструкции:\n"
                                      " 1. Войдите в ЛК;\n"
                                      " 2. Перейдите в раздел статистики;\n "
                                      "3. Продемонстрируйте статистику по конверсиям (ftd, std (rd), сумма депозитов, хиты/хосты, переходы, уники при наличии)\n "
                                      "за различные месяцы в разрезе каждого отдельно (например, отдельно за ноябрь, за декабрь, за январь); \n"
                                      "4. Статистика в идеале должна быть свежей.</code>", parse_mode='HTML', reply_markup=remove_keyboard)
    elif message.text == 'Фикс. оплата':
        bot.send_message(message.chat.id, "<code>Укажите, с какой компанией работали по данной модели? "
                                          "Пришлите пример рекламной интеграции в зависимости от вашего источника трафика (скрин из группы, текст поста, ссылка на видео)</code>", parse_mode='HTML' , reply_markup=remove_keyboard)


    log_response(datetime.now(), message.chat.id, message.from_user.first_name, "Вы работали по партнерской программе/по фиксированно оплате?", message.text)
    bot.register_next_step_handler(message, final_message)

@bot.message_handler(content_types=['text'])
def final_message(message):
    remove_keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "<code>Если ваша заявка пройдет модерацию, с вами свяжется "
                                      "менеджер в течение 1-3 дней в зависимости от загруженности.\n\n"
                                      " Если менеджер с вами не связался, ваша заявка не была апрувлена по трем причинам: \n"
                                      "- низкое качество траффика по предоставленным данным; \n"
                                      "- нарушение шаблона подачи заявки: какая-то информация из требуемого списка отсутствует;\n "
                                      "- нет активных источников на руках: если вы в процессе создания источника, свяжитесь с нами по готовности (ИСКЛЮЧЕНИЕ: ваш источник трафика ASO, и вы планируете делать приложение под БК Лига Ставок. \n"
                                      "Просим быть внимательными и не оставлять вопросы без ответа. Это очень важно при принятии решения! :)</code>", parse_mode='HTML', reply_markup=remove_keyboard)
    log_response(datetime.now(), message.chat.id, message.from_user.first_name, "Запрос стат-ки", message.text)
    #bot.stop_polling()
    #bot.stop_bot()

keep_alive()#запускаем flask-сервер в отдельном потоке..

bot.polling(non_stop=True, interval=0) #запуск бота
