import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

# ---------------------------------------------------------
# بيانات المنتجات (كل قسم فرعي -> مجموعة صور مع وصف)
# ---------------------------------------------------------
PRODUCTS = {
    "sawany_acrylic": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"},
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف2"}
    ],
    "sawany_wood": [
        {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}
    ],
    "taarat_acrylic": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "taarat_wood": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "haram_acrylic": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "haram_metal": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "haram_wood": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "doro3_acrylic": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "doro3_metal": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "doro3_wood": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "aqlam_touch_metal": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "aqlam_touch_light": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "mugat_white": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "mugat_magic": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "mugat_digital": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "wallets_havan": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "wallets_brown": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "wallets_black": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
    "sublimation": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"}],
}

# ---------------------------------------------------------
# القوائم الرئيسية والفرعية
# ---------------------------------------------------------
MAIN_MENU = [
    [InlineKeyboardButton("💍 صواني شبكة", callback_data='sawany')],
    [InlineKeyboardButton("💍 طارات خطوبة وكتب الكتاب", callback_data='taarat')],
    [InlineKeyboardButton("🏛️ هرم مكتب", callback_data='haram')],
    [InlineKeyboardButton("🛡️ دروع", callback_data='doro3')],
    [InlineKeyboardButton("✏️ اقلام", callback_data='aqlam')],
    [InlineKeyboardButton("☕ مجات", callback_data='mugat')],
    [InlineKeyboardButton("👛 محافظ محفورة بالاسم", callback_data='wallets')],
    [InlineKeyboardButton("🎨 مستلزمات سبلميشن", callback_data='sublimation')],
]

SUB_MENUS = {
    "sawany": [
        [InlineKeyboardButton("صواني شبكة اكليريك", callback_data='sawany_acrylic')],
        [InlineKeyboardButton("صواني شبكة خشب", callback_data='sawany_wood')]
    ],
    "taarat": [
        [InlineKeyboardButton("طارات خطوبة وكتب الكتاب اكليريك", callback_data='taarat_acrylic')],
        [InlineKeyboardButton("طارات خطوبة وكتب الكتاب خشب", callback_data='taarat_wood')]
    ],
    "haram": [
        [InlineKeyboardButton("هرم مكتب اكليريك", callback_data='haram_acrylic')],
        [InlineKeyboardButton("هرم مكتب بديل المعدن", callback_data='haram_metal')],
        [InlineKeyboardButton("هرم مكتب خشب", callback_data='haram_wood')]
    ],
    "doro3": [
        [InlineKeyboardButton("دروع اكليريك", callback_data='doro3_acrylic')],
        [InlineKeyboardButton("دروع بديل المعدن", callback_data='doro3_metal')],
        [InlineKeyboardButton("دروع خشب", callback_data='doro3_wood')]
    ],
    "aqlam": [
        [InlineKeyboardButton("قلم تاتش معدن", callback_data='aqlam_touch_metal')],
        [InlineKeyboardButton("قلم تاتش مضئ", callback_data='aqlam_touch_light')]
    ],
    "mugat": [
        [InlineKeyboardButton("مج ابيض", callback_data='mugat_white')],
        [InlineKeyboardButton("مج سحري", callback_data='mugat_magic')],
        [InlineKeyboardButton("مج ديجتال", callback_data='mugat_digital')]
    ],
    "wallets": [
        [InlineKeyboardButton("هافان (بيج)", callback_data='wallets_havan')],
        [InlineKeyboardButton("بني", callback_data='wallets_brown')],
        [InlineKeyboardButton("اسود", callback_data='wallets_black')]
    ],
    "sublimation": [
        [InlineKeyboardButton("مستلزمات سبلميشن", callback_data='sublimation')]
    ]
}

# ---------------------------------------------------------
# start command
# ---------------------------------------------------------
def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    welcome_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختار طلبك من القائمة:"
    update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(MAIN_MENU))

# ---------------------------------------------------------
# التعامل مع القوائم
# ---------------------------------------------------------
def menu_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    query.answer()

    # إذا فيه قائمة فرعية
    if data in SUB_MENUS:
        query.edit_message_text("اختر القسم الفرعي:", reply_markup=InlineKeyboardMarkup(SUB_MENUS[data]))
        return

    # إذا اخترنا منتج فعلي
    if data in PRODUCTS:
        send_product_group(query, context, data)
        return

# ---------------------------------------------------------
# إرسال مجموعة صور لمنتج مع وصف + زر شراء + رجوع
# ---------------------------------------------------------
def send_product_group(query, context, product_key):
    products = PRODUCTS[product_key]
    for item in products:
        media = InputMediaPhoto(item["photo"], caption=item["description"])
        context.bot.send_media_group(chat_id=query.message.chat_id, media=[media])

        # زر شراء وزر رجوع
        keyboard = [
            [InlineKeyboardButton("شراء", callback_data=f"buy_{product_key}")],
            [InlineKeyboardButton("🔙 رجوع للقائمة السابقة", callback_data=product_key)]
        ]
        context.bot.send_message(chat_id=query.message.chat_id, text="اختار:", reply_markup=InlineKeyboardMarkup(keyboard))

# ---------------------------------------------------------
# شراء (هنا يمكن توليد رابط واتساب)
# ---------------------------------------------------------
def buy_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    product_key = query.data.replace("buy_", "")
    # هنا نقدر نطلب من العميل بيانات الطلب لاحقاً
    msg = f"لشراء {product_key}، سيتم تحويلك إلى واتساب مع رابط جاهز لتكملة الطلب."
    whatsapp_link = f"https://wa.me/رقمك_هنا?text=طلب+{product_key}"
    query.edit_message_text(f"{msg}\n{whatsapp_link}")

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        print("Error: TOKEN environment variable is not set.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(menu_handler, pattern='^(?!buy_).+'))
    dp.add_handler(CallbackQueryHandler(buy_handler, pattern='^buy_'))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
