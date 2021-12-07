import sqlite3 as sq
from create_bot import dp, bot

def star_home_db():
    global base, cur
    base = sq.connect("home.db")
    cur = base.cursor()
    if base:
        print("Data base connected successful")
    base.execute("CREATE TABLE IF NOT EXISTS flashlight (date TEXT PRIMARY KEY, counter TEXT)")
    base.commit()

async def sql_add(state):
    async with state.proxy() as data:
        cur.execute("INSERT or REPLACE INTO flashlight VALUES (?, ?)", tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute("SELECT * FROM flashlight ORDER BY date").fetchall():
        await bot.send_message(message.from_user.id, f"На {ret[0]} - {ret[1]} кВт")


async def sql_read_last3(message):
    for ret in cur.execute("SELECT * FROM flashlight ORDER BY date DESC LIMIT 3").fetchall():
        await bot.send_message(message.from_user.id, f"На {ret[0]} - {ret[1]} кВт")

async def sql_read_price(message):
   counter = cur.execute("SELECT counter FROM flashlight ORDER BY date DESC LIMIT 2").fetchall()
   try:
       counter_func = abs(int(counter[0][0]) - int(counter[1][0]))
       counter_price = counter_func * 7.29
       await bot.send_message(message.from_user.id, f"Между двумя последними показаниями {counter_func} кВт")
       await bot.send_message(message.from_user.id, f"Что в денежном эквиваленте по курсу 7.29 р/кВт составляет {counter_price} руб")
   except:
       await bot.send_message(message.from_user.id, f"Хм, странно - в базе меньше двух значений!")


async def sql_read2():
    return cur.execute("SELECT * FROM flashlight ORDER BY date").fetchall()


async def sql_delete_command(data):
    cur.execute("DELETE FROM flashlight WHERE date == ?", (data,))
    base.commit()
