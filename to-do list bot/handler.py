from aiogram import Bot, Dispatcher, types, html, F, Router
from aiogram.filters import CommandStart, Command
import datetime
import keyboard as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from todolist.keyboard import create_reply_buttons, get_notes_list
from todolist import database as db
router = Router()


class TaskStates(StatesGroup):
    choosing_task = State()

class Taskadd(StatesGroup):
    task_add = State()



class commands:      # Класс команд (/start)
    @router.message(CommandStart())         #роутер, который принимает только команды / от пользователя
    async def start(message: types.Message):      #асинхронная функция - обработчик команд

        try:                # Метод try. В случае ошибки, программа не ляжет, а выполнит except
            await db.add_id(message.from_user.id)
            await message.answer('Привет. Это бот - ежедневник. Здесь ты сможешь'
                                'закрепить свои задачи, отмечать их выполнение и добавлять' #После сообщения пользователя ответит и выведет клавиатуру main из kb
                                'новые задачи!', reply_markup=kb.main)


        except Exception as error:              # Если возникает ошибка, то закидывает ошибку в переменную e
            await message.answer(f'Ошибка выполнения команды. Обратитесь к @Dolmon4ik \nОшибка: {str(error)}"') # Выводит пользователю ошибку

class buttons:      #Класс функций, принимающий данные с кнопок

    @router.message(F.text == "Мои задачи📋")        #Роутер с фильтром. Функция ниже выполняется, если пользователь нажал на "Мои задачи📋"
    async def my_notes(message: types.Message):         #Асинхронная функция - обработчик
        try:
            notes_list = get_notes_list(message.from_user.id)
            keyboard = await create_reply_buttons(notes_list)     #Переменная keyboard, принимающая значения из функции keyboard.create_reply_buttons
            await message.answer('Твои задачи', reply_markup=keyboard)  #Отвечает пользователю сообщением "Твои задачи" и выводит клавиатуру с задачами
        except Exception as error:
            await message.answer(f'Ошибка выполнения команды. Обратитесь к @Dolmon4ik \nОшибка: {str(error)}"')

    @router.message(F.text == "Назад⬅️")
    async def back(message: types.Message):

        try:
            await message.answer('Главное меню', reply_markup=kb.main)

        except Exception as error:
            await message.answer(f'Ошибка выполнения команды. Обратитесь к @Dolmon4ik \nОшибка: {str(error)}"')

    @router.message(F.text == 'Выполнить задачу✅')
    async def remove(message: types.Message, state: FSMContext):    ######
        try:
            notes_list = get_notes_list(message.from_user.id)
            keyboard = await create_reply_buttons(notes_list)
            await message.answer('Выбери задачу, которую хочешь выполнить / удалить', reply_markup=keyboard)
            await state.set_state(TaskStates.choosing_task) #После выполнения функции устанавливает статус choosing_task
        except Exception as error:
            await message.answer(f'Ошибка выполнения команды. Обратитесь к @Dolmon4ik \nОшибка: {str(error)}"')

    @router.message(TaskStates.choosing_task)       #Выполняет функцию ниже, если статус == choosing_task
    async def removing(message: types.Message, state: FSMContext):
        try:
            notes_list = get_notes_list(message.from_user.id)

            if message.text in notes_list:                                              #Если сообщение пользователя содержит строку, которая == объекту в листе, то
                notes_list.remove(message.text)                                         #удаляет эту строку из листа и
                await db.remove_note(str(message.text), message.from_user.id)
                await message.answer('Задача выполнена✅', reply_markup=kb.main)   #отвечает пользователю, что задача выполнена (удалена из списка) и
                await  state.clear()                                                    #очищает статус

            elif message.text ==  'Назад⬅️':                                            #либо если пользователь нажал кнопку Назад⬅️, то
                await message.answer('Главное меню', reply_markup=kb.main)          #Перекидывает на главное меню и
                await state.clear()                                                      #очищает статус

            else:                                                                        #либо
                await message.answer('Пожалуйста, выберите задачу из списка.')           #Просит выбрать задачу, которая подходит
        except Exception as error:
            await message.answer(f'Ошибка выполнения команды. Обратитесь к @Dolmon4ik \nОшибка: {str(error)}"')

    @router.message(F.text == 'Добавить задачу📌')
    async def addtask(message: types.Message, state: FSMContext):
        try:
            await message.answer('Введи название для новой задачи')
            await state.set_state(Taskadd.task_add)
        except Exception as error:
            await message.answer(f'Ошибка выполнения команды. Обратитесь к @Dolmon4ik \nОшибка: {str(error)}"')

    @router.message(Taskadd.task_add)
    async def add(message: types.Message, state: FSMContext):
        try:
            notes_list = get_notes_list(message.from_user.id)
            if message.text not in notes_list:
                await db.add_note(str(message.text), message.from_user.id)
                await message.answer('Задача добавлена!')
                await state.clear()
            else:
                await message.answer('Такая задача уже есть!')
        except Exception as error:
            await message.answer(f'Ошибка выполнения команды. Обратитесь к @Dolmon4ik \nОшибка: {str(error)}"')





