import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 
import logging

# تفعيل تسجيل الدخول (لأغراض التصحيح)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ⚠️ إعدادات الواتساب: استبدل بالرقم الخاص بك
WHATSAPP_NUMBER = "201288846355" # مثال
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE" # استبدل برمز البوت الخاص بك

# --------------------
# 1. تعريف حالات المحادثة
# --------------------

GET_WALLET_NAME = 1          # حالة المحافظ
GET_PEN_NAME = 2             # حالة الأقلام 
GET_BOX_COLOR = 3            # حالة اختيار لون البوكس
GET_BOX_NAMES = 4            # حالة كتابة أسماء العرسان للبوكس
GET_TRAY_NAMES = 5           # حالة كتابة الأسماء للصينية الاكليريك
GET_TRAY_DATE = 6            # حالة كتابة التاريخ للصينية الاكليريك
GET_KHASHAB_TRAY_NAMES = 7   # حالة كتابة الأسماء لصينية الخشب
GET_KHASHAB_TRAY_DATE = 8    # حالة كتابة التاريخ لصينية الخشب
GET_AKRILIK_TAARAT_NAMES = 9 # حالة أسماء طارات اكليريك
GET_AKRILIK_TAARAT_DATE = 10 # حالة تاريخ طارات اكليريك
GET_KHASHAB_TAARAT_NAMES = 11 # حالة أسماء طارات خشب
GET_KHASHAB_TAARAT_DATE = 12 # حالة تاريخ طارات خشب
GET_BSAMAT_NAMES = 13        # حالة أسماء البصمات
GET_BSAMAT_DATE = 14         # حالة تاريخ البصمات
GET_TISSUE_DATE = 15         # حالة تاريخ علبة المناديل

# --------------------
# 2. تعريف قوائم المنتجات
# --------------------

# القائمة الرئيسية
main_menu = [
    {"label": "محافظ حفر اسم", "callback": "engraved_wallet"},
    {"label": "أقلام حفر اسم", "callback": "aqlam"}, # تم تعديلها لتصبح قائمة فرعية
    {"label": "بوكس كتب كتاب", "callback": "katb_kitab_box"},
    {"label": "صواني", "callback": "sawany"}, 
    {"label": "طارات", "callback": "taarat"}, 
    {"label": "طقم هرم", "callback": "haram"},
    {"label": "دروع و شهادات", "callback": "doro3"},
    {"label": "مجات", "callback": "mugat"},
    {"label": "بصمات", "callback": "bsamat"},
    {"label": "علب مناديل كتب كتاب", "callback": "wedding_tissues"},
    {"label": "أباجورات", "callback": "abajorat"}
]

# قائمة المحافظ
engraved_wallet_submenu = [
    {"label": "محفظة بيج (هافان)", "callback": "wallet_bege", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بيج (هافان)."},
    {"label": "محفظة بني", "callback": "wallet_brown", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بني."},
    {"label": "محفظة سوداء", "callback": "wallet_black", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون أسود."}
]

# 🛑 START OF NEW PEN LOGIC: قائمة الأقلام الجديدة
aqlam_submenu = [
    {
        "label": "قلم تاتش مضئ", 
        "callback": "aqlam_luminous", 
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/489809156_1164483322357054_6286791651911010777_n.jpg?stp=dst-jpg_s590x590_tt6&_nc_cat=107&ccb=1-7&_nc_sid=833d8c&_nc_ohc=ELb9pciSoD0Q7kNvwG_rdLE&_nc_oc=AdkDWLOZBcjZp9AbNO2Fs-zK-suPtGc1D-KC3JP7NlzhwgJB3WZeGQQfCQIsfxZgvrg&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=U5_JMOw_cSsgrQQLv77j7g&oh=00_Afg-wJrTmoGZo5m1kVVh2IU0227UQ7pUtKSjRx_YEFoGWg&oe=6923B3BA", 
        "description": "قلم تاتش مضئ بتقنية متطورة ومناسب للحفر بالليزر. عند اختياره، يتم توجيهك لصفحة بها صورته ووصفه وزر شراء."
    },
    {
        "label": "قلم تاتش معدن", 
        "callback": "aqlam_metal", 
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/475773348_986832329974720_6197915277469223378_n.jpg?stp=dst-jpg_s720x720_tt6&_nc_cat=107&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=KrebndL4u2oQ7kNvwH3smA2&_nc_oc=AdkT6T_o5SpJKdr9FQ5OhX2vuI5Cp3WjQl0pV9vRotIn9csOIX1DX-I9dC3FpvlBLJM&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=JFYgN-MxG5oy8y3q9Os6Ew&oh=00_AfhJxajOEm9owiAqd00_zEZ4Hy4qzX7DYATV6p4tWdRxeA&oe=6923BE1B", 
        "description": "قلم تاتش معدن عالي الجودة ومناسب للحفر بالليزر. عند اختياره، يتم توجيهك لصفحة بها صورته ووصفه وزر شراء."
    }
]
# END OF NEW PEN LOGIC

# صواني
sawany_submenu = [
    {"label": "صينية اكليريك", "callback": "akerik_tray"},
    {"label": "صينية خشب", "callback": "khashab_tray"}
]

# طارات
taarat_submenu = [
    {"label": "طارة اكليريك", "callback": "akerik_taarat"},
    {"label": "طارة خشب", "callback": "khashab_taarat"}
]
# ... (تعريف باقي القوائم مثل haram, doro3, mugat, bsamat, wedding_tissues, abajorat)

# قائمة شاملة لجميع القوائم الفرعية
all_submenus = {
    "sawany": sawany_submenu,
    "taarat": taarat_submenu,
    "engraved_wallet": engraved_wallet_submenu,
    "aqlam": aqlam_submenu, # تم تضمينها هنا أيضاً لـ show_submenu
    # ... (باقي القوائم الفرعية)
}


# --------------------
# 3. الدوال المساعدة والبدء
# --------------------

def create_whatsapp_link(message):
    """إنشاء رابط واتساب جاهز للإرسال."""
    encoded_message = quote_plus(message)
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"

def prepare_whatsapp_message(chat_data):
    """تجهيز رسالة الطلب بناءً على البيانات المخزنة في chat_data."""
    # (هنا يتم بناء الرسالة حسب نوع المنتج والبيانات)
    
    # مثال لبناء رسالة القلم
    if 'pen_type' in chat_data and 'pen_name' in chat_data:
        pen_name = chat_data.get('pen_name')
        pen_label = chat_data.get('pen_label', 'قلم') # Retrieve the full label
        
        # رسالة طلب القلم
        message = f"طلب حفر قلم:\n" \
                  f"نوع القلم: {pen_label}\n" \
                  f"الاسم المطلوب حفره: {pen_name}\n" \
                  f"رقم العميل: (سيتم إرساله من الواتساب)\n" \
                  f"---"
        return message
    
    # ... (باقي المنتجات مثل المحفظة، البوكس، الصواني)

    # رسالة افتراضية
    return "مرحباً، أود الاستفسار عن منتج لديكم. شكراً!"


def start(update, context):
    """يبدأ المحادثة ويرسل القائمة الرئيسية."""
    keyboard = []
    
    # بناء لوحة المفاتيح بـ 3 أزرار في كل صف
    for i in range(0, len(main_menu), 3):
        row = [InlineKeyboardButton(item["label"], callback_data=item["callback"]) for item in main_menu[i:i+3]]
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # إرسال الرسالة الترحيبية
    update.message.reply_text('أهلاً بك في بوت طلبات الحفر بالليزر! اختر المنتج الذي ترغب في تخصيصه:', reply_markup=reply_markup)
    
def show_submenu(update, context, submenu, title, back_callback):
    """دالة لعرض القوائم الفرعية (مثل قائمة أنواع الأقلام أو الصواني)."""
    query = update.callback_query
    
    if query:
        query.answer()
        query.edit_message_text(
            text=f"قائمة منتجات: **{title}**.\n\nمن فضلك اختر النوع المطلوب:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in submenu
                ] + [
                    [InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)] # زر الرجوع المطلوب
                ]
            )
        )
        
def show_product_page(update, product_key, product_list, is_direct_list=False):
    """دالة لعرض قائمة المنتجات التفصيلية (صور ووصف وأزرار)."""
    # ... (Logic for showing product list, not directly modified but kept for context)
    pass
    

# 🛑 START OF NEW PEN DETAILS HANDLER (show_pen_details_and_buy)
def show_pen_details_and_buy(update, context, pen_callback_data):
    """
    تعرض تفاصيل القلم المحدد (صورة، وصف) وزر الشراء وزر الرجوع إلى قائمة أنواع الأقلام.
    """
    query = update.callback_query
    if query:
        query.answer()

    # 1. البحث عن بيانات القلم
    selected_pen_data = next((item for item in aqlam_submenu if item["callback"] == pen_callback_data), None)

    if not selected_pen_data:
        update.effective_chat.send_message("عفواً، لم يتم العثور على المنتج.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return 

    # 2. حذف الرسالة السابقة (قائمة أنواع الأقلام)
    if query and query.message:
        try:
            query.message.delete()
        except Exception:
            pass
            
    # 3. بناء لوحة المفاتيح: [شراء], [رجوع لقائمة أنواع الأقلام]
    
    # زر الشراء (مدخل الـ ConversationHandler)
    buy_button = [InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{pen_callback_data}")]
    
    # زر الرجوع (يعود لقائمة أنواع الأقلام)
    back_button = [InlineKeyboardButton("🔙 رجوع", callback_data="aqlam")] 
    
    combined_keyboard = [buy_button, back_button]
    reply_markup = InlineKeyboardMarkup(combined_keyboard)
    
    # 4. إرسال الصورة والوصف
    context.user_data['pen_label'] = selected_pen_data['label']
    caption_text = f"**{selected_pen_data['label']}**\n\n{selected_pen_data['description']}\n\nاختر *شراء* لبدء تخصيص الحفر أو *رجوع* لتغيير نوع القلم."
    
    try:
        update.effective_message.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_pen_data['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest:
        # Fallback if image fails (send as message)
        update.effective_message.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    return

# 🛑 END OF NEW PEN DETAILS HANDLER

# ... (باقي دوال الرجوع والتنقل مثل back_to_wallets_color, cancel_and_end)


# --------------------
# 4. دوال معالجة المحادثات (Conversation Handlers)
# --------------------

# دوال الأقلام (تم الحفاظ عليها)
def prompt_for_pen_name(update, context):
    """
    تبدأ عملية طلب الحفر للقلم. 
    هذه هي الدالة التي يتم استدعاؤها بعد الضغط على زر "شراء" (buy_aqlam_luminous أو buy_aqlam_metal).
    """
    query = update.callback_query
    
    if query:
        query.answer()
        # تخزين نوع القلم للرجوع إليه لاحقاً
        # data format is 'buy_aqlam_type'
        pen_callback_data = query.data.split('buy_')[1] 
        
        # يمكنك تخزين نوع القلم إذا لزم الأمر
        context.user_data['pen_type'] = pen_callback_data 
        
        # حذف الرسالة السابقة (صورة وتفاصيل القلم)
        try:
            query.message.delete()
        except Exception:
            pass
            
    
    # رسالة طلب الاسم مع زر الرجوع
    keyboard = [[InlineKeyboardButton("🔙 رجوع للقائمة السابقة", callback_data="aqlam")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.message.reply_text(
        "📝 **يرجى كتابة الاسم/العبارة المطلوب حفرها على القلم الآن**.\n\n"
        "أو اضغط زر *رجوع* للعودة إلى قائمة أنواع الأقلام.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_PEN_NAME

def receive_pen_name_and_prepare_whatsapp(update, context):
    """تستقبل الاسم المحفور وتجهز زر إرسال الطلب عبر الواتساب."""
    pen_name = update.message.text
    context.user_data['pen_name'] = pen_name
    
    # تجهيز رسالة الطلب
    whatsapp_msg = prepare_whatsapp_message(context.user_data)
    whatsapp_link = create_whatsapp_link(whatsapp_msg)
    
    keyboard = [
        [InlineKeyboardButton("✅ إرسال الطلب على الواتساب", url=whatsapp_link)],
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        f"شكراً لك! سيتم حفر الاسم: **{pen_name}**.\n\n"
        f"لإتمام الطلب وتحديد طريقة الشحن، يرجى الضغط على زر *إرسال الطلب على الواتساب*.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    # إنهاء المحادثة
    return ConversationHandler.END

# ... (باقي دوال المحادثات الأخرى: wallet, box, tray, bsamat, tissue)

def back_to_pen_types(update, context):
    """يعود إلى قائمة أنواع الأقلام عند الضغط على رجوع من شاشة طلب الاسم."""
    # استدعاء دالة زر "aqlam" مباشرة
    return button(update, context) # تقوم بتوجيهها إلى show_submenu لـ aqlam

def back_to_main_menu_from_conv(update, context):
    """دالة العودة من أي محادثة إلى القائمة الرئيسية."""
    query = update.callback_query
    if query:
        query.answer()
        query.edit_message_text(
            "تم إلغاء الطلب. يمكنك اختيار منتج آخر:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
            )
        )
    return ConversationHandler.END


# --------------------
# 5. دالة معالج الأزرار الرئيسية (button)
# --------------------

def button(update, context):
    """معالج الأزرار الرئيسي لجميع خيارات القوائم والتنقل."""
    query = update.callback_query
    data = query.data
    
    query.answer()
    
    # 1. معالجة زر القائمة الرئيسية
    if data == 'main_menu':
        # (استدعاء دالة البداية start لفتح القائمة الرئيسية)
        # لحذف الرسالة القديمة وإرسال القائمة الجديدة
        query.edit_message_text(text="أهلاً بك! اختر المنتج الذي ترغب في تخصيصه:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in main_menu
        ]))
        return

    # 2. معالجة فتح القوائم المتداخلة (sawany, taarat, haram, doro3, mugat)
    if data in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        # Find the title of the main menu item
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus.get(data, []), clean_title, back_callback="main_menu")
        return

    # 🛑 NEW: معالجة زر "اقلام" لعرض القائمة الفرعية (زرين فرعيين + رجوع)
    if data == "aqlam":
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        # show_submenu displays the pen types + 'Back to main_menu' button
        show_submenu(update, context, aqlam_submenu, clean_title, back_callback="main_menu")
        return


    # 3. معالجة فتح قوائم المستوى الأول المباشرة (التي تعرض تفاصيل المنتجات كلها مباشرة)
    if data in ["engraved_wallet", "bsamat", "wedding_tissues", "abajorat", "katb_kitab_box"]: 
        submenu_list = all_submenus.get(data)
        if submenu_list:
            if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "engraved_wallet"]: 
                show_product_page(update, data, submenu_list, is_direct_list=True)
                return
        # ... (باقي المعالجة إذا لم يتم العثور على القائمة)
        return

    # 🛑 NEW: معالجة اختيار نوع القلم (لعرض تفاصيل القلم وزر الشراء)
    if data in ["aqlam_luminous", "aqlam_metal"]:
        show_pen_details_and_buy(update, context, data)
        return
        
    # 5. معالجة عرض صفحات المنتجات مباشرة (قوائم المستوى الثاني: wallet_bege, wallet_brown, etc.)
    # ... (باقي معالجات الأزرار والمنتجات)


# --------------------
# 6. إعداد وتشغيل البوت
# --------------------

def main():
    """الدالة الرئيسية لتشغيل البوت."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # 1. تعريف ConversationHandler للأقلام
    # يستخدم regex لمطابقة "buy_" يتبعها نوع القلم
    engraved_pen_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(prompt_for_pen_name, pattern='^buy_aqlam_') 
        ],
        states={
            GET_PEN_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp)],
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_pen_types, pattern='^aqlam$'), # يرجع إلى قائمة أنواع الأقلام
            CallbackQueryHandler(back_to_main_menu_from_conv, pattern='^main_menu$') # يرجع للقائمة الرئيسية
        ]
    )

    # ... (باقي تعريفات ConversationHandler الأخرى مثل box_handler, wallet_handler, etc.)
    # (افتراضاً أنها معرّفة هنا)

    # 2. تعريف بعض الـ Conversation Handlers الأساسية الأخرى
    # (لأغراض العرض، سنضع مثال للمحفظة أيضاً)
    engraved_wallet_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(prompt_for_pen_name, pattern='^buy_wallet_') 
        ],
        states={
            GET_WALLET_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp)],
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_pen_types, pattern='^engraved_wallet$'), 
            CallbackQueryHandler(back_to_main_menu_from_conv, pattern='^main_menu$') 
        ]
    )
    # ... (باقي الـ Conversation Handlers)

    # 3. إضافة جميع ConversationHandler أولاً لضمان الأولوية
    # dp.add_handler(box_handler)
    # dp.add_handler(tray_handler)
    # ...
    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler)
    
    
    # 4. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 5. معالج أزرار القائمة والتنقل (يجب أن يأتي بعد معالجات المحادثة)
    dp.add_handler(CallbackQueryHandler(button)) 

    # 6. معالج للرسائل النصية غير المعالجة
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_messages))
    
    # ابدأ البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()