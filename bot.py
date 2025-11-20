import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus

# إعدادات الواتساب
WHATSAPP_NUMBER = "201288846355"

# حالات المحادثة
GET_WALLET_NAME = 1
GET_PEN_NAME = 2
GET_BOX_COLOR = 3
GET_BOX_NAMES = 4
GET_TRAY_NAMES = 5
GET_TRAY_DATE = 6

# حالات جديدة لمنتجات الخشب
GET_WOOD_TRAY_NAMES = 7
GET_WOOD_TRAY_DATE = 8

# بيانات القوائم (مثال بسيط، يمكنك تعديلها حسب الحاجة)
doro3_submenu = [
    {
        "label": "صواني شبكة خشب",
        "callback": "khashab",
        "items": [
            {"label": "صينية خشب موديل 1", "callback": "khashab_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف صينية خشب موديل 1."},
            {"label": "صينية خشب موديل 2", "callback": "khashab_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف صينية خشب موديل 2."}
        ]
    }
]

# البيانات العامة
main_menu = [
    {"label": "💍 شبكة الخشب", "callback": "sawany_khashab"},
]
all_submenus = {
    "sawany_khashab": doro3_submenu
}

product_to_submenu_map = {
    "khashab_m1": "sawany_khashab",
    "khashab_m2": "sawany_khashab"
}

# الدوال الأساسية
def start(update, context):
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in main_menu]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("مرحباً بك! اختر نوع المنتج:", reply_markup=reply_markup)

def show_submenu(update, context, submenu_list, title, back_callback="main"):
    query = update.callback_query
    if query:
        query.answer()
        try:
            query.message.delete()
        except:
            pass
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in submenu_list]
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    chat_id = update.effective_chat.id
    if query:
        chat_id = query.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=f"⚙️ {title}:", reply_markup=reply_markup)

def show_product_page(update, product_callback, product_data):
    query = update.callback_query
    if query:
        query.answer()
        try:
            query.message.delete()
        except:
            pass
    # عرض المنتج
    context = update.callback_context
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=product_data["image"],
        caption=f"📦 {product_data['label']}\n{product_data['description']}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{product_callback}")]])
    )

# حالتان لطلب الاسم والتاريخ لمنتجات الخشب
def start_wood_tray_purchase(update, context):
    query = update.callback_query
    query.answer()
    product_callback = query.data.replace("buy_", "")
    # ابحث عن المنتج في القائمة
    product = None
    for item in doro3_submenu[0]['items']:
        if item['callback'] == product_callback:
            product = item
            break
    if not product:
        query.message.reply_text("عذراً، لم يتم العثور على المنتج.")
        return ConversationHandler.END
    # حفظ المنتج
    context.user_data['wood_tray'] = product
    context.user_data['state'] = GET_WOOD_TRAY_NAMES
    try:
        query.message.delete()
    except:
        pass
    # عرض الصورة وطلب الاسم
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=product['image'],
        caption="📝 من فضلك، اكتب اسم العريس والعروسة في رسالة نصية أدناه، أو اضغط رجوع للعودة.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_khashab")]])
    )
    return GET_WOOD_TRAY_NAMES

def save_wood_tray_names(update, context):
    names = update.message.text
    context.user_data['names'] = names
    context.user_data['state'] = GET_WOOD_TRAY_DATE
    try:
        update.message.delete()
    except:
        pass
    update.message.reply_text("📅 اكتب التاريخ (مثال: 2024/1/1)، أو اضغط رجوع للعودة.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_wood_tray_names")]]))
    return GET_WOOD_TRAY_DATE

def receive_wood_tray_date(update, context):
    date_text = update.message.text
    product = context.user_data.get('wood_tray')
    names = context.user_data.get('names')
    if not product or not names:
        update.message.reply_text("حدث خطأ، يرجى البدء من جديد.")
        return ConversationHandler.END
    user = update.message.from_user
    message_body = (
        f"🔔 طلب جديد من شبكة الخشب\n"
        f"المنتج: {product['label']}\n"
        f"الأسماء: {names}\n"
        f"التاريخ: {date_text}\n"
        f"الكود: {product['callback']}\n"
        f"الاسم: {user.first_name}\n"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("✅ أرسل الطلب على واتساب", url=wa_link)]])
    update.message.reply_text("تم تجميع طلبك، اضغط على الزر أدناه لإرساله على الواتساب.", reply_markup=reply_markup)
    # مسح البيانات
    context.user_data.clear()
    return ConversationHandler.END

def back_to_wood_tray_names(update, context):
    query = update.callback_query
    if query:
        query.answer()
        try:
            query.message.delete()
        except:
            pass
        # إرجاع لعرض الصورة وطلب الاسم مجددًا
        product = context.user_data.get('wood_tray')
        if not product:
            start(update, context)
            return ConversationHandler.END
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=product['image'],
            caption="📝 من فضلك، اكتب اسم العريس والعروسة في رسالة نصية أدناه، أو اضغط رجوع للعودة.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_khashab")]])
        )
        return GET_WOOD_TRAY_NAMES
    return ConversationHandler.END

# إعداد الـ ConversationHandler لمنتجات الخشب
wood_tray_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_wood_tray_purchase, pattern='^buy_khashab_.*')],
    states={
        GET_WOOD_TRAY_NAMES: [MessageHandler(Filters.text & ~Filters.command, save_wood_tray_names)],
        GET_WOOD_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_wood_tray_date)],
    },
    fallbacks=[
        CallbackQueryHandler(back_to_wood_tray_names, pattern='^back_to_wood_tray_names$'),
        CommandHandler('start', start),
        MessageHandler(Filters.text & ~Filters.command, lambda update, context: None),
    ]
)

# الدالة الرئيسية
def main():
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # أمر البداية
    dp.add_handler(CommandHandler("start", start))
    # قائمة رئيسية
    dp.add_handler(CallbackQueryHandler(lambda update, context: show_submenu(update, context, doro3_submenu[0]['items'], "شبكة الخشب"), pattern='^sawany_khashab$'))
    # هاندلر المنتجات الخشبية
    dp.add_handler(wood_tray_conv_handler)

    # زر شراء من المنتج
    dp.add_handler(CallbackQueryHandler(start_wood_tray_purchase, pattern='^buy_khashab_.*'))

    # زر رجوع من الاسم
    dp.add_handler(CallbackQueryHandler(back_to_wood_tray_names, pattern='^back_to_wood_tray_names$'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()