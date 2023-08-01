import telebot


from auth_data import token
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InputMediaPhoto, CallbackQuery

from template_text import post_tennis, start_acquaintance, continue_acquaintance

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start_message(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    menu = KeyboardButton("Давай знакомиться 🤪")

    markup.add(menu)

    bot.send_message(message.chat.id, text="Привет, {0.first_name}🫰 Меня зовут Артём! Здесь ты найдешь немного"
                                           " информации обо мне)".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    chat_id = message.chat.id

    if message.text == "Давай знакомиться 🤪":
        show_my_photos = KeyboardButton("1 🫰🏻")
        post = KeyboardButton("2 🎾")
        voice = KeyboardButton("3 🔊")

        markup.add(show_my_photos, post, voice)

        bot.send_message(chat_id, text=start_acquaintance, reply_markup=markup)

    elif message.text == "1 🫰🏻":
        photos = [r'https://disk.yandex.ru/i/UNn4fYZTVoymbQ',
                  r'https://disk.yandex.ru/i/VLif3ihAQFMmmg',
                  r'https://disk.yandex.ru/i/7mNAS-d5J-Jx4Q']

        media_group = []

        for photo, url in enumerate(photos):
            media_group.append(InputMediaPhoto(media=url, caption=photo))
        bot.send_media_group(chat_id, media=media_group)
        bot.send_message(chat_id, text=continue_acquaintance)

    elif message.text == "2 🎾":
        bot.send_message(chat_id, text=post_tennis.format(message.from_user), reply_markup=markup)
        bot.send_message(chat_id, text=continue_acquaintance, reply_markup=markup)

    elif message.text == "3 🔊":
        voice_keyboard = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text="Рассказ о чате GPT 🤯", callback_data="gpt"),
            InlineKeyboardButton(text="Разница между SQL и NoSQL 🥲", callback_data="db"),
            InlineKeyboardButton(text="История первой любви 😍", callback_data="story")
        )

        bot.send_message(chat_id, text="{0.first_name}, тут можешь послушать мои голосовые:)".format(message.from_user),
                         reply_markup=voice_keyboard)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            req = call.data.split('_')
            voice_gpt = open("media/gpt.ogg", "rb")
            voice_db = open("media/db.ogg", "rb")
            voice_story = open("media/love_story.ogg", "rb")
            if req[0] == "gpt":
                bot.send_message(call.message.chat.id, text="Рассказ о чате 🤯")
                bot.send_voice(call.message.chat.id, voice=voice_gpt)
            elif req[0] == "db":
                bot.send_message(call.message.chat.id, text="Голосовое про SQL и NoSQL 🥲")
                bot.send_voice(call.message.chat.id, voice=voice_db)
            elif req[0] == "story":
                bot.send_message(call.message.chat.id, text="История любви 🥰")
                bot.send_voice(call.message.chat.id, voice=voice_story)
                bot.send_message(call.message.chat.id, text="{0.first_name}, мы посмотрели все разделы :) \n \n"
                                                            "Если хочешь взглянуть на код - напиши _посмотреть код_"
                                                            .format(message.from_user),
                                                            parse_mode='Markdown')

    elif message.text == "Посмотреть код" or "посмотреть код":
        bot.send_message(chat_id, text='Вот код 🫰🏻\n \n https://github.com/otyomaa/Blog')

    else:
        bot.send_message(chat_id, text="Ошибочка вышла, проверь свою команду)", reply_markup=markup)
        bot.send_message(chat_id, text=continue_acquaintance)


if __name__ == '__main__':
    bot.polling(none_stop=True)
