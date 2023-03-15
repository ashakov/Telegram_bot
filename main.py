import telebot
#import telegram
#from telegram.ext import Updater, MessageHandler, Filters

bot = telebot.TeleBot('6100483283:AAGAXER5F5lEn7f_vZaRc0Ofsik_UoPZ8H4')
bot.delete_webhook()
@bot.message_handler(commands = ['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}, Мы очень рады видеть тебя здесь! ' \
           f'Чтобы скорее начать работу, пройди несколько несложных шагов. Готов начать? (Да,Нет)</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')

    keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');  # кнопка «Да»
    keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    bot.send_message(message.from_user.id, text="Принято", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == "Да":
        global email;
        email = message.text;
        bot.send_message(message.from_user.id, text='Укажите почту, на которую вы регистрировались', reply_markup=keyboard);
        bot.register_next_step_handler(message, get_user_text);
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Возвращайтесь по готовности", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Проверьте ответ", parse_mode='html')







bot.polling(none_stop=True)