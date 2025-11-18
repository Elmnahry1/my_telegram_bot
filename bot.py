import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler

# بيانات المنتجات (كما هي)
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

# دالة لعرض القائمة الرئيسية
def start(update, context):
    if hasattr(update, 'message') and update.message:
        user_name = update.message.from_user.first_name
        reply_source = update.message
    elif hasattr(update, 'callback_query') and update.callback_query:
        user_name = update.callback_query.from_user.first_name
        reply_source = update.callback_query
    else:
        return

    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختر طلبك من القائمة:"
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in main_menu]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if hasattr(update, 'message') and update.message:
        update.message.reply_text(greeting_text, reply_markup=reply_markup)
    elif hasattr(update, 'callback_query') and update.callback_query:
        update.callback_query.edit_message_text(greeting_text, reply_markup=reply_markup)

# دالة لعرض القوائم الفرعية مع زر رجوع
def show_submenu(update, context, submenu, title, previous_callback):
    if hasattr(update, 'callback_query') and update.callback_query:
        reply_source = update.callback_query
    elif hasattr(update, 'message') and update.message:
        reply_source = update.message
    else:
        return
    # أزرار المنتجات
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in submenu]
    # زر رجوع يعيد إلى الصفحة السابقة
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=previous_callback)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_source.edit_message_text(f"اختر {title}:", reply_markup=reply_markup)

# دالة لعرض المنتج مع وصف وصورة، مع تحديد الصفحة السابقة
def show_product(update, product, previous_callback):
    if hasattr(update, 'callback_query') and update.callback_query:
        reply_source = update.callback_query
    elif hasattr(update, 'message') and update.message:
        reply_source = update.message
    else:
        return

    # أزرار الشراء والرجوع
    keyboard = [
        [InlineKeyboardButton("شراء", callback_data="buy")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=previous_callback)]  # الرجوع إلى الصفحة السابقة
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    reply_source.bot.send_photo(
        chat_id=reply_source.message.chat_id,
        photo=product["image"],
        caption=f"{product['label']}\n\n{product.get('description', 'لا يوجد وصف')}",
        reply_markup=reply_markup
    )

# دالة لعرض منتج معين عند الاختيار، مع تحديد الصفحة السابقة
def show_specific_product(update, image_url, description, previous_callback):
    if hasattr(update, 'callback_query') and update.callback_query:
        reply_source = update.callback_query
    elif hasattr(update, 'message') and update.message:
        reply_source = update.message
    else:
        return

    # أزرار الشراء والرجوع
    keyboard = [
        [InlineKeyboardButton("شراء", callback_data="buy")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=previous_callback)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    reply_source.bot.send_photo(
        chat_id=reply_source.message.chat_id,
        photo=image_url,
        caption=f"{description}",
        reply_markup=reply_markup
    )

# معالج الضغط على الأزرار
def button(update, context):
    query = update.callback_query
    data = query.data

    # العودة للقائمة الرئيسية
    if data == "main_menu":
        start(update, context)
        return

    # الرجوع حسب الصفحة السابقة
    elif data.startswith("back_to_") or data == "back":
        # نحدد الصفحة السابقة من callback_data
        previous_callback = data.replace("back_to_", "") if data.startswith("back_to_") else "main_menu"
        start(update, context)
        return
    elif data == "back":
        start(update, context)
        return

    # حالات القوائم الرئيسية
    elif data == "sawany":
        show_submenu(update, context, sawany_submenu, "نوع الصواني", previous_callback="main_menu")
        return
    elif data == "taarat":
        show_submenu(update, context, taarat_submenu, "نوع الطارات", previous_callback="main_menu")
        return
    elif data == "haram":
        show_submenu(update, context, haram_submenu, "نوع هرم المكتب", previous_callback="main_menu")
        return
    elif data == "doro3":
        show_submenu(update, context, doro3_submenu, "نوع الدروع", previous_callback="main_menu")
        return
    elif data == "aqlam":
        show_submenu(update, context, aqlam_submenu, "نوع الأقلام", previous_callback="main_menu")
        return
    elif data == "mugat":
        show_submenu(update, context, mugat_submenu, "نوع المجات", previous_callback="main_menu")
        return

    # إذا كانت رجوع من قائمة فرعية، نعيد بناء اسم الصفحة السابقة
    if data.startswith("back_from_"):
        previous_page = data.replace("back_from_", "")
        if previous_page == "sawany":
            show_submenu(update, context, sawany_submenu, "نوع الصواني", previous_callback="sawany")
        elif previous_page == "taarat":
            show_submenu(update, context, taarat_submenu, "نوع الطارات", previous_callback="taarat")
        elif previous_page == "haram":
            show_submenu(update, context, haram_submenu, "نوع هرم المكتب", previous_callback="haram")
        elif previous_page == "doro3":
            show_submenu(update, context, doro3_submenu, "نوع الدروع", previous_callback="doro3")
        elif previous_page == "aqlam":
            show_submenu(update, context, aqlam_submenu, "نوع الأقلام", previous_callback="aqlam")
        elif previous_page == "mugat":
            show_submenu(update, context, mugat_submenu, "نوع المجات", previous_callback="mugat")
        return

    # إذا اختير منتج معين
    for submenu in [sawany_submenu, taarat_submenu, haram_submenu, doro3_submenu, aqlam_submenu, mugat_submenu]:
        for item in submenu:
            if data == item["callback"]:
                show_specific_product(update, item["image"], item["description"], previous_callback=item["callback"])
                return

# إعداد البوت
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