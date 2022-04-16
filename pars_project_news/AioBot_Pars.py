import asyncio
import json

from aiogram import Bot, Dispatcher, executor, types
from auth_date_bot import token, user_id
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from main import chake_news_update

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(messega: types.Message):
    start_buttons = ["Все новости", "Последние 5-ть новостей", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await messega.answer('Лента новостей', reply_markup=keyboard)


@dp.message_handler(Text(equals='Все новости'))
async def get_all_news(message: types.Message):
    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        # news = f"<b>{(v['article_title'])}</b>\n" \
        #        f"<u>{v['article_url']}</u>\n" \
        #        f"<code>{v['article_date_time']}</code>\n"
        # news = f"{hbold(v['article_title'])}\n" \
        #        f"{hlink(v['article_title'], v['article_url'])}\n" \
        #        f"{hunderline(v['article_date_time'])}\n"
        news = f"{hlink(v['article_title'], v['article_url'])}\n" \
               f"{hunderline(v['article_date_time'])}\n"

        await message.answer(news)

@dp.message_handler(Text(equals='Последние 5-ть новостей'))
async def get_last_five_news(message: types.Message):
    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hlink(v['article_title'], v['article_url'])}\n" \
               f"{hunderline(v['article_date_time'])}\n"

        await message.answer(news)

@dp.message_handler(Text(equals='Свежие новости'))
async def get_fresh_news(message: types.Message):
    fresh_news = chake_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items())[-5:]:
            news = f"{hlink(v['article_title'], v['article_url'])}\n" \
                   f"{hunderline(v['article_date_time'])}\n"

            await message.answer(news)
    else:
        await message.answer("Пока нет свежих новостей...")

async def news_every_ninute():
    while True:
        fresh_news = chake_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items())[-5:]:
                news = f"{hlink(v['article_title'], v['article_url'])}\n" \
                       f"{hunderline(v['article_date_time'])}\n"

                # get your id Userinfobot
                await bot.send_message(user_id, news, disable_notification=True)
        else:
            await bot.send_message(user_id, 'Пока нет свежих новостей...', disable_notification=True)

        await asyncio.sleep(3600)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_ninute())

    executor.start_polling(dp)