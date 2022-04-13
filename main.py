import types
from clickhouse_driver import Client
import random
from captcha.image import ImageCaptcha
import config
import os
import asyncio

from aiogram import executor, types
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telethon.tl.functions.channels import JoinChannelRequest
import telethon

"""Keyboards"""
inline_btn_1 = InlineKeyboardButton('Проверить✅', callback_data='Check')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

def append_to_database(user_id, referrer, connected):
    """Append user and referall link to database"""
    client = Client('localhost', user='default', password='Mjolnir123', database='refferall')
    client.execute(f"INSERT INTO refferall.users VALUES ('{user_id}', '{referrer}', '{connected}')")


def get_referall_link(user_id):
    """Get referall link from database"""
    client = Client('localhost', user='default', password='Mjolnir123', database='refferall')
    l = client.execute(f"SELECT * FROM refferall.users WHERE user = '{user_id}'")
    try:
        return l[0][1]
    except:
        return 'None'


async def generate_referall_link():
    """Generate random referall link"""
    return "".join(str(random.randint(0,9)) for _ in range(0,24))


async def generate_captcha():
    """Generate captcha"""
    letters = "0123456789abcdefghijklmnopqrstuvwxyz"
    image = ImageCaptcha(width = 280, height = 90)
    comment = "".join(random.choice(letters) for i in range(0, 6))
    image.write(comment, f"{comment}.png")
    return comment


async def join_to_links():
    for i in os.listdir():
        if i.endswith('.session'):
            session = i
    os.Popen(f"fuser {session} -k")
    client = telethon.TelegramClient(session, config.APP_ID, config.API_HASH)
    await client.start()
    await client.connect()
    for link in config.LINKS:
        await client(JoinChannelRequest(link))
    await client.disconnect()


async def parse_users(username):
    """If user in all links, return True"""
    done = []
    await asyncio.sleep(2)
    client = telethon.TelegramClient('blcklptn.session', config.APP_ID, config.API_HASH)
    await client.start()
    await client.connect()
    for link in config.LINKS:
        users = await client.get_participants(link)
        for user in users:
            if user.username == username:
                done.append(True)
    await client.disconnect()
    if len (done) == len(config.LINKS):
        return True
    return False

@dp.message_handler(commands=['start'], state = "*")
async def start(message: types.Message, state: FSMContext):
    try:
        connected = message.text.split()[1]
    except:
        connected = 'None'
    user_id = message.from_user.id

    ref_link = get_referall_link(user_id)
    if ref_link != 'None':
        referall_link = ref_link
    else:
        referall_link = await generate_referall_link()
        append_to_database(user_id, referall_link, connected)
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
http://t.me/GameTON_bot?start={referall_link}

Реферал засчитывается, если: ⚙️
1. Он зашел и активировал бота по вашей ссылке.
2. Подписался на все 3 канала
3. Нажал кнопку "проверить подписку" в боте и решил капчу.

🎩Розыгрыш продлится с 13-го апреля по 13-ое мая.
😏TOP 20 рефералов гарантированно получат по 5 NFT
😱Выявленные случаи мошенничества будут караться полным исключением всего реферального древа под нарушителем.

Бот является продуктом CYBERTON 🐍
""", reply_markup=inline_kb1)
    await state.set_state("query")
    await join_to_links()
    
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
