from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler

# قائمة الأزرار الرئيسية
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

# القوائم الفرعية لكل قسم مع المنتجات
sawany_submenu = [
    {"label": "صواني شبكة اكليريك", "callback": "sawany_akerik"},
    {"label": "صواني شبكة خشب", "callback": "sawany_khashab"}
]

taarat_submenu = [
    {"label": "طارات اكليريك", "callback": "taarat_akerik"},
    {"label": "طارات خشب", "callback": "taarat_khashab"}
]

haram_submenu = [
    {"label": "هرم مكتب اكليريك", "callback": "haram_akerik"},
    {"label": "هرم مكتب معدن بديل", "callback": "haram_metal"},
    {"label": "هرم مكتب خشب", "callback": "haram_khashab"}
]

doro3_submenu = [
    {"label": "دروع اكليريك", "callback": "doro3_akerik"},
    {"label": "دروع معدن بديل", "callback": "doro3_metal"},
    {"label": "دروع قطيفة", "callback": "doro3_qatifah"},
    {"label": "دروع خشب", "callback": "doro3_khashab"}
]

aqlam_submenu = [
    {"label": "قلم تاتش معدن", "callback": "aqlam_metal"},
    {"label": "قلم تاتش مضئ", "callback": "aqlam_luminous"}
]

mugat_submenu = [
    {"label": "مج ابيض", "callback": "mugat_white"},
    {"label": "مج سحري", "callback": "mugat_magic"},
    {"label": "مج ديجتال", "callback": "mugat_digital"}
]

# دالة لعرض القائمة الرئيسية
def start(update, context):
    user_name = update.message.from_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختر طلبك من القائمة:"
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in main_menu]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(greeting_text, reply_markup=reply_markup)

# دالة لمعالجة الضغط على الأزرار
def button(update, context):
    query = update.callback_query
    data = query.data

    # عرض القوائم الفرعية حسب الزر الذي تم الضغط عليه
    if data == "sawany":
        keyboard = [[InlineKeyboardButton(product["label"], callback_data=product["callback"])] for product in sawany_submenu]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("اختر نوع الصواني:", reply_markup=reply_markup)

    elif data == "taarat":
        keyboard = [[InlineKeyboardButton(product["label"], callback_data=product["callback"])] for product in taarat_submenu]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("اختر نوع الطارات:", reply_markup=reply_markup)

    elif data == "haram":
        keyboard = [[InlineKeyboardButton(product["label"], callback_data=product["callback"])] for product in haram_submenu]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("اختر نوع هرم المكتب:", reply_markup=reply_markup)

    elif data == "doro3":
        keyboard = [[InlineKeyboardButton(product["label"], callback_data=product["callback"])] for product in doro3_submenu]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("اختر نوع الدروع:", reply_markup=reply_markup)

    elif data == "aqlam":
        keyboard = [[InlineKeyboardButton(product["label"], callback_data=product["callback"])] for product in aqlam_submenu]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("اختر نوع الأقلام:", reply_markup=reply_markup)

    elif data == "mugat":
        keyboard = [[InlineKeyboardButton(product["label"], callback_data=product["callback"])] for product in mugat_submenu]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("اختر نوع المجات:", reply_markup=reply_markup)

    # عرض المنتجات عند اختيار نوع معين
    elif data == "sawany_akerik":
        query.edit_message_text("صور وتفاصيل صواني شبكة اكليريك هنا.")
    elif data == "sawany_khashab":
        query.edit_message_text("صور وتفاصيل صواني شبكة خشب هنا.")
    elif data == "taarat_akerik":
        query.edit_message_text("صور وتفاصيل طارات اكليريك هنا.")
    elif data == "taarat_khashab":
        query.edit_message_text("صور وتفاصيل طارات خشب هنا.")
    elif data == "haram_akerik":
        query.edit_message_text("صور وتفاصيل هرم مكتب اكليريك هنا.")
    elif data == "haram_metal":
        query.edit_message_text("صور وتفاصيل هرم مكتب معدن بديل هنا.")
    elif data == "haram_khashab":
        query.edit_message_text("صور وتفاصيل هرم مكتب خشب هنا.")
    elif data == "doro3_akerik":
        query.edit_message_text("صور وتفاصيل دروع اكليريك هنا.")
    elif data == "doro3_metal":
        query.edit_message_text("صور وتفاصيل دروع معدن بديل هنا.")
    elif data == "doro3_qatifah":
        query.edit_message_text("صور وتفاصيل دروع قطيفة هنا.")
    elif data == "doro3_khashab":
        query.edit_message_text("صور وتفاصيل دروع خشب هنا.")
    elif data == "aqlam_metal":
        query.edit_message_text("صور وتفاصيل قلم تاتش معدن هنا.")
    elif data == "aqlam_luminous":
        query.edit_message_text("صور وتفاصيل قلم تاتش مضئ هنا.")
    elif data == "mugat_white":
        query.edit_message_text("صور وتفاصيل مج ابيض هنا.")
    elif data == "mugat_magic":
        query.edit_message_text("صور وتفاصيل مج سحري هنا.")
    elif data == "mugat_digital":
        query.edit_message_text("صور وتفاصيل مج ديجتال هنا.")

# إعدادات البوت
def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()