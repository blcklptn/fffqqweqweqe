from sqlite3 import connect
import aiogram
from aiogram import executor, Dispatcher, Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from captcha.image import ImageCaptcha
import telethon
import config
import random
import os
from clickhouse_driver import Client

inline_btn_1 = InlineKeyboardButton('Проверить✅', callback_data='Check')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
links = ['@WeTON_play', '@Toncoin_blokchain', '@TON_NFT_Collection']

async def connect_to_links():
    for i in os.listdir():
        if i.endswith('.session'):
            session = i
    client = telethon.TelegramClient(session, config.APP_ID, config.API_HASH)
    await client.start()
    await client.connect()
    for link in links:
        await client(JoinChannelRequest(link))
    await client.disconnect()


async def parse_users(username):
    done = []
    client = telethon.TelegramClient('blcklptn.session', config.APP_ID, config.API_HASH)
    await client.start()
    await client.connect()
    for link in links:
        users = await client.get_participants(link)
        for user in users:
            if user.username == username:
                print('yes')
                done.append(True)
    await client.disconnect()
    if len (done) == len(links):
        print('FUCK')
        print(len(done))
        print(len(links))
        return True
    print(len(done))
    print(len(links))
    print("Whoops")
    return False


async def generate_captcha():
    letters = "0123456789abcdefghijklmnopqrstuvwxyz"
    image = ImageCaptcha(width = 280, height = 90)
    comment = "".join(random.choice(letters) for i in range(0, 6))
    data = image.generate(comment)
    image.write(comment, f"{comment}.png")
    return comment

async def get_referal_link(user):
    #get from database

    #generate link
    return "https://t.me/GameTON_bot?start=r" + "".join(str(random.randint(0,9)) for _ in range(0,9))

@dp.message_handler(commands=['start'], state = "*")
async def start(message: types.Message, state: FSMContext):
    try:
        him_link = message.text.split()[1]
    except:
        him_link = "None"
    referal_link = await get_referal_link(message.from_user.id)
    await message.answer(f"""WeTON_play  проводит розыгрыш 1000 NFT из 5 игровык коллекций
  
Давайте еще раз вспомним про них:
WeTON Butterflies - бабочки переносящие энергию кристаллов
NOTangels - рыбки способные заряжать кристаллы энергией
TON Shark's - амулет акулы усиливающий остальные NFT
SupporTON - таинственные существа позволяющие добывать кристаллы где угодно и когда угодно
Crystal Dragons - драконы контролирующие земли и увеличивающие мощь армии

Для участия в AIRDROP необходимо 👇
1. подписаться на каналы ✅
@WeTON_play 🎩
@Toncoin_blokchain 🌐
@TON_NFT_Collection 🧩
2. Пригласить 1 человека по ссылке 🔗
{referal_link}

Реферал засчитывается, если: ⚙️
1. Он зашел и активировал бота по вашей ссылке.
2. Подписался на все 3 канала
3. Нажал кнопку "проверить подписку" в боте и решил капчу.

🎩Розыгрыш продлится с 13-го апреля по 13-ое мая.
😏TOP 20 рефералов гарантированно получат по 5 NFT
😱Выявленные случаи мошенничества будут караться полным исключением всего реферального древа под нарушителем.

Бот является продуктом CYBERTON 🐍
""",reply_markup=inline_kb1)
    await state.set_state("query")
    await connect_to_links()

@dp.callback_query_handler(text='Check', state="query")
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    if await parse_users(callback_query.from_user.username) == True:
        answer = await generate_captcha()
        await state.update_data(answer=answer)
        with open(f"{answer}.png", "rb") as f:
            await bot.send_photo(callback_query.from_user.id, f)
            await state.set_state("query2")
    else:
        await bot.send_message(callback_query.from_user.id,"Для участия в конкурсе подпишитесь на канал @WeTON_play @Toncoin_blokchain @TON_NFT_Collection, а затем нажмите кнопку проверить.")

@dp.callback_query_handler(text='Check', state="query2")
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    if await parse_users(callback_query.from_user.username) == True:
        answer = await generate_captcha()
        await state.update_data(answer=answer)
        with open(f"{answer}.png", "rb") as f:
            await bot.send_photo(callback_query.from_user.id, f)
            await state.set_state("query2")
    else:
        await bot.send_message(callback_query.from_user.id,"Для участия в конкурсе подпишитесь на канал @WeTON_play @Toncoin_blokchain @TON_NFT_Collection, а затем нажмите кнопку проверить.")

@dp.message_handler(state = 'query2', content_types = ContentType.TEXT)
async def process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == data['answer']:
        print('yes')
        await message.answer("OK")
        os.remove(f"{data['answer']}.png")
        ## FUNCTION HERE
    else:
        os.remove(f"{data['answer']}.png")
        answer = await generate_captcha()
        await state.update_data(answer=answer)
        with open(f"{answer}.png", "rb") as f:
            await bot.send_photo(message.chat.id, f)
            await state.set_state("query2")



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


