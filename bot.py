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
GET_PEN_NAME = 2    # حالة الأقلام 
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

# حالات مناديل كتب الكتاب (تم إضافتها هنا)
GET_TISSUE_NAMES = 15  # حالة كتابة أسماء العرسان للمناديل
GET_TISSUE_DATE = 16   # حالة كتابة التاريخ للمناديل


# --------------------
# 2. بيانات القوائم والمنتجات
# --------------------

# --- قوائم فرعية مباشرة ---
bsamat_submenu = [
    {"label": "بصامة موديل 1", "callback": "bsamat_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 1."},
    {"label": "بصامة موديل 2", "callback": "bsamat_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 2."}
]
wedding_tissues_submenu = [
    {"label": "منديل موديل 1", "callback": "tissue_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 1."},
    {"label": "منديل موديل 2", "callback": "tissue_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 2."}
]
katb_kitab_box_submenu = [
    {"label": "بوكس كتب كتاب موديل 1", "callback": "box_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف بوكس كتب الكتاب موديل 1، يحتوي على تصميم مميز."},
    {"label": "بوكس كتب كتاب موديل 2", "callback": "box_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف بوكس كتب الكتاب موديل 2، خامة عالية الجودة."}
]
abajorat_submenu = [
    {"label": "أباجورة موديل 1", "callback": "abajora_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف الأباجورة موديل 1."},
    {"label": "أباجورة موديل 2", "callback": "abajora_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف الأباجورة موديل 2."}
]
engraved_wallet_submenu = [
    {"label": "محفظة بيج (هافان)", "callback": "wallet_bege", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بيج (هافان)."},
    {"label": "محفظة بني", "callback": "wallet_brown", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بني."},
    {"label": "محفظة سوداء", "callback": "wallet_black", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون أسود."}
]
aqlam_submenu = [
    {
        "label": "قلم تاتش معدن", 
        "callback": "aqlam_metal", 
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/475773348_986832329974720_6197915277469223378_n.jpg?stp=dst-jpg_s720x720_tt6&_nc_cat=107&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=KrebndL4u2oQ7kNvwH3smA2&_nc_oc=AdkT6T_o5SpJKdr9FQ5OhX2vuI5Cp3WjQl0pV9vRotIn9csOIX1DX-I9dC3FpvlBLJM&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=JFYgN-MxG5oy8y3q9Os6Ew&oh=00_AfhJxajOEm9owiAqd00_zEZ4Hy4qzX7DYATV6p4tWdRxeA&oe=6923BE1B", 
        "description": "قلم تاتش معدن عالي الجودة ومناسب للحفر بالليزر."
    },
    {
        "label": "قلم تاتش مضئ", 
        "callback": "aqlam_luminous", 
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/489809156_1164483322357054_6286791651911010777_n.jpg?stp=dst-jpg_s590x590_tt6&_nc_cat=107&ccb=1-7&_nc_sid=833d8c&_nc_ohc=ELb9pciSoD0Q7kNvwG_rdLE&_nc_oc=AdkDWLOZBcjZp9AbNO2Fs-zK-suPtGc1D-KC3JP7NlzhwgJB3WZeGQQfCQIsfxZgvrg&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=U5_JMOw_cSsgrQQLv77j7g&oh=00_Afg-wJrTmoGZo5m1kVVh2IU0227UQ7pUtKSjRx_YEFoGWg&oe=6923B3BA", 
        "description": "قلم تاتش مضئ بتقنية متطورة ومناسب للحفر بالليزر."
    }
]

# --- القوائم المتداخلة ---
# ... (sawany_submenu, taarat_submenu, haram_submenu, doro3_submenu, mugat_submenu - No changes here) ...


# --------------------
# 3. الدوال الرئيسية والمساعدة
# --------------------
# ... (cancel_and_end, start, show_submenu, show_product_page - No changes here) ...

# 💡 دالة جديدة: لعرض صفحة منتج القلم المفرد (الخطوة 2 في طلبك)
def display_single_pen_product(update, context, product_callback):
    query = update.callback_query
    query.answer()
    
    # البحث عن بيانات القلم في القائمة الفرعية
    selected_pen_data = next((item for item in aqlam_submenu if item["callback"] == product_callback), None)
    
    if not selected_pen_data:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return 

    # حذف رسالة القائمة السابقة
    try:
        query.message.delete()
    except Exception:
        pass

    # إنشاء لوحة المفاتيح: زر الشراء وزر الرجوع إلى قائمة أنواع الأقلام ('aqlam')
    item_keyboard = [
        [InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{selected_pen_data['callback']}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="aqlam")] 
    ]
    item_reply_markup = InlineKeyboardMarkup(item_keyboard)
    
    # إرسال الصورة والوصف
    caption_text = f"**{selected_pen_data['label']}**\n\n{selected_pen_data['description']}"

    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_pen_data['image'],
            caption=caption_text,
            reply_markup=item_reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest:
         context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=item_reply_markup,
            parse_mode="Markdown"
        )
        

# --- [دوال المحادثات الخاصة بالأقلام] ---

# 🛑 تم تعديل هذه الدالة (كانت prompt_for_pen_name) لتبدأ المحادثة بعد الضغط على زر الشراء (الخطوة 3 في طلبك)
def start_pen_purchase_conversation(update, context):
    query = update.callback_query
    data = query.data  # buy_aqlam_metal
    query.answer()
    
    # استخراج المفتاح الأصلي للمنتج
    product_callback = data.replace("buy_", "")
    
    selected_pen_data = next((item for item in aqlam_submenu if item["callback"] == product_callback), None)
    
    context.user_data['pen_data'] = selected_pen_data
    context.user_data['state'] = GET_PEN_NAME
    
    try: 
        query.message.delete()
    except Exception:
        pass
        
    # زر الرجوع يعود للقائمة الفرعية للأقلام
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_pen_types")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # نص الرسالة حسب طلب العميل
    caption_text = (
        f"**اختيارك: {selected_pen_data['label']}**\n\n"
        f"تظهر رسالة للعميل **اكتب الاسم المطلوب حفره علي القلم** او اضغط زر رجوع للعودة الي القائمة السابقة"
    )

    try:
        update.effective_chat.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_pen_data['image'],
            caption=caption_text,
            reply_markup=back_reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        update.effective_chat.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=back_reply_markup,
            parse_mode="Markdown"
        )
    return GET_PEN_NAME


# 🛑 تم تعديل هذه الدالة (كانت receive_pen_name_and_prepare_whatsapp) لإنشاء زر إرسال الطلب على الواتساب (الخطوة 4 في طلبك)
def receive_pen_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    product_data = context.user_data.get('pen_data')
    
    if not product_data:
        update.effective_chat.send_message("عفواً، حدث خطأ. يرجى البدء من القائمة الرئيسية.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    # رسالة الواتساب
    message_body = (
        f"🔔 *طلب شراء جديد (قلم)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الاسم المطلوب حفره: *{engraving_name}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    # لوحة المفاتيح: زر الإرسال على الواتساب وزر العودة للقائمة الرئيسية
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n✏️ المنتج: {product_data['label']}\n✍️ الاسم المطلوب: {engraving_name}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    
    context.user_data.clear()
    return ConversationHandler.END

# 🛑 تم تعديل هذه الدالة (كانت back_to_pen_types) لإظهار القائمة الفرعية للأقلام عند الرجوع من المحادثة
def back_to_pen_types(update, context):
    query = update.callback_query
    query.answer()
    # لا نقوم بمسح الـ user_data هنا حتى لا ننهي المحادثة عن طريق الخطأ قبل أن يرسل المستخدم الاسم
    # context.user_data.clear() # يتم مسحها في الدالة receive_pen_name_and_prepare_whatsapp عند الانتهاء
    try:
        query.message.delete()
    except Exception:
        pass
    
    # نستخدم show_submenu لعرض قائمة الأقلام (الخطوة 1)
    submenu_list = aqlam_submenu
    show_submenu(update, context, submenu_list, "اقلام محفورة بالاسم", back_callback="main_menu")
    return ConversationHandler.END # ننهي المحادثة ونعود إلى معالج الأزرار العام


# --- [دوال المحادثات الأخرى] ---
# ... (get_wedding_tissues_items, start_tissue_purchase, etc. - No changes here) ...

# --------------------
# 4. معالج الأزرار العام (button)
# --------------------

def button(update, context):
    query = update.callback_query
    data = query.data
    
    # 1. معالجة زر الرجوع للقائمة الرئيسية
    if data == "main_menu":
        start(update, context)
        return

    # 2. معالجة فتح القوائم المتداخلة (sawany, taarat, haram, doro3, mugat)
    # ... (No changes here) ...
    
    # 3. معالجة فتح قوائم المستوى الأول المباشرة (engraved_wallet, aqlam, bsamat, etc.)
    
    # 🛑 التعامل الخاص مع قائمة الأقلام (الخطوة 1: عرض قائمة الأنواع)
    if data == "aqlam":
        submenu_list = all_submenus.get(data)
        show_submenu(update, context, submenu_list, "اقلام محفورة بالاسم", back_callback="main_menu")
        return
        
    # 🛑 التعامل الخاص مع اختيار نوع القلم (الخطوة 2: عرض تفاصيل القلم وزر الشراء)
    if data in ["aqlam_metal", "aqlam_luminous"]:
        display_single_pen_product(update, context, data)
        return

    # 4. معالجة قوائم المستوى الأول المباشرة الأخرى (التي تعرض المنتجات مباشرة)
    if data in ["engraved_wallet", "bsamat", "wedding_tissues", "abajorat", "katb_kitab_box"]:
        submenu_list = all_submenus.get(data)
        show_product_page(update, data, submenu_list, is_direct_list=True)
        return

    # 5. معالجة عرض صفحات المنتجات مباشرة (قوائم المستوى الثاني)
    # ... (No changes here) ...

    # 6. معالجة أزرار الشراء الفردية (للمنتجات التي لا تحتاج محادثة)
    # ... (No changes here) ...
    

    query.answer("إجراء غير معروف.", show_alert=True)
    start(update, context) # عودة للقائمة الرئيسية كإجراء احتياطي

# ... (rest of the file remains the same until the ConversationHandler definitions) ...


# --------------------
# 5. تعريف معالجات المحادثات (Conversation Handlers)
# --------------------

# ... (box_handler, tray_handler, khashab_tray_handler, akerik_taarat_handler, khashab_taarat_handler, bsamat_handler, tissue_handler, engraved_wallet_handler - No changes here) ...


# 🛑 تم تعديل engraved_pen_handler لتبدأ عند زر الشراء (buy_aqlam_*) وليس عند زر نوع القلم (aqlam_*)
engraved_pen_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_pen_purchase_conversation, pattern='^buy_aqlam_.*')],
    states={
        GET_PEN_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp)],
    },
    fallbacks=[
        CommandHandler('start', start),
        CallbackQueryHandler(back_to_pen_types, pattern='^back_to_pen_types$'),
        CallbackQueryHandler(cancel_and_end)
    ]
)


def main():
    # 1. إعدادات التوكن
    # ... (No changes here) ...
    
    # 4. إضافة جميع ConversationHandler أولاً لضمان الأولوية
    dp.add_handler(box_handler)
    dp.add_handler(tray_handler)
    dp.add_handler(khashab_tray_handler)
    dp.add_handler(akerik_taarat_handler) 
    dp.add_handler(khashab_taarat_handler) 
    dp.add_handler(bsamat_handler) 
    dp.add_handler(tissue_handler) 
    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler)
    
    
    # 5. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 6. معالج أزرار القائمة والتنقل (يجب أن يأتي بعد معالجات المحادثة)
    dp.add_handler(CallbackQueryHandler(button)) 

    # 7. معالج للرسائل النصية
    # ... (No changes here) ...

# ... (main function - No changes here) ...