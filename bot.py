import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

# ---------------------------------------------------------
# إعداد المنتجات لكل قسم وقسم فرعي
# ---------------------------------------------------------
products = {
    "sawany_acrylic": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"},
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف2"}
    ],
    "sawany_wood": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "taarat_acrylic": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "taarat_wood": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "bsamat": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "wedding_tissues": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "haram_acrylic": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "haram_metal": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "haram_wood": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "doro3_acrylic": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "doro3_metal": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "doro3_wood": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "abajorat": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "aqlam_touch_metal": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "aqlam_touch_light": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "mugat_white": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "mugat_magic": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "mugat_digital": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "engraved_wallet": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "sublimation": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ]
}

# ---------------------------------------------------------
# المرحلة: إدخال البيانات عند شراء منتج
# ---------------------------------------------------------
ASK_QUANTITY = 1
customer_data = {}

# ---------------------------------------------------------
# قائمة رئيسية
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
# إرسال الصور مع وصف وزر شراء
# ---------------------------------------------------------
def send_product_photos(update, context, product_key):
    query = update.callback_query
    query.answer()

    items = products.get(product_key, [])
    for idx, item in enumerate(items):
        media = InputMediaPhoto(media=item['photo'], caption=item['description'])
        context.bot.send_photo(chat_id=query.message.chat_id, photo=item['photo'], caption=f"{item['description']}\n\n✅ اضغط شراء لطلب هذا المنتج", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{product_key}_{idx}")],
            [InlineKeyboardButton("🔙 رجوع", callback_data=f"back_{product_key}")]
        ]))

# ---------------------------------------------------------
# التحكم في الأزرار
# ---------------------------------------------------------
def button_handler(update, context):
    query = update.callback_query
    data = query.data

    # رجوع للقائمة الرئيسية
    if data == "back_main":
        start(update, context)
        return

    # معالجة الأقسام الرئيسية
    sections = {
        "sawany": ["sawany_acrylic", "sawany_wood"],
        "taarat": ["taarat_acrylic", "taarat_wood"],
        "bsamat": ["bsamat"],
        "wedding_tissues": ["wedding_tissues"],
        "haram": ["haram_acrylic", "haram_metal", "haram_wood"],
        "doro3": ["doro3_acrylic", "doro3_metal", "doro3_wood"],
        "abajorat": ["abajorat"],
        "aqlam": ["aqlam_touch_metal", "aqlam_touch_light"],
        "mugat": ["mugat_white", "mugat_magic", "mugat_digital"],
        "engraved_wallet": ["engraved_wallet"],
        "sublimation": ["sublimation"]
    }

    # إذا كان القسم يحتوي على أقسام فرعية
    if data in sections:
        subs = sections[data]
        keyboard = [[InlineKeyboardButton(sub.replace("_", " ").title(), callback_data=sub)] for sub in subs]
        keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"اختر القسم الفرعي:", reply_markup=reply_markup)
        return

    # إذا كان القسم فرعي أو منتجات مباشرة
    if data in products:
        send_product_photos(update, context, data)
        return

    # إذا كان الضغط على زر شراء
    if data.startswith("buy_"):
        parts = data.split("_")
        key = "_".join(parts[1:-1])
        idx = int(parts[-1])
        item = products[key][idx]
        phone_number = "201288846355"  # ضع رقم واتساب هنا مع كود الدولة بدون +
        text = f"طلب منتج من البوت:\nالمنتج: {key}\nالوصف: {item['description']}"
        wa_link = f"https://wa.me/{phone_number}?text={text}"
        query.answer(text="يتم فتح واتساب لإرسال الطلب", show_alert=True)
        query.bot.send_message(chat_id=query.message.chat_id, text=f"اضغط هنا لإرسال الطلب على واتساب:\n{wa_link}")

# ---------------------------------------------------------
# تشغيل البوت
# ---------------------------------------------------------
def main():
    TOKEN = os.getenv("TOKEN")
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
