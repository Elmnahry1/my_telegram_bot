import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات الواتساب: استبدل بالرقم الخاص بك
WHATSAPP_NUMBER = "201288846355" 

# --------------------
# 1. تعريف حالات المحادثة
# --------------------

GET_WALLET_NAME = 1 # حالة المحافظ
GET_PEN_NAME = 2    # حالة الأقلام 
GET_BOX_COLOR = 3   # حالة اختيار لون البوكس
GET_BOX_NAMES = 4   # حالة كتابة أسماء العرسان للبوكس
GET_TRAY_NAMES = 5  # 🆕 حالة كتابة الأسماء للصينية
GET_TRAY_DATE = 6   # 🆕 حالة كتابة التاريخ للصينية
GET_WOOD_TRAY_NAMES = 7  # حالة كتابة أسماء العريس والعروسة لصواني الخشب
GET_WOOD_TRAY_DATE = 8   # حالة كتابة التاريخ لصواني الخشب

# --------------------
# 2. بيانات القوائم والمنتجات
# --------------------

# (القوائم والمنتجات كما هي في الكود الذي أرسلته سابقًا، مع استمرارية الكود)

# ... (كل البيانات واللوائح كما هي)

# --------------------
# 3. الدوال الرئيسية والمساعدة
# --------------------

# (الدوال start، show_submenu، show_product_page، وغيرها كما هي)

# ------------------------------------
# دوال المحافظ والأقلام والبوكس
# ------------------------------------

# (كما هي، مع عدم تعديلها)

# ------------------------------------
# دوال صواني شبكة اكليريك (Acrylic Trays Handlers)
# ------------------------------------

# 1. دالة بدء طلب من منتجات الخشب مع طلب الاسم
def start_wood_tray_purchase(update, context):
    """
    الخطوة 1: عند الضغط على زر شراء للمنتج من الخشب، نطلب الاسم أولاً.
    """
    query = update.callback_query
    query.answer()
    data = query.data  # مثلا: buy_khashab_m1
    product_callback = data.replace("buy_", "")

    # البحث عن المنتج
    # نبحث داخل قائمة خشب الصواني
    items_list = doro3_submenu[2]['items']  # قائمة المنتجات الخشب
    selected_tray = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_tray:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    # حفظ المنتج في الـ user_data
    context.user_data['wood_tray_product'] = selected_tray
    # الانتقال إلى حالة كتابة الأسماء
    context.user_data['state'] = GET_WOOD_TRAY_NAMES

    # زر رجوع
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_khashab")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    try:
        query.message.delete()
    except:
        pass

    # إرسال الصورة مع رسالة
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=selected_tray['image'],
        caption=f"✅ **{selected_tray['label']}**\n\nمن فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل أو اضغط زر رجوع للعودة إلى القائمة السابقة:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_WOOD_TRAY_NAMES

# 2. دالة حفظ الأسماء وطلب التاريخ
def save_wood_tray_names_and_ask_date(update, context):
    names = update.message.text
    context.user_data['wood_tray_names'] = names

    # زر رجوع
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_wood_tray_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    # الانتقال إلى حالة كتابة التاريخ
    return GET_WOOD_TRAY_DATE

# 3. دالة استقبال التاريخ وإظهار زر الإرسال
def receive_wood_tray_date_and_show_button(update, context):
    date_text = update.message.text
    product_data = context.user_data.get('wood_tray_product')
    names_text = context.user_data.get('wood_tray_names')

    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END

    user_info = update.message.from_user

    message_body = (
        f"🔔 *طلب شراء جديد (صواني شبكة خشب)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الأسماء: *{names_text}*\n"
        f"التاريخ: *{date_text}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )

    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"

    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        f"شكراً لك! تفاصيل الطلب:\n\n💍 المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )

    # مسح البيانات
    context.user_data.clear()
    return ConversationHandler.END

# 4. دالة الرجوع من الأسماء
def back_to_wood_tray_names(update, context):
    """
    زر رجوع من مرحلة الأسماء يعيدنا لعرض الصورة مرة أخرى
    """
    query = update.callback_query
    query.answer()

    selected_tray = context.user_data.get('wood_tray_product')
    if not selected_tray:
        start(update, context)
        return ConversationHandler.END

    # إعادة عرض الصورة مع رسالة
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_khashab")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    try:
        query.message.delete()
    except:
        pass

    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=selected_tray['image'],
        caption=f"✅ **{selected_tray['label']}**\n\nمن فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل أو اضغط زر رجوع للعودة إلى القائمة السابقة:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    # العودة للحالة
    return GET_WOOD_TRAY_NAMES

# 5. تعديل الـ ConversationHandler ليشمل الحالة الجديدة
tray_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_wood_tray_purchase, pattern='^buy_akerik_.*')],
    states={
        GET_WOOD_TRAY_NAMES: [MessageHandler(Filters.text & ~Filters.command, save_wood_tray_names_and_ask_date)],
        GET_WOOD_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_wood_tray_date_and_show_button)],
        # زر رجوع من الأسماء
        # يمكن إضافته هنا إذا أردت
    },
    fallbacks=[
        CommandHandler('start', start),
        CallbackQueryHandler(back_to_wood_tray_names, pattern='^back_to_tray_names$'), # رجوع من التاريخ للأسماء
        CallbackQueryHandler(button)
    ]
)

# ------------------------------------
# 4. إعداد البوت 
# ------------------------------------
def main():
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN).")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # 1. المحافظ
    engraved_wallet_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prompt_for_name, pattern='^(' + '|'.join([item['callback'] for item in engraved_wallet_submenu]) + ')$')],
        states={GET_WALLET_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_name_and_prepare_whatsapp)]},
        fallbacks=[CommandHandler('start', start), CallbackQueryHandler(back_to_wallets_color, pattern='^back_to_wallets_color$'), CallbackQueryHandler(button)]
    )

    # 2. اقلام
    engraved_pen_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prompt_for_pen_name, pattern='^(' + '|'.join([item['callback'] for item in aqlam_submenu]) + ')$')],
        states={GET_PEN_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp)]},
        fallbacks=[CommandHandler('start', start), CallbackQueryHandler(back_to_pen_types, pattern='^back_to_pen_types$'), CallbackQueryHandler(button)]
    )

    # 3. بوكس كتب الكتاب
    box_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_box_purchase, pattern='^buy_box_.*')],
        states={
            GET_BOX_COLOR: [CallbackQueryHandler(save_box_color_ask_names, pattern='^color_.*|katb_kitab_box$')],
            GET_BOX_NAMES: [MessageHandler(Filters.text & ~Filters.command, receive_box_names_and_finish)]
        },
        fallbacks=[CommandHandler('start', start), CallbackQueryHandler(back_to_box_color, pattern='^back_to_box_color$'), CallbackQueryHandler(button)]
    )

    # 🆕 4. صواني شبكة اكليريك
    dp.add_handler(tray_handler) # هاندلر الصواني الجديد

    # باقي الـ Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()