
import telebot
import telegram
import openpyxl
from openpyxl import Workbook
import telegram.ext
import types
from telegram.ext import Updater, MessageHandler, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telebot
import openpyxl
from openpyxl import Workbook
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
bot.delete_webhook()


# функция для записи ответа пользователя в Excel файл
def log_response(timestamp,user_id,first_name, question, response):
    row = (timestamp,user_id, first_name, question, response)
    sheet.append(row)
    workbook.save("user_responses.xlsx")

@bot.message_handler(commands = ['start'])
def start(message):
    # Создаем клавиатуру Да/Нет
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Да, продолжить'))
    #keyboard.add(KeyboardButton('Нет'))

    # Отправляем приветственное сообщение с клавиатурой Да/Нет
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Мы очень рады видеть тебя здесь! "
                                      f"Чтобы скорее начать работу, пройди несколько несложных шагов. Готов начать?",
                     reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Да, продолжить")
def ask_email(message):
    # Отправляем вопрос "Какая у вас почта?" и ждем ответа
    bot.send_message(message.chat.id, "Укажите почту, на которую вы регистрировались")
    bot.register_next_step_handler(message, ask_traffic_source)
    log_response(datetime.now(),message.chat.id, message.from_user.first_name, "Готовность", message.text)

    #save_to_excel(message) # add this line

# Обработчик ответа на вопрос "Какая у вас почта?"
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
    bot.send_message(message.chat.id, "Укажите источник трафика, с которым планируете работать:", reply_markup=keyboard)
    log_response(datetime.now(), message.chat.id, message.from_user.first_name, "Укажите почту, на которую вы регистрировались", message.text)

    #Ответы кнопок:
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # получаем ID чата, из которого пришел запрос
    chat_id = call.message.chat.id

    # проверяем, какую кнопку нажал пользователь
    if call.data == 'seo':
        # если пользователь нажал кнопку "Да", отправляем сообщение "Вы нажали Да"
        bot.send_message(chat_id, "Укажите ссылку на сайт, прикрепите статистику по посещаемости сайта, опишите,как планируете рекламировать БК «Лига Ставок»: баннер, рейтинг и т.д.")
        #save_to_excel(call)  # add this line
        #bot.register_next_step_handler(message, ask_experience)
    elif call.data == 'aso':
        # если пользователь нажал кнопку "Нет", отправляем сообщение "Вы нажали Нет"
        bot.send_message(chat_id, "Укажите ссылку на приложение, место в рейтинге. "
                                      "Если планируете делать брендовое приложение - опишите его вид, механику и т.д., "
                                      "примерно сроки реализации")
        #save_to_excel(call)
    elif call.data == 'no_active':
        # если пользователь нажал кнопку "Нет", отправляем сообщение "Вы нажали Нет"
        bot.send_message(chat_id, "В данный момент мы не можем с вами сотрудничать.")
      #  save_to_excel(call)
        bot.stop_bot()
    elif call.data == "context ad":
        bot.send_message(call.message.chat.id, "Укажите, по каким ключам планируете запускать рекламу, где? При запуске через ЯД, пришлите статистику из ЛК ЯД")
        #save_to_excel(call)
    elif call.data == "social":
        bot.send_message(call.message.chat.id, "Укажите, являетесь ли вы владельцем сообщества/ планируете закупать рекламу. Прикрепите ссылки. Если это группа ВК - пришлите статистику по охватам")
      #  save_to_excel(call)
    elif call.data == "streaming":
        bot.send_message(call.message.chat.id, "Укажите ссылки на стримы, прикрепите портфолио с опытом в сфере стрим-индустрии")
      #  save_to_excel(call)
    elif call.data == "youtube":
        bot.send_message(call.message.chat.id, "Укажите ссылку на ютуб канал/каналы, пришлите статистику по охватам")
    #    save_to_excel(call)
    elif call.data == "others":
        bot.send_message(call.message.chat.id, "Укажите источник самостоятельно")
     #   save_to_excel(call)
    log_response(datetime.now(), call.message.chat.id, call.from_user.first_name, "Источник трафика", call.data)



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
        # Отправ
        # ляем вопрос "Какая у вас почта?" и ждем ответа
        bot.send_message(message.chat.id, "В какой вертикали имеется статистика?")
        bot.register_next_step_handler(message, stat_requester)

    #    save_to_excel(message)
        #bot.register_next_step_handler(message, ask_traffic_source)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Жаль, что у вас нет опыта. В данный момент мы не можем с вами сотрудничать.")
     #   save_to_excel(message)
        bot.stop_bot()
    # Сохраняем данные пользователя в файл# Сохраняем данные пользователя в файл

    log_response(datetime.now(), message.chat.id, message.from_user.first_name, "Был ли у вас опыт в сфере арбитража трафика?", message.text)

@bot.message_handler(content_types=['text'])
def stat_requester(message):
    bot.send_message(message.chat.id, "Необходимо прислать статистику в формате видео по следующей инструкции:"
                                      " 1. Войдите в ЛК;"
                                      " 2. Перейдите в раздел статистики; "
                                      "3. Продемонстрируйте статистику по конверсиям (ftd, std (rd), сумма депозитов, хиты/хосты, переходы, уники при наличии) "
                                      "за различные месяцы в разрезе каждого отдельно (например, отдельно за ноябрь, за декабрь, за январь); "
                                      "4. Статистика в идеале должна быть свежей.")
    log_response(datetime.now(), message.chat.id, message.from_user.first_name, "В какой вертикали имеется стат-ка?", message.text)
    bot.register_next_step_handler(message, final_message)
@bot.message_handler(content_types=['text'])
def final_message(message):
    bot.send_message(message.chat.id, "Если ваша заявка пройдет модерацию, с вами свяжется "
                                      "менеджер в течение 1-3 дней в зависимости от загруженности."
                                      " Если менеджер с вами не связался, ваша заявка не была апрувлена по трем причинам: "
                                      "- низкое качество траффика по предоставленным данным; "
                                      "- нарушение шаблона подачи заявки: какая-то информация из требуемого списка отсутствует; "
                                      "- нет активных источников на руках: если вы в процессе создания источника, свяжитесь с нами по готовности (ИСКЛЮЧЕНИЕ: ваш источник трафика ASO, и вы планируете делать приложение под БК Лига Ставок. "
                                      "Просим быть внимательными и не оставлять вопросы без ответа. Это очень важно при принятии решения! :)")
    log_response(datetime.now(), message.chat.id, message.from_user.first_name, "Запрос стат-ки", message.text)

    bot.stop_bot()


bot.polling(none_stop=True)