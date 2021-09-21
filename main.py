import asyncio
import logging
import os
import sqlite3
from asyncio import sleep

from telethon import TelegramClient, events
from telethon.network import connection
from telethon.tl import types, functions

import datetime
import scret
import sqlite3
import socks

loop = asyncio.get_event_loop()

global kano;

try:
    db = sqlite3.connect('main.db')
    cur = db.cursor()
    print('[DB Connect]-[{time}] Подключение к БД успешно, инициализация бота...'.format(time=datetime.datetime.now()))
except:
    print('[DB Connect]-[{time}] Не удалось подключиться к БД, не могу продолжить запуск.'.format(
        time=datetime.datetime.now()))

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

bd = sqlite3.connect("main.db")
cur = bd.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (
    first_name BLOB,
    last_name  BLOB,
    username   BLOB,
    id         BLOB,
    phone      BLOB,
    isBot      BLOB,
    isScam     BLOB,
    isFake     BLOB,
    money      BIGINT DEFAULT (50),
    amountWin  BIGINT DEFAULT (0),
    amountLose BIGINT DEFAULT (0),
    amountDraw BIGINT DEFAULT (0) 
)""")

bot = TelegramClient('@KanoShuuya', scret.API_ID, scret.API_HASH, connection=connection.http.ConnectionHttp, proxy=(socks.HTTP, '127.0.0.1', 80)).start(bot_token=scret.API_TOKEN)

@bot.on(events.NewMessage(pattern='/messageMethod'))
async def rep_minus(msg):
    await msg.reply("Запонить их тебе уже пора!: https://core.telegram.org/bots/api#message")


@bot.on((events.NewMessage(pattern="/dice")))
async def testFunc2(msg):
    my_msg = await bot.send_file(msg.chat_id, types.InputMediaDice('🎲'))
    botDiceValue = my_msg.dice.value;
    await bot.send_message(msg.chat_id, "киньте кубик, ответом на кубик бота")
    try:
        async with bot.conversation(msg.chat_id) as conv:
            reply = await conv.get_reply(my_msg)
            try:
                playerDiceValue = reply.dice.value
            except:
                await reply.reply("Ты кинули не кубик, так что я в гроб")
            else:
                await sleep(5)
                playerDiceValue = reply.dice.value;
                if botDiceValue == playerDiceValue:
                    await bot.send_message(msg.chat_id, "ничья, победил бот")
                if botDiceValue > playerDiceValue:
                    await bot.send_message(msg.chat_id, "Тебя выиграл бот, лох")
                if botDiceValue < playerDiceValue:
                    await bot.send_message(msg.chat_id, "Бедный бот, его выиграл такой людишка как ты =(")
    except:
        await bot.send_message(msg.chat_id, "Ошибка")


@bot.on(events.NewMessage(pattern="/methods"))
async def methods(msg):
    print(dir(msg.sender))
    print(dir(msg))
    print(dir(kano))


@bot.on(events.NewMessage(pattern="!baseConsoleAll"))
async def baseConsoleAll(msg):
    cur.execute(f"SELECT * FROM users")
    result = cur.fetchall()
    print(result)


@bot.on(events.NewMessage(pattern="/inBase"))
async def inBase(msg):
    if (msg.sender.id == kano.id):
        if msg.is_reply:
            reply = await msg.get_reply_message()
            test = reply.sender
            print(test)
            user = (
            test.first_name, test.last_name, test.username, test.id, test.phone, test.bot, test.scam, test.fake, 50, 0,
            0, 0)
            cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user)
            cur.execute("COMMIT;")
            db.commit()
    else:
        await bot.send_message(msg.chat_id, "Кыш! Ты не Кано!")


# @bot.on(events.NewMessage(pattern="youtube"))
# async def testFunc2(msg):
#    os.system("start http://youtube.com")
#    msg.reply("Открываю!")

@bot.on(events.NewMessage(pattern='/show'))
async def test(msg):
    if msg.reply:
        reply = await msg.get_reply_message()
        print(reply.raw_text)


@bot.on(events.ChatAction)
async def join(e):
    if e.user_joined:
        await e.reply("Он зашел!")
    if e.user_added:
        await e.reply("Ну и кто тебя такого умного добавил сюда?")
    if e.user_left:
        await e.reply("Скатертью дорожка!")


# @bot.on(events.NewMessage(pattern=r'(?i).*sl.v[e|е]*|.*m.st.r*|.*[c|с]um*|.*dunge.n*|.*fu[c|с]k*|.*fuk*|.*wee*|.*[gey|gay] s.x*|.*.ick*|.*l..ther*|.*[a|а]ss*|.*c[o|о]ck*|.*f.sting*|.*s[e|е]men*'))
# async def antigachi(msg):
#    await msg.delete()

async def kanos():
    global kano
    kano = await bot.get_entity(1054408787)


loop.run_until_complete(kanos())

bot.run_until_disconnected()
