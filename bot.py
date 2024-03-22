import os
import re

import telebot

bot = telebot.TeleBot('6777619680:AAHqkL1UxCTbfk4RJYl7dJOjnMx4SqPtj8o')

main_keyboards = telebot.types.InlineKeyboardMarkup()
button_sad = telebot.types.InlineKeyboardButton(text='Грустное', callback_data='sad')
button_alarm = telebot.types.InlineKeyboardButton(text='Тревожное', callback_data='alarm')
button_good = telebot.types.InlineKeyboardButton(text='Отличное', callback_data='good')
button_boring = telebot.types.InlineKeyboardButton(text='Скучное', callback_data='boring')
button_romantic = telebot.types.InlineKeyboardButton(text='Романтичное', callback_data='romantic')

main_keyboards.add(button_sad, button_alarm, button_romantic, button_boring, button_good)

current_dir = os.getcwd()

sad_dir_name = 'Грусть'
alarm_dir_name = 'Тревожность'
good_dir_name = 'Отличное'
boring_dir_name = 'Скучное'
romantic_dir_name = 'Романтика'

book_type_dir_name = {
    'sad': sad_dir_name,
    'alarm': alarm_dir_name,
    'good': good_dir_name,
    'boring': boring_dir_name,
    'romantic': romantic_dir_name
}

sad_mood = """1.Кулинарная битва.\nАвтор: Кей Джей Дель’Антониа
            \n2.Застенчивость в квадрате.\nAвтор: Сара Хоглn 
            \n3.Когда жизнь подкидывает тебе лимоны.\nАвтор: Фиона Гибсон
            \n4.Соль и сахар. Aвтор:\nРебекка Карвальо
            \n5.Когда приходит шторм.\nAвтор: Карина Шнелль
            \n6.Преступление и наказание.\nАвтор: Федор Достаевский
            """

alarm_mood = """1.Выгорание. \nАвтор: Амелия Нагоски, Эмили Нагоски
                \n2.Психология стресса. \nАвтор: Роберт Сапольски 
                \n3.Свобода от тревоги. \nАвтор: Роберт Лихи
                \n4.Дары несовершенства. \nАвтор: Брене Браун
                
               
                """

good_mood = """1.Благословение небожителей. \nAвтор: Мосян Тунсю
                \n2.Гарри Поттер и философский камень. \nАвтор: Роулинг Джоан Кэтлин
                \n3.Мара и Морок. \nАвтор: Арден Л
                \n4.Система «Спаси-себя-сам» для Главного Злодея. \nАвтор: Мосян Тунсю
                \n5.Вторая жизнь Уве. \nАвтор: Фредрик Бакман
                \n6.Шестерка воронов. \nАвтор: Ли Бардуго
                """
boring_mood = """1.Atomic Heart. Предыстория «Предприятия 3826». \nAвтор: Хорф Харальд
                \n2.Проза бродячих псов. \nAвтор: Асагири Кафка
                \n3.Шестерка воронов. \nAвтор: Бардуго Ли
                \n4.Зацепить 13-го. \nАвтор: Хлоя Уолш
                \n5.Граф Аверин. \nАвтор: Виктор Дашкевич
                \n6.Преступление и наказание. \nАвтор: Федор Достаевский
                
                """

romantic_mood = """1.К себе нежно. Книга о том, как ценить и беречь себя. \nАвтор: Примаченко Ольга
                    \n2.Когда я падаю во сне. \nАвтор: Карен Уайт
                    \n3.Влюбленные и одинокие. \nАвтор: Морган Ортен
                    \n4.Стеклянные дети. \nАвтор: Елена Ронина
                    \n5.Третья стадия. \nАвтор: Люба Макаревская
                    
                    """


def choose_book_kb(books_info, books_type):
    keyboard = telebot.types.InlineKeyboardMarkup()
    numbers = re.findall(r'^(\d+)\.', books_info, re.MULTILINE)

    buttons = []
    for i, book_info in enumerate(numbers, start=1):
        if book_info.strip():
            book_button = telebot.types.InlineKeyboardButton(text=f'Книга {i}', callback_data=f'book|{books_type}|{i}')
            buttons.append(book_button)

    buttons_per_row = 3
    button_chunks = [buttons[i:i + buttons_per_row] for i in range(0, len(buttons), buttons_per_row)]

    for chunk in button_chunks:
        keyboard.row(*chunk)

    back_button = telebot.types.InlineKeyboardButton(text='Назад', callback_data='back')
    keyboard.add(back_button)

    return keyboard


success_image_kb = telebot.types.InlineKeyboardMarkup()
button_sad = telebot.types.InlineKeyboardButton(text='Назад', callback_data='back_to_main')
button_alarm = telebot.types.InlineKeyboardButton(text='Спасибо!', callback_data='thanks')
success_image_kb.add(button_sad, button_alarm)


def get_path_to_image(folder_path, file_number):
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            number = file_name.split('_')[0]
            if number == file_number:
                return os.path.join(folder_path, file_name)
    return None


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text.lower() == "привет")
@bot.message_handler(func=lambda message: message.text.lower() == "hello")
@bot.message_handler(func=lambda message: message.text.lower() == "start")
def hello_msg(message):
    bot.send_message(message.chat.id, text=f'Привет {message.from_user.first_name}!'
                                           f'\nЯ помогу выбрать тебе книгу📚'
                                           f'\n\nПодскажи, какое у тебя настроение?',
                     reply_markup=main_keyboards)


@bot.callback_query_handler(func=lambda call: call.data.startswith('book'))
def book_call(call):
    data = call.data.split('|')
    book_type = data[1]
    book_number = data[2]
    folder_path = os.path.join(current_dir, book_type_dir_name[book_type])
    image_path = get_path_to_image(folder_path, book_number)
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text='Подожди немного. Загружаю...')
    if image_path is not None:
        with open(image_path, 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, reply_markup=success_image_kb)


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_call(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Подскажи, какое у тебя настроение?',
                          reply_markup=main_keyboards)


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main')
@bot.callback_query_handler(func=lambda call: call.data == 'thanks')
def back_to_main(call):
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=None)
    bot.send_message(chat_id=call.message.chat.id,
                     text='Подскажи, какое у тебя настроение?',
                     reply_markup=main_keyboards)


@bot.callback_query_handler(func=lambda call: call.data == 'sad')
def sad_call(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Книги под грустное настроение:\n\n' + sad_mood,
                          reply_markup=choose_book_kb(sad_mood, 'sad'))


@bot.callback_query_handler(func=lambda call: call.data == 'good')
def good_call(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Книги под хорошее настроение:\n\n' + good_mood,
                          reply_markup=choose_book_kb(good_mood, 'good'))


@bot.callback_query_handler(func=lambda call: call.data == 'alarm')
def alarm_call(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Книги под тревожное настроение:\n\n' + alarm_mood,
                          reply_markup=choose_book_kb(alarm_mood, 'alarm'))


@bot.callback_query_handler(func=lambda call: call.data == 'boring')
def boring_call(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Следует почитать когда скучно:\n\n' + boring_mood,
                          reply_markup=choose_book_kb(boring_mood, 'boring'))


@bot.callback_query_handler(func=lambda call: call.data == 'romantic')
def romantic_call(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Книги под романтичное настроение:\n\n' + romantic_mood,
                          reply_markup=choose_book_kb(romantic_mood, 'romantic'))


if __name__ == '__main__':
    print("start")
    bot.infinity_polling(allowed_updates=None)
