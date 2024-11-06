from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.all_kb import main_kb
from aiogram import types
start_router = Router()

# Начальный роутер который активируется при запуске бота и при команде /start
# В команду /start можно вписать аргументы посредством ссылки t.me/<bot>/start=<text>
# Можно сделать реферальную систему

# Задачи:
# + Main router /start
# + Keyboard

@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Hello world!',
                         reply_markup=main_kb())