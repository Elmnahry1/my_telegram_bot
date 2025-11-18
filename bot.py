import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# ---------------------------------------------------------
# القائمة الرئيسية
# ---------------------------------------------------------
def start(update, context):
    user_name = update.message.from_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختار طلبك من القائمة:"
    keyboard = [
        [InlineKeyboardButton("💍💍 صواني شبكة", callback_data='sawany')],
        [InlineKeyboardButton("💍 طارات خطوبة وكتب الكتاب", callback_data='taarat')],
        [InlineKeyboardButton("✋ بصامات", callback_data='bsamat')],
        [InlineKeyboardButton("📜 مناديل كتب الكتاب", callback_data='wedding_tissues')],
        [InlineKeyboardButton("🗄️ هرم مكتب", callback_data='haram')],
        [InlineKeyboardButton("🏆 دروع", callback_data='doro3')],
        [InlineKeyboardButton("💡 اباجورات", callback_data='abajorat')],
        [InlineKeyboardButton("✏️ اقلام", callback_data='aqlam')],
        [InlineKeyboardButton("☕ مجات", callback_data='mugat')],
        [InlineKeyboardButton("👝 محافظ محفورة بالاسم", callback_data='engraved_wallet')],
        [InlineKeyboardButton("🖨️ مستلزمات سبلميشن", callback_data='sublimation')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(greeting_text, reply_markup=reply_markup)

# ---------------------------------------------------------
# دالة إرسال الصور + زر الرجوع
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
# التحكم في الأزرار
# ---------------------------------------------------------
def button_handler(update, context):
    query = update.callback_query
    data = query.data

    if data == "back":
        start(update, context)
        return

    # روابط تجريبية للصور (حط الروابط الحقيقية بعدين)
    image_url = "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"

    if data == "sawany":
        send_photos(update, context, [image_url, image_url])
    elif data == "taarat":
        send_photos(update, context, [image_url])
    elif data == "bsamat":
        send_photos(update, context, [image_url])
    elif data == "haram":
        send_photos(update, context, [image_url])
    elif data == "doro3":
        send_photos(update, context, [image_url])
    elif data == "abajorat":
        send_photos(update, context, [image_url])
    elif data == "aqlam":
        send_photos(update, context, [image_url])
    elif data == "mugat":
        send_photos(update, context, [image_url])
    elif data == "sublimation":
        send_photos(update, context, [image_url])

# ---------------------------------------------------------
# تشغيل البوت
# ---------------------------------------------------------
def main():
    TOKEN = os.getenv("TOKEN")  # يجب أن يكون موجود كـ Environment Variable على Railway

    if not TOKEN:
        print("Error: TOKEN environment variable is not set.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
