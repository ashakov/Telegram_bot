import telebot
import telegram
import openpyxl
from openpyxl import Workbook
import telegram.ext
import types
from telegram.ext import Updater, MessageHandler, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# rest of the code here
import telebot
import openpyxl
from openpyxl import Workbook
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import types


bot = telebot.TeleBot('6100483283:AAGAXER5F5lEn7f_vZaRc0Ofsik_UoPZ8H4')
bot.delete_webhook()
@bot.message_handler(commands = ['start'])
def start(message):
    # Создаем клавиатуру Да/Нет
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Да'))
    keyboard.add(KeyboardButton('Нет'))

    # Отправляем приветственное сообщение с клавиатурой Да/Нет
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Мы очень рады видеть тебя здесь! "
                                      f"Чтобы скорее начать работу, пройди несколько несложных шагов. Готов начать?",
                     reply_markup=keyboard)
@bot.message_handler(func=lambda message: message.text == "Да")
def ask_email(message):
    # Отправляем вопрос "Какая у вас почта?" и ждем ответа
    bot.send_message(message.chat.id, "Какая у вас почта?")
    bot.register_next_step_handler(message, ask_traffic_source)


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

    # Отправляем вопрос "Выберите источник трафика" с клавиатурой
    bot.send_message(message.chat.id, "Выберите источник трафика:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "SEO")
def ask_link(message):
    # Отправляем вопрос "Какая у вас почта?" и ждем ответа
    bot.send_message(message.chat.id, "Укажите ссылку на сайт, прикрепите статистику по посещаемости сайта, опишите,как планируете рекламировать БК «Лига Ставок»: баннер, рейтинг и т.д.")
    bot.register_next_step_handler(message, ask_experience)


# Обработчик ответа на вопрос "Выберите источник трафика"
@bot.callback_query_handler(func=lambda call: True)
def ask_experience(call):
    # Сохраняем ответ на вопрос "Выберите источник трафика"
    traffic_source = call.data

    # Создаем клавиатуру Да/Нет
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Да'))
    keyboard.add(KeyboardButton('Нет'))

    # Отправляем вопрос "Был ли у вас опыт в сфере арбитража трафика?" с клавиатурой Да/Нет
    bot.send_message(call.message.chat.id, "Был ли у вас опыт в сфере арбитража трафика?", reply_markup=keyboard)
    bot.register_next_step_handler(call.message, send_statistics, traffic_source)

@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def send_statistics(call):
    user_id = call.message.chat.id
    answer = 'Да' if call.data == 'yes' else 'Нет'
    user_data['has_experience'] = answer
    if answer == 'Да':
        message = 'Отлично! Укажите ссылку на сайт, прикрепите статистику по посещаемости сайта, опишите, как планируете рекламировать БК «Лига Ставок»: баннер, рейтинг и т.д.'
        bot.send_message(user_id, message)
    else:
        message = 'Жаль, что у вас нет опыта. В данный момент мы не можем с вами сотрудничать.'
        bot.send_message(user_id, message)

# Сохраняем данные пользователя в файл
    save_user_data(user_data)
# Удаляем сообщение с вопросом
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id)

#@bot.message_handler(content_types=['text'])
#def get_user_text(message):
#    if message.text == "Да":
#        global email;
#       email = message.text;
#        bot.send_message(message.from_user.id, text='Укажите почту, на которую вы регистрировались');
 #       bot.register_next_step_handler(message, get_user_text);
#    elif message.text == "Нет":
  #      bot.send_message(message.chat.id, "Возвращайтесь по готовности", parse_mode='html')
   # else:
   #     bot.send_message(message.chat.id, "Проверьте ответ", parse_mode='html')

bot.polling(none_stop=True)