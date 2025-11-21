import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# تم استيراد Updater بدلاً من Application
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات الواتساب: استبدل بالرقم الخاص بك
WHATSAPP_NUMBER = "201288846355" 

# --------------------
# 1. تعريف حالات المحادثة
# --------------------

GET_WALLET_NAME = 1 # حالة المحافظ
GET_PEN_NAME = 2    # حالة الأقلام (استقبال الاسم)
GET_BOX_COLOR = 3   # حالة اختيار لون البوكس
GET_BOX_NAMES = 4   # حالة كتابة أسماء العرسان للبوكس
GET_TRAY_NAMES = 5  # حالة كتابة الأسماء للصينية الاكليريك
GET_TRAY_DATE = 6   # حالة كتابة التاريخ للصينية الاكليريك
GET_KHASHAB_TRAY_NAMES = 7 # حالة كتابة الأسماء لصينية الخشب
GET_KHASHAB_TRAY_DATE = 8  # حالة كتابة التاريخ لصينية الخشب
GET_AKRILIK_TAARAT_NAMES = 9 # حالة أسماء طارات اكليريك
GET_AKRILIK_TAARAT_DATE = 10 # حالة تاريخ طارات اكليريك
GET_KHASHAB_TAARAT_NAMES = 11 # حالة أسماء طارات خشب
GET_KHASHAB_TAARAT_DATE = 12 # حالة تاريخ طارات خشب

# حالات البصامات
GET_BSAMAT_NAMES = 13  # حالة كتابة أسماء العرسان للبصامات
GET_BSAMAT_DATE = 14   # حالة كتابة التاريخ للبصامات

# حالات مناديل كتب الكتاب
GET_TISSUE_NAMES = 15  # حالة كتابة أسماء العرسان للمناديل
GET_TISSUE_DATE = 16   # حالة كتابة التاريخ للمناديل

# 🆕 حالة اختيار نوع القلم الجديد
SELECT_PEN_TYPE = 17 


# --------------------
# 2. بيانات القوائم والمنتجات (تم استخدام صور وهمية/بسيطة)
# --------------------

def get_placeholder_image():
    # صورة وهمية للمنتجات التي لا تظهر صورها في القوائم الفرعية
    return "https://via.placeholder.com/300x200?text=Product+Image"


# القوائم الفرعية
bsamat_submenu = [{"label": "بصامة موديل 1", "callback": "bsamat_m1", "image": get_placeholder_image(), "description": "وصف البصامة موديل 1."}]
wedding_tissues_submenu = [{"label": "منديل موديل 1", "callback": "tissue_m1", "image": get_placeholder_image(), "description": "وصف منديل كتب الكتاب موديل 1."}]
katb_kitab_box_submenu = [{"label": "بوكس كتب كتاب موديل 1", "callback": "box_m1", "image": get_placeholder_image(), "description": "وصف بوكس كتب الكتاب موديل 1."}]
abajorat_submenu = [{"label": "أباجورة موديل 1", "callback": "abajora_m1", "image": get_placeholder_image(), "description": "وصف الأباجورة موديل 1."}]
engraved_wallet_submenu = [
    {"label": "محفظة بيج", "callback": "wallet_bege", "image": get_placeholder_image(), "description": "محفظة بيج."},
    {"label": "محفظة بني", "callback": "wallet_brown", "image": get_placeholder_image(), "description": "محفظة بني."},
]
aqlam_submenu = [
    {
        "label": "قلم تاتش معدن", 
        "callback": "aqlam_metal", 
        "image": "https://i.imgur.com/Kz9Gf4M.png", # Placeholder image
        "description": "قلم تاتش معدن عالي الجودة."
    },
    {
        "label": "قلم تاتش مضئ", 
        "callback": "aqlam_luminous", 
        "image": "https://i.imgur.com/H1JbQ2t.png", # Placeholder image
        "description": "قلم تاتش مضئ بتقنية متطورة."
    }
]
sawany_submenu = [{"label": "صواني اكليريك", "callback": "sawany_akerik"}, {"label": "صواني خشب", "callback": "sawany_khashab"}] 
taarat_submenu = [{"label": "طارات اكليريك", "callback": "taarat_akerik"}, {"label": "طارات خشب", "callback": "taarat_khashab"}]
haram_submenu = [] 
doro3_submenu = [] 
mugat_submenu = [] 

# --- القائمة الرئيسية ---
main_menu = [
    {"label": "💍💍 صواني شبكة", "callback": "sawany"},
    {"label": "💍 طارات خطوبة وكتب الكتاب", "callback": "taarat"},
    {"label": "✋ بصامات", "callback": "bsamat"}, 
    {"label": "📜 مناديل كتب الكتاب", "callback": "wedding_tissues"},
    {"label": "🎁 بوكس كتب الكتاب", "callback": "katb_kitab_box"},
    {"label": "🗄️ هرم مكتب", "callback": "haram"},
    {"label": "🏆 دروع", "callback": "doro3"},
    {"label": "💡 اباجورات", "callback": "abajorat"}, 
    {"label": "✏️ اقلام", "callback": "aqlam"}, # 🎯 نقطة دخول المحادثة
    {"label": "☕ مجات", "callback": "mugat"},
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"},
    {"label": "🖨️ مستلزمات سبلميشن", "callback": "sublimation"}
]


all_submenus = {
    "sawany": sawany_submenu,
    "taarat": taarat_submenu,
    "haram": haram_submenu,
    "doro3": doro3_submenu,
    "aqlam": aqlam_submenu,
    "mugat": mugat_submenu,
    "bsamat": bsamat_submenu, 
    "wedding_tissues": wedding_tissues_submenu,
    "katb_kitab_box": katb_kitab_box_submenu,
    "abajorat": abajorat_submenu,
    "engraved_wallet": engraved_wallet_submenu
}


# --------------------
# 3. الدوال الرئيسية والمساعدة
# --------------------

def create_whatsapp_link(message, phone_number=WHATSAPP_NUMBER):
    """تنشئ رابط واتساب مع رسالة محددة."""
    text = quote_plus(message)
    return f"https://wa.me/{phone_number}?text={text}"


def cancel_and_end(update, context):
    query = update.callback_query
    if query:
        query.answer("تم إلغاء العملية الحالية. يرجى اختيار طلبك مرة أخرى.", show_alert=True)
        try:
            query.message.delete()
        except Exception:
            pass
    
    context.user_data.clear()
    return start(update, context) 


def start(update, context):
    query = update.callback_query
    # Clearing user_data when starting/restarting
    context.user_data.clear()
        
    if query:
        query.answer()
    
    user_name = update.effective_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختر طلبك من القائمة:"
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in main_menu]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query:
        try:
            query.edit_message_text(greeting_text, reply_markup=reply_markup, parse_mode="Markdown")
        except telegram.error.BadRequest:
            update.effective_chat.send_message(greeting_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        update.effective_message.reply_text(greeting_text, reply_markup=reply_markup, parse_mode="Markdown")
        
    return ConversationHandler.END


# دالة وهمية لعرض القوائم الفرعية
def show_submenu(update, context, submenu_list, title, back_callback="main_menu"):
    query = update.callback_query
    query.answer()
    
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in submenu_list]
    keyboard.append([InlineKeyboardButton("رجوع", callback_data=back_callback)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = f"قائمة **{title}**:\nالرجاء اختيار المنتج:"
    
    try:
        query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest:
        update.effective_chat.send_message(message_text, reply_markup=reply_markup, parse_mode="Markdown")


# دالة وهمية لعرض صفحات المنتجات المباشرة
def show_product_page(update, product_callback_data, product_list, is_direct_list=False):
    query = update.callback_query
    query.answer()
    
    message_text = "قائمة المنتجات المباشرة:\n"
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=f"buy_{item['callback']}")] for item in product_list]
    keyboard.append([InlineKeyboardButton("رجوع", callback_data="back_to_main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        query.edit_message_text(message_text, reply_markup=reply_markup)
    except telegram.error.BadRequest:
        update.effective_chat.send_message(message_text, reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    data = query.data
    query.answer()

    # 1. معالجة زر الرجوع للقائمة الرئيسية
    if data == "back_to_main_menu":
        return start(update, context)

    # 2. معالجة فتح قوائم المستوى الأول المتداخلة 
    if data in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus[data], clean_title, back_callback="back_to_main_menu")
        return

    # 3. معالجة فتح قوائم المستوى الأول المباشرة 
    if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "engraved_wallet"]: 
        submenu_list = all_submenus.get(data)
        show_product_page(update, data, submenu_list, is_direct_list=True)
        return

    # 4. معالجة عرض صفحات المنتجات مباشرة (قوائم المستوى الثاني)
    product_list_keys = ["sawany_akerik", "sawany_khashab"] 
    if data in product_list_keys:
        query.edit_message_text(f"تم اختيار {data}. يرجى اختيار المنتج المطلوب.", 
                                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="sawany")]]))
        return
        
    # 5. معالجة أزرار الشراء الفردية التي لم تعالج بواسطة Conversation Handlers
    if data.startswith("buy_"):
        product_callback = data.replace("buy_", "")
        wa_link = create_whatsapp_link(f"طلب شراء المنتج ذو الكود: {product_callback}")
        keyboard = [[InlineKeyboardButton("ارسال الطلب الي الواتساب", url=wa_link)],
                    [InlineKeyboardButton("رجوع", callback_data="back_to_main_menu")]]
        query.edit_message_text("هذا المنتج جاهز للشراء الفوري. اضغط إرسال الطلب.", 
                                reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # 6. معالج أزرار السبلميشن
    if data == "sublimation":
        wa_link = create_whatsapp_link("استفسار عن مستلزمات السبلميشن")
        keyboard = [[InlineKeyboardButton("للاستفسار عن السبلميشن اضغط هنا", url=wa_link)],
                    [InlineKeyboardButton("رجوع", callback_data="back_to_main_menu")]]
        query.edit_message_text("للاستفسار عن أسعار وكميات مستلزمات السبلميشن، يرجى التواصل عبر الواتساب.", 
                                reply_markup=InlineKeyboardMarkup(keyboard))
        return


def handle_messages(update, context):
    # وظيفة لمعالجة الرسائل النصية التي لا تبدأ بأمر /
    if context.user_data.get('state') is None:
        update.effective_message.reply_text("من فضلك اختر طلبك من القائمة الرئيسية أولاً.", 
                                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_to_main_menu")]]))


# --------------------
# 4. دوال ConversationHandler الخاصة بالأقلام (المعدلة)
# --------------------

def select_pen_type_menu(update, context):
    """
    (الدالة الجديدة) تعرض قائمة بأنواع الأقلام (مضئ ومعدن) وزر رجوع.
    """
    query = update.callback_query
    query.answer()
    
    # مسح البيانات المخزنة من محادثة سابقة عند الرجوع
    context.user_data.pop('pen_data', None)
            
    # الأزرار المطلوبة: قلم مضئ، قلم معدن، رجوع
    keyboard = [
        [InlineKeyboardButton("قلم تاتش مضئ", callback_data='aqlam_luminous')], 
        [InlineKeyboardButton("قلم تاتش معدن", callback_data='aqlam_metal')],   
        [InlineKeyboardButton("رجوع", callback_data='back_to_main_menu')] # زر الرجوع للقائمة الرئيسية
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = "الرجاء اختيار نوع القلم المطلوب حفره:"
    
    if query and query.message:
        try:
            query.edit_message_text(
                text=message_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        except telegram.error.BadRequest:
            update.effective_chat.send_message(
                text=message_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
    else:
        update.effective_message.reply_text(message_text, reply_markup=reply_markup, parse_mode="Markdown")
            
    return SELECT_PEN_TYPE


def prompt_for_pen_name(update, context):
    """
    (الدالة الجديدة) تخزن نوع القلم وتطلب من العميل إدخال الاسم.
    """
    query = update.callback_query
    data = query.data # aqlam_luminous or aqlam_metal
    query.answer()
    
    selected_pen_data = next((item for item in aqlam_submenu if item["callback"] == data), None)
    if not selected_pen_data:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['pen_data'] = selected_pen_data
    
    # رسالة طلب الإسم وزر الرجوع المطلوبين
    message_text = f"**اختيارك: {selected_pen_data['label']}**\n\nاكتب الاسم المطلوب حفره علي القلم او اضغط الرجوع للعودة الي القائمة السابقة"
    # زر الرجوع يعود لقائمة اختيار أنواع القلم (callback 'aqlam')
    back_keyboard = [[InlineKeyboardButton("رجوع", callback_data='aqlam')]] 
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # محاولة تعديل الرسالة
    try:
        # محاولة تعديل الرسالة النصية
        query.edit_message_text(
            text=message_text,
            reply_markup=back_reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest:
        # إذا فشل التعديل، نرسل رسالة جديدة
        update.effective_chat.send_message(
            text=message_text,
            reply_markup=back_reply_markup,
            parse_mode="Markdown"
        )
            
    return GET_PEN_NAME


def receive_pen_name_and_prepare_whatsapp(update, context):
    """
    (الدالة المعدلة) تستقبل الاسم وتعد رسالة الواتساب وزر الإرسال.
    """
    engraving_name = update.message.text
    product_data = context.user_data.pop('pen_data', None) # استرجاع وحذف البيانات
    
    if not product_data:
        update.effective_chat.send_message("عفواً، حدث خطأ. يرجى البدء من القائمة الرئيسية.", 
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_to_main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (اقلام)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الاسم المطلوب حفره: *{engraving_name}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}"
    )
    # إنشاء رابط الواتساب
    wa_link = create_whatsapp_link(message_body)
    
    # ⚠️ الأزرار المطلوبة: "ارسال الطلب الي الواتساب" و "زر رجوع"
    keyboard = [
        [InlineKeyboardButton("ارسال الطلب الي الواتساب", url=wa_link)],
        [InlineKeyboardButton("رجوع", callback_data="back_to_main_menu")] # العودة للقائمة الرئيسية
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        f"شكراً لك! تفاصيل الطلب:\n\n✏️ المنتج: {product_data['label']}\n✍️ الاسم المطلوب: {engraving_name}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END


# --------------------
# 5. دوال ConversationHandler Placeholder الأخرى (للتشغيل)
# --------------------

# دوال المحافظ (Placeholder)
def prompt_for_name(update, context):
    query = update.callback_query
    query.answer()
    context.user_data['wallet_type'] = query.data
    keyboard = [[InlineKeyboardButton("رجوع", callback_data='back_to_wallets_color')]]
    query.edit_message_text("اكتب الاسم المطلوب حفره على المحفظة:", reply_markup=InlineKeyboardMarkup(keyboard))
    return GET_WALLET_NAME

def receive_wallet_name_and_prepare_whatsapp(update, context):
    wallet_type = context.user_data.pop('wallet_type', 'محفظة غير محددة')
    engraving_name = update.message.text
    message_body = f"طلب حفر: {engraving_name} على {wallet_type}"
    wa_link = create_whatsapp_link(message_body)
    keyboard = [[InlineKeyboardButton("ارسال الطلب الي الواتساب", url=wa_link)],
                [InlineKeyboardButton("رجوع", callback_data="back_to_main_menu")]]
    update.message.reply_text("تم استلام الطلب. اضغط إرسال الطلب.", reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

def back_to_wallets_color(update, context):
    return start(update, context) # Simplification: back to main menu

# دالة وهمية للخطوات التالية في المحادثات الأخرى
def handle_next_step(update, context):
    update.effective_message.reply_text("هذا المنتج غير متاح حاليًا في المحادثة. يرجى البدء من جديد.", 
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_to_main_menu")]]))
    return ConversationHandler.END


# --------------------
# 6. تعريف معالجات المحادثة (Conversation Handlers)
# --------------------

# 1. معالج الأقلام (المعدل)
engraved_pen_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(select_pen_type_menu, pattern='^aqlam$')],
    
    states={
        SELECT_PEN_TYPE: [
            CallbackQueryHandler(prompt_for_pen_name, pattern='^(aqlam_luminous|aqlam_metal)$')
        ],
        
        GET_PEN_NAME: [
            MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp)
        ]
    },
    
    fallbacks=[
        CallbackQueryHandler(select_pen_type_menu, pattern='^aqlam$'),
        CommandHandler('start', start),
        CallbackQueryHandler(cancel_and_end) 
    ]
)

# 2. معالج المحافظ
engraved_wallet_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(prompt_for_name, pattern='^(wallet_bege|wallet_brown|wallet_black)$')],
    states={
        GET_WALLET_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_wallet_name_and_prepare_whatsapp)]
    },
    fallbacks=[
        CommandHandler('start', start),
        CallbackQueryHandler(back_to_wallets_color, pattern='^back_to_wallets_color$'),
        CallbackQueryHandler(cancel_and_end)
    ]
)

# 3. معالج بوكس كتب الكتاب (Placeholder)
box_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(handle_next_step, pattern='^(box_m1|box_m2)$')],
    states={
        GET_BOX_COLOR: [CallbackQueryHandler(handle_next_step, pattern='^color_')],
    },
    fallbacks=[
        CommandHandler('start', start),
        CallbackQueryHandler(cancel_and_end)
    ]
)
# 4. معالج صواني اكليريك (Placeholder)
tray_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(handle_next_step, pattern='^sawany_akerik_')],
    states={
        GET_TRAY_NAMES: [MessageHandler(Filters.text & ~Filters.command, handle_next_step)],
    },
    fallbacks=[
        CommandHandler('start', start),
        CallbackQueryHandler(cancel_and_end)
    ]
)
# 5. معالج طارات اكليريك (Placeholder)
akerik_taarat_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(handle_next_step, pattern='^taarat_akerik_')],
    states={
        GET_AKRILIK_TAARAT_NAMES: [MessageHandler(Filters.text & ~Filters.command, handle_next_step)],
    },
    fallbacks=[
        CommandHandler('start', start),
        CallbackQueryHandler(cancel_and_end)
    ]
)
# 6. معالج بصامات (Placeholder)
bsamat_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(handle_next_step, pattern='^bsamat_m')],
    states={
        GET_BSAMAT_NAMES: [MessageHandler(Filters.text & ~Filters.command, handle_next_step)],
    },
    fallbacks=[
        CommandHandler('start', start),
        CallbackQueryHandler(cancel_and_end)
    ]
)
# 7. معالج مناديل كتب الكتاب (Placeholder)
tissue_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(handle_next_step, pattern='^tissue_m')],
    states={
        GET_TISSUE_NAMES: [MessageHandler(Filters.text & ~Filters.command, handle_next_step)],
    },
    fallbacks=[
        CommandHandler('start', start),
        CallbackQueryHandler(cancel_and_end)
    ]
)

# Placeholder for Khashab Tray, Khashab Taarat
khashab_tray_handler = ConversationHandler(entry_points=[CallbackQueryHandler(handle_next_step, pattern='^sawany_khashab_')], states={1: [MessageHandler(Filters.text, handle_next_step)]}, fallbacks=[CommandHandler('start', start)])
khashab_taarat_handler = ConversationHandler(entry_points=[CallbackQueryHandler(handle_next_step, pattern='^taarat_khashab_')], states={1: [MessageHandler(Filters.text, handle_next_step)]}, fallbacks=[CommandHandler('start', start)])


# --------------------
# 7. دالة MAIN
# --------------------

def main():
    # ⚠️ استدعاء التوكن من متغير البيئة 'Token'
    token = os.environ.get('TOKEN') 
    
    if not token:
        print("خطأ: لم يتم العثور على متغير البيئة 'Token'. يرجى التأكد من إضافته بشكل صحيح.")
        return

    updater = Updater(token, use_context=True) 

    dp = updater.dispatcher

    # 4. إضافة جميع ConversationHandler أولاً لضمان الأولوية
    dp.add_handler(engraved_pen_handler)
    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(box_handler)
    dp.add_handler(tray_handler)
    dp.add_handler(khashab_tray_handler)
    dp.add_handler(akerik_taarat_handler) 
    dp.add_handler(khashab_taarat_handler) 
    dp.add_handler(bsamat_handler) 
    dp.add_handler(tissue_handler) 
    
    
    # 5. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 6. معالج أزرار القائمة والتنقل (يجب أن يأتي بعد معالجات المحادثة)
    dp.add_handler(CallbackQueryHandler(button)) 

    # 7. معالج للرسائل النصية غير المعالجة
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    # ابدأ البوت
    print("Bot is starting...")
    updater.start_polling()
    updater.idle()

# --------------------
# 8. تشغيل الدالة
# --------------------
if __name__ == '__main__':
    main()