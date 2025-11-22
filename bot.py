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

# --- القوائم المتداخلة (Placeholder) ---
sawany_submenu = [
    {"label": "صينية اكليريك", "callback": "sawany_acrylic"},
    {"label": "صينية خشب", "callback": "sawany_khashab"},
]
taarat_submenu = [
    {"label": "طارات اكليريك", "callback": "taarat_acrylic"},
    {"label": "طارات خشب", "callback": "taarat_khashab"},
]
haram_submenu = [
    {"label": "هرم موديل 1", "callback": "haram_m1"},
]
doro3_submenu = [
    {"label": "درع موديل 1", "callback": "doro3_m1"},
]
mugat_submenu = [
    {"label": "مج موديل 1", "callback": "mugat_m1"},
]


# قاموس يجمع جميع القوائم الفرعية لسهولة الوصول إليها في دالة button
all_submenus = {
    "engraved_wallet": engraved_wallet_submenu,
    "aqlam": aqlam_submenu,
    "bsamat": bsamat_submenu,
    "wedding_tissues": wedding_tissues_submenu,
    "katb_kitab_box": katb_kitab_box_submenu,
    "abajorat": abajorat_submenu,
    "sawany": sawany_submenu,
    "taarat": taarat_submenu,
    "haram": haram_submenu,
    "doro3": doro3_submenu,
    "mugat": mugat_submenu,
}

# --------------------
# 3. الدوال الأساسية (start, cancel_and_end, show_submenu, show_product_page)
# --------------------

def cancel_and_end(update, context):
    """ينهي أي محادثة جارية ويمسح بيانات المستخدم."""
    if update.callback_query:
        query = update.callback_query
        query.answer()
        try:
            query.message.delete()
        except Exception:
            pass
        update.effective_chat.send_message("تم إلغاء الطلب. يمكنك البدء من جديد.")
    
    if 'state' in context.user_data:
        context.user_data.clear()
        
    return ConversationHandler.END


def start(update, context):
    """يرسل رسالة الترحيب والقائمة الرئيسية."""
    if update.callback_query:
        query = update.callback_query
        try:
            query.message.delete()
        except Exception:
            pass
    
    # تعريف لوحة المفاتيح الرئيسية
    keyboard = [
        [InlineKeyboardButton("محافظ جلد محفورة بالاسم", callback_data="engraved_wallet")],
        [InlineKeyboardButton("اقلام محفورة بالاسم", callback_data="aqlam")], 
        [InlineKeyboardButton("بصمات كتب كتاب", callback_data="bsamat")],
        [InlineKeyboardButton("مناديل كتب كتاب", callback_data="wedding_tissues")],
        [InlineKeyboardButton("بوكس كتب كتاب", callback_data="katb_kitab_box")],
        [InlineKeyboardButton("أباجورات", callback_data="abajorat")],
        [InlineKeyboardButton("صواني تقديم", callback_data="sawany")],
        [InlineKeyboardButton("طارات شبكة وديكور", callback_data="taarat")],
        [InlineKeyboardButton("هرم الصور", callback_data="haram")],
        [InlineKeyboardButton("دروع", callback_data="doro3")],
        [InlineKeyboardButton("مجّات", callback_data="mugat")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="مرحباً بك في بوت خدمة العملاء! اختر من القائمة ما يناسبك:",
        reply_markup=reply_markup
    )
    # مسح بيانات المحادثات السابقة عند العودة للقائمة الرئيسية
    if 'state' in context.user_data:
        context.user_data.clear()
    
    # لا نعود بأي حالة لأنها ليست جزء من ConversationHandler

def show_submenu(update, context, submenu_list, title, back_callback):
    """دالة مساعدة لعرض قوائم فرعية (زرين أو أكثر)."""
    query = update.callback_query
    query.answer()

    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in submenu_list]
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        query.edit_message_text(
            text=f"القائمة: {title}\n\nيرجى اختيار النوع المطلوب:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception:
        # في حالة فشل التعديل، نرسل رسالة جديدة
        update.effective_chat.send_message(
            text=f"القائمة: {title}\n\nيرجى اختيار النوع المطلوب:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

def show_product_page(update, context, data, submenu_list, is_direct_list=False):
    """دالة مساعدة لعرض صفحة المنتج (صورة، وصف، زر شراء)."""
    
    query = update.callback_query
    query.answer()
    
    if is_direct_list and submenu_list:
        selected_item_data = submenu_list[0]
        back_callback = "main_menu"
    else:
        # هذا الجزء مخصص لاختيار منتج محدد من قائمة فرعية
        selected_item_data = next((item for item in submenu_list if item["callback"] == data), None)
        # Placeholder for back_callback, should be dynamically determined based on the product type
        if data.startswith("wallet_"):
            back_callback = "engraved_wallet" 
        elif data.startswith("bsamat_"):
            back_callback = "bsamat"
        elif data.startswith("tissue_"):
            back_callback = "wedding_tissues"
        elif data.startswith("box_"):
            back_callback = "katb_kitab_box"
        elif data.startswith("abajora_"):
            back_callback = "abajorat"
        # يمكن إضافة باقي حالات الرجوع هنا
        else:
             back_callback = "main_menu" # Fallback 

    if not selected_item_data:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return

    item_keyboard = [
        [InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{selected_item_data['callback']}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)] 
    ]
    item_reply_markup = InlineKeyboardMarkup(item_keyboard)
    
    caption_text = f"**{selected_item_data['label']}**\n\n{selected_item_data['description']}"

    # حذف رسالة القائمة السابقة
    try:
        query.message.delete()
    except Exception:
        pass

    try:
        update.effective_chat.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_item_data['image'],
            caption=caption_text,
            reply_markup=item_reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest:
         update.effective_chat.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=item_reply_markup,
            parse_mode="Markdown"
        )


# --------------------
# 4. دوال المحادثات الخاصة بالأقلام (تم تطبيق المطلوب هنا)
# --------------------

# دالة لعرض صفحة منتج القلم المفرد (الخطوة 2)
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
        

# دالة لبدء محادثة الشراء (الخطوة 3)
def start_pen_purchase_conversation(update, context):
    query = update.callback_query
    data = query.data 
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


# دالة لاستلام الاسم وإعداد رابط الواتساب (الخطوة 4)
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

# دالة الرجوع من المحادثة إلى قائمة الأقلام
def back_to_pen_types(update, context):
    query = update.callback_query
    query.answer()
    
    try:
        query.message.delete()
    except Exception:
        pass
    
    # نستخدم show_submenu لعرض قائمة الأقلام (الخطوة 1)
    submenu_list = aqlam_submenu
    show_submenu(update, context, submenu_list, "اقلام محفورة بالاسم", back_callback="main_menu")
    return ConversationHandler.END


# --- [دوال المحادثات الأخرى] --- (Placeholder)
# يجب تعريف باقي دوال المحادثات هنا مثل (get_wedding_tissues_items, start_tissue_purchase, etc.)


# --------------------
# 5. معالج الأزرار العام (button)
# --------------------

def button(update, context):
    query = update.callback_query
    data = query.data
    
    if data == "main_menu":
        start(update, context)
        return

    # معالجة فتح القوائم المتداخلة (المستوى الأول)
    if data in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        submenu_list = all_submenus.get(data)
        # يمكن تحسين الحصول على اسم القائمة إذا لم يكن موجوداً في الرسالة الأصلية
        title = next((item for sublist in [engraved_wallet_submenu, aqlam_submenu, bsamat_submenu, wedding_tissues_submenu, katb_kitab_box_submenu, abajorat_submenu] for item in sublist if item.get("callback") == data), {}).get("label", "قائمة فرعية")
        show_submenu(update, context, submenu_list, title, back_callback="main_menu")
        return
    
    # التعامل الخاص مع قائمة الأقلام (الخطوة 1)
    if data == "aqlam":
        submenu_list = all_submenus.get(data)
        show_submenu(update, context, submenu_list, "اقلام محفورة بالاسم", back_callback="main_menu")
        return
        
    # التعامل الخاص مع اختيار نوع القلم (الخطوة 2)
    if data in ["aqlam_metal", "aqlam_luminous"]:
        display_single_pen_product(update, context, data)
        return

    # معالجة قوائم المستوى الأول المباشرة الأخرى (التي تعرض المنتجات مباشرة أو خيارات المنتجات)
    if data in ["engraved_wallet", "bsamat", "wedding_tissues", "abajorat", "katb_kitab_box"]:
        submenu_list = all_submenus.get(data)
        # هنا قد تحتاج لـ show_submenu إذا كانت تعرض أكثر من خيار، أو show_product_page إذا كانت تعرض المنتج مباشرة
        # بناءً على تعريف القوائم أعلاه (مثل المحافظ والبصمات)، نستخدم show_submenu ثم يتم استخدام show_product_page لاحقاً
        title_map = {"engraved_wallet": "محافظ جلد محفورة بالاسم", "bsamat": "بصمات كتب كتاب", "wedding_tissues": "مناديل كتب كتاب", "abajorat": "أباجورات", "katb_kitab_box": "بوكس كتب كتاب"}
        show_submenu(update, context, submenu_list, title_map.get(data, "قائمة"), back_callback="main_menu")
        return

    # معالجة عرض صفحات المنتجات مباشرة (قوائم المستوى الثاني مثل wallet_bege, bsamat_m1)
    if data in [item["callback"] for sublist in all_submenus.values() for item in sublist if item["callback"] not in ["sawany_acrylic", "sawany_khashab", "taarat_acrylic", "taarat_khashab"]]:
        
        # تحديد القائمة الفرعية المناسبة للرجوع
        if data.startswith("wallet_"):
            submenu = engraved_wallet_submenu
        elif data.startswith("bsamat_"):
            submenu = bsamat_submenu
        elif data.startswith("tissue_"):
            submenu = wedding_tissues_submenu
        elif data.startswith("box_"):
            submenu = katb_kitab_box_submenu
        elif data.startswith("abajora_"):
            submenu = abajorat_submenu
        elif data.startswith("haram_"):
            submenu = haram_submenu
        elif data.startswith("doro3_"):
            submenu = doro3_submenu
        elif data.startswith("mugat_"):
            submenu = mugat_submenu
        else:
            query.answer("خطأ في تحديد المنتج.", show_alert=True)
            return

        show_product_page(update, context, data, submenu)
        return

    query.answer("إجراء غير معروف.", show_alert=True)
    start(update, context) # عودة للقائمة الرئيسية كإجراء احتياطي


# --------------------
# 6. تعريف معالجات المحادثات (Conversation Handlers)
# --------------------

# مثال: تعريف محادثة المحافظ
engraved_wallet_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(lambda u,c: c.bot.send_message(u.effective_chat.id, "ادخل الاسم المطلوب..."), pattern='^buy_wallet_.*')],
    states={
        GET_WALLET_NAME: [MessageHandler(Filters.text & ~Filters.command, lambda u,c: (c.bot.send_message(u.effective_chat.id, f"تم الطلب باسم {u.message.text}"), ConversationHandler.END)[1])]
    },
    fallbacks=[CommandHandler('start', start)]
)

# معالج محادثة الأقلام (تم تطبيقه وفقاً للمتطلبات)
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


# --- [يجب إضافة باقي معالجات المحادثات هنا، مثل box_handler, tray_handler, إلخ] ---
# placeholder definitions for missing handlers to prevent errors
def dummy_handler(entry_pattern):
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(lambda u, c: ConversationHandler.END, pattern=entry_pattern)],
        states={},
        fallbacks=[CommandHandler('start', start)]
    )

box_handler = dummy_handler('^buy_box_.*')
tray_handler = dummy_handler('^buy_sawany_acrylic_.*')
khashab_tray_handler = dummy_handler('^buy_sawany_khashab_.*')
akerik_taarat_handler = dummy_handler('^buy_taarat_acrylic_.*')
khashab_taarat_handler = dummy_handler('^buy_taarat_khashab_.*')
bsamat_handler = dummy_handler('^buy_bsamat_.*')
tissue_handler = dummy_handler('^buy_tissue_.*')


# --------------------
# 7. دالة main
# --------------------

def main():
    # 1. إعدادات التوكن
    # 🛑 ⚠️ هام: يجب استبدال "YOUR_BOT_TOKEN" بالتوكن الفعلي الخاص ببوت تليجرام
    TOKEN = "YOUR_BOT_TOKEN" 
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
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

    # 7. معالج للرسائل النصية غير المعالجة (يمكن إزالته إذا لم يكن ضرورياً)
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: update.message.reply_text("عفواً، لا أفهم هذا الأمر. يرجى استخدام الأزرار في القائمة.")))

    # 8. بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()