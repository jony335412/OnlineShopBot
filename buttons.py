from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import get_categories


all_cats = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
cats = get_categories()

for cat in cats:
    all_cats.insert(KeyboardButton(text=cat[1]))
all_cats.insert(KeyboardButton(text="Savatcha"))


miqdor = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

for i in range(1, 10):
    miqdor.insert(KeyboardButton(text=str(i)))

miqdor.insert(KeyboardButton(text="Orqaga"))
miqdor.insert(KeyboardButton(text="Bosh sahifa"))