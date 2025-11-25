import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
# تم استيراد Updater بدلاً من Application
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات التوكن، الواتساب ورقم فودافون كاش
# ⛔️ برجاء استبدال هذا التوكن بتوكن البوت الخاص بك
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE" 
WHATSAPP_NUMBER = "201288846355" 
VODAFONE_CASH_NUMBER = "01032328500" # 🔥 تم إضافة رقم المحفظة هنا

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
GET_AKRILIK_TAARAT_DATE = 10  # حالة تاريخ طارات اكليريك
GET_KHASHAB_TAARAT_NAMES = 11 # حالة أسماء طارات خشب
GET_KHASHAB_TAARAT_DATE = 12 # حالة تاريخ طارات خشب
GET_BSAMAT_NAMES = 13 # حالة أسماء البصمات
GET_BSAMAT_DATE = 14 # حالة تاريخ البصمات
GET_TISSUE_NAMES = 15 # حالة أسماء مناديل كتب الكتاب
GET_TISSUE_DATE = 16 # حالة تاريخ مناديل كتب الكتاب
GET_MUG_PHOTO = 17 # حالة استلام صور المجات
GET_PAYMENT_RECEIPT = 18 # حالة استلام إيصال الدفع لجميع المنتجات

# حالات المج الديجتال
GET_DIGITAL_MUG_NAME = 19

# 🔥🔥 حالات المرايا المحفورة
GET_MIRROR_SIZE = 20  # حالة تحديد المقاس
GET_MIRROR_NAME = 21  # حالة كتابة اسم العروسة


# --------------------
# 2. بيانات القوائم والمنتجات (تم إضافة السعر لكل منتج)
# --------------------

# --- صواني شبكة (sawany) ---
sawany_submenu = [
    {"label": "صواني اكليريك موديل 1", "callback": "tray_a1", "image": "https://example.com/tray_a1.jpg", "description": "صينية اكليريك فاخرة، تصميم عصري وأنيق.", "price": "350 ج"},
    {"label": "صواني خشب موديل 1", "callback": "tray_k1", "image": "https://example.com/tray_k1.jpg", "description": "صينية خشب طبيعي محفور بالليزر، لمسة كلاسيكية.", "price": "300 ج"},
]

# --- طارات خطوبة وكتب الكتاب (taarat) ---
taarat_submenu = [
    {"label": "طارة اكليريك موديل 1", "callback": "taara_a1", "image": "https://example.com/taara_a1.jpg", "description": "طارة اكليريك شفافة، مقاس 30 سم.", "price": "150 ج"},
    {"label": "طارة خشب موديل 1", "callback": "taara_k1", "image": "https://example.com/taara_k1.jpg", "description": "طارة خشبية أنيقة، مقاس 40 سم.", "price": "200 ج"},
]

# --- بصامات (bsamat) ---
bsamat_submenu = [
    {"label": "بصامة خشب موديل 1", "callback": "bsama_k1", "image": "https://example.com/bsama_k1.jpg", "description": "بصامة زفاف خشبية بالأسماء والتاريخ.", "price": "180 ج"},
    {"label": "بصامة قماش موديل 1", "callback": "bsama_q1", "image": "https://example.com/bsama_q1.jpg", "description": "لوحة بصمات قماشية مع ألوان الحبر.", "price": "250 ج"},
]

# --- مناديل كتب الكتاب (wedding_tissues) ---
wedding_tissues_submenu = [
    {"label": "منديل كتب كتاب مطرز 1", "callback": "tissue_e1", "image": "https://example.com/tissue_e1.jpg", "description": "منديل مطرز بخيوط حريرية، تصميم راقي.", "price": "120 ج"},
    {"label": "منديل كتب كتاب مطبوع 1", "callback": "tissue_p1", "image": "https://example.com/tissue_p1.jpg", "description": "منديل قطن مطبوع، تصميم عصري.", "price": "90 ج"},
]

# --- بوكس كتب الكتاب (katb_kitab_box) ---
katb_kitab_box_submenu = [
    {"label": "بوكس كتب كتاب (الوان)", "callback": "box_w1", "image": "https://example.com/box_w1.jpg", "description": "بوكس خشبي أنيق بألوان متعددة.", "price": "400 ج"},
]
# الوان بوكس كتب الكتاب
box_colors_data = {
    "white": "أبيض",
    "pink": "وردي",
    "blue": "أزرق",
}

# --- هرم مكتب (haram) ---
haram_submenu = [
    {"label": "هرم مكتبي اكليريك", "callback": "haram_a1", "image": "https://example.com/haram_a1.jpg", "description": "هرم مكتب لتزيين المكاتب والمنزل.", "price": "150 ج"},
]

# --- دروع تكريم (doro3) ---
doro3_submenu = [
    {"label": "درع اكليريك", "callback": "dor3_a1", "image": "https://example.com/dor3_a1.jpg", "description": "درع تكريم اكليريك مقاس 20 سم.", "price": "100 ج"},
]

# --- شمعدان (shamadan) ---
shamadan_submenu = [
    {"label": "شمعدان موديل 1", "callback": "shamadan_m1", "image": "https://example.com/shamadan_m1.jpg", "description": "شمعدان خشبي بتصميم ريفي.", "price": "80 ج"},
]

# --- أباجورات (abajorat) ---
abajorat_submenu = [
    {"label": "أباجورة موديل 1", "callback": "abajora_m1", "image": "https://example.com/abajora_m1.jpg", "description": "أباجورة خشبية إضاءة LED.", "price": "220 ج"},
]

# 🔥 قائمة المرايا المحفورة الجديدة
engraved_mirrors_submenu = [
    {"label": "مرايا محفورة موديل 1", "callback": "mirror_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "مرايا دائرية فاخرة، تصميم أنيق ومميز.", "price": "100-300 ج"},
    {"label": "مرايا محفورة موديل 2", "callback": "mirror_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "مرايا مستطيلة بإطار خشبي، خامة عالية الجودة.", "price": "100-300 ج"}
]

# بيانات المقاسات والأسعار
mirror_sizes_data = {
    "size_1": {"label": "مقاس 1", "price": "100 ج"},
    "size_2": {"label": "مقاس 2", "price": "200 ج"},
    "size_3": {"label": "مقاس 3", "price": "300 ج"},
}

# --- محافظ محفورة (engraved_wallet) ---
engraved_wallet_submenu = [
    {"label": "محفظة جلد طبيعي", "callback": "wallet_l1", "image": "https://example.com/wallet_l1.jpg", "description": "محفظة جلد طبيعي محفورة بالاسم.", "price": "200 ج"},
]

# --- أقلام محفورة (engraved_pen) ---
engraved_pen_submenu = [
    {"label": "قلم معدني حفر ليزر", "callback": "pen_m1", "image": "https://example.com/pen_m1.jpg", "description": "قلم معدني فاخر محفور بالاسم.", "price": "120 ج"},
]

# --- لوازم السابلميشن (sublimation) ---
sublimation_supplies_submenu = [
    {"label": "مج سادة للتصنيع", "callback": "sub_mug", "image": "https://example.com/sub_mug.jpg", "description": "مج سادة بجودة عالية مخصص للطباعة.", "price": "50 ج"},
    {"label": "تيشيرت سادة للتصنيع", "callback": "sub_shirt", "image": "https://example.com/sub_shirt.jpg", "description": "تيشيرت بوليستر مخصص للطباعة.", "price": "80 ج"},
]

# --- المجات (mugs) ---
mugs_submenu = [
    {"label": "مج مطبوع بالصورة", "callback": "mug_photo", "image": "https://example.com/mug_photo.jpg", "description": "مج ابيض مطبوع بصورتك الشخصية.", "price": "90 ج"},
    {"label": "مج ديجتال بالاسم", "callback": "mug_digital_name", "image": "https://example.com/mug_digital_name.jpg", "description": "مج سحري أو عادي بالاسم حسب اختيارك.", "price": "150 ج"},
]


# --- القائمة الرئيسية ---
main_menu = [
    {"label": "💍💍 صواني شبكة", "callback": "sawany"},
    {"label": "💍 طارات خطوبة وكتب الكتاب", "callback": "taarat"},
    {"label": "✋ بصامات", "callback": "bsamat"}, 
    {"label": "📜 مناديل كتب الكتاب", "callback": "wedding_tissues"},
    {"label": "🎁 بوكس كتب الكتاب", "callback": "katb_kitab_box"},
    # 🔥 الزر الجديد للمرايا المحفورة
    {"label": "🪞 مرايا محفورة بأسم العروسة", "callback": "engraved_mirrors"}, 
    {"label": "🗄️ هرم مكتب", "callback": "haram"},
    {"label": "🛡️ دروع تكريم", "callback": "doro3"},
    {"label": "🕯️ شمعدان", "callback": "shamadan"},
    {"label": "💡 أباجورات", "callback": "abajorat"},
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"},
    {"label": "🖊️ أقلام محفورة بالاسم", "callback": "engraved_pen"},
    {"label": "☕ مجات مخصصة", "callback": "mugs"},
    {"label": "⚙️ لوازم السابلميشن", "callback": "sublimation"},
]

# خريطة لتجميع كل القوائم الفرعية
all_submenus = {
    "sawany": sawany_submenu,
    "taarat": taarat_submenu,
    "bsamat": bsamat_submenu,
    "wedding_tissues": wedding_tissues_submenu,
    "katb_kitab_box": katb_kitab_box_submenu,
    "haram": haram_submenu,
    "doro3": doro3_submenu,
    "shamadan": shamadan_submenu,
    "abajorat": abajorat_submenu,
    "engraved_wallet": engraved_wallet_submenu,
    "engraved_pen": engraved_pen_submenu,
    "mugs": mugs_submenu,
    "sublimation": sublimation_supplies_submenu, 
    # 🔥 إضافة قائمة المرايا المحفورة
    "engraved_mirrors": engraved_mirrors_submenu 
}

# خريطة لمعرفة القائمة الأم للمنتج
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box", "sublimation", "engraved_mirrors"]: # 🔥 إضافة 'engraved_mirrors'
        # هذه قوائم يتم الدخول عليها مباشرة من القائمة الرئيسية
        # لا نحتاج لزر 'رجوع' للقائمة الأم
        for product in submenu_list:
            product_to_submenu_map[product["callback"]] = menu_key
    else:
        # قوائم فرعية (مثل sawany/taarat/mugs)
        for product in submenu_list:
            product_to_submenu_map[product["callback"]] = menu_key

# --------------------
# 3. الدوال المساعدة
# --------------------

# دالة لبناء الأزرار (القوائم الرئيسية/الفرعية)
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.extend(footer_buttons)
    return menu

# دالة تسترجع القائمة الفرعية من الـ callback
def get_submenu(callback_data):
    return all_submenus.get(callback_data)

# دالة لبدء البوت وإظهار القائمة الرئيسية
def start(update, context):
    context.user_data.clear()
    
    keyboard = build_menu(
        [InlineKeyboardButton(item["label"], callback_data=item["callback"]) for item in main_menu],
        n_cols=2
    )
    reply_markup = InlineKeyboardMarkup(keyboard)

    # التحقق من نوع الحدث (رسالة /start أو ضغطة زر رجوع)
    if update.callback_query:
        query = update.callback_query
        query.answer()
        try:
            query.message.delete()
        except:
            pass # الرسالة قد تكون محذوفة بالفعل
        
    text = "مرحباً بك في بوت متجر **(اسم المتجر)**.\n\nمن فضلك، اختر القسم المطلوب من القائمة الرئيسية:"
    
    # إرسال أو تعديل الرسالة
    if update.callback_query:
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=text, 
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        update.message.reply_text(
            text, 
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    return ConversationHandler.END

# دالة لإظهار صفحة المنتجات (قائمة فرعية)
def show_product_page(update, callback_data, submenu_list, is_direct_list=False):
    if update.callback_query:
        query = update.callback_query
        query.answer()
        try:
            query.message.delete()
        except:
            pass # الرسالة قد تكون محذوفة بالفعل

    # تجهيز الأزرار
    product_buttons = []
    for product in submenu_list:
        # زر المنتج (لعرض التفاصيل)
        product_buttons.append(InlineKeyboardButton(product["label"], callback_data=product["callback"]))
    
    # زر الرجوع للقائمة الرئيسية
    back_button = [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
    
    keyboard = build_menu(
        product_buttons,
        n_cols=1,
        footer_buttons=back_button
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # إرسال الرسالة
    text = "من فضلك، اختر المنتج المطلوب للمعاينة:"
    
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return ConversationHandler.END

# دالة لإظهار تفاصيل المنتج وصفحة الشراء
def show_details(update, context):
    query = update.callback_query
    query.answer()
    product_callback_data = query.data
    
    # تحديد القائمة الأم للرجوع إليها
    parent_menu_key = product_to_submenu_map.get(product_callback_data)
    
    # 1. تحديد زر الرجوع
    if product_callback_data in ["sawany", "taarat", "mugs"]:
        # قوائم أم (يتم عرضها بزر القائمة الرئيسية فقط)
        back_callback = "main_menu"
    # 1. إذا كانت قائمة مباشرة من القائمة الرئيسية (مثل بصمات، أباجورات)
    elif product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation", "engraved_mirrors"]: # 🔥 إضافة 'engraved_mirrors'
        back_callback = "main_menu"
    elif parent_menu_key:
        back_callback = parent_menu_key
    else:
        back_callback = "main_menu"
        
    
    # 2. تحديد المنتج وبياناته
    submenu_list = all_submenus.get(parent_menu_key)
    if not submenu_list:
        # إذا كان المنتج هو في الحقيقة قائمة فرعية (مثل mugs)
        submenu_list = get_submenu(product_callback_data)
        if submenu_list:
            return show_product_page(update, product_callback_data, submenu_list)
        else:
            # المنتج هو العنصر النهائي الذي يجب عرض تفاصيله
            # البحث عن المنتج ضمن جميع القوائم
            selected_product = None
            for sublist in all_submenus.values():
                selected_product = next((item for item in sublist if item["callback"] == product_callback_data), None)
                if selected_product:
                    break
    else:
        selected_product = next((item for item in submenu_list if item["callback"] == product_callback_data), None)

    if not selected_product:
        query.answer("عذراً، لم نجد تفاصيل لهذا المنتج.", show_alert=True)
        return ConversationHandler.END

    # 3. حفظ بيانات المنتج للحالات المستقبلية
    context.user_data.clear()
    context.user_data['direct_product'] = selected_product

    # 4. تجهيز الأزرار: زر شراء و زر رجوع (الزر يختلف حسب المنتج)
    buy_callback = f"buy_{selected_product['callback']}"
    
    # المنتجات ذات التدفق الخاص (أسماء/تاريخ/لون/مقاس)
    if product_callback_data.startswith("tray_"):
        buy_callback = "start_tray_names"
    elif product_callback_data.startswith("taara_"):
        buy_callback = "start_taarat_names"
    elif product_callback_data.startswith("box_"):
        buy_callback = "start_box_color"
    elif product_callback_data.startswith("bsama_"):
        buy_callback = "start_bsamat_names"
    elif product_callback_data.startswith("tissue_"):
        buy_callback = "start_tissue_names"
    elif product_callback_data.startswith("wallet_"):
        buy_callback = "start_wallet_name"
    elif product_callback_data.startswith("pen_"):
        buy_callback = "start_pen_name"
    elif product_callback_data == "mug_photo":
        buy_callback = "start_mug_photo"
    elif product_callback_data == "mug_digital_name":
        buy_callback = "start_digital_mug_name"
    # 🔥 حالة المرايا المحفورة
    elif product_callback_data.startswith("mirror_"):
        buy_callback = f"buy_{selected_product['callback']}" # سيتم التقاطها بواسطة mirror_handler

    # تجهيز أزرار الشراء والرجوع
    keyboard = [
        [InlineKeyboardButton("🛒 شراء المنتج", callback_data=buy_callback)],
        [InlineKeyboardButton(f"🔙 رجوع لقائمة {all_submenus.get(back_callback, main_menu)[0].get('label', 'الرئيسية') if back_callback != 'main_menu' else 'الرئيسية'}", callback_data=back_callback)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # 5. بناء النص
    caption_text = (
        f"**{selected_product['label']}**\n\n"
        f"**الوصف:** {selected_product['description']}\n"
        f"**السعر:** {selected_product['price']}"
    )
    
    # 6. إرسال/تعديل الرسالة
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_photo(
        chat_id=update.effective_chat.id, 
        photo=selected_product["image"],
        caption=caption_text, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

# --------------------
# 4. دوال تدفق الشراء (معالجة الرسائل واستقبال المدخلات)
# --------------------

# ... (هنا ستكون جميع الدوال الخاصة بـ (صواني، طارات، بوكس، بصمات، مناديل، محافظ، أقلام، مجات صور، مجات ديجتال))
# ... (تم حذفها للاختصار ولأنها لم يُطلب تعديلها، ولكن يجب أن تكون موجودة في الكود الأصلي)

def get_mirror_items():
    return engraved_mirrors_submenu

# دالة تبدأ عملية شراء المرايا وتسأل عن المقاس
def start_mirror_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_mirror_m1 or buy_mirror_m2
    product_callback = data.replace("buy_", "")
    
    # 1. الحصول على بيانات المنتج
    items_list = get_mirror_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data.clear()
    context.user_data['mirror_product'] = selected_product
    context.user_data['state'] = GET_MIRROR_SIZE
    
    # 2. تجهيز الأزرار (أزرار المقاسات + زر الرجوع)
    keyboard = []
    # أزرار المقاسات والأسعار
    for size_key, size_data in mirror_sizes_data.items():
        keyboard.append([InlineKeyboardButton(f"{size_data['label']} بسعر {size_data['price']}", callback_data=f"size_{size_key}")])

    # زر الرجوع للقائمة السابقة (قائمة منتجات المرايا)
    keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة السابقة", callback_data="engraved_mirrors")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # 3. إرسال الرسالة
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}**\n\n*برجاء تحديد المقاس المطلوب:*"
    
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=caption_text, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_MIRROR_SIZE

# دالة للرجوع من مرحلة الاسم إلى مرحلة اختيار المقاس
def back_to_mirror_sizes(update, context):
    query = update.callback_query
    query.answer()
    
    selected_product = context.user_data.get('mirror_product')
    if not selected_product:
        # إذا لم نجد المنتج نعود للقائمة الرئيسية (أو ننهي المحادثة)
        return start(update, context) 
    
    # 2. تجهيز الأزرار (نفس منطق start_mirror_purchase)
    keyboard = []
    for size_key, size_data in mirror_sizes_data.items():
        keyboard.append([InlineKeyboardButton(f"{size_data['label']} بسعر {size_data['price']}", callback_data=f"size_{size_key}")])

    keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة السابقة", callback_data="engraved_mirrors")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # 3. إرسال الرسالة
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}**\n\n*برجاء تحديد المقاس المطلوب:*"
    
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=caption_text, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_MIRROR_SIZE

# دالة لحفظ المقاس والتحول لطلب اسم العروسة
def save_mirror_size_ask_name(update, context):
    query = update.callback_query
    query.answer()
    
    data = query.data # size_size_1
    size_key = data.replace("size_", "")
    selected_size = mirror_sizes_data.get(size_key)
    
    if not selected_size:
        query.answer("خطأ في تحديد المقاس", show_alert=True)
        return GET_MIRROR_SIZE

    context.user_data['mirror_size'] = selected_size
    context.user_data['state'] = GET_MIRROR_NAME
    
    # زر الرجوع للقائمة السابقة (اختيار المقاس)
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع للقائمة السابقة", callback_data="back_to_mirror_sizes")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # رسالة طلب اسم العروسة
    try:
        query.message.delete()
    except:
        pass
    
    caption_text = f"✅ تم اختيار المقاس: **{selected_size['label']}** (السعر: *{selected_size['price']}*)\n\n*برجاء كتابة اسم العروسة المطلوب حفره علي المرايا في رسالة نصية بالأسفل:*"
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=caption_text, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_MIRROR_NAME

# دالة مساعدة لزر الرجوع من المقاس إلى قائمة المنتجات
def show_product_page_for_mirror_back(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    
    # إعادة عرض قائمة المرايا
    show_product_page(update, "engraved_mirrors", engraved_mirrors_submenu, is_direct_list=True)
    return ConversationHandler.END

# --------------------
# 5. دوال الدفع والإيصال
# --------------------

# دالة لحفظ الاسم والتحول لمرحلة الدفع
def receive_mirror_name_and_finish(update, context):
    name_text = update.message.text
    context.user_data['mirror_name'] = name_text
    
    # استخراج البيانات للدفع
    product_data = context.user_data.get('mirror_product')
    size_data = context.user_data.get('mirror_size')
    
    # إعداد البيانات لـ prompt_for_payment_and_receipt
    product_type = f"مرايا محفورة ({size_data['label']})"
    # تحديث البيانات المحفوظة لتمرير السعر النهائي لـ prompt_for_payment_and_receipt
    
    # حفظ نسخة من البيانات في direct_product لاستخدامها في دالة الدفع العامة
    # يجب نسخ البيانات لتجنب تعديل القوائم الأصلية
    temp_product_data = product_data.copy()
    temp_product_data['label'] = f"{product_data['label']} - {size_data['label']}"
    temp_product_data['price'] = size_data['price'] 
    
    context.user_data['direct_product'] = temp_product_data 
    
    return prompt_for_payment_and_receipt(update, context, product_type=product_type)

# دالة عامة لطلب إيصال الدفع
def prompt_for_payment_and_receipt(update, context, product_type=None):
    # 1. استرجاع بيانات المنتج والأسماء/التاريخ حسب النوع
    product_data = None
    names_details = ""
    
    if product_type == "محفظة":
        # ... (المنطق الحالي)
        product_data = context.user_data.get('wallet_product')
        names_details = context.user_data.get('wallet_name')
    elif product_type == "قلم":
        # ... (المنطق الحالي)
        product_data = context.user_data.get('pen_product')
        names_details = context.user_data.get('pen_name')
    elif product_type == "مج ديجتال": 
        # ... (المنطق الحالي)
        product_data = context.user_data.get('digital_mug_product')
        names_details = context.user_data.get('digital_mug_name')
    # 🔥🔥 إضافة حالة المرايا المحفورة لاسترجاع الاسم والمقاس
    elif product_type.startswith("مرايا محفورة"): 
        product_data = context.user_data.get('mirror_product')
        name = context.user_data.get('mirror_name')
        size = context.user_data.get('mirror_size')
        names_details = f"الاسم: {name}\nالمقاس: {size['label']}"
        product_data['price'] = size['price'] # تحديث السعر النهائي
    elif 'direct_product' in context.user_data: 
        # هذا لجميع المنتجات الأخرى ذات التدفق المعقد التي تم تخزينها في direct_product مؤقتاً
        product_data = context.user_data.get('direct_product')
        # ... (منطق استخراج الأسماء والتواريخ لـ (صواني، طارات، بوكس، بصمات، مناديل))
        
    if not product_data:
        # Fallback in case of an error
        context.bot.send_message(update.effective_chat.id, "عذراً، حدث خطأ أثناء إعداد طلبك. برجاء المحاولة مرة أخرى من القائمة الرئيسية.")
        return start(update, context)

    # 2. إعداد نص الرسالة النهائية (الطلب ومرحلة الدفع)
    product_name = product_data['label']
    product_price = product_data['price']
    
    details_text = f"\n\n**التفاصيل المطلوبة:**\n{names_details}" if names_details else ""
    
    whatsapp_link = f"https://wa.me/{WHATSAPP_NUMBER}"
    
    caption = (
        f"**الطلب:** {product_name}\n"
        f"**السعر النهائي:** {product_price}\n"
        f"**نوع المنتج:** {product_type}\n"
        f"{details_text}\n"
        "---------------------------\n"
        "**مرحلة الدفع:**\n"
        "برجاء الدفع عبر فودافون كاش على الرقم:\n"
        f"*{VODAFONE_CASH_NUMBER}*\n"
        "ثم إرسال صورة إيصال الدفع في رسالة منفصلة.\n\n"
        "أو يمكنك التواصل مباشرة عبر واتساب للمتابعة:\n"
        f"[اضغط هنا للتواصل عبر واتساب]({whatsapp_link})"
    )
    
    keyboard = [
        [InlineKeyboardButton("إلغاء الطلب والرجوع للقائمة الرئيسية", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 3. إرسال الرسالة
    if update.callback_query:
        query = update.callback_query
        try:
            query.message.delete()
        except:
            pass
            
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=caption, 
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        # إذا كانت الرسالة مدخل نصي (مثل اسم العروسة)
        update.message.reply_text(
            caption, 
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    context.user_data['state'] = GET_PAYMENT_RECEIPT
    return GET_PAYMENT_RECEIPT

# دالة لمعالجة إيصال الدفع (الصورة)
def handle_payment_photo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="تم استلام إيصال الدفع. سيتم مراجعة الطلب والتواصل معك قريباً لتأكيد الشحن.\nشكراً لثقتكم!",
        parse_mode="Markdown"
    )
    
    # إعادة البوت للحالة الأساسية
    return start(update, context)

# دالة لمعالجة أزرار مرحلة الدفع (مثل الإلغاء)
def handle_payment_buttons(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data == 'cancel':
        context.user_data.clear()
        query.edit_message_text(
            text="تم إلغاء الطلب بنجاح.",
            parse_mode="Markdown"
        )
        return start(update, context)

# دالة للإنهاء في حالة حدوث خطأ
def cancel_and_end(update, context):
    context.user_data.clear()
    return ConversationHandler.END

# --------------------
# 6. إضافة المعالجات (Handlers)
# --------------------

# دوال لتوجيه الـ Callbacks إلى الدوال المناسبة
def general_callback_handler(update, context):
    query = update.callback_query
    callback_data = query.data

    if callback_data == "main_menu":
        return start(update, context)
    
    # قوائم فرعية
    submenu_list = get_submenu(callback_data)
    if submenu_list:
        return show_product_page(update, callback_data, submenu_list)
    
    # تفاصيل منتج
    return show_details(update, context)

def setup_handlers(dp):
    
    # 1. Conversation Handler للقوائم التي تتطلب اسم/تاريخ/لون (يجب تعريفها كلها هنا)
    
    # ... (هنا ستكون جميع الـ ConversationHandler الخاصة بالمنتجات الأخرى)
    
    # مثال على ConversationHandler بسيط (مج ديجتال يطلب اسم فقط)
    digital_mug_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_digital_mug_name, pattern='^start_digital_mug_name$')],
        states={
            GET_DIGITAL_MUG_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_digital_mug_name_and_finish),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # معالج الطلبات المباشرة (المنتجات التي لا تتطلب مدخلات)
    direct_buy_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prompt_for_payment_and_receipt, pattern='^buy_(haram|doro3|shamadan|abajora|subli)_.*')],
        states={
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 🔥🔥 معالج خاص للمرايا المحفورة (يطلب مقاس ثم اسم العروسة)
    mirror_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_mirror_purchase, pattern='^buy_mirror_.*')],
        states={
            GET_MIRROR_SIZE: [
                CallbackQueryHandler(save_mirror_size_ask_name, pattern='^size_.*$'),
                # زر الرجوع لقائمة المنتجات
                CallbackQueryHandler(show_product_page_for_mirror_back, pattern='^engraved_mirrors$') 
            ],
            GET_MIRROR_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_mirror_name_and_finish),
                # زر الرجوع لاختيار المقاس
                CallbackQueryHandler(back_to_mirror_sizes, pattern='^back_to_mirror_sizes$') 
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    
    # 4. إضافة جميع ConversationHandler أولاً لضمان الأولوية
    # ... (إضافة جميع معالجات المنتجات الأخرى هنا)
    dp.add_handler(digital_mug_handler) 
    
    # 🔥 إضافة معالج المرايا المحفورة
    dp.add_handler(mirror_handler) 
    
    dp.add_handler(direct_buy_handler) 

    
    # 5. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 6. معالج لجميع الـ Callbacks الأخرى (القوائم وتفاصيل المنتجات)
    dp.add_handler(CallbackQueryHandler(general_callback_handler))


def main():
    # ⚠️ تم استعادة استخدام متغير البيئة BOT_TOKEN كما طلبت
    TOKEN = os.environ.get('TOKEN') 
    if not TOKEN:
         # يفضل طباعة رسالة خطأ أو استخدام قيمة placeholder إذا لم يتم العثور على التوكن
         print("Error: BOT_TOKEN environment variable is not set. Please set it or hardcode the token.")
         return
         
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    setup_handlers(dp)

    # بدء البوت
    print("🚀 Bot started. Press Ctrl+C to stop.")
    updater.start_polling()
    updater.idle()

# يجب أن تكون دوال start_digital_mug_name, receive_digital_mug_name_and_finish موجودة في الكود الأصلي
def start_digital_mug_name(update, context): 
    # Placeholder for the original function
    return GET_DIGITAL_MUG_NAME
def receive_digital_mug_name_and_finish(update, context):
    # Placeholder for the original function
    return GET_PAYMENT_RECEIPT

if __name__ == '__main__':
    main()