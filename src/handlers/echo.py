from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from dependency_injector.wiring import inject, Provide
from injection import Container


EchoRouter = Router()

@EchoRouter.message()
async def Echo(message: Message, state: FSMContext):
    await message.answer(message.text, reply_markup=ReplyKeyboardRemove())