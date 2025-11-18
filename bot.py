import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler

# بيانات المنتجات مع الصور - ضع مسارات الصور الحقيقية هنا
sawany_submenu = [
    {"label": "صواني شبكة اكليريك", "callback": "sawany_akerik", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"},
    {"label": "صواني شبكة خشب", "callback": "sawany_khashab", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"}
]
taarat_submenu = [
    {"label": "طارات اكليريك", "callback": "taarat_akerik", "image": "path/to/taarat_akerik.jpg"},
    {"label": "طارات خشب", "callback": "taarat_khashab", "image": "path/to/taarat_khashab.jpg"}
]
haram_submenu = [
    {"label": "هرم مكتب اكليريك", "callback": "haram_akerik", "image": "path/to/haram_akerik.jpg"},
    {"label": "هرم مكتب معدن بديل", "callback": "haram_metal", "image": "path/to/haram_metal.jpg"},
    {"label": "هرم مكتب خشب", "callback": "haram_khashab", "image": "path/to/haram_khashab.jpg"}
]
doro3_submenu = [
    {"label": "دروع اكليريك", "callback": "doro3_akerik", "image": "path/to/doro3_akerik.jpg"},
    {"label": "دروع معدن بديل", "callback": "doro3_metal", "image": "path/to/doro3_metal.jpg"},
    {"label": "دروع قطيفة", "callback": "doro3_qatifah", "image": "path/to/doro3_qatifah.jpg"},
    {"label": "دروع خشب", "callback": "doro3_khashab", "image": "path/to/doro3_khashab.jpg"}
]
aqlam_submenu = [
    {"label": "قلم تاتش معدن", "callback": "aqlam_metal", "image": "path/to/aqlam_metal.jpg"},
    {"label": "قلم تاتش مضئ", "callback": "aqlam_luminous", "image": "path/to/aqlam_luminous.jpg"}
]
mugat_submenu = [
    {"label": "مج ابيض", "callback": "mugat_white", "image": "path/to/mugat_white.jpg"},
    {"label": "مج سحري", "callback": "mugat_magic", "image": "path/to/mugat_magic.jpg"},
    {"label": "مج ديجتال", "callback": "mugat_digital", "image": "path/to/mugat_digital.jpg"}
]

# القائمة الرئيسية
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
    # التحقق من نوع التحديث
    if hasattr(update, 'message') and update.message:
        user_name = update.message.from_user.first_name
        chat_id = update.message.chat_id
        reply_source = update.message
    elif hasattr(update, 'callback_query') and update.callback_query:
        user_name = update.callback_query.from_user.first_name
        chat_id = update.callback_query.message.chat_id
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

# دالة لعرض القوائم الفرعية
def show_submenu(update, context, submenu, title):
    if hasattr(update, 'callback_query') and update.callback_query:
        reply_source = update.callback_query
    elif hasattr(update, 'message') and update.message:
        reply_source = update.message
    else:
        return
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in submenu]
    keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_source.edit_message_text(f"اختر {title}:", reply_markup=reply_markup)

# دالة لعرض المنتج
def show_product(update, product):
    if hasattr(update, 'callback_query') and update.callback_query:
        reply_source = update.callback_query
    elif hasattr(update, 'message') and update.message:
        reply_source = update.message
    else:
        return
    # زر الرجوع
    keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    with open(product["image"], 'rb') as photo:
        reply_source.bot.send_photo(
            chat_id=reply_source.message.chat_id if hasattr(reply_source, 'message') else reply_source.message.chat_id,
            photo=photo,
            caption=product["label"],
            reply_markup=reply_markup
        )

# معالجة الضغط على الأزرار
def button(update, context):
    query = update.callback_query
    data = query.data

    if data == "main_menu":
        start(update, context)
        return
    elif data == "back":
        start(update, context)
        return
    elif data == "sawany":
        show_submenu(update, context, sawany_submenu, "نوع الصواني")
        return
    elif data == "taarat":
        show_submenu(update, context, taarat_submenu, "نوع الطارات")
        return
    elif data == "haram":
        show_submenu(update, context, haram_submenu, "نوع هرم المكتب")
        return
    elif data == "doro3":
        show_submenu(update, context, doro3_submenu, "نوع الدروع")
        return
    elif data == "aqlam":
        show_submenu(update, context, aqlam_submenu, "نوع الأقلام")
        return
    elif data == "mugat":
        show_submenu(update, context, mugat_submenu, "نوع المجات")
        return
    else:
        # البحث عن المنتج المحدد
        for submenu in [sawany_submenu, taarat_submenu, haram_submenu, doro3_submenu, aqlam_submenu, mugat_submenu]:
            for item in submenu:
                if data == item["callback"]:
                    show_product(update, item)
                    return

# إعدادات البوت
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