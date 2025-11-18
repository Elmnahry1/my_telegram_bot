import os
import urllib.parse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

ASK_NAME, ASK_PHONE, ASK_QTY, ASK_EXTRA = range(4)

# ---------------------------------------------------------
MAIN_MENU = [
    [InlineKeyboardButton("💍 صواني شبكة", callback_data='sawany')],
    [InlineKeyboardButton("💍 طارات خطوبة وكتب الكتاب", callback_data='taarat')],
    [InlineKeyboardButton("📛 بصامات", callback_data='bsamat')],
    [InlineKeyboardButton("🔺 هرم مكتب", callback_data='haram')],
    [InlineKeyboardButton("🏆 دروع", callback_data='doro3')],
    [InlineKeyboardButton("🖊️ اقلام", callback_data='aqlam')],
    [InlineKeyboardButton("☕ مجات", callback_data='mugat')],
    [InlineKeyboardButton("👝 محافظ محفورة بالاسم", callback_data='wallets')],
    [InlineKeyboardButton("🎨 مستلزمات سبلميشن", callback_data='sublimation')]
]

# ---------------------------------------------------------
SUB_MENUS = {
    "sawany": [
        [InlineKeyboardButton("صواني شبكة اكليريك", callback_data="sawany_acrylic")],
        [InlineKeyboardButton("صواني شبكة خشب", callback_data="sawany_wood")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main")]
    ],
    # باقي الأقسام زي المثال السابق
}

PRODUCTS = {
    "sawany_acrylic": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"},
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف2"}
    ],
    # باقي الأقسام بنفس النظام
}

PRODUCT_PARENT_MENU = {
    "sawany_acrylic": "sawany",
    "sawany_wood": "sawany",
    # باقي الأقسام
}

# ---------------------------------------------------------
user_order = {}

WHATSAPP_NUMBER = "201288846355"  # ضع رقمك هنا بصيغة دولية بدون + أو 00

def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    welcome_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختار طلبك من القائمة:"
    update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(MAIN_MENU))

def send_product_group(query, context, product_key):
    products = PRODUCTS[product_key]
    parent_menu = PRODUCT_PARENT_MENU.get(product_key)
    for idx, item in enumerate(products):
        media = InputMediaPhoto(item["photo"], caption=item["description"])
        context.bot.send_media_group(chat_id=query.message.chat_id, media=[media])

        keyboard = [
            [InlineKeyboardButton("شراء", callback_data=f"buy_{product_key}_{idx}")]
        ]
        if parent_menu:
            keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة السابقة", callback_data=parent_menu)])
        else:
            keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main")])

        context.bot.send_message(chat_id=query.message.chat_id, text="اختار:", reply_markup=InlineKeyboardMarkup(keyboard))

# ---------------------------------------------------------
def menu_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    query.answer()

    if data == "main":
        query.edit_message_text("اختار طلبك من القائمة:", reply_markup=InlineKeyboardMarkup(MAIN_MENU))
        return

    if data in SUB_MENUS:
        query.edit_message_text("اختر القسم الفرعي:", reply_markup=InlineKeyboardMarkup(SUB_MENUS[data]))
        return

    if data in PRODUCTS:
        send_product_group(query, context, data)
        return

    if data.startswith("buy_"):
        parts = data.split("_")
        product_key = "_".join(parts[1:-1])
        product_idx = int(parts[-1])
        user_order[update.effective_user.id] = {
            "product_key": product_key,
            "product_idx": product_idx
        }
        context.bot.send_message(chat_id=query.message.chat_id, text="أدخل اسمك:")
        return ASK_NAME

# ---------------------------------------------------------
def ask_name(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_order[user_id]["name"] = update.message.text
    update.message.reply_text("أدخل رقم الهاتف:")
    return ASK_PHONE

def ask_phone(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_order[user_id]["phone"] = update.message.text
    update.message.reply_text("أدخل الكمية المطلوبة:")
    return ASK_QTY

def ask_qty(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_order[user_id]["quantity"] = update.message.text
    update.message.reply_text("يمكنك كتابة أي تفاصيل إضافية (أو ارسل 'لا' إذا لا يوجد):")
    return ASK_EXTRA

def ask_extra(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_order[user_id]["extra"] = update.message.text

    order = user_order[user_id]
    product_info = PRODUCTS[order["product_key"]][order["product_idx"]]

    text = f"طلب جديد:\nالمنتج: {order['product_key']} - {product_info['description']}\n" \
           f"الاسم: {order['name']}\nرقم الهاتف: {order['phone']}\n" \
           f"الكمية: {order['quantity']}\nتفاصيل إضافية: {order['extra']}\n"

    msg_text = urllib.parse.quote(text)
    photo_url = product_info["photo"]
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={msg_text}"

    update.message.reply_text(f"اضغط هنا لإرسال الطلب على واتساب:\n{wa_link}")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("تم إلغاء الطلب.")
    return ConversationHandler.END

# ---------------------------------------------------------
def main():
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        print("Error: TOKEN environment variable is not set.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(menu_handler)],
        states={
            ASK_NAME: [MessageHandler(Filters.text & ~Filters.command, ask_name)],
            ASK_PHONE: [MessageHandler(Filters.text & ~Filters.command, ask_phone)],
            ASK_QTY: [MessageHandler(Filters.text & ~Filters.command, ask_qty)],
            ASK_EXTRA: [MessageHandler(Filters.text & ~Filters.command, ask_extra)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True
    )
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
