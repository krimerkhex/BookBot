# bot = telebot.TeleBot("5533579119:AAHtcL9aKrZESemtIp0w8K-6NXb2s6j-mLg")

import telebot
from telebot import types

# import kernel
import dal

login = ""
camp = ""
pas = ""
chat_id = ""
chose = ""
start_time = ""
end_time = ""
bidi = 2
messa = telebot.types.Message

bot = telebot.TeleBot("5533579119:AAHtcL9aKrZESemtIp0w8K-6NXb2s6j-mLg")

START_MESSAGE = 'Это бот для бронированая разных элементов Школы 21.\nОн написан силами:\n' \
                '->hashtagr@student.21-school.ru\n->karleneg@student.21-school.ru\n' \
                'В случае обнаружения багов или помощью в\n' \
                'разработке обращайтесь по указанным электронным адресам.\n' \
                'Для получения информации /help\n'


@bot.message_handler(commands=['start'])
def SendHello(message):
    bot.reply_to(message, START_MESSAGE)
    print(message)
    global chat_id, messa
    messa = message
    chat_id = message.chat.id
    flag = dal.find_login(chat_id)
    if flag:
        bot.send_message(chat_id, text="Пользователь авторизован")
        give_menu()
    else:
        bot.send_message(chat_id, text="Давайте начнем регистрацию,\n"
                                       "Введите ваш логин:")
        bot.register_next_step_handler(message, get_login)


def check_login(message):
    global chat_id
    flag = dal.find_login(chat_id)
    if flag:
        bot.send_message(chat_id, text="Пользователь авторизован")
        give_menu()
    else:
        bot.send_message(chat_id, text="Давайте начнем регистрацию\n"
                                       "Введите ваш логин:")
        bot.register_next_step_handler(message, get_login)


@bot.message_handler(commands=(['regist']))
def registry(message):
    global chat_id
    chat_id = message.chat.id
    bot.send_message(chat_id, text="Давайте начнем регистрацию,\n"
                                   "Введите ваш логин:")
    bot.register_next_step_handler(message, get_login)


def get_login(message):
    if check_valid(message.text):
        global login
        login = message.text
        print(login)
        bot.send_message(message.chat.id, text="Введите пароль доступа(получите его у администрации):")
        bot.register_next_step_handler(message, get_pass)
    else:
        bot.send_message(message.chat.id, text="Регистрация провалена")
        check_login(message)


def get_pass(message):
    if check_valid(message.text):
        global pas
        pas = message.text
        print(pas)
        bot.send_message(chat_id, text="Введите кампус:", reply_markup=types.InlineKeyboardMarkup(row_width=3).add(
            types.InlineKeyboardButton(text='MSK', callback_data='msk'),
            types.InlineKeyboardButton(text='KZN', callback_data='kzn'),
            types.InlineKeyboardButton(text='NSK', callback_data='nsk')
        ))
    else:
        bot.send_message(message.chat.id, text="Регистрация провалена")
        check_login(message)


def type_parser(password):
    user_type = ""
    if password == "adm":
        user_type = "ADM"
    elif password == "stu":
        user_type = "STU"
    elif password == "abi":
        user_type = "ABI"
    return user_type


def get_camp():
    global login, pas, camp, chat_id, messa
    print(login, pas, camp)
    if pas in ["adm", "stu", "abi"] and camp in ['MSK', 'KZN', 'NSK']:
        user_type = type_parser(pas)
        if dal.add_user(chat_id=str(chat_id), login_=str(login), campus_=str(camp),
                        type_=user_type):
            give_menu()
        else:
            bot.send_message(chat_id=chat_id, text="Ошибка регистрации")
            registry()
    else:
        check_login(messa)


@bot.message_handler(commands=(['menu']))
def give_menu():
    global chat_id, camp
    camp = dal.get_campus(chat_id)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🆕 Добавить бронирование')
    btn2 = types.KeyboardButton('ℹ️ Просмотр моих бронирований')
    if dal.get_type(chat_id) == 'ADM':
        btn3 = types.KeyboardButton('✅ Просмотр всех подтвержденных бронирований в кампусе')
        btn4 = types.KeyboardButton('‼️ Просмотр листа ожидания подтверждения')
        btn5 = types.KeyboardButton('➕ Добавить новый объект бронирования')
        kb.add(btn1, btn2, btn3, btn4, btn5)
    else:
        kb.add(btn1, btn2)
    bot.send_message(chat_id, text="Выбери действие из меню ниже:", reply_markup=kb)


def add_booking():
    global chat_id
    item_speak = types.InlineKeyboardButton(text="Переговорная комната", callback_data="speak")
    item_sport = types.InlineKeyboardButton(text="Спортивный инвентарь", callback_data="sport")
    item_bg = types.InlineKeyboardButton(text="Настольные игры", callback_data="boardgm")
    item_kich = types.InlineKeyboardButton(text="Кухни", callback_data="kitch")
    markup = types.InlineKeyboardMarkup(row_width=1).add(item_sport, item_bg, item_speak, item_kich)
    bot.send_message(chat_id=chat_id, text='К какой категории относится интересующий вас объект?',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda message: True)
def GetUserObjectName(call):
    global camp, chat_id, o_type, o_name

    if call.data == 'speak':
        name_list = dal.get_object_name_list("conf_room", camp)
        message_text = ''
        for arr in name_list:
            message_text += "- " + arr[0] + "\n"
        bot.send_message(chat_id, text='Какую переговорку выберете? Отправьте сообщение с \
        одним из пунктов списка ниже')
        bot.send_message(chat_id, text=message_text)
        bot.register_next_step_handler(call.message, get_chose)

    elif call.data == 'sport':
        name_list = dal.get_object_name_list("sport_equ", camp)
        message_text = ''
        for arr in name_list:
            message_text += "- " + arr[0] + "\n"
        bot.send_message(chat_id, text='Какой спортивный инвентарь выберете? Отправьте сообщение с \
        одним из пунктов списка ниже')
        bot.send_message(chat_id, text=message_text)
        bot.register_next_step_handler(call.message, get_chose)

    elif call.data == 'boardgm':
        name_list = dal.get_object_name_list("board_game", camp)
        bot.send_message(chat_id, text='Какую настольную игру выберете?\nОтправьте сообщение с \
        одним из пунктов списка ниже')
        message_text = ''
        for arr in name_list:
            message_text += "- " + arr[0] + "\n"
        bot.send_message(chat_id, text=message_text)
        bot.register_next_step_handler(call.message, get_chose)

    elif call.data == 'kitch':
        name_list = dal.get_object_name_list("kitchen", camp)
        message_text = ''
        for arr in name_list:
            message_text += "- " + arr[0] + "\n"
        bot.send_message(chat_id, text='Кухню какого этажа выберете?\nОтправьте сообщение с \
        одним из пунктов списка ниже')
        bot.send_message(chat_id, text=message_text)
        bot.register_next_step_handler(call.message, get_chose)

    elif call.data == 'access':
        bot.send_message(chat_id, text='Укажите id бронирования')
        bot.register_next_step_handler(call.message, get_access)

    elif call.data == 'delete':
        bot.send_message(chat_id, text='Укажите id бронирования')
        bot.register_next_step_handler(call.message, delete_any_booking)

    elif call.data == 'conf_room':
        o_type = str(call.data)
        bot.send_message(chat_id, text="Введите имя объекта:")
        bot.register_next_step_handler(call.message, add_new_object_end)

    elif call.data == 'kitchen':
        o_type = str(call.data)
        bot.send_message(chat_id, text="Введите имя объекта:")
        bot.register_next_step_handler(call.message, add_new_object_end)

    elif call.data == 'sport_equ':
        o_type = str(call.data)
        bot.send_message(chat_id, text="Введите имя объекта:")
        bot.register_next_step_handler(call.message, add_new_object_end)

    elif call.data == 'board_game':
        o_type = str(call.data)
        bot.send_message(chat_id, text="Введите имя объекта:")
        bot.register_next_step_handler(call.message, add_new_object_end)

    elif call.data == 'msk':
        camp = 'MSK'
        get_camp()

    elif call.data == 'kzn':
        camp = 'KZN'
        get_camp()

    elif call.data == 'nsk':
        camp = 'NSK'
        get_camp()


def get_access(message):
    global bidi
    bidi = message.text
    bot.send_message(chat_id, text='Укажите статус для бронирования:\n'
                                   '0 - Бронирование не принято\n'
                                   '1 - Бронирование принято\n'
                                   '2 - Ожидание рассмотрения')
    bot.register_next_step_handler(message, get_status)


def get_status(message):
    print("IN get_status")
    global bidi, chat_id
    if dal.update_status(str(bidi), str(message.text)):
        bot.send_message(chat_id,
                         text=f'Статус бронирования №{str(bidi)} изменен на {status_parser(int(message.text))}')
    else:
        bot.send_message(chat_id, text='Статус не изменен')


def delete_any_booking(message):
    global chat_id
    if dal.delete_booking(message.text, chat_id):
        bot.send_message(chat_id, text=f'Бронирование под id{message.text}: Удалено')
    else:
        bot.send_message(chat_id, text='Ошибка удаления')


def get_chose(message):
    global chose, camp, chat_id
    name_list = []
    for arr in dal.get_object_name_list("sport_equ", camp):
        name_list.append(arr[0])
    for arr in dal.get_object_name_list("conf_room", camp):
        name_list.append(arr[0])
    for arr in dal.get_object_name_list("kitchen", camp):
        name_list.append(arr[0])
    for arr in dal.get_object_name_list("board_game", camp):
        name_list.append(arr[0])
    chose = message.text
    if chose in name_list:
        bot.send_message(chat_id, text='Укажите время начала бронирования в формате ГГГГ-ММ-ДД ЧЧ:ММ :')
        bot.register_next_step_handler(message, get_time_start)
    else:
        bot.send_message(chat_id, text='Бронирование провалено')


def get_time_start(message):
    global start_time
    start_time = message.text
    bot.send_message(chat_id, text='Укажите окончания бронирования в формате ГГГГ-ММ-ДД ЧЧ:ММ :')
    bot.register_next_step_handler(message, get_time_end)


def get_time_end(message):
    global end_time, start_time, chose
    end_time = message.text
    if dal.add_booking(dal.get_login(message.chat.id), dal.get_object_id(chose), start_time, end_time,
                       dal.get_campus(message.chat.id)):
        bot.send_message(chat_id, text='Бронирование создано')
    else:
        bot.send_message(chat_id, text='Ошибка бронирования')


def status_parser(num):
    if num == 0:
        return "Не подтверждено."
    elif num == 1:
        return "Подтверждено."
    elif num == 2:
        return "Ожидание."


def watch_my_bookings():
    global chat_id
    book_list = dal.get_my_bookings(chat_id)
    if book_list != 0:
        message_text = ''
        for row in range(dal.get_range_of_mybook_list(chat_id)):
            message_line = "Бронирование №" + str(book_list[row][0]) + ": " + book_list[row][1] + \
                           " с " + book_list[row][2] + " до " + book_list[row][3] + ". Статус бронирования: " + \
                           status_parser(book_list[row][4]) + "\n\n"
            message_text += message_line
        bot.send_message(chat_id, text=message_text, reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text='Удалить бронирование', callback_data='delete')))
    else:
        bot.send_message(chat_id, text='У вас нет бронирований')


def watch_all_bookings(campus):
    global chat_id
    book_list = dal.get_all_bookings(campus)
    message_text = ''
    list_range = len(book_list)
    if list_range != 0:
        for row in range(list_range):
            message_line = "book_id " + str(book_list[row][0]) + ": " + book_list[row][1] + " забронировал(а) " + \
                           book_list[row][2] + " " + book_list[row][3] + " с " + book_list[row][4] + " по " + \
                           book_list[row][5] + ", статус: " + status_parser(book_list[row][6]) + "\n\n"
            message_text += message_line
    else:
        message_text = "В вашем кампусе нет подвержденных бронирований"
    bot.send_message(chat_id, text=message_text)


def watch_waiting_list(campus):
    global chat_id
    book_list = dal.get_waiting_list(campus)
    message_text = ''
    list_range = len(book_list)
    if list_range != 0:
        for row in range(list_range):
            message_line = "book_id " + str(book_list[row][0]) + ": " + book_list[row][1] + \
                           " ожидает подтверждения бронирования " + \
                           book_list[row][2] + " " + book_list[row][3] + " с " + book_list[row][4] + " по " + \
                           book_list[row][5] + "\n\n"
            message_text += message_line
    else:
        message_text = "Лист ожидания пуст"
    kb = types.InlineKeyboardMarkup()
    btn_a = types.InlineKeyboardButton(text='Подтвердить бронирование', callback_data='access')
    btn_b = types.InlineKeyboardButton(text='Удаление бронирования', callback_data='delete')
    kb.add(btn_a, btn_b)
    bot.send_message(chat_id, text=message_text, reply_markup=kb)


o_type = ''
o_name = ''
o_info = ''


def add_new_object_type():
    global chat_id
    btn1 = types.InlineKeyboardButton(text='Переговорка', callback_data='conf_room')
    btn2 = types.InlineKeyboardButton(text='Кухня', callback_data='kitchen')
    btn3 = types.InlineKeyboardButton(text='Спортивный инвентарь', callback_data='sport_equ')
    btn4 = types.InlineKeyboardButton(text='Настольная игра', callback_data='board_game')
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(btn1, btn2, btn3, btn4)
    bot.send_message(chat_id, text="Выберите тип объекта:", reply_markup=kb)


def add_new_object_end(message):
    global o_type, o_name, camp
    o_name = message.text
    if dal.add_object(str(dal.get_object_type_id(o_type)), o_name, camp):
        bot.send_message(chat_id, text="Запись прошла успешно")
    else:
        bot.send_message(chat_id, text="Что-то пошло не так, попробуйте еще раз")


@bot.message_handler(content_types=['text'])
def menu_engine(message):
    global chat_id, camp
    chat_id = message.chat.id
    camp = dal.get_campus(chat_id)
    if message.text == '🆕 Добавить бронирование':
        add_booking()
    elif message.text == 'ℹ️ Просмотр моих бронирований':
        watch_my_bookings()
    elif message.text == '✅ Просмотр всех подтвержденных бронирований в кампусе':
        if dal.get_type(chat_id) == 'ADM':
            watch_all_bookings(dal.get_campus(chat_id))
        else:
            bot.send_message(chat_id, text="⛔️ У вас нет прав доступа")
    elif message.text == '‼️ Просмотр листа ожидания подтверждения':
        if dal.get_type(chat_id) == 'ADM':
            watch_waiting_list(dal.get_campus(chat_id))
        else:
            bot.send_message(chat_id, text="⛔️ У вас нет прав доступа")
    elif message.text == '➕ Добавить новый объект бронирования':
        if dal.get_type(chat_id) == 'ADM':
            add_new_object_type()
        else:
            bot.send_message(chat_id, text="⛔️ У вас нет прав доступа")


def check_valid(string):
    chars = [chr(i) for i in range(97, 123)]
    flag = True
    for i in string:
        if i not in chars:
            flag = False
            break
    return flag
