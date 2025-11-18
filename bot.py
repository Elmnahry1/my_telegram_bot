import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler

# --------------------
# 1. بيانات القوائم والمنتجات (كما هي)
# --------------------
sawany_submenu = [
    {"label": "صواني شبكة اكليريك", "callback": "sawany_akerik", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف صواني شبكة اكليريك"},
    {"label": "صواني شبكة خشب", "callback": "sawany_khashab", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف صواني شبكة خشب"}
]

taarat_submenu = [
    {"label": "طارات اكليريك", "callback": "taarat_akerik", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارات اكليريك"},
    {"label": "طارات خشب", "callback": "taarat_khashab", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارات خشب"}
]

haram_submenu = [
    {"label": "هرم مكتب اكليريك", "callback": "haram_akerik", "image": "path/to/haram_akerik.jpg", "description": "وصف هرم مكتب اكليريك"},
    {"label": "هرم مكتب معدن بديل", "callback": "haram_metal", "image": "path/to/haram_metal.jpg", "description": "وصف هرم مكتب معدن بديل"},
    {"label": "هرم مكتب خشب", "callback": "haram_khashab", "image": "path/to/haram_khashab.jpg", "description": "وصف هرم مكتب خشب"}
]

doro3_submenu = [
    {"label": "دروع اكليريك", "callback": "doro3_akerik", "image": "path/to/doro3_akerik.jpg", "description": "وصف دروع اكليريك"},
    {"label": "دروع معدن بديل", "callback": "doro3_metal", "image": "path/to/doro3_metal.jpg", "description": "وصف دروع معدن بديل"},
    {"label": "دروع قطيفة", "callback": "doro3_qatifah", "image": "path/to/doro3_qatifah.jpg", "description": "وصف دروع قطيفة"},
    {"label": "دروع خشب", "callback": "doro3_khashab", "image": "path/to/doro3_khashab.jpg", "description": "وصف دروع خشب"}
]

aqlam_submenu = [
    {"label": "قلم تاتش معدن", "callback": "aqlam_metal", "image": "path/to/aqlam_metal.jpg", "description": "وصف قلم تاتش معدن"},
    {"label": "قلم تاتش مضئ", "callback": "aqlam_luminous", "image": "path/to/aqlam_luminous.jpg", "description": "وصف قلم تاتش مضئ"}
]

mugat_submenu = [
    {"label": "مج ابيض", "callback": "mugat_white", "image": "path/to/mugat_white.jpg", "description": "وصف مج ابيض"},
    {"label": "مج سحري", "callback": "mugat_magic", "image": "path/to/mugat_magic.jpg", "description": "وصف مج سحري"},
    {"label": "مج ديجتال", "callback": "mugat_digital", "image": "path/to/mugat_digital.jpg", "description": "وصف مج ديجتال"}
]

main_menu = [
    {"label": "💍💍 صواني شبكة", "callback": "sawany"},
    {"label": "💍 طارات خطوبة وكتب الكتاب", "callback": "taarat"},
    {"label": "✋ بصامات", "callback": "bsamat"},
    {"label": "📜 مناديل كتب الكتاب", "callback": "wedding_tissues"},
    {"label": "🗄️ هرم مكتب", "callback": "haram"},
    {"label": "🏆 دروع", "callback": "doro3"},
    {"label": "💡 اباجورات", "callback": "abajorat"},
    {"label": "✏️ اقلام", "callback": "aqlam"},
    {"label": "☕ مجات", "callback": "mugat"},
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"},
    {"label": "🖨️ مستلزمات سبلميشن", "callback": "sublimation"}
]

product_to_submenu_map = {}
all_submenus = {
    "sawany": sawany_submenu,
    "taarat": taarat_submenu,
    "haram": haram_submenu,
    "doro3": doro3_submenu,
    "aqlam": aqlam_submenu,
    "mugat": mugat_submenu
}
for menu_key, submenu_list in all_submenus.items():
    for item in submenu_list:
        product_to_submenu_map[item["callback"]] = menu_key
# -----------------------------------------------------------


# --------------------
# 2. الدوال المساعدة (تم تطبيق منطق الحذف والإرسال الجديد)
# --------------------
def start(update, context):
    query = update.callback_query
    if query:
        query.answer()
        reply_source = query
    else:
        reply_source = update.message
    
    user_name = reply_source.from_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختر طلبك من القائمة:"
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in main_menu]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query:
        # 💡 عند العودة من قائمة فرعية، نحذف الرسالة القديمة ونرسل رسالة جديدة
        try:
            query.message.delete()
        except Exception:
            pass # نتجاهل الأخطاء
        
        update.effective_chat.send_message(greeting_text, reply_markup=reply_markup)
    else:
        update.message.reply_text(greeting_text, reply_markup=reply_markup)

def show_submenu(update, context, submenu, title):
    query = update.callback_query
    
    if query:
        query.answer()
        
        # 💡 عند العودة من صفحة منتج، نحذف رسالة الصورة ونرسل رسالة جديدة
        try:
            query.message.delete()
        except Exception:
            pass # نتجاهل الأخطاء
        
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in submenu]
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 💡 نرسل رسالة نصية جديدة بدلاً من التعديل لضمان الانتقال السلس
    update.effective_chat.send_message(f"اختر {title}:", reply_markup=reply_markup)


def show_product_page(update, product_callback_data, image_url, description):
    query = update.callback_query
    if query:
        query.answer()

    previous_submenu_key = product_to_submenu_map.get(product_callback_data, "main_menu")

    keyboard = [
        [InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{product_callback_data}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=previous_submenu_key)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # نحذف الرسالة السابقة (القائمة الفرعية)
    if query and query.message:
        try:
            query.message.delete()
        except Exception:
            pass
        
    update.effective_message.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_url,
        caption=f"**{product_callback_data.replace('_', ' ').title()}**\n\n{description}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def button(update, context):
    query = update.callback_query
    data = query.data

    # 1. حالة العودة إلى القائمة الرئيسية 
    if data == "main_menu":
        start(update, context)
        return

    # 2. حالات القوائم الرئيسية أو الرجوع إلى قائمة فرعية (يعمل الآن من زر الرجوع في صفحة المنتج)
    if data in all_submenus:
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1] 
        show_submenu(update, context, all_submenus[data], clean_title)
        return

    # 3. إذا اختير منتج معين
    for submenu_key, submenu in all_submenus.items():
        for item in submenu:
            if data == item["callback"]:
                show_product_page(update, item["callback"], item["image"], item["description"])
                return
    
    # 4. حالة زر الشراء
    if data.startswith("buy_"):
        product_key = data.replace("buy_", "")
        query.answer(text=f"سيتم الآن تجهيز طلب شراء للمنتج: {product_key}", show_alert=True)
        return


# --------------------
# 3. إعداد البوت 
# --------------------
def main():
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN) في بيئة العمل. يرجى التأكد من تعيينه.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()