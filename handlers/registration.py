import asyncio

from aiogram import Router, F

import keyboards.all_kb
from create_bot import bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram import types
from utils.aiosqlite import DatabaseBot
reg_router = Router()

# В этом роутере реализуем регистрацию пользователя с помощью aiogram.FSM и последующей записи в Базу данных
# Пользователь может использовать текущий юзернейм Телеграм или вписать свой никнейм вручную
# А также вместо ввода пароля - кошелёк TON

# Задачи:
# + Сделать начальную точку в виде команды /reg
# + Привязать платежку в виде оплаты на TON кошелёк платы за лицензию на сумму 1 TON
# + Доделать регистрацию пользователя в интерфейсе aiogram.FSM
# - Придумать конструктор пароля пользователя (возможно access_token или UUID, нужно учесть безопасность данных)
# мб что-то с TON Connect payload proof
# https://docs.ton.org/develop/dapps/ton-connect/sign#how-does-it-work
# + Сделать запись данных в Базу данных
# - Переделать команду /reg в Кнопку клавиатуры или что-то ещё
# - Profit!

# Кошельки с отправкой TON монет:
# f"ton://transfer/{WALLET}?amount=1000000000&text={air_type}"
# f"https://app.tonkeeper.com/transfer/{WALLET}?amount=1000000000&text={air_type}"
# f"https://tonhub.com/transfer/{WALLET}?amount=1000000000&text={air_type}"
#

# aiohttp.web_request()
# def add_v_transaction(source, hash, value, comment):
#     cur.execute("INSERT INTO transactions (source, hash, value, comment) VALUES (?, ?, ?, ?)",
#                 (source, hash, value, comment))
#     locCon.commit()
#
# def check_transaction(hash):
#     cur.execute(f"SELECT hash FROM transactions WHERE hash = '{hash}'")
#     result = cur.fetchone()
#     if result:
#         return True
#     return False

class Form(StatesGroup):
    username = State()
    wallet = State()
@reg_router.message(Command('reg'))
async def start_reg_process(message: Message, state: FSMContext):
    async with DatabaseBot("main") as db:
        if not await db.check_user(message.from_user.id):
            await db.reg_user(message.from_user.id)
    await state.clear()
    user = message.from_user
    user_fn_ln = str("" if not user.first_name else user.first_name) + " " + str("" if not user.last_name else user.last_name)
    response = f'Hello, {user.mention_html(user_fn_ln)}, please enter your desired Minecraft nickname'
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer(response, reply_markup=keyboards.all_kb.self_username_tg(user.username))
    await state.set_state(Form.username)

@reg_router.message(F.text, Form.username)
async def capturedUsername(message: Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer(f"Done! Nickname {message.text} is booked for 15 minutes. Enter your wallet from where you want to make the payment"
                             ,reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.wallet)

@reg_router.message(F.text, Form.wallet)
async def capturedWallet(message: Message, state: FSMContext):
    mainwallet = "MAINWALLET" # Кошелек на который производиться оплата
    await state.update_data(wallet=message.text) # Кошелек юзера, с которого производиться оплата
    data = await state.get_data()
    username = data.get('username')
    wallets = [f"ton://transfer/{mainwallet}?amount=1&text={username}",
               f"https://app.tonkeeper.com/transfer/{mainwallet}?amount=1&text={username}",
               f"https://tonhub.com/transfer/{mainwallet}?amount=1&text={username}"]
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        response = "\n".join(wallets) + "\nMake the payment and click the \"Paid\" button"
        await message.answer(response, reply_markup=keyboards.all_kb.paid_kb())
    await state.clear()

async def paymentAccepted(state: FSMContext):
    async with DatabaseBot("main") as db:
        data = await state.get_data()
        username = data.get('username')
        await db.set_username("INPUT")