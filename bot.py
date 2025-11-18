import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# ---------------------------------------------------------
# القوائم الرئيسية والفرعية
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

SUB_MENUS = {
    "sawany": [
        [InlineKeyboardButton("صواني شبكة اكليريك", callback_data="sawany_acrylic")],
        [InlineKeyboardButton("صواني شبكة خشب", callback_data="sawany_wood")]
    ],
    "taarat": [
        [InlineKeyboardButton("طارات خطوبة وكتب الكتاب اكليريك", callback_data="taarat_acrylic")],
        [InlineKeyboardButton("طارات خطوبة وكتب الكتاب خشب", callback_data="taarat_wood")]
    ],
    "haram": [
        [InlineKeyboardButton("هرم مكتب اكليريك", callback_data="haram_acrylic")],
        [InlineKeyboardButton("هرم مكتب بديل المعدن", callback_data="haram_metal")],
        [InlineKeyboardButton("هرم مكتب خشب", callback_data="haram_wood")]
    ],
    "doro3": [
        [InlineKeyboardButton("دروع اكليريك", callback_data="doro3_acrylic")],
        [InlineKeyboardButton("دروع بديل المعدن", callback_data="doro3_metal")],
        [InlineKeyboardButton("دروع خشب", callback_data="doro3_wood")]
    ],
    "aqlam": [
        [InlineKeyboardButton("قلم تاتش معدن", callback_data="aqlam_touch_metal")],
        [InlineKeyboardButton("قلم تاتش مضئ", callback_data="aqlam_touch_light")]
    ],
    "mugat": [
        [InlineKeyboardButton("مج ابيض", callback_data="mugat_white")],
        [InlineKeyboardButton("مج سحري", callback_data="mugat_magic")],
        [InlineKeyboardButton("مج ديجتال", callback_data="mugat_digital")]
    ],
    "wallets": [
        [InlineKeyboardButton("هافان (بيج)", callback_data="wallets_havan")],
        [InlineKeyboardButton("بني", callback_data="wallets_brown")],
        [InlineKeyboardButton("اسود", callback_data="wallets_black")]
    ]
}

# ---------------------------------------------------------
# المنتجات مع الصور والوصف
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
# الرجوع للقائمة السابقة لكل منتج
# ---------------------------------------------------------
PRODUCT_PARENT_MENU = {
    "sawany_acrylic": "sawany",
    "sawany_wood": "sawany",
    "taarat_acrylic": "taarat",
    "taarat_wood": "taarat",
    "haram_acrylic": "haram",
    "haram_metal": "haram",
    "haram_wood": "haram",
    "doro3_acrylic": "doro3",
    "doro3_metal": "doro3",
    "doro3_wood": "doro3",
    "aqlam_touch_metal": "aqlam",
    "aqlam_touch_light": "aqlam",
    "mugat_white": "mugat",
    "mugat_magic": "mugat",
    "mugat_digital": "mugat",
    "wallets_havan": "wallets",
    "wallets_brown": "wallets",
    "wallets_black": "wallets",
    "sublimation": None
}

# ---------------------------------------------------------
# دوال البوت
# ---------------------------------------------------------
def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    welcome_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختار طلبك من القائمة:"
    update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(MAIN_MENU))

def send_product_group(query, context, product_key):
    products = PRODUCTS[product_key]
    parent_menu = PRODUCT_PARENT_MENU.get(product_key, None)
    for item in products:
        media = InputMediaPhoto(item["photo"], caption=item["description"])
        context.bot.send_media_group(chat_id=query.message.chat_id, media=[media])

        keyboard = [[InlineKeyboardButton("شراء", callback_data=f"buy_{product_key}")]]
        if parent_menu:
            keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة السابقة", callback_data=parent_menu)])
        else:
            keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main")])

        context.bot.send_message(chat_id=query.message.chat_id, text="اختار:", reply_markup=InlineKeyboardMarkup(keyboard))

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

def main():
    TOKEN = os.getenv("TOKEN")  # يجب أن يكون موجود كـ Environment Variable
    if not TOKEN:
        print("Error: TOKEN environment variable is not set.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(menu_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
