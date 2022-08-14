import logging

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
import aiogram.utils.markdown as md

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InfoUser.settings")

import django
django.setup()

from django.contrib.auth.models import User
from info.models import Profile
from asgiref.sync import sync_to_async


@sync_to_async
def create_user(username, password, name, nickname, state_id):
    try:
        User.objects.create_user(username=username, password=password)
        user = User.objects.get(username=username)
        Profile.objects.create(
            user=user,
            name=name,
            username=nickname,
            state_id=state_id
        )
    except Exception as e:
        print('Warning: ', e)

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5556043918:AAFQCHlYg7DMrg43Oo5prsKgoFJIYftB88A'

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

b1 = types.KeyboardButton('/Да')
b2 = types.KeyboardButton('/Нет')
b3 = types.KeyboardButton('/Логин')
b4 = types.KeyboardButton('/Пароль')
b5 = types.KeyboardButton('/Отменить')

key_client_1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
key_client_1.row(b1, b2)
register = types.ReplyKeyboardMarkup(resize_keyboard=True)
register.row(b3, b4)
cancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add(b5)

class RegistrationForm(StatesGroup):
    login = State()  # Will be represented in storage as 'RegistrationForm:login'
    password = State()  # Will be represented in storage as 'RegistrationForm:password'

def check_password(password):
    if len(password) <= 8:
        return not password
    elif len(password) > 8 and len(password) < 26:
        if not password.istitle():
            return not password
        else:
            return password

@sync_to_async
def check_user(username):
    try:
        profile = Profile.objects.get(username=username)
        if profile:
            return False
        else:
            return True
    except:
        return True

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    if message.text == '/start':
        await message.answer("Привет %s!\nЯ RegisterBot!\nТы хочешь зарегистрироваться?" % message.from_user.full_name,
            reply_markup=key_client_1)
    elif message.text == '/help':
        await message.answer("Напиши /start чтобы начать")

@dp.message_handler(commands=['Да', 'Нет'])
async def check_answer(message: types.Message):
    result = await check_user(message.from_user.username)
    if result:
        if message.text == '/Да':
            await RegistrationForm.login.set()
            await message.reply("Придумайте логин", reply_markup=cancel)
        elif message.text == '/Нет':
            await message.answer("%s Может зарегистрируешься?" % message.from_user.full_name, reply_markup=key_client_1)
    else:
        markup = types.ReplyKeyboardRemove()
        await message.answer("%s вы уже зарегестрированы." % message.from_user.full_name, reply_markup=markup)

@dp.message_handler(state='*', commands='Отменить')
@dp.message_handler(Text(equals='Отменить', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inRegistrationform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Отменено.', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=RegistrationForm.login)
async def process_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
 
    await RegistrationForm.next()
    await message.reply("Придумайте пароль")

# Check password. Age gotta be digit
@dp.message_handler(lambda message: not check_password(message.text), state=RegistrationForm.password)
async def process_password_invalid(message: types.Message):
    """
    If password is invalid
    """
    return await message.reply(
        "Пароль должен начинаться с большой буквы и в пароле\
        должно быть больше 8 символов.\nПопробуйте снова.")

@dp.message_handler(state=RegistrationForm.password)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        await create_user(
            username=data['login'],
            password=data['password'],
            name = message.from_user.full_name,
            nickname = message.from_user.username,
            state_id = message.from_user.id
        )
        

        # And send message
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Логин:', md.bold(data['login'])),
                md.text('Пароль:', md.code(data['password'])),
                md.text('Вернитесь на сайт чтобы войти'),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    # Finish conversation
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)