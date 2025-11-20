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
GET_NAMES = 5       # حالة كتابة الأسماء (عامة للصواني/الطارات/البصمات/المناديل)
GET_DATE = 6        # حالة كتابة التاريخ (عامة للصواني/الطارات/البصمات/المناديل)

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
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/475773348_986832329974720_6197915277469223378_n.jpg?stp=dst-jpg_s720x720_tt6&_nc_cat=107&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=KrebndL4u2oQ7kNvwH3smA2&_nc_oc=AdkT6T_o5SpJKdr9FQ5OhX2vuI5Cp3WjQl0pV9vRotIn9csOIX1DX-I9dC3FpvlBLJM&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=JFYgN-MxG5oy8y3q9Os6Ew&oh=00_AfhJxajOEm9owiAqd00_zEZ4Hy4qzT7DYATV6p4tWdRxeA&oe=6923BE1B", 
        "description": "قلم تاتش معدن عالي الجودة ومناسب للحفر بالليزر."
    },
    {
        "label": "قلم تاتش مضئ", 
        "callback": "aqlam_luminous", 
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/489809156_1164483322357054_6286791651911010777_n.jpg?stp=dst-jpg_s590x590_tt6&_nc_cat=107&ccb=1-7&_nc_sid=833d8c&_nc_ohc=ELb9pciSoD0Q7kNvwG_rdLE&_nc_oc=AdkDWLOZBcjZp9AbNO2Fs-zK-suPtGc1D-KC3JP7NlzhwgJB3WZeGQQfCQIsfxZgvrg&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=U5_JMOw_cSsgrQQLv77j7g&oh=00_Afg-wJrTmoGZo5m1kVVh2IU0227UQ7pUtKSjRx_YEFoGWg&oe=6923B3BA", 
        "description": "قلم تاتش مضئ بتقنية متطورة ومناسب للحفر بالليزر."
    }
]

# --- القوائم المتداخلة (مختصرة لأجل الإيجاز) ---
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
    {
        "label": "طارات اكليريك", "callback": "taarat_akerik", "items": [
             {"label": "طارة اكليريك موديل 1", "callback": "taarat_akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة اكليريك موديل 1"},
             {"label": "طارة اكليريك موديل 2", "callback": "taarat_akerik_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة اكليريك موديل 2"}
        ]
    },
    {
        "label": "طارات خشب", "callback": "taarat_khashab", "items": [
            {"label": "طارة خشب موديل 1", "callback": "taarat_khashab_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة خشب موديل 1"},
            {"label": "طارة خشب موديل 2", "callback": "taarat_khashab_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة خشب موديل 2"}
        ]
    }
]
haram_submenu = [
    {
        "label": "هرم مكتب اكليريك", "callback": "haram_akerik", "items": [
             {"label": "هرم اكليريك موديل 1", "callback": "haram_akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم اكليريك موديل 1"},
             {"label": "هرم اكليريك موديل 2", "callback": "haram_akerik_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم اكليريك موديل 2"}
        ]
    }
]
doro3_submenu = [
    {
        "label": "دروع اكليريك", "callback": "doro3_akerik", "items": [
             {"label": "درع اكليريك موديل 1", "callback": "doro3_akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع اكليريك موديل 1"},
             {"label": "درع اكليريك موديل 2", "callback": "doro3_akerik_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع اكليريك موديل 2"}
        ]
    }
]
mugat_submenu = [
    {
        "label": "مج ابيض", "callback": "mugat_white", "items": [
             {"label": "مج ابيض موديل 1", "callback": "mugat_white_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج ابيض موديل 1"},
             {"label": "مج ابيض موديل 2", "callback": "mugat_white_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج ابيض موديل 2"}
        ]
    }
]


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
    "katb_kitab_box": katb_kitab_box_submenu,
    "abajorat": abajorat_submenu,
    "engraved_wallet": engraved_wallet_submenu
}

# بناء خريطة المنتجات
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box"]: 
        for product in submenu_list:
            product_to_submenu_map[product["callback"]] = menu_key
    else:
        for item in submenu_list:
            product_to_submenu_map[item["callback"]] = menu_key 
            if 'items' in item:
                for sub_item in item['items']:
                    product_to_submenu_map[sub_item["callback"]] = item["callback"] 


# تحديد جميع مفاتيح المنتجات التي تتطلب محادثة (أسماء وتاريخ)
NAMES_DATE_PRODUCT_KEYS = []
for item in bsamat_submenu:
    NAMES_DATE_PRODUCT_KEYS.append(item['callback'])
for item in wedding_tissues_submenu:
    NAMES_DATE_PRODUCT_KEYS.append(item['callback'])
for submenu in [sawany_submenu, taarat_submenu]:
    for item in submenu:
        if 'items' in item:
            for sub_item in item['items']:
                NAMES_DATE_PRODUCT_KEYS.append(sub_item['callback'])


# --------------------
# 3. الدوال الرئيسية والمساعدة
# --------------------

def start(update, context):
    query = update.callback_query
    if context.user_data.get('state'):
        context.user_data.clear()
        context.user_data['state'] = None
        
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

def show_submenu(update, context, submenu_list, title, back_callback="main_menu"):
    query = update.callback_query
    
    if query:
        query.answer()
        try:
            query.message.delete()
        except Exception:
            pass 
        
    keyboard = []
    for item in submenu_list:
        keyboard.append([InlineKeyboardButton(item["label"], callback_data=item["callback"])])

    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = f"✅ *{title}*:\n\nمن فضلك اختر طلبك من القائمة:"

    update.effective_chat.send_message(
        text=message_text, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
        
def find_product_by_callback(callback_key):
    for submenu_list in all_submenus.values():
        product = next((item for item in submenu_list if item.get("callback") == callback_key), None)
        if product: return product
        for item in submenu_list:
            if 'items' in item:
                product = next((sub_item for sub_item in item['items'] if sub_item.get("callback") == callback_key), None)
                if product: return product
    return None

def show_product_page(update, product_callback_data, product_data, is_direct_list=False):
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
    
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "aqlam"]:
        back_callback = "main_menu"
        back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
    else:
        back_callback = product_to_submenu_map.get(product_callback_data, "main_menu")
        
        if back_callback in ["sawany", "taarat", "haram", "doro3", "mugat"]:
             back_callback = product_to_submenu_map.get(product_callback_data, "main_menu")
             back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
        else:
             back_callback = back_callback
             back_text = "🔙 اضغط للرجوع إلى القائمة الفرعية"


    back_keyboard = [[InlineKeyboardButton(back_text, callback_data=back_callback)]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
        
    update.effective_message.bot.send_message(
        chat_id=update.effective_chat.id,
        text="---", 
        reply_markup=back_reply_markup
    )


# ------------------------------------
# دوال المحافظ
# ------------------------------------

def back_to_wallets_color(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    try:
        query.message.delete()
    except Exception:
        pass
    show_submenu(update, context, engraved_wallet_submenu, "محافظ محفورة بالاسم", back_callback="main_menu")
    return ConversationHandler.END 

def prompt_for_name(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    selected_wallet_data = next((item for item in engraved_wallet_submenu if item["callback"] == data), None)
    
    if not selected_wallet_data:
        query.answer("خطأ في بيانات المنتج.", show_alert=True)
        return ConversationHandler.END

    context.user_data['wallet_data'] = selected_wallet_data
    context.user_data['state'] = GET_WALLET_NAME
    
    try:
        query.message.delete() 
    except Exception:
        pass
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_wallets_color")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    caption_text = (
        f"**اختيارك: {selected_wallet_data['label']}**\n\n"
        f"اكتب الاسم المراد حفره علي المحفظة"
    )
    
    update.effective_chat.bot.send_photo(
        chat_id=update.effective_chat.id, 
        photo=selected_wallet_data['image'], 
        caption=caption_text, 
        reply_markup=back_reply_markup, 
        parse_mode="Markdown"
    )
    
    return GET_WALLET_NAME

def receive_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    product_data = context.user_data.get('wallet_data')
    if not product_data:
        update.effective_chat.send_message("عفواً، حدث خطأ. يرجى البدء من القائمة الرئيسية.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
    user_info = update.message.from_user
    product_label = product_data['label']
    try:
        color = product_label.split('محفظة ', 1)[1].strip() 
        wallet_type = "محفظة سافوكس الاصلية التقيلة" 
    except IndexError:
        color = product_label
        wallet_type = product_label
    message_body = (f"🔔 *طلب شراء جديد (محافظ)* 🔔\n\nالمنتج: {wallet_type}\nاللون: {color}\n الاسم المطلوب حفره: *{engraving_name}*\nالكود: {product_data['callback']}\n\nاسم العميل: {user_info.first_name}\nاليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n🔗 صورة: {product_data['image']}")
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)], [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text=f"شكراً لك! سيتم حفر اسم **{engraving_name}** على **{product_data['label']}**.\n\nلإتمام الطلب، اضغط على الزر التالي:", reply_markup=reply_markup, parse_mode="Markdown")
    context.user_data.clear()
    return ConversationHandler.END

# ------------------------------------
# دوال الأقلام
# ------------------------------------

def back_to_pen_types(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    try:
        query.message.delete()
    except Exception:
        pass
    
    show_product_page(update, "aqlam", aqlam_submenu, is_direct_list=True)
    return ConversationHandler.END 

def prompt_for_pen_name(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    product_callback = data.replace("buy_", "")
    
    selected_pen_data = next((item for item in aqlam_submenu if item["callback"] == product_callback), None)
    context.user_data['pen_data'] = selected_pen_data
    context.user_data['state'] = GET_PEN_NAME
    try:
        query.message.delete()
    except Exception:
        pass
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_pen_types")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    caption_text = (f"**اختيارك: {selected_pen_data['label']}**\n\nاكتب الاسم المراد حفره علي القلم او اضغط زر رجوع للعودة للقائمة السابقة")
    
    update.effective_chat.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_pen_data['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    return GET_PEN_NAME

def receive_pen_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    product_data = context.user_data.get('pen_data')
    if not product_data:
        update.effective_chat.send_message("عفواً، حدث خطأ. يرجى البدء من القائمة الرئيسية.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
    user_info = update.message.from_user
    message_body = (f"🔔 *طلب شراء جديد (اقلام)* 🔔\n\nالمنتج: {product_data['label']}\n الاسم المطلوب حفره: *{engraving_name}*\nالكود: {product_data['callback']}\n\nاسم العميل: {user_info.first_name}\nاليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n🔗 صورة: {product_data['image']}")
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)], [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text=f"شكراً لك! سيتم حفر اسم **{engraving_name}** على **{product_data['label']}**.\n\nلإتمام الطلب، اضغط على الزر التالي:", reply_markup=reply_markup, parse_mode="Markdown")
    context.user_data.clear()
    return ConversationHandler.END

# ------------------------------------
# دوال بوكس كتب الكتاب
# ------------------------------------

def start_box_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    selected_box = next((item for item in katb_kitab_box_submenu if item["callback"] == product_callback), None)
    if not selected_box:
         query.answer("خطأ في العثور على المنتج", show_alert=True)
         return ConversationHandler.END
    context.user_data['box_product'] = selected_box
    context.user_data['state'] = GET_BOX_COLOR
    keyboard = [[InlineKeyboardButton("اسود في دهبي", callback_data="color_black_gold")], [InlineKeyboardButton("ابيض في دهبي", callback_data="color_white_gold")], [InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query.message.delete()
    except:
        pass
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ **{selected_box['label']}**\n\nمن فضلك اختر **لون البوكس**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_BOX_COLOR

def save_box_color_ask_names(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    if data == "katb_kitab_box":
        show_product_page(update, "katb_kitab_box", katb_kitab_box_submenu, is_direct_list=True)
        context.user_data.clear()
        return ConversationHandler.END
    color_name = "أسود في ذهبي" if data == "color_black_gold" else "أبيض في ذهبي"
    context.user_data['box_color'] = color_name
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_box_color")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"لقد اخترت اللون: **{color_name}**\n\nمن فضلك الآن **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_BOX_NAMES

def back_to_box_color(update, context):
    query = update.callback_query
    query.answer()
    selected_box = context.user_data.get('box_product')
    if not selected_box:
        start(update, context)
        return ConversationHandler.END
    keyboard = [[InlineKeyboardButton("اسود في دهبي", callback_data="color_black_gold")], [InlineKeyboardButton("ابيض في دهبي", callback_data="color_white_gold")], [InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query.message.delete()
    except:
        pass
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ **{selected_box['label']}**\n\nمن فضلك اختر **لون البوكس**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_BOX_COLOR

def receive_box_names_and_finish(update, context):
    names_text = update.message.text
    product_data = context.user_data.get('box_product')
    color_name = context.user_data.get('box_color')
    if not product_data or not color_name:
        update.effective_chat.send_message("حدث خطأ.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
    user_info = update.message.from_user
    message_body = (f"🔔 *طلب شراء جديد (بوكس كتب الكتاب)* 🔔\n\nالمنتج: {product_data['label']}\nاللون: {color_name}\nالأسماء: *{names_text}*\nالكود: {product_data['callback']}\n\nاسم العميل: {user_info.first_name}\n🔗 صورة: {product_data['image']}")
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)], [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text=f"شكراً لك! البيانات:\n\n📦 المنتج: {product_data['label']}\n🎨 اللون: {color_name}\n✍️ الأسماء: {names_text}\n\nلإتمام الطلب، اضغط على الزر التالي:", reply_markup=reply_markup)
    context.user_data.clear()
    return ConversationHandler.END


# ------------------------------------
# دوال عامة (أسماء وتاريخ) لـ (صواني، طارات، بصمات، مناديل)
# ------------------------------------

def start_names_date_purchase(update, context):
    query = update.callback_query
    query.answer()
    product_callback = query.data.replace("buy_", "")

    selected_product = find_product_by_callback(product_callback) 

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['names_date_product'] = selected_product
    context.user_data['state'] = GET_NAMES 

    back_key = product_to_submenu_map.get(product_callback, "main_menu")
    final_back_key = product_to_submenu_map.get(product_callback, "main_menu")
    context.user_data['names_date_back_callback'] = final_back_key


    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=final_back_key)]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    try:
        query.message.delete()
    except:
        pass

    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=selected_product['image'],
        caption=f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_NAMES

def save_names_ask_date(update, context):
    names = update.message.text
    context.user_data['names'] = names

    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_names_input")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_DATE

def back_to_names_input(update, context):
    query = update.callback_query
    query.answer()
    
    selected_product = context.user_data.get('names_date_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END

    back_key = context.user_data.get('names_date_back_callback')
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_key)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    try:
        query.message.delete()
    except:
        pass

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_NAMES


def receive_date_and_finish_whatsapp(update, context):
    date_text = update.message.text
    product_data = context.user_data.get('names_date_product')
    names_text = context.user_data.get('names')

    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user

    message_body = (
        f"🔔 *طلب شراء جديد (منتج حفر أسماء وتاريخ)* 🔔\n\n"
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

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n📦 المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )

    context.user_data.clear()
    return ConversationHandler.END


# ------------------------------------
# الدالة الرئيسية لمعالجة ضغطات الأزرار
# ------------------------------------
def button(update, context):
    query = update.callback_query
    data = query.data

    # 1. حالة العودة للقائمة الرئيسية
    if data == "main_menu":
        start(update, context)
        return

    # 2. معالجة فتح قائمة المحافظ 
    if data == "engraved_wallet":
        show_submenu(update, context, engraved_wallet_submenu, "محافظ محفورة بالاسم", back_callback="main_menu")
        return 
        
    # 3. معالجة فتح قائمة الأقلام وبقية القوائم المباشرة (عرض صفحة المنتجات)
    if data in ["aqlam", "bsamat", "wedding_tissues", "abajorat", "katb_kitab_box"]:
        product_list = all_submenus[data]
        show_product_page(update, data, product_list, is_direct_list=True)
        return 
        
    # 4. معالجة اختيار المنتج (محفظة) - الدخول في حالة المحادثة
    if data in [item["callback"] for item in engraved_wallet_submenu]:
        return prompt_for_name(update, context) 
    
    # 5. معالجة فتح القوائم الفرعية المتداخلة (Sawany, Taarat, Haram, Doro3, Mugat)
    if data in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus[data], clean_title, back_callback="main_menu") 
        return
        
    # 6. معالجة ضغط زر المنتج للذهاب لصفحة الشراء (القوائم المتداخلة: صواني اكليريك/خشب، طارات اكليريك/خشب، أهرامات، دروع، مجات)
    if data in product_to_submenu_map:
        product_data = None
        # نبحث عن بيانات القائمة (المستوى الأول من القائمة المتداخلة)
        for submenu_key, submenu_list in all_submenus.items():
            item = next((i for i in submenu_list if i.get("callback") == data), None)
            if item:
                 product_data = item
                 break
        
        if product_data:
            show_product_page(update, data, product_data)
            return
        else:
            query.answer(text="عذراً، لم يتم العثور على بيانات المنتج.", show_alert=True)
            return

    # 7. حالة زر الشراء (المنتجات العادية والمنتجات التي تحتاج محادثة)
    if data.startswith("buy_"):
        product_key = data.replace("buy_", "")
        
        # 🟢 التحقق من المنتجات التي تتطلب محادثة وبدء المحادثة
        if product_key in NAMES_DATE_PRODUCT_KEYS:
            query.answer() 
            return start_names_date_purchase(update, context)
            
        elif product_key.startswith('aqlam_'):
            query.answer()
            return prompt_for_pen_name(update, context)
            
        elif product_key.startswith('box_m'):
            query.answer()
            return start_box_purchase(update, context)
        
        # 8. إذا لم يكن منتجاً يحتاج إلى محادثة (مثل أباجورة، هرم، درع، مج...)
        
        product_data = find_product_by_callback(product_key)
        
        if not product_data:
            query.answer(text="عذراً، لم يتم العثور على بيانات المنتج.", show_alert=True)
            return
            
        # إرسال طلب واتساب عادي (لأباجورات، أهرام، دروع، مجات، ومستلزمات السبلميشن إن وجدت)
        user_info = query.from_user
        message_body = (f"🔔 *طلب شراء جديد*\nالمنتج: {product_data['label']}\nالكود: {product_key}\nالعميل: {user_info.first_name}\n🔗 صورة: {product_data['image']}")
        encoded_text = quote_plus(message_body)
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
        
        query.answer(text="سيتم فتح واتساب...", show_alert=False)
        keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            query.message.delete()
        except Exception:
            pass
        context.bot.send_message(chat_id=query.message.chat_id, text=f"شكراً لطلبك! اضغط أدناه للإرسال:", reply_markup=reply_markup)
        return


# --------------------
# 4. إعداد البوت والتشغيل (تم تحديثه لقراءة التوكن من بيئة العمل)
# --------------------
def main():
    # 🛑 تم التحديث: قراءة التوكن من متغير البيئة المسمى 'TELEGRAM_BOT_TOKEN'
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") 
    
    if not TOKEN: 
         print("❌ فشل التشغيل: يرجى التأكد من تعيين توكن البوت في متغير البيئة المسمى 'TELEGRAM_BOT_TOKEN'.")
         # يمكنك إضافة سطر الخروج هذا إذا كنت تريد أن يتوقف البرنامج فوراً
         # return 
         # لكن سنستمر لطباعة أي خطأ آخر قد يظهر
         return

    # 💡 إذا ظهر خطأ بعد هذه النقطة، فيجب أن يكون مشكلة في الاتصال بالشبكة أو في الكود نفسه.
    try:
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher
    except telegram.error.InvalidToken:
        print("❌ فشل التشغيل: رمز التوكن غير صحيح. يرجى مراجعته مع BotFather.")
        return
    except Exception as e:
        print(f"❌ خطأ غير متوقع عند إنشاء Updater: {e}")
        return
    
    # 1. محافظ (ConversationHandler)
    engraved_wallet_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prompt_for_name, pattern='^(' + '|'.join([item['callback'] for item in engraved_wallet_submenu]) + ')$')],
        states={GET_WALLET_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_name_and_prepare_whatsapp)]},
        fallbacks=[CommandHandler('start', start), CallbackQueryHandler(back_to_wallets_color, pattern='^back_to_wallets_color$'), CallbackQueryHandler(button)]
    )

    # 2. اقلام (ConversationHandler)
    pen_callbacks = [item['callback'] for item in aqlam_submenu] 
    buy_pen_callbacks_pattern = '^buy_(' + '|'.join(pen_callbacks) + ')$'
    
    engraved_pen_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prompt_for_pen_name, pattern=buy_pen_callbacks_pattern)],
        states={GET_PEN_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp)]},
        fallbacks=[CommandHandler('start', start), CallbackQueryHandler(back_to_pen_types, pattern='^back_to_pen_types$'), CallbackQueryHandler(button)]
    )

    # 3. بوكس كتب الكتاب (ConversationHandler)
    box_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_box_purchase, pattern='^buy_box_.*')],
        states={
            GET_BOX_COLOR: [CallbackQueryHandler(save_box_color_ask_names, pattern='^color_.*|katb_kitab_box$')],
            GET_BOX_NAMES: [MessageHandler(Filters.text & ~Filters.command, receive_box_names_and_finish)]
        },
        fallbacks=[CommandHandler('start', start), CallbackQueryHandler(back_to_box_color, pattern='^back_to_box_color$'), CallbackQueryHandler(button)]
    )

    # 4. محادثة عامة للأسماء والتاريخ (لجميع الصواني، الطارات، البصامات، المناديل)
    buy_names_date_pattern = '^buy_(' + '|'.join(NAMES_DATE_PRODUCT_KEYS) + ')$'
    
    names_date_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_names_date_purchase, pattern=buy_names_date_pattern)],
        states={
            GET_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_names_ask_date),
                CallbackQueryHandler(button, pattern='^(' + '|'.join(product_to_submenu_map.values()) + ')$') 
            ],
            GET_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_date_and_finish_whatsapp)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_names_input, pattern='^back_to_names_input$'), 
            CallbackQueryHandler(button)
        ]
    )

    # إضافة كل محادثات الشراء أولاً
    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler)
    dp.add_handler(box_handler)
    dp.add_handler(names_date_handler)
    
    # إضافة الأوامر العامة ومعالج الأزرار كمعالج عام في النهاية
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 البوت يعمل الآن...")
    
    # تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()