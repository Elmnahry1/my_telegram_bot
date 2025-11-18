import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات الواتساب: استبدل بالرقم الخاص بك (كود الدولة + الرقم بدون علامة +)
WHATSAPP_NUMBER = "201288846355" 

# --------------------
# 1. بيانات القوائم والمنتجات (الكاملة)
# --------------------

# --- تعريف حالات المحادثة للمنتجات المخصصة ---
GET_NAME = 1 

# --- القوائم الفرعية (كما أرسلتها مع إضافة المحافظ) ---
bsamat_submenu = [
    {"label": "بصامة موديل 1", "callback": "bsamat_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 1."},
    {"label": "بصامة موديل 2", "callback": "bsamat_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 2."}
]
wedding_tissues_submenu = [
    {"label": "منديل موديل 1", "callback": "tissue_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 1."},
    {"label": "منديل موديل 2", "callback": "tissue_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 2."}
]
abajorat_submenu = [
    {"label": "أباجورة موديل 1", "callback": "abajora_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف الأباجورة موديل 1."},
    {"label": "أباجورة موديل 2", "callback": "abajora_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف الأباجورة موديل 2."}
]

# 🛑 قائمة المحافظ الجديدة
engraved_wallet_submenu = [
    {"label": "محفظة بيج (هافان)", "callback": "wallet_bege", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بيج (هافان)."},
    {"label": "محفظة بني", "callback": "wallet_brown", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بني."},
    {"label": "محفظة سوداء", "callback": "wallet_black", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون أسود."}
]

# --- القوائم المتداخلة ---
sawany_submenu = [
    {
        "label": "صواني شبكة اكليريك", "callback": "sawany_akerik", 
        "items": [ 
            {"label": "صينية اكليريك موديل 1", "callback": "akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "صينية اكليريك: وصف المنتج الأول."},
            {"label": "صينية اكليريك موديل 2", "callback": "akerik_m2", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "صينية اكليريك: وصف المنتج الثاني."}
        ]
    },
    {
        "label": "صواني شبكة خشب", "callback": "sawany_khashab", 
        "items": [
            {"label": "صينية خشب موديل 1", "callback": "khashab_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "صينية خشب: وصف المنتج الأول."},
            {"label": "صينية خشب موديل 2", "callback": "khashab_m2", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "صينية خشب: وصف المنتج الثاني."}
        ]
    }
]
taarat_submenu = [
    {"label": "طارات اكليريك", "callback": "taarat_akerik", "items": [{"label": "طارة اكليريك موديل 1", "callback": "taarat_akerik_m1", "image": "...", "description": "..."}]},
    {"label": "طارات خشب", "callback": "taarat_khashab", "items": [{"label": "طارة خشب موديل 1", "callback": "taarat_khashab_m1", "image": "...", "description": "..."}]}
]
haram_submenu = [
    {"label": "هرم مكتب اكليريك", "callback": "haram_akerik", "items": [{"label": "هرم اكليريك موديل 1", "callback": "haram_akerik_m1", "image": "...", "description": "..."}]},
]
doro3_submenu = [
    {"label": "دروع اكليريك", "callback": "doro3_akerik", "items": [{"label": "درع اكليريك موديل 1", "callback": "doro3_akerik_m1", "image": "...", "description": "..."}]},
]
aqlam_submenu = [
    {"label": "قلم تاتش معدن", "callback": "aqlam_metal", "items": [{"label": "قلم معدن موديل 1", "callback": "aqlam_metal_m1", "image": "...", "description": "..."}]},
]
mugat_submenu = [
    {"label": "مج ابيض", "callback": "mugat_white", "items": [{"label": "مج ابيض موديل 1", "callback": "mugat_white_m1", "image": "...", "description": "..."}]},
]
# -------------------------------------------------------------------------


# --- القائمة الرئيسية ---
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


all_submenus = {
    "sawany": sawany_submenu,
    "taarat": taarat_submenu,
    "haram": haram_submenu,
    "doro3": doro3_submenu,
    "aqlam": aqlam_submenu,
    "mugat": mugat_submenu,
    "bsamat": bsamat_submenu, 
    "wedding_tissues": wedding_tissues_submenu, 
    "abajorat": abajorat_submenu,
    "engraved_wallet": engraved_wallet_submenu
}

# بناء خريطة المنتجات
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if isinstance(submenu_list, list):
        for product in submenu_list:
            if 'callback' in product:
                 product_to_submenu_map[product["callback"]] = menu_key
            if 'items' in product:
                for sub_item in product['items']:
                    product_to_submenu_map[sub_item["callback"]] = product["callback"]


# --------------------
# 2. الدوال المساعدة 
# --------------------

def start(update, context):
    # 💡 تنظيف بيانات المحادثة عند البداية الجديدة
    if context.user_data.get('state') == GET_NAME:
        context.user_data.clear()
        context.user_data['state'] = None
        
    query = update.callback_query
    if query:
        query.answer()
    
    user_name = update.effective_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختر طلبك من القائمة:"
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in main_menu]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query:
        try:
            query.message.delete()
        except Exception:
            pass 
        
        update.effective_chat.send_message(greeting_text, reply_markup=reply_markup)
    else:
        update.effective_message.reply_text(greeting_text, reply_markup=reply_markup)

# دالة عرض القائمة الفرعية
def show_submenu(update, context, submenu_list, title, back_callback="main_menu"):
    query = update.callback_query
    query.answer()
    
    keyboard = []
    
    if back_callback == "engraved_wallet":
        message_text = f"✅ *{title}*:\n\nمن فضلك اختر اللون المطلوب:"
    else:
        message_text = f"✅ *{title}*:\n\nمن فضلك اختر طلبك من القائمة:"

    # إنشاء الأزرار
    for item in submenu_list:
        keyboard.append([InlineKeyboardButton(item["label"], callback_data=item["callback"])])

    # إضافة زر الرجوع
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # تحرير الرسالة الحالية
    try:
        query.edit_message_text(
            text=message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        if "Message is not modified" not in str(e):
            query.message.reply_text(text=message_text, reply_markup=reply_markup, parse_mode="Markdown")
        

def show_product_page(update, product_callback_data, product_data, is_direct_list=False):
    # الدالة كما هي، وظيفتها عرض المنتج/المنتجات مع زر الشراء
    query = update.callback_query
    if query:
        query.answer()

    products_to_show = []
    if is_direct_list:
        products_to_show = product_data
    elif 'items' in product_data:
        products_to_show = product_data['items']
    else:
        products_to_show = [product_data]

    if query and query.message:
        try:
            query.message.delete()
        except Exception:
            pass
    
    for item in products_to_show:
        item_keyboard = [[InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{item['callback']}")]]
        item_reply_markup = InlineKeyboardMarkup(item_keyboard)
        
        update.effective_message.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=item['image'],
            caption=f"**{item['label']}**\n\n{item['description']}",
            reply_markup=item_reply_markup,
            parse_mode="Markdown"
        )
    
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat"]:
        back_callback = "main_menu"
        back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
    else:
        # إذا كان المسار هو قائمة فرعية متداخلة (مثل 'sawany_akerik')، فالرجوع يكون للقائمة الفرعية الأم
        back_callback = product_to_submenu_map.get(product_callback_data, "main_menu")
        back_text = "🔙 اضغط للرجوع إلى القائمة الفرعية"

    back_keyboard = [[InlineKeyboardButton(back_text, callback_data=back_callback)]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
        
    update.effective_message.bot.send_message(
        chat_id=update.effective_chat.id,
        text="---", 
        reply_markup=back_reply_markup
    )

# 🛑 دالة العودة لقائمة الألوان (لتستخدم في زر الرجوع) - تم تحسينها
def back_to_wallets_color(update, context):
    query = update.callback_query
    query.answer()
    
    # تنظيف حالة المحادثة أولاً
    context.user_data.clear()
    
    # يجب حذف رسالة الصورة والطلب السابقة
    try:
        query.message.delete()
    except Exception:
        pass

    # بناء قائمة الألوان مرة أخرى
    keyboard = []
    for item in engraved_wallet_submenu:
        keyboard.append([InlineKeyboardButton(item["label"], callback_data=item["callback"])])
    
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *محافظ محفورة بالاسم*:\n\nمن فضلك اختر اللون المطلوب:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    return ConversationHandler.END # إنهاء المحادثة

# 🛑 دالة المحادثة 1: تبدأ المحادثة وتطلب الاسم 
def prompt_for_name(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    # البحث عن بيانات المحفظة المختارة (باللون)
    selected_wallet_data = next((item for item in engraved_wallet_submenu if item["callback"] == data), None)
    context.user_data['wallet_data'] = selected_wallet_data
    context.user_data['state'] = GET_NAME

    # 1. نحذف رسالة القائمة السابقة
    try:
        query.message.delete()
    except Exception:
        pass

    # 2. بناء الرسالة الجديدة (صورة + نص + زر رجوع)
    
    # بناء لوحة المفاتيح: زر الرجوع إلى قائمة الألوان
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_wallets_color")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # 🛑 إرسال صورة المحفظة ونص الطلب
    caption_text = (
        f"**اختيارك: {selected_wallet_data['label']}**\n\n"
        f"من فضلك، **اكتب الاسم الذي تريد حفره** على المحفظة في رسالة نصية بالأسفل.\n"
        f"أو اضغط زر الرجوع لتغيير اللون."
    )
    
    update.effective_chat.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=selected_wallet_data['image'],
        caption=caption_text,
        reply_markup=back_reply_markup,
        parse_mode="Markdown"
    )
    
    # ننتقل إلى حالة GET_NAME لاستقبال الرسالة النصية التالية
    return GET_NAME 

# 🛑 دالة المحادثة 2: تستقبل الاسم وتجهز رابط الواتساب النهائي
def receive_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    product_data = context.user_data.get('wallet_data')
    
    if not product_data:
        update.effective_chat.send_message("عفواً، حدث خطأ في استرجاع بيانات المنتج. يرجى البدء من القائمة الرئيسية.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        context.user_data.clear()
        return ConversationHandler.END

    # استرجاع بيانات العميل
    user_info = update.message.from_user
    
    # محاولة استخلاص اللون
    product_label = product_data['label']
    try:
        # اللون هو الجزء بعد كلمة "محفظة" (مثلاً "بيج (هافان)")
        color = product_label.split('محفظة ', 1)[1].strip() 
        wallet_type = "محفظة سافوكس الاصلية التقيلة" # نوع المنتج الأساسي
    except IndexError:
        color = product_label
        wallet_type = product_label

    # 💡 تكوين نص الرسالة الذي سيُفتح في واتساب - (للمحافظ المحفورة)
    message_body = (
        f"🔔 *طلب شراء جديد (محافظ محفورة بالاسم)* 🔔\n\n"
        f"المنتج: {wallet_type}\n"
        f"اللون: {color}\n" # حقل اللون
        f" الاسم المطلوب حفره: *{engraving_name}*\n" # حقل الحفر
        f"الكود: {product_data['callback']}\n\n"

        f"اسم العميل: {user_info.first_name} {user_info.last_name if user_info.last_name else ''}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}\n"
        f"رابط التواصل عبر التليجرام: tg://user?id={user_info.id}"
    )
    
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    # 🛑 زر تأكيد الطلب المطلوب
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]) 
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text=f"شكراً لك! سيتم حفر اسم **{engraving_name}** على **{product_data['label']}**.\n\nلإتمام الطلب، اضغط على الزر التالي:", 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    context.user_data.clear()
    return ConversationHandler.END

# 🛑 الدالة المُعدَّلة: لمعالجة جميع ضغطات الأزرار
def button(update, context):
    query = update.callback_query
    data = query.data

    if data == "main_menu":
        start(update, context)
        return

    # 🛑 1. معالجة فتح قائمة المحافظ 
    if data == "engraved_wallet":
        # عرض قائمة الألوان المطلوبة
        show_submenu(update, context, engraved_wallet_submenu, "محافظ محفورة بالاسم", back_callback="main_menu")
        return 
    
    # 2. معالجة اختيار اللون: يتم التعامل معها في ConversationHandler
    if data in [item["callback"] for item in engraved_wallet_submenu]:
        return 

    # 3. معالجة فتح القوائم الفرعية المتداخلة (Sawany, Taarat, ...)
    if data in ["sawany", "taarat", "haram", "doro3", "aqlam", "mugat"]:
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus[data], clean_title)
        return
        
    # 4. معالجة القوائم الفرعية التي تعرض المنتجات مباشرة (Bsamat, Wedding_Tissues, Abajorat)
    if data in ["bsamat", "wedding_tissues", "abajorat"]:
        product_list = all_submenus[data]
        show_product_page(update, data, product_list, is_direct_list=True)
        return

    # 5. معالجة ضغط زر المنتج للذهاب لصفحة الشراء
    if data in product_to_submenu_map:
        parent_key = product_to_submenu_map[data]
        
        # البحث عن بيانات المنتج (سواء كان قائمة متداخلة أو منتج نهائي)
        product_data = None
        for submenu_list in all_submenus.values():
             if isinstance(submenu_list, list):
                 for item in submenu_list:
                     if item.get("callback") == data: # قائمة متداخلة (مثل sawany_akerik)
                         product_data = item
                         break
                     if 'items' in item:
                         product_data = next((sub_item for sub_item in item['items'] if sub_item["callback"] == data), None) # منتج نهائي
                     if product_data:
                         break
                 if product_data:
                     break
        
        if product_data:
            # إذا كان العنصر يحتوي على 'items'، فهذا يعني أنه قائمة فرعية (مثل 'صواني اكليريك')
            if 'items' in product_data:
                show_product_page(update, data, product_data)
            else:
                # هذا منتج نهائي فردي (غير المحافظ)
                show_product_page(update, data, {'label': product_data['label'], 'description': product_data['description'], 'image': product_data['image']}, is_direct_list=False)

        else:
            query.answer(text="عذراً، لم يتم العثور على بيانات المنتج.", show_alert=True)
            
        return

    # 6. حالة زر الشراء (المنتجات العادية)
    if data.startswith("buy_"):
        product_key = data.replace("buy_", "")
        product_data = None
        
        # ... (منطق البحث عن بيانات المنتج كما هو في الكود السابق)
        for submenu in all_submenus.values():
            if isinstance(submenu, list):
                for item in submenu:
                    if item.get("callback") == product_key and 'items' not in item:
                        product_data = item
                        break
                    if 'items' in item:
                        for sub_item in item['items']:
                            if sub_item.get("callback") == product_key:
                                product_data = sub_item
                                break
                    if product_data:
                        break
                if product_data:
                    break
        
        if not product_data:
            query.answer(text="عذراً، لم يتم العثور على بيانات المنتج.", show_alert=True)
            return
            
        user_info = query.from_user
        
        # تكوين نص الرسالة الذي سيُفتح في واتساب
        message_body = (
            f"🔔 *طلب شراء جديد من بوت تليجرام* 🔔\n"
            f"المنتج: {product_data['label']}\n"
            f"الكود: {product_key}\n"
            f"العميل: {user_info.first_name}\n"
            f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
            f"🔗 رابط صورة المنتج: {product_data['image']}\n" 
            f"رابط التواصل عبر تليجرام: tg://user?id={user_info.id}"
        )
        
        encoded_text = quote_plus(message_body)
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
        
        query.answer(text="سيتم فتح تطبيق واتساب الآن لإرسال الطلب.", show_alert=False)

        keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            query.message.delete()
        except Exception:
            pass

        context.bot.send_message(
            chat_id=query.message.chat_id, 
            text=f"شكراً لطلبك! لإنهاء عملية الشراء، اضغط على الزر التالي لإرسال تفاصيل الطلب:", 
            reply_markup=reply_markup
        )
        
        return


# --------------------
# 3. إعداد البوت 
# --------------------
def main():
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN) في بيئة العمل. يرجى التأكد من تعيينه.")
        return
    
    if WHATSAPP_NUMBER == "201288846355":
        print("⚠️ يرجى استبدال WHATSAPP_NUMBER برقمك الحقيقي.")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # 🛑 تعريف مُعالج المحادثة لـ "محافظ محفورة بالاسم" - (تم تعديل الـ fallbacks)
    engraved_wallet_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                prompt_for_name, 
                pattern='^(' + '|'.join([item['callback'] for item in engraved_wallet_submenu]) + ')$'
            )
        ],
        states={
            # الحالة: استقبال الرسالة النصية (الاسم المطلوب حفره)
            GET_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_name_and_prepare_whatsapp),
            ],
        },
        fallbacks=[
            CommandHandler('start', start), # في حالة أرسل /start خلال المحادثة
            # 🛑 هذا هو معالج زر الرجوع الذي كان يحتاج للنقل هنا
            CallbackQueryHandler(back_to_wallets_color, pattern='^back_to_wallets_color$'),
            # معالج الأزرار الأخرى التي قد يضغطها المستخدم بالخطأ خلال المحادثة
            CallbackQueryHandler(button)
        ]
    )

    # إضافة مُعالج المحادثة أولاً
    dp.add_handler(engraved_wallet_handler)
    
    # إضافة معالجات الأوامر والأزرار الأخرى
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()