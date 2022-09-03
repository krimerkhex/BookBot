# Header:
# Файл содержит в себе взаимодействие с БД

import sqlite3


def find_login(chat_id):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT COUNT(*) FROM users WHERE chat_id = '" + str(chat_id) + "'"
    cursor.execute(tmp)
    res = cursor.fetchone()
    print(res[0])
    cursor.close()
    if res[0] == 1:
        return True
    else:
        return False


def add_user(chat_id, login_, campus_, type_):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "INSERT INTO users (chat_id, login, campus, type) VALUES (" + str(chat_id) + ", '" \
          + login_ + "', '" + campus_ + "', '" + type_ + "')"
    try:
        cursor.execute(tmp)
    except sqlite3.IntegrityError:
        cursor.close()
        con.close()
        return False
    else:
        con.commit()
        cursor.close()
        con.close()
        return True


def get_campus(chat_id):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT campus FROM users WHERE chat_id = '" + str(chat_id) + "'"
    cursor.execute(tmp)
    res = cursor.fetchone()
    cursor.close()
    con.close()
    return res[0]


def get_type(chat_id):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT type FROM users WHERE chat_id = '" + str(chat_id) + "'"
    cursor.execute(tmp)
    res = cursor.fetchone()
    cursor.close()
    con.close()
    return res[0]


def get_login(chat_id):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT login FROM users WHERE chat_id = '" + str(chat_id) + "'"
    cursor.execute(tmp)
    res = cursor.fetchone()
    cursor.close()
    con.close()
    return res[0]


def add_booking(login_, object_id_, time_start_, time_end_, campus_):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "INSERT INTO book_list (user_id, object_id, time_start, time_end, status, campus)\
    VALUES ((SELECT id FROM users WHERE login = '" + login_ + "'), " + str(object_id_) + ", '" \
          + time_start_ + "', '" + time_end_ + "', 2, '" + campus_ + "')"
    try:
        cursor.execute(tmp)
    except sqlite3.IntegrityError:
        cursor.close()
        con.close()
        return False
    else:
        con.commit()
        cursor.close()
        con.close()
        return True


def get_object_id(object_name_):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT id FROM objects WHERE object_name = '" + object_name_ + "'"
    cursor.execute(tmp)
    res = cursor.fetchone()
    cursor.close()
    con.close()
    return res[0]


def get_my_bookings(chat_id):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT book_list.id, objects.object_name, book_list.time_start, book_list.time_end, book_list.status\
    FROM book_list JOIN objects\
    ON book_list.object_id = objects.id\
    WHERE book_list.user_id = (SELECT id\
    FROM users\
    WHERE chat_id = '" + str(chat_id) + "')"
    cursor.execute(tmp)
    res = cursor.fetchall()
    if res == None:
        res = 0
    cursor.close()
    con.close()
    return res


def get_all_bookings(campus_):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT book_list.id, users.login, object_types.name, objects.object_name, \
    book_list.time_start, book_list.time_end, book_list.status \
    FROM book_list JOIN users ON book_list.user_id = users.id \
    JOIN objects ON book_list.object_id = objects.id \
    JOIN object_types ON objects.object = object_types.id \
    WHERE book_list.status = 1 AND book_list.campus = '" + campus_ + "'  \
    ORDER BY book_list.time_start"
    cursor.execute(tmp)
    res = cursor.fetchall()
    if res == None:
        res = 0
    cursor.close()
    con.close()
    return res


def update_status(book_id_, status_):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "UPDATE book_list SET status = " + status_ + " WHERE id = " + book_id_
    try:
        cursor.execute(tmp)
    except sqlite3.IntegrityError:
        cursor.close()
        con.close()
        return False
    else:
        con.commit()
        cursor.close()
        con.close()
        return True


def delete_booking(book_id_, chat_id):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "DELETE FROM book_list\
    WHERE id = " + str(book_id_) + " AND user_id = (SELECT id FROM users WHERE chat_id = " + str(chat_id) + ")"
    try:
        cursor.execute(tmp)
    except sqlite3.IntegrityError:
        cursor.close()
        con.close()
        return False
    else:
        con.commit()
        cursor.close()
        con.close()
        return True


def get_waiting_list(campus_):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT book_list.id, users.login, object_types.name, objects.object_name, \
        book_list.time_start, book_list.time_end, book_list.status \
        FROM book_list JOIN users ON book_list.user_id = users.id \
        JOIN objects ON book_list.object_id = objects.id \
        JOIN object_types ON objects.object = object_types.id \
        WHERE book_list.status = 2 AND book_list.campus = '" + campus_ + "'  \
        ORDER BY book_list.time_start"
    cursor.execute(tmp)
    res = cursor.fetchall()
    if res == None:
        res = 0
    cursor.close()
    con.close()
    return res


def get_object_type_list():
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = 'SELECT name FROM object_types'
    cursor.execute(tmp)
    res = cursor.fetchall()
    cursor.close()
    con.close()
    return res


def get_object_name_list(type_, campus_):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT objects.object_name FROM objects \
    JOIN object_types ON object_types.id = objects.object \
    WHERE object_types.type = '" + type_ + "' AND objects.campus = '" + campus_ + "'"
    cursor.execute(tmp)
    res = cursor.fetchall()
    cursor.close()
    con.close()
    return res


def get_object_info(obj_id_):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT info FROM object_types \
    WHERE id = " + str(obj_id_)
    cursor.execute(tmp)
    res = cursor.fetchall()
    cursor.close()
    con.close()
    return res


def get_range_of_mybook_list(chat_id):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT COUNT(*)\
        FROM book_list JOIN objects\
        ON book_list.object_id = objects.id\
        WHERE book_list.user_id = (SELECT id\
        FROM users\
        WHERE chat_id = '" + str(chat_id) + "')"
    cursor.execute(tmp)
    res = cursor.fetchone()
    cursor.close()
    con.close()
    return res[0]


def add_object(object_, object_name_, campus_):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "INSERT INTO objects (object, object_name, campus) \
          VALUES (" + object_ + ", '" + object_name_ + "', '" + campus_ + "')"
    try:
        cursor.execute(tmp)
    except sqlite3.IntegrityError:
        cursor.close()
        con.close()
        return False
    else:
        con.commit()
        cursor.close()
        con.close()
        return True


def get_info_for_buttons(campus_):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT name, type FROM object_types"
    cursor.execute(tmp)
    res = cursor.fetchall()
    cursor.close()
    con.close()
    return res


def get_object_type_id(name_):
    con = sqlite3.connect('Dataset/book_bot.db')
    cursor = con.cursor()
    tmp = "SELECT id FROM object_types WHERE type ='" + name_ + "'"
    cursor.execute(tmp)
    res = cursor.fetchone()
    cursor.close()
    con.close()
    return res[0]
