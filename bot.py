import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# ---------------------------------------------------------
#  القائمة الرئيسية
# ---------------------------------------------------------
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("صواني شبكة", callback_data='sawany')],
        [InlineKeyboardButton("طارات خطوبة وكتب الكتاب", callback_data='taarat')],
        [InlineKeyboardButton("بصامات", callback_data='bsamat')],
        [InlineKeyboardButton("هرم مكتب", callback_data='haram')],
        [InlineKeyboardButton("دروع", callback_data='doro3')],
        [InlineKeyboardButton("اباجورات", callback_data='abajorat')],
        [InlineKeyboardButton("اقلام", callback_data='aqlam')],
        [InlineKeyboardButton("مجات", callback_data='mugat')],
        [InlineKeyboardButton("مستلزمات سبلميشن", callback_data='sublimation')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        update.callback_query.edit_message_text("اختار القسم اللي تريده:", reply_markup=reply_markup)
    else:
        update.message.reply_text("اختار القسم اللي تريده:", reply_markup=reply_markup)


# ---------------------------------------------------------
#  دالة إرسال الصور + زر الرجوع
# ---------------------------------------------------------
def send_photos(update, context, photos):
    query = update.callback_query
    query.answer()

    media = [InputMediaPhoto(p) for p in photos]
    context.bot.send_media_group(chat_id=query.message.chat_id, media=media)

    back_keyboard = [[InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    context.bot.send_message(chat_id=query.message.chat_id, text="اختار:", reply_markup=reply_markup)


# ---------------------------------------------------------
#  التحكم في الأزرار
# ---------------------------------------------------------
def button_handler(update, context):
    query = update.callback_query
    data = query.data

    if data == "back":
        start(update, context)
        return

    if data == "sawany":
        send_photos(update, context, ["PHOTO_URL_1", "PHOTO_URL_2"])
    elif data == "taarat":
        send_photos(update, context, ["PHOTO_URL_1"])
    elif data == "bsamat":
        send_photos(update, context, ["PHOTO_URL_1"])
    elif data == "haram":
        send_photos(update, context, ["PHOTO_URL_1"])
    elif data == "doro3":
        send_photos(update, context, ["PHOTO_URL_1"])
    elif data == "abajorat":
        send_photos(update, context, ["PHOTO_URL_1"])
    elif data == "aqlam":
        send_photos(update, context, ["PHOTO_URL_1"])
    elif data == "mugat":
        send_photos(update, context, ["PHOTO_URL_1"])
    elif data == "sublimation":
        send_photos(update, context, ["PHOTO_URL_1"])


# ---------------------------------------------------------
#  تشغيل البوت
# ---------------------------------------------------------
def main():
    TOKEN = os.getenv("TOKEN")   # للرفع على Render أو Railway

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
