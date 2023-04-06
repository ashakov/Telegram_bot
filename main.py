# pip.main(['install', 'python-telegram-bot', 'pytelegrambotapi'])
import os
from background import keep_alive  # импорт функции для поддержки работоспособности
import pip
import telebot
import telegram
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import openpyxl
from telegram import ReplyKeyboardRemove
import io
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
sheet["F1"] = "File_name"
bot = telebot.TeleBot('6100483283:AAGAXER5F5lEn7f_vZaRc0Ofsik_UoPZ8H4')


# bot.delete_webhook()


# функция для записи ответа пользователя в Excel файл
def log_response(timestamp, user_id, first_name, question, response, file_name=None):
    row = (timestamp, user_id, first_name, question, response, file_name)
    sheet.append(row)
    workbook.save("user_responses.xlsx")


user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    # Сбрасываем флаги при перезапуске бота
    if user_id in user_data:
        user_data[user_id]["asked_email"] = False
        user_data[user_id]["asked_experience"] = False
        # сбросьте флаги для других функций

    # Создаем клавиатуру Да/Нет
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Да, продолжить'))
    # keyboard.add(KeyboardButton('Нет'))

    # Отправляем приветственное сообщение с клавиатурой Да/Нет
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Мы очень рады видеть тебя здесь! "
                                      f"Чтобы скорее начать работу, пройди несколько несложных шагов. Готов начать?",
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_email)


@bot.message_handler(func=lambda msg: msg.text == "Да" or msg.text == "Да, продолжить" or msg.text == "да")
def ask_email(message):
    user_id = message.from_user.id

    # Если пользователь отсутствует в словаре, добавляем его с asked_email = False
    if user_id not in user_data:
        user_data[user_id] = {"asked_email": False}

    # Если вопрос уже был задан, пропускаем его
    if user_id in user_data and "asked_email" in user_data[user_id] and user_data[user_id]["asked_email"]:
        return

    # Отправляем вопрос "Какая у вас почта?" и ждем ответа
    remove_keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Укажите почту, под которой вы регистрировались.",
                     reply_markup=remove_keyboard)
    log_response(datetime.now(), message.chat.id, message.from_user.first_name, "Готовность", message.text)
    bot.register_next_step_handler(message, ask_traffic_source)

    # Устанавливаем asked_email в True
    user_data[user_id]["asked_email"] = True


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
    bot.send_message(message.chat.id,
                     "Укажите источники трафика, с которыми планируете работать. Также, информируем вас о ряде запрещенных источников, которые не сможем согласовать:\n "
                     "- трафик с порнографических сайтов,\n"
                     "- контекстная реклама с указанием бренда Рекламодателя,\n"
                     "- мотивированный трафик,\n"
                     "- спам-рассылка в личных сообщениях в аккаунтах социальных сетей,\n "
                     "- трафик из Фейсбук, Инстаграм, Тик Ток.", reply_markup=keyboard, parse_mode='HTML')
    log_response(datetime.now(), message.chat.id, message.from_user.first_name,
                 "Укажите почту, на которую вы регистрировались", message.text)
    bot.register_callback_query_handler(message, handle_callback_query)

    # Ответы кнопок:


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Получаем ID чата, из которого пришел запрос
    chat_id = call.message.chat.id if call.message else call.chat.id
    message_id = call.message.id if call.message else call.message_id

    # Проверяем, какую кнопку нажал пользователь
    if call.data == 'seo':
        bot.send_message(chat_id, " - Укажите ссылку на сайт;\n "
                                  "<b> - Прикрепите статистику по посещаемости сайта;</b>\n"
                                  "- Опишите, как планируете рекламировать БК «Лига Ставок»: баннер, рейтинг и т.д.\n"
                                  "- Если РК будет проводиться посредством запуска контекстной рекламы, также укажите данную информацию.\n"
                                  "<b> - Прикрепите видео с панели администрирования/скан владения доменом (если данный пункт неосуществим, указать причину, но отсутствие статистики может негативно сказаться на результатах модерации).</b>\n\n"

                                  "НА ДАННОМ ЭТАПЕ ФАЙЛЫ ПРИКРЕПЛЯТЬ НЕ НУЖНО. В самом конце после ответа на вопросы у вас будет возможность прикрепить все необходимые видео/фото материалы.\n\n"

                                  " *Для данного источника трафика может потребоваться дополнительная проверка после прохождения модерации.",
                         parse_mode='HTML')
    elif call.data == 'aso':
        bot.send_message(chat_id, "- Укажите ссылку на приложение, место в рейтинге; \n"
                                  "- Если планируете делать брендовое приложение - опишите его вид, механику и т.д., примерные сроки реализации;\n"
                                  "- Прикрепите видео из кабинета разработчика (если данный пункт неосуществим, указать причину, но отсутствие статистики может негативно сказаться на результатах модерации)(в конце опроса);\n\n"

                                  "НА ДАННОМ ЭТАПЕ ФАЙЛЫ ПРИКРЕПЛЯТЬ НЕ НУЖНО. В самом конце после ответа на вопросы у вас будет возможность прикрепить все необходимые видео/фото материалы.",
                         parse_mode='HTML')
    elif call.data == "context ad":
        bot.send_message(chat_id, "- Укажите, по каким ключам планируете запускать рекламу, где? \n"
                                  "<b>- При запуске через ЯД прикрепите статистику из ЛК ЯД.</b>\n\n"

                                  "НА ДАННОМ ЭТАПЕ ФАЙЛЫ ПРИКРЕПЛЯТЬ НЕ НУЖНО. В самом конце после ответа на вопросы у вас будет возможность прикрепить все необходимые видео/фото материалы.\n\n"

                                  "*Для данного источника трафика может потребоваться дополнительная проверка после прохождения модерации.",
                         parse_mode='HTML')
    elif call.data == "social":
        bot.send_message(chat_id, "- Укажите, являетесь ли вы владельцем сообщества/ планируете закупать рекламу. \n"
                                  "- Прикрепите ссылки на источники. <b>Если это группа в ВК - пришлите статистику по ее охватам;</b>\n"
                                  "- Прикрепите подтверждение того, что владеете каналом/группой(формат - видео/фото).\n"

                                  "НА ДАННОМ ЭТАПЕ ФАЙЛЫ ПРИКРЕПЛЯТЬ НЕ НУЖНО. В самом конце после ответа на вопросы у вас будет возможность прикрепить все необходимые видео/фото материалы.",
                         parse_mode='HTML')
    elif call.data == "streaming":
        bot.send_message(chat_id, "- Укажите ссылки на стримы,\n "
                                  "- Прикрепите портфолио с опытом в сфере стрим-индустрии, если проводите стримы самостоятельно (формат - текстовый файл);\n"
                                  "- Укажите, на каких платформах планируете проводить эфиры и формат размещения БК “Лига Ставок”;\n"
                                  "- Если вы планируете закупать рекламу у стримеров, также укажите ссылки на их стримы, по возможности портфолио (формат - текстовый файл), формат размещения БК “Лига Ставок”. \n\n "

                         , parse_mode='HTML')
    elif call.data == "youtube":
        bot.send_message(chat_id, "-Укажите ссылку/и на YouTube канал/ы;\n"
                                  "<b>- Прикрепите статистику по охватам канала/ов;</b>\n"
                                  " - Укажите, планируете ли вы закуп рекламы на данной платформе или канал принадлежит вам;\n"
                                  "- Если источник/и ваш/и- прикрепите подтверждение.(формат - видео/фото).\n"

                                  "НА ДАННОМ ЭТАПЕ ФАЙЛЫ ПРИКРЕПЛЯТЬ НЕ НУЖНО. В самом конце после ответа на вопросы у вас будет возможность прикрепить все необходимые видео/фото материалы.",
                         parse_mode='HTML')
    elif call.data == "others":
        bot.send_message(chat_id, "Укажите источник самостоятельно")
    elif call.data == "no_active":
        bot.send_message(chat_id, " Если ваша заявка пройдет модерацию, с вами свяжется "
                                  "менеджер в течение 1-3 дней в зависимости от загруженности.\n\n"
                                  " Если менеджер с вами не связался, ваша заявка не была апрувлена по трем причинам: \n"
                                  "- низкое качество траффика по предоставленным данным; \n"
                                  "- нарушение шаблона подачи заявки: какая-то информация из требуемого списка отсутствует;\n "
                                  "- нет активных источников на руках: если вы в процессе создания источника, свяжитесь с нами по готовности (ИСКЛЮЧЕНИЕ: ваш источник трафика ASO, и вы планируете делать приложение под БК Лига Ставок. \n\n"
                                  "Просим быть внимательными и не оставлять вопросы без ответа. Это очень важно при принятии решения! :)",
                         parse_mode='HTML')
        bot.clear_step_handler_by_chat_id(chat_id)

    log_response(datetime.now(), chat_id, call.from_user.first_name, "Источник трафика", call.data)
    bot.register_next_step_handler(call.message, ask_experience)


@bot.message_handler(content_types=['text', 'photo', 'video', 'document'])
def handle_messages(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    target_user_id = 475132584  # 62667001
    if message.content_type == 'video':
        video = message.video
        video_id = video.file_id
        file_name = f"video_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
        file_info = bot.get_file(video_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_message(message.chat.id, "Видео отправлено.")
        # сохраняем файл на сервере
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        # отправляем видео другому пользователю
        # target_user_id = 62667001  # замените на ID целевого пользователя
        caption = f"Получено от пользователя {user_id}: {message.caption if message.caption else 'нет комментария'}"
        with open(file_name, 'rb') as video:
            sent_message = bot.send_video(chat_id=target_user_id, video=video, caption=caption)

        # сохраняем комментарии в файл
        log_response(datetime.now(), chat_id, message.from_user.first_name,
                     f"Отправлено видео пользователю {target_user_id}", file_name=file_name,
                     response=f"Комментарий к видео: {caption}")

    elif message.content_type == 'photo':
        photo = message.photo[-1]  # получаем только самое большое разрешение фото
        file_id = photo.file_id
        file_name = f"photo_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_message(message.chat.id, "Фото отправлено.")
        # сохраняем файл на сервере
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        comment = message.caption if message.caption else ""

        # отправляем фото другому пользователю
        # target_user_id = 62667001  # замените на ID целевого пользователя
        user_name = message.from_user.first_name
        caption = f"Получено от пользователя {user_name} (ID: {user_id}).\n{comment}"
        with open(file_name, 'rb') as photo:
            sent_message = bot.send_photo(chat_id=target_user_id, photo=photo, caption=caption)

    elif message.content_type == 'document':
        document = message.document
        document_id = document.file_id
        document_extension = os.path.splitext(document.file_name)[1]
        file_name = f"document_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}{document_extension}"
        file_info = bot.get_file(document_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_message(message.chat.id, "Документ отправлен.")
        # сохраняем файл на сервере
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        comment = message.caption if message.caption else ""

        # отправляем документ другому пользователю
        # target_user_id = 62667001  # замените на ID целевого пользователя
        user_name = message.from_user.first_name
        caption = f"Получено от пользователя {user_name} (ID: {user_id}).\n{comment}"
        with open(file_name, 'rb') as document:
            sent_message = bot.send_document(chat_id=target_user_id, document=document, caption=caption)

        # Save the comment to the Excel file
        log_response(datetime.now(), user_id, message.from_user.first_name, "Document", file_name, comment)

    bot.register_callback_query_handler(message, ask_experience)


@bot.message_handler(content_types=['text', 'video', 'document', 'photo'])
def ask_experience(message):
    user_id = message.from_user.id

    # Если пользователь отсутствует в словаре, добавляем его с asked_experience = False
    if user_id not in user_data:
        user_data[user_id] = {"ask_experience_done": False}

    # Если ключ 'ask_experience' отсутствует в словаре пользователя или его значение равно False, выполняем код
    if not user_data[user_id].get("asked_experience", False):
        # Создаем клавиатуру Да/Нет
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Да'))
        keyboard.add(KeyboardButton('Нет'))

        # Отправляем вопрос "Был ли у вас опыт в сфере арбитража трафика?" с клавиатурой Да/Нет
        bot.send_message(message.chat.id, "Был ли у вас опыт в сфере арбитража трафика?",
                         reply_markup=keyboard)

        log_response(datetime.now(), message.chat.id, message.from_user.first_name, "Запрос информации по источникам",
                     message.text)

        # Устанавливаем asked_experience в True
        user_data[user_id]["asked_experience"] = True

        # Устанавливаем asked_experience_done в False для нового сообщения
        user_data[user_id]['ask_experience_done'] = False

        # Регистрируем следующий обработчик
        bot.register_next_step_handler(message, send_statistics)


@bot.message_handler(content_types=['text'])
def send_statistics(message):
    user_id = message.from_user.id

    # Если пользователь отсутствует в словаре, добавляем его
    if user_id not in user_data:
        user_data[user_id] = {}

    # Если ключ 'ask_experience_done' присутствует в словаре пользователя и его значение равно True, пропускаем выполнение
    if user_data[user_id].get("ask_experience_done", False):
        return

    if message.text == "Да":
        # Отправляем вопрос "По работе в какой вертикали арбитража трафика имеется статистика?" и ждем ответа
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Беттинг'))
        keyboard.add(KeyboardButton('Гемблинг'))
        keyboard.add(KeyboardButton('Фин. офферы'))
        keyboard.add(KeyboardButton('Другие'))

        bot.send_message(message.chat.id, "По работе в какой вертикали арбитража трафика имеется статистика?",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, prev_payments)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Если ваша заявка пройдет модерацию, с вами свяжется "
                                          "менеджер в течение 1-3 дней в зависимости от загруженности.\n\n"
                                          " Если менеджер с вами не связался, ваша заявка не была апрувлена по трем причинам: \n"
                                          "- низкое качество траффика по предоставленным данным; \n"
                                          "- нарушение шаблона подачи заявки: какая-то информация из требуемого списка отсутствует;\n "
                                          "- нет активных источников на руках: если вы в процессе создания источника, свяжитесь с нами по готовности (ИСКЛЮЧЕНИЕ: ваш источник трафика ASO, и вы планируете делать приложение под БК Лига Ставок. \n"
                                          "Просим быть внимательными и не оставлять вопросы без ответа. Это очень важно при принятии решения! :)",
                         parse_mode='HTML')

    # Устанавливаем значение ключа 'ask_experience_done' в True после выполнения функции
    user_data[user_id]['ask_experience_done'] = True

    log_response(datetime.now(), message.chat.id, message.from_user.first_name,
                 "Был ли у вас опыт в сфере арбитража трафика?", message.text)


@bot.message_handler(content_types=['text'])
def prev_payments(message):
    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Партнерская программа'))
    keyboard.add(KeyboardButton('Фикс. оплата'))

    if message.text == "Другие":
        remove_keyboard = telebot.types.ReplyKeyboardRemove()

        bot.send_message(message.chat.id, "Введите название вертикали, по которой есть статистика:",
                         reply_markup=remove_keyboard)
        bot.register_next_step_handler(message, send_other, keyboard)
        log_response(datetime.now(), message.chat.id, message.from_user.first_name,
                     "По работе в какой вертикали арбитража трафика имеется статистика?", message.text)
    else:
        bot.send_message(message.chat.id, "Вы работали по партнерской программе/по фиксированной оплате?",
                         parse_mode='HTML',
                         reply_markup=keyboard)
        log_response(datetime.now(), message.chat.id, message.from_user.first_name,
                     "По работе в какой вертикали арбитража трафика имеется статистика?", message.text)
        bot.register_next_step_handler(message, stat_requester)

    # log_response(datetime.now(), message.chat.id, message.from_user.first_name,
    #   "По работе в какой вертикали арбитража трафика имеется статистика?", message.text)


def send_other(message, prev_keyboard):
    # Сохраняем ответ на вопрос "Другие"
    other = message.text
    # Отправляем ответ пользователю
    bot.send_message(message.chat.id, "<code>Вы работали по партнерской программе/по фиксированной оплате?</code>",
                     parse_mode='HTML', reply_markup=prev_keyboard)
    log_response(datetime.now(), message.chat.id, message.from_user.first_name,
                 "Ответ на вопрос 'По работе в какой вертикали арбитража трафика имеется статистика?'", message.text)
    bot.register_next_step_handler(message, stat_requester)


@bot.message_handler(content_types=['text'])
def stat_requester(message):
    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Согласен'))
    if message.text == 'Партнерская программа':
        bot.send_message(message.chat.id,
                         "В конце опроса после отправки ответов, необходимо прислать статистику в формате видео по следующей инструкции:\n"
                         " 1. Войдите в ЛК;\n"
                         " 2. Перейдите в раздел статистики;\n "
                         "3. Продемонстрируйте статистику по конверсиям (ftd, std (rd), сумма депозитов, хиты/хосты, переходы, уники при наличии)\n "
                         "за различные месяцы в разрезе каждого отдельно (например, отдельно за ноябрь, за декабрь, за январь); \n"
                         "4. Статистика в идеале должна быть свежей.", parse_mode='HTML', reply_markup=keyboard)
    elif message.text == 'Фикс. оплата':
        bot.send_message(message.chat.id, "Укажите, с какой компанией работали по данной модели? "
                                          "Пришлите пример рекламной интеграции в зависимости от вашего источника трафика (скрин из группы, текст поста, ссылка на видео)",
                         reply_markup=keyboard)

    log_response(datetime.now(), message.chat.id, message.from_user.first_name,
                 "Вы работали по партнерской программе/по фиксированно оплате?", message.text)
    bot.register_next_step_handler(message, final_message)


@bot.message_handler(content_types=['text'])
def final_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    # Добавление кнопок
    keyboard.add(telebot.types.KeyboardButton("Начать с начала"))
    keyboard.add(telebot.types.KeyboardButton("Отправить ответы и приступить к отправке файлов"))

    bot.send_message(message.chat.id, "Если ваша заявка пройдет модерацию, с вами свяжется "
                                      "менеджер в течение 1-3 дней в зависимости от загруженности.\n\n"

                                      " Если менеджер с вами не связался, ваша заявка не была апрувлена по трем причинам: \n"
                                      "- низкое качество траффика по предоставленным данным; \n"
                                      "- нарушение шаблона подачи заявки: какая-то информация из требуемого списка отсутствует;\n "
                                      "- нет активных источников на руках: если вы в процессе создания источника, свяжитесь с нами по готовности (ИСКЛЮЧЕНИЕ: ваш источник трафика ASO, и вы планируете делать приложение под БК Лига Ставок. \n\n"

                                      "Просим быть внимательными и не оставлять вопросы без ответа. Это очень важно при принятии решения! :)",
                     parse_mode='HTML', reply_markup=keyboard)

    log_response(datetime.now(), message.chat.id, message.from_user.first_name, "Запрос стат-ки", message.text)

    # Устанавливаем обработчик нажатий на кнопки
    bot.register_next_step_handler(message, handle_button_click)


def handle_button_click(message):
    if message.text == "Начать с начала":
        # Перезапускаем бота с начала
        bot.clear_step_handler_by_chat_id(message.chat.id)
        start(message)
    elif message.text == "Отправить ответы и приступить к отправке файлов":
        # Отправка файла с ответами указанному пользователю
        target_user_id = 475132584  # 62667001  # Замените на ID целевого пользователя
        with open("user_responses.xlsx", "rb") as file:
            bot.send_document(chat_id=target_user_id, document=file, caption="Ответы пользователей")
            bot.send_message(message.chat.id, "Ответы отправлены, спасибо! Не забудьте отправить вложения.")
            # Удаляем обработчик следующего шага после выполнения
        # bot.clear_step_handler_by_chat_id(message.chat.id)


keep_alive()  # запускаем flask-сервер в отдельном потоке..

bot.polling(non_stop=True, interval=0)  # запуск бота
