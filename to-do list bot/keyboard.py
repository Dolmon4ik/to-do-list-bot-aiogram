from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from todolist.database import add_note
import sqlite3
con = sqlite3.connect('database.db')
cur = con.cursor()


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Мои задачи📋')],
    [KeyboardButton(text='Добавить задачу📌')],
    [KeyboardButton(text='Выполнить задачу✅')]
],
                        resize_keyboard=True,   #Уменьшает клавиатуру
                        )

def get_notes_list(id):
    result = cur.execute("SELECT note FROM notes WHERE user_id = ('{key}')".format(key = id)).fetchall()
    return [item[0] for item in result]

async def create_reply_buttons(items):
    buttons = [[KeyboardButton(text=item)] for item in items]   #Создаёт генератор списка из списка.... Да...
    buttons.append([KeyboardButton(text='Назад⬅️')])            #Добавляет к новому списку объект - кнопку
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)      #Создаёт клавиатуру из нового списка и уменьшает ее сразу
    return keyboard                                             #Возвращает клавиатуру

