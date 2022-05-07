import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from db import add_user_info, get_category_by_id, get_all_data, get_product_by_id, add_product_info, get_cart_products
from states import Shop
from buttons import all_cats, miqdor


# logging sozlash
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'], state="*")
async def do_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username
    try:
        add_user_info(tg_id=user_id, full_name=fullname, user_name=username)
        await message.answer(f"Salom {fullname}\nID: {user_id}\nUsername: @{username}\nSizning ma'lumotlar bazaga qo'shildi", reply_markup=all_cats)
        await Shop.category.set()
    except:
        pass


@dp.message_handler(state=Shop.category, text='Savatcha')
async def get_cart(message: types.Message):
    products = get_cart_products(tg_id=message.from_user.id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    msg = "Sizning mahsulotlar\n\n"
    for product in products:
        msg += f"{product[0]} - {product[1]} ta\n"
        markup.add(KeyboardButton(text=f"❌ {product[0]} ❌"))
    markup.add(KeyboardButton(text="Orqaga"))
    await message.answer(msg, reply_markup=markup)
    await Shop.product.set()


@dp.message_handler(state=Shop.category)
async def get_products(message:types.Message, state: FSMContext):
    category = message.text
    results = get_category_by_id(title=category)
    product_name = results[0]
    cat_id = results[1]
    await state.update_data({
        'cat_id': cat_id
    })
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for product in product_name:
        markup.insert(KeyboardButton(text=product[0]))
    markup.add(KeyboardButton(text="Orqaga"))
    await message.answer("Mahsulotlardan birini tanlang", reply_markup=markup)
    await Shop.next()


@dp.message_handler(state=Shop.product, text='Orqaga')
async def go_main1(message: types.Message):
    await message.answer("Asosiy sahifa", reply_markup=all_cats)
    await Shop.category.set()


@dp.message_handler(state=Shop.product)
async def get_about(message: types.Message, state: FSMContext):
    data = get_all_data(title=message.text)
    await state.update_data({
        'product': data[1],
        'price': data[-4]
    })
    msg = f"<b>{data[1]} - {data[-4]} $</b>\n\n<i>Ishlab chiqarilgan sana: {data[-2]}</i>\n\n{data[2]}"
    await message.answer_photo(photo=data[-3], caption=msg, parse_mode="html", reply_markup=miqdor)    
    await Shop.next()


@dp.message_handler(state=Shop.amount, text="Bosh sahifa")
async def go_main(message: types.Message):
    await message.answer("Asosiy sahifa", reply_markup=all_cats)
    await Shop.category.set()


@dp.message_handler(state=Shop.amount, text="Orqaga")
async def go_products(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cat_id = data.get('cat_id')
    all_products = get_product_by_id(cat_id=cat_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for product in all_products:
        markup.insert(KeyboardButton(text=product[0]))
    markup.add(KeyboardButton(text="Orqaga"))
    await message.answer("Mahsulotlardan birini tanlang", reply_markup=markup)
    await Shop.product.set()



@dp.message_handler(state=Shop.amount)
async def get_amount(message: types.Message, state: FSMContext):
    try:
        quantity = message.text
        if int(quantity) > 0:
            data = await state.get_data()
            name = data.get('product')
            price = data.get('price')
            await message.answer(f"{quantity} ta {name} savatga qo'shildi\n\n{quantity} x {price} = {int(quantity)*int(price)} $", reply_markup=all_cats)
            add_product_info(product_name=name, quantity=int(quantity), tg_id=message.from_user.id)
            await Shop.category.set()
        else:
            await message.answer("Faqat musbat butun son kirita olasiz!")
            await Shop.amount.set()
    except:
        await message.answer("Faqat musbat butun son kirita olasiz!")
        await Shop.amount.set()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)