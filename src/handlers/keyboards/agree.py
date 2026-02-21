from aiogram.types import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

__all__ = ["AgreeKeyboard"]

class AgreeKeyboard:
    YesButtonText = "Да"
    NoButtonText = "Нет"

    @staticmethod
    def Create():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=AgreeKeyboard.YesButtonText), KeyboardButton(text=AgreeKeyboard.NoButtonText)],
            ],
            resize_keyboard=True,
        )