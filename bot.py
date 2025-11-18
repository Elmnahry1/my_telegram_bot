import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler

# دالة لعرض القائمة الرئيسية
def start(update, context):
    if hasattr(update, 'message'):
        reply_source = update.message
    elif hasattr(update, 'callback_query'):
        reply_source = update.callback_query
    else:
        return

    user_name = reply_source.from_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختر طلبك من القائمة:"
    keyboard = [
        [InlineKeyboardButton("صواني شبكة اكليريك", callback_data="sawany_akerik")]
        # يمكنك إضافة أزرار أخرى هنا
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_source.edit_message_text(greeting_text, reply_markup=reply_markup)

# دالة لعرض المنتج مع الصورة والأزرار
def show_product(update, image_url, label, description=""):
    if hasattr(update, 'callback_query'):
        reply_source = update.callback_query
    elif hasattr(update, 'message'):
        reply_source = update.message
    else:
        return

    keyboard = [
        [InlineKeyboardButton("شراء", callback_data="buy")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    reply_source.bot.send_photo(
        chat_id=reply_source.message.chat_id if hasattr(reply_source, 'message') else reply_source.chat_id,
        photo=image_url,
        caption=f"{label}\n\n{description}",
        reply_markup=reply_markup
    )

# معالجة أزرار الكيبورد
def button(update, context):
    query = update.callback_query
    data = query.data

    if data == "back":
        start(update, context)
    elif data == "sawany_akerik":
        # هنا يتم عرض المنتج
        show_product(
            update,
            "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png",
            "صواني شبكة اكليريك",
            "وصف المنتج هنا"
        )
    # يمكنك إضافة حالات أخرى هنا للمنتجات أو الأزرار

# البرنامج الرئيسي
def main():
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()