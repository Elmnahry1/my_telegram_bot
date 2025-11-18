import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# ---------------------------------------------------------
#  ??????? ????????
# ---------------------------------------------------------
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("????? ????", callback_data='sawany')],
        [InlineKeyboardButton("????? ????? ???? ??????", callback_data='taarat')],
        [InlineKeyboardButton("??????", callback_data='bsamat')],
        [InlineKeyboardButton("??? ????", callback_data='haram')],
        [InlineKeyboardButton("????", callback_data='doro3')],
        [InlineKeyboardButton("????????", callback_data='abajorat')],
        [InlineKeyboardButton("?????", callback_data='aqlam')],
        [InlineKeyboardButton("????", callback_data='mugat')],
        [InlineKeyboardButton("???????? ???????", callback_data='sublimation')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # ?? ??? ?? ????? callback ? ?????? edit
    if update.callback_query:
        update.callback_query.edit_message_text("????? ????? ???? ?????:", reply_markup=reply_markup)
    else:
        update.message.reply_text("????? ????? ???? ?????:", reply_markup=reply_markup)


# ---------------------------------------------------------
#  ???? ????? ????? + ?? ??????
# ---------------------------------------------------------
def send_photos(update, context, photos):
    query = update.callback_query
    query.answer()

    # ????? ?????? ?????
    media = [InputMediaPhoto(p) for p in photos]
    context.bot.send_media_group(chat_id=query.message.chat_id, media=media)

    # ????? ?? ?????? ??? ?????
    back_keyboard = [[InlineKeyboardButton("?? ???? ??????? ????????", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    context.bot.send_message(chat_id=query.message.chat_id, text="?????:", reply_markup=reply_markup)


# ---------------------------------------------------------
#  ?????? ?? ???????
# ---------------------------------------------------------
def button_handler(update, context):
    query = update.callback_query
    data = query.data

    # ?? ?????? ??????? ????????
    if data == "back":
        start(update, context)
        return

    # ??????? — ?????? ???? ???? ?? ?????? ????????
    if data == "sawany":
        send_photos(update, context, [
            "PHOTO_URL_1",
            "PHOTO_URL_2"
        ])

    elif data == "taarat":
        send_photos(update, context, [
            "PHOTO_URL_1"
        ])

    elif data == "bsamat":
        send_photos(update, context, [
            "PHOTO_URL_1"
        ])

    elif data == "haram":
        send_photos(update, context, [
            "PHOTO_URL_1"
        ])

    elif data == "doro3":
        send_photos(update, context, [
            "PHOTO_URL_1"
        ])

    elif data == "abajorat":
        send_photos(update, context, [
            "PHOTO_URL_1"
        ])

    elif data == "aqlam":
        send_photos(update, context, [
            "PHOTO_URL_1"
        ])

    elif data == "mugat":
        send_photos(update, context, [
            "PHOTO_URL_1"
        ])

    elif data == "sublimation":
        send_photos(update, context, [
            "PHOTO_URL_1"
        ])


# ---------------------------------------------------------
#  ????? ?????
# ---------------------------------------------------------
def main():
    TOKEN = os.getenv("TOKEN")   # ????? ??? Render ?? Railway
    # TOKEN = "??_??????_???"   # ?? ??? ?????

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
