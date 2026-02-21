from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

EchoRouter = Router()

@EchoRouter.message()
async def Echo(message: Message, state: FSMContext):
    await message.answer(message.text, reply_markup=ReplyKeyboardRemove())