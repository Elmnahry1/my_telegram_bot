import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler

# بيانات المنتجات (كمثال)
sawany_submenu = [
    {
        "label": "صواني شبكة اكليريك",
        "callback": "sawany_akerik",
        "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png",
        "description": "وصف صواني شبكة اكليريك"
    },
    # يمكنك إضافة منتجات أخرى هنا
]

# دالة لعرض قائمة رئيسية
def start(update, context):
    if hasattr(update, 'message'):
        reply_source = update.message
    elif hasattr(update, 'callback_query'):
        reply_source = update.callback_query
    else:
        return

    user_name = reply_source.from_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختر طلبك من القائمة:"
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in sawany_submenu]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_source.edit_message_text(greeting_text, reply_markup=reply_markup)

# دالة لعرض المنتج مع الصورة والأزرار
def show_product(update, product):
    if hasattr(update, 'callback_query'):
        reply_source = update.callback_query
    elif hasattr(update, 'message'):
        reply_source = update.message
    else:
        return

    keyboard = [
        [InlineKeyboardButton("شراء", callback_data="buy")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_from_product")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    reply_source.bot.send_photo(
        chat_id=reply_source.message.chat_id if hasattr(reply_source, 'message') else reply_source.chat_id,
        photo=product["image"],
        caption=f"{product['label']}\n\n{product.get('description', '')}",
        reply_markup=reply_markup
    )

# معالجة الأزرار
def button(update, context):
    query = update.callback_query
    data = query.data

    if data == "main_menu" or data == "back":
        start(update, context)
        return
    elif data == "back_from_product":
        start(update, context)
        return
    elif data.startswith("sawany_"):
        # مثال لعرض منتج معين
        for item in sawany_submenu:
            if data == item["callback"]:
                show_product(update, item)
                return
    # أضف هنا حالات المنتجات الأخرى إذا لديك

# الإعدادات الأساسية للبوت
def main():
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()