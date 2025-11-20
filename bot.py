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
GET_TRAY_NAMES = 5  # حالة كتابة الأسماء للصينية الاكليريك
GET_TRAY_DATE = 6   # حالة كتابة التاريخ للصينية الاكليريك
GET_KHASHAB_TRAY_NAMES = 7 # حالة كتابة الأسماء لصينية الخشب
GET_KHASHAB_TRAY_DATE = 8  # حالة كتابة التاريخ لصينية الخشب
# 🆕 حالات الطارات
GET_AKRILIK_TAARAT_NAMES = 9 # حالة أسماء طارات اكليريك
GET_AKRILIK_TAARAT_DATE = 10 # حالة تاريخ طارات اكليريك
GET_KHASHAB_TAARAT_NAMES = 11 # حالة أسماء طارات خشب
GET_KHASHAB_TAARAT_DATE = 12 # حالة تاريخ طارات خشب


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
    },
    {
        "label": "هرم مكتب معدن بديل", "callback": "haram_metal", "items": [
             {"label": "هرم معدن موديل 1", "callback": "haram_metal_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم معدن موديل 1"},
             {"label": "هرم معدن موديل 2", "callback": "haram_metal_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم معدن موديل 2"}
        ]
    },
    {
        "label": "هرم مكتب خشب", "callback": "haram_khashab", "items": [
             {"label": "هرم خشب موديل 1", "callback": "haram_khashab_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم خشب موديل 1"},
             {"label": "هرم خشب موديل 2", "callback": "haram_khashab_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم خشب موديل 2"}
        ]
    }
]
doro3_submenu = [
    {
        "label": "دروع اكليريك", "callback": "doro3_akerik", "items": [
             {"label": "درع اكليريك موديل 1", "callback": "doro3_akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع اكليريك موديل 1"},
             {"label": "درع اكليريك موديل 2", "callback": "doro3_akerik_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع اكليريك موديل 2"}
        ]
    },
    {
        "label": "دروع معدن بديل", "callback": "doro3_metal", "items": [
             {"label": "درع معدن موديل 1", "callback": "doro3_metal_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع معدن موديل 1"},
             {"label": "درع معدن موديل 2", "callback": "doro3_metal_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع معدن موديل 2"}
        ]
    },
    {
        "label": "دروع قطيفة", "callback": "doro3_qatifah", "items": [
             {"label": "درع قطيفة موديل 1", "callback": "doro3_qatifah_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع قطيفة موديل 1"},
             {"label": "درع قطيفة موديل 2", "callback": "doro3_qatifah_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع قطيفة موديل 2"}
        ]
    },
    {
        "label": "دروع خشب", "callback": "doro3_khashab", "items": [
             {"label": "درع خشب موديل 1", "callback": "doro3_khashab_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع خشب موديل 1"},
             {"label": "درع خشب موديل 2", "callback": "doro3_khashab_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع خشب موديل 2"}
        ]
    }
]
mugat_submenu = [
    {
        "label": "مج ابيض", "callback": "mugat_white", "items": [
             {"label": "مج ابيض موديل 1", "callback": "mugat_white_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج ابيض موديل 1"},
             {"label": "مج ابيض موديل 2", "callback": "mugat_white_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج ابيض موديل 2"}
        ]
    },
    {
        "label": "مج سحري", "callback": "mugat_magic", "items": [
             {"label": "مج سحري موديل 1", "callback": "mugat_magic_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج سحري موديل 1"},
             {"label": "مج سحري موديل 2", "callback": "mugat_magic_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج سحري موديل 2"}
        ]
    },
    {
        "label": "مج ديجتال", "callback": "mugat_digital", "items": [
             {"label": "مج ديجتال موديل 1", "callback": "mugat_digital_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج ديجتال موديل 1"},
             {"label": "مج ديجتال موديل 2", "callback": "mugat_digital_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج ديجتال موديل 2"}
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

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box"]: 
        # للقوائم المباشرة، نضيف كل منتج مباشرة
        for product in submenu_list:
            product_to_submenu_map[product["callback"]] = menu_key
    else:
        # للقوائم المتداخلة (sawany, taarat, ...)
        for item in submenu_list:
            # المستوى الأول (مثل: sawany_akerik)
            product_to_submenu_map[item["callback"]] = menu_key 
            if 'items' in item:
                for sub_item in item['items']:
                    # المستوى الثاني (مثل: akerik_m1)
                    product_to_submenu_map[sub_item["callback"]] = item["callback"] 


# --------------------
# 3. الدوال الرئيسية والمساعدة
# --------------------

def start(update, context):
    query = update.callback_query
    # إنهاء أي محادثة جارية عند استخدام /start أو العودة للقائمة الرئيسية
    if context.user_data.get('state'):
        context.user_data.clear()
        context.user_data['state'] = None
        
    if query:
        query.answer()
    
    user_name = update.effective_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختر طلبك من القائمة:"
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in main_menu]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # منطق عرض القائمة الرئيسية (حذف الرسالة القديمة وإرسال رسالة جديدة)
    if query:
        try:
            query.message.delete()
        except Exception:
            pass 
        
        update.effective_chat.send_message(greeting_text, reply_markup=reply_markup)
    else:
        update.effective_message.reply_text(greeting_text, reply_markup=reply_markup)

# 💡 دالة عرض القائمة الفرعية 
def show_submenu(update, context, submenu_list, title, back_callback="main_menu"):
    query = update.callback_query
    
    if query:
        query.answer()
        # نحذف الرسالة القديمة ونرسل رسالة جديدة بالكامل
        try:
            query.message.delete()
        except Exception:
            pass 
        
    # بناء الأزرار (كل زر في صف منفصل)
    keyboard = []
    for item in submenu_list:
        keyboard.append([InlineKeyboardButton(item["label"], callback_data=item["callback"])])

    # إضافة زر الرجوع
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)])
    
    # إنشاء لوحة المفاتيح النهائية
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = f"✅ *{title}*:\n\nمن فضلك اختر طلبك من القائمة:"

    # إرسال رسالة جديدة
    update.effective_chat.send_message(
        text=message_text, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
        

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

    # نحذف رسالة القائمة السابقة
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
    
    # تحديد زر الرجوع
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box"]:
        back_callback = "main_menu"
        back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
    # قائمة "صواني شبكة"
    elif product_callback_data in ["sawany_akerik", "sawany_khashab"]:
        back_callback = "sawany" # العودة لقائمة "صواني شبكة"
        back_text = "🔙 اضغط للرجوع إلى القائمة الفرعية"
    # 🆕 قائمة "طارات"
    elif product_callback_data in ["taarat_akerik", "taarat_khashab"]: 
        back_callback = "taarat" # العودة لقائمة "طارات خطوبة وكتب الكتاب"
        back_text = "🔙 اضغط للرجوع إلى القائمة الفرعية"
    else:
        back_callback = product_to_submenu_map.get(product_callback_data, "main_menu")
        
        if back_callback in ["sawany", "taarat", "haram", "doro3", "mugat"]:
             back_callback = back_callback
             back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
        elif back_callback in ["engraved_wallet", "aqlam"]:
             back_callback = back_callback
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
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in engraved_wallet_submenu]
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ *محافظ محفورة بالاسم*:\n\nمن فضلك اختر اللون المطلوب:", reply_markup=reply_markup, parse_mode="Markdown")
    return ConversationHandler.END 

def prompt_for_name(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    selected_wallet_data = next((item for item in engraved_wallet_submenu if item["callback"] == data), None)
    context.user_data['wallet_data'] = selected_wallet_data
    context.user_data['state'] = GET_WALLET_NAME
    try:
        query.message.delete()
    except Exception:
        pass
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_wallets_color")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    caption_text = (f"**اختيارك: {selected_wallet_data['label']}**\n\n من فضلك، **اكتب الاسم الذي تريد حفره** على المحفظة في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة.\nأو اضغط زر الرجوع لتغيير اللون.")
    update.effective_chat.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_wallet_data['image'], caption=caption_text, reply_markup=back_reply_markup, parse_mode="Markdown")
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
    message_body = (f"🔔 *طلب شراء جديد (محافظ)* 🔔\n\nالمنتج: {wallet_type}\nاللون: {color}\n الاسم المطلوب حفره: *{engraving_name}*\nالكود: {product_data['callback']}\n\nاسم العميل: {user_info.first_name}\nاليوزر: @{user_info.username}\n🔗 صورة: {product_data['image']}")
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
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in aqlam_submenu]
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ *اقلام محفورة بالاسم*:\n\nمن فضلك اختر نوع القلم المطلوب:", reply_markup=reply_markup, parse_mode="Markdown")
    return ConversationHandler.END 

def prompt_for_pen_name(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    selected_pen_data = next((item for item in aqlam_submenu if item["callback"] == data), None)
    context.user_data['pen_data'] = selected_pen_data
    context.user_data['state'] = GET_PEN_NAME
    try:
        query.message.delete()
    except Exception:
        pass
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_pen_types")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    caption_text = (f"**اختيارك: {selected_pen_data['label']}**\n\nمن فضلك، **اكتب الاسم الذي تريد حفره** على القلم في رسالة نصية بالأسفل.او اضغط زر رجوع للعودة الي القائمة السابقة\nأو اضغط زر الرجوع لتغيير نوع القلم.")
    update.effective_chat.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_pen_data['image'], caption=caption_text, reply_markup=back_reply_markup, parse_mode="Markdown")
    return GET_PEN_NAME

def receive_pen_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    product_data = context.user_data.get('pen_data')
    if not product_data:
        update.effective_chat.send_message("عفواً، حدث خطأ. يرجى البدء من القائمة الرئيسية.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
    user_info = update.message.from_user
    message_body = (f"🔔 *طلب شراء جديد (اقلام)* 🔔\n\nالمنتج: {product_data['label']}\n الاسم المطلوب حفره: *{engraving_name}*\nالكود: {product_data['callback']}\n\nاسم العميل: {user_info.first_name}\nاليوزر: @{user_info.username}\n🔗 صورة: {product_data['image']}")
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
# دوال صواني شبكة اكليريك (Acrylic Trays Handlers)
# ------------------------------------

def start_tray_purchase(update, context):
    """
    الخطوة 1: التقاط زر شراء للصينية وطلب الأسماء
    """
    query = update.callback_query
    query.answer()
    data = query.data  # مثال: buy_akerik_m1
    product_callback = data.replace("buy_", "")

    # البحث في قائمة صواني اكليريك (sawany_akerik)
    items_list = sawany_submenu[0]['items'] 
    selected_tray = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_tray:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['tray_product'] = selected_tray
    context.user_data['state'] = GET_TRAY_NAMES

    # زر رجوع يعيدنا لصفحة عرض منتجات الصواني الاكليريك
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_akerik")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_tray['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
    try:
        # ⚠️ محاولة إرسال الصورة
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_tray['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        # 💡 في حالة فشل إرسال الصورة (قد يكون الرابط غير صالح)، نرسل النص فقط ونستمر
        print(f"Error sending photo in start_tray_purchase: {e}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        

    return GET_TRAY_NAMES

def back_to_tray_names(update, context):
    """
    زر رجوع من خطوة التاريخ إلى خطوة الأسماء (اكليريك)
    """
    query = update.callback_query
    query.answer()
    
    selected_tray = context.user_data.get('tray_product')
    if not selected_tray:
        start(update, context)
        return ConversationHandler.END

    # زر رجوع يعيدنا لصفحة المنتجات
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_akerik")]]
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
    return GET_TRAY_NAMES


def save_tray_names_ask_date(update, context):
    """
    الخطوة 2: حفظ الأسماء وطلب التاريخ (اكليريك)
    """
    names = update.message.text
    context.user_data['tray_names'] = names

    # زر رجوع يعيدنا لخطوة الأسماء
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_tray_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_TRAY_DATE

def receive_tray_date_and_finish(update, context):
    """
    الخطوة 3: استلام التاريخ وإرسال الواتساب (اكليريك)
    """
    date_text = update.message.text
    product_data = context.user_data.get('tray_product')
    names_text = context.user_data.get('tray_names')

    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user

    message_body = (
        f"🔔 *طلب شراء جديد (صينية اكليريك)* 🔔\n\n"
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
        text=f"شكراً لك! تفاصيل الطلب:\n\n💍 المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )

    context.user_data.clear()
    return ConversationHandler.END


# ------------------------------------
# دوال صواني شبكة خشب (Khashab Trays Handlers)
# ------------------------------------

def start_khashab_tray_purchase(update, context):
    """
    الخطوة 1: التقاط زر شراء لصينية الخشب وطلب الأسماء
    """
    query = update.callback_query
    query.answer()
    data = query.data  # مثال: buy_khashab_m1
    product_callback = data.replace("buy_", "")

    # البحث في قائمة صواني خشب (sawany_khashab)
    # نبحث داخل الـ items الخاصة بالعنصر الثاني في sawany_submenu (الذي هو الخشب)
    items_list = sawany_submenu[1]['items'] 
    selected_tray = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_tray:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['khashab_tray_product'] = selected_tray
    context.user_data['state'] = GET_KHASHAB_TRAY_NAMES

    # زر رجوع يعيدنا لصفحة عرض منتجات الصواني الخشب
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_khashab")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_tray['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"

    try:
        # ⚠️ محاولة إرسال الصورة
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_tray['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        # 💡 في حالة فشل إرسال الصورة (قد يكون الرابط غير صالح)، نرسل النص فقط ونستمر
        print(f"Error sending photo in start_khashab_tray_purchase: {e}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    return GET_KHASHAB_TRAY_NAMES

def back_to_khashab_tray_names(update, context):
    """
    زر رجوع من خطوة التاريخ إلى خطوة الأسماء (خشب)
    """
    query = update.callback_query
    query.answer()
    
    selected_tray = context.user_data.get('khashab_tray_product')
    if not selected_tray:
        start(update, context)
        return ConversationHandler.END

    # زر رجوع يعيدنا لصفحة المنتجات
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_khashab")]]
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
    return GET_KHASHAB_TRAY_NAMES


def save_khashab_tray_names_ask_date(update, context):
    """
    الخطوة 2: حفظ الأسماء وطلب التاريخ (خشب)
    """
    names = update.message.text
    context.user_data['khashab_tray_names'] = names

    # زر رجوع يعيدنا لخطوة الأسماء
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_khashab_tray_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_KHASHAB_TRAY_DATE

def receive_khashab_tray_date_and_finish(update, context):
    """
    الخطوة 3: استلام التاريخ وإرسال الواتساب (خشب)
    """
    date_text = update.message.text
    product_data = context.user_data.get('khashab_tray_product')
    names_text = context.user_data.get('khashab_tray_names')

    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user

    message_body = (
        f"🔔 *طلب شراء جديد (صينية خشب)* 🔔\n\n"
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
        text=f"شكراً لك! تفاصيل الطلب:\n\n💍 المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )

    context.user_data.clear()
    return ConversationHandler.END


# ------------------------------------
# 🆕 دوال طارات اكليريك (Acrylic Hoops Handlers)
# ------------------------------------

def get_akerik_taarat_items():
    # taarat_submenu[0] is 'طارات اكليريك'
    return taarat_submenu[0]['items']

def start_akerik_taarat_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_taarat_akerik_m1
    product_callback = data.replace("buy_", "")
    
    items_list = get_akerik_taarat_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['taarat_akerik_product'] = selected_product
    context.user_data['state'] = GET_AKRILIK_TAARAT_NAMES

    # زر رجوع يعيدنا لصفحة عرض منتجات طارات اكليريك
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_akerik")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        print(f"Error sending photo in start_akerik_taarat_purchase: {e}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    return GET_AKRILIK_TAARAT_NAMES

def back_to_akerik_taarat_names(update, context):
    query = update.callback_query
    query.answer()
    
    selected_product = context.user_data.get('taarat_akerik_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END

    # زر رجوع يعيدنا لصفحة المنتجات
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_akerik")]]
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
    return GET_AKRILIK_TAARAT_NAMES


def save_akerik_taarat_names_ask_date(update, context):
    names = update.message.text
    context.user_data['taarat_akerik_names'] = names

    # زر رجوع يعيدنا لخطوة الأسماء
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_akerik_taarat_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_AKRILIK_TAARAT_DATE

def receive_akerik_taarat_date_and_finish(update, context):
    date_text = update.message.text
    product_data = context.user_data.get('taarat_akerik_product')
    names_text = context.user_data.get('taarat_akerik_names')

    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user

    message_body = (
        f"🔔 *طلب شراء جديد (طارة اكليريك)* 🔔\n\n"
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
        text=f"شكراً لك! تفاصيل الطلب:\n\n💍 المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )

    context.user_data.clear()
    return ConversationHandler.END

# ------------------------------------
# 🆕 دوال طارات خشب (Wood Hoops Handlers)
# ------------------------------------

def get_khashab_taarat_items():
    # taarat_submenu[1] is 'طارات خشب'
    return taarat_submenu[1]['items']

def start_khashab_taarat_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_taarat_khashab_m1
    product_callback = data.replace("buy_", "")

    items_list = get_khashab_taarat_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['taarat_khashab_product'] = selected_product
    context.user_data['state'] = GET_KHASHAB_TAARAT_NAMES

    # زر رجوع يعيدنا لصفحة عرض منتجات طارات خشب
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_khashab")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        print(f"Error sending photo in start_khashab_taarat_purchase: {e}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    return GET_KHASHAB_TAARAT_NAMES

def back_to_khashab_taarat_names(update, context):
    query = update.callback_query
    query.answer()
    
    selected_product = context.user_data.get('taarat_khashab_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END

    # زر رجوع يعيدنا لصفحة المنتجات
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_khashab")]]
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
    return GET_KHASHAB_TAARAT_NAMES


def save_khashab_taarat_names_ask_date(update, context):
    names = update.message.text
    context.user_data['taarat_khashab_names'] = names

    # زر رجوع يعيدنا لخطوة الأسماء
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_khashab_taarat_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_KHASHAB_TAARAT_DATE

def receive_khashab_taarat_date_and_finish(update, context):
    date_text = update.message.text
    product_data = context.user_data.get('taarat_khashab_product')
    names_text = context.user_data.get('taarat_khashab_names')

    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user

    message_body = (
        f"🔔 *طلب شراء جديد (طارة خشب)* 🔔\n\n"
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
        text=f"شكراً لك! تفاصيل الطلب:\n\n💍 المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
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
        
    # 3. معالجة فتح قائمة الأقلام (محادثة)
    if data == "aqlam":
        show_submenu(update, context, aqlam_submenu, "اقلام محفورة بالاسم", back_callback="main_menu")
        return 
        
    # 4. معالجة اختيار المنتج (سواء محفظة أو قلم)
    if data in [item["callback"] for item in engraved_wallet_submenu]:
        return prompt_for_name(update, context) 
    
    if data in [item["callback"] for item in aqlam_submenu]:
        return prompt_for_pen_name(update, context) 

    # 5. معالجة فتح القوائم الفرعية المتداخلة (Sawany, Taarat, Haram, Doro3, Mugat)
    if data in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus[data], clean_title, back_callback="main_menu") 
        return
        
    # 6. معالجة القوائم الفرعية التي تعرض المنتجات مباشرة (بصمات، مناديل، بوكسات، أباجورات)
    if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box"]:
        product_list = all_submenus[data]
        show_product_page(update, data, product_list, is_direct_list=True)
        return
    
    # 🛑 6-B: معالجة خاصة لزر "صواني شبكة اكليريك" لعرض منتجاتها مباشرة
    if data == "sawany_akerik":
        products = sawany_submenu[0]['items']
        show_product_page(update, "sawany_akerik", products, is_direct_list=True)
        return
    
    # 🛑 6-C: معالجة خاصة لزر "صواني شبكة خشب" لعرض منتجاتها مباشرة
    if data == "sawany_khashab":
        products = sawany_submenu[1]['items']
        show_product_page(update, "sawany_khashab", products, is_direct_list=True)
        return
    
    # 🛑 6-D: 🆕 معالجة خاصة لزر "طارات اكليريك" لعرض منتجاتها مباشرة
    if data == "taarat_akerik":
        products = taarat_submenu[0]['items']
        show_product_page(update, "taarat_akerik", products, is_direct_list=True)
        return
    
    # 🛑 6-E: 🆕 معالجة خاصة لزر "طارات خشب" لعرض منتجاتها مباشرة
    if data == "taarat_khashab":
        products = taarat_submenu[1]['items']
        show_product_page(update, "taarat_khashab", products, is_direct_list=True)
        return

    # 7. معالجة ضغط زر المنتج للذهاب لصفحة الشراء 
    if data in product_to_submenu_map:
        product_data = None
        for submenu_key, submenu_list in all_submenus.items():
            for item in submenu_list:
                if data == item.get("callback") and 'items' not in item:
                    product_data = item
                    break
                if 'items' in item:
                    sub_item = next((si for si in item['items'] if si.get("callback") == data), None)
                    if sub_item:
                         product_data = sub_item
                         break
            if product_data:
                break
        
        if product_data:
            show_product_page(update, data, product_data)
            return
        else:
            query.answer(text="عذراً، لم يتم العثور على بيانات المنتج.", show_alert=True)
            return

    # 8. حالة زر الشراء (المنتجات العادية)
    if data.startswith("buy_"):
        # ⚠️ هام: نستثني هنا البوكسات والصواني والطارات لأن لهم ConversationHandler خاص
        # هذه القائمة هنا لتعمل كـ "safeguard" إذا فشل الـ ConversationHandler في التقاط الحدث.
        if "akerik_m" in data or "khashab_m" in data or "taarat_akerik_m" in data or "taarat_khashab_m" in data: 
             # يتم التقاطها بواسطة ConversationHandler
             query.answer()
             return

        product_key = data.replace("buy_", "")
        product_data = None
        
        for submenu in all_submenus.values():
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
# 4. إعداد البوت 
# --------------------
def main():
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN).")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # 1. محافظ
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

    # 4. صواني شبكة اكليريك - 🟢 تم التعديل
    tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tray_purchase, pattern=r'^buy_akerik_m\d+$')],
        states={
            GET_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_akerik$')
            ],
            GET_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_tray_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_tray_names, pattern='^back_to_tray_names$'),
            CallbackQueryHandler(button)
        ]
    )
    
    # 5. صواني شبكة خشب - 🟢 تم التعديل
    khashab_tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_tray_purchase, pattern=r'^buy_khashab_m\d+$')],
        states={
            GET_KHASHAB_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_khashab$')
            ],
            GET_KHASHAB_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_khashab_tray_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_khashab_tray_names, pattern='^back_to_khashab_tray_names$'),
            CallbackQueryHandler(button)
        ]
    )

    # 6. طارات اكليريك - النمط كان صحيحاً بالفعل
    akerik_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_taarat_purchase, pattern=r'^buy_taarat_akerik_m\d+$')],
        states={
            GET_AKRILIK_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_akerik_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_akerik$')
            ],
            GET_AKRILIK_TAARAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_akerik_taarat_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_akerik_taarat_names, pattern='^back_to_akerik_taarat_names$'),
            CallbackQueryHandler(button)
        ]
    )
    
    # 7. طارات خشب - النمط كان صحيحاً بالفعل
    khashab_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_taarat_purchase, pattern=r'^buy_taarat_khashab_m\d+$')],
        states={
            GET_KHASHAB_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_khashab$')
            ],
            GET_KHASHAB_TAARAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_khashab_taarat_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_khashab_taarat_names, pattern='^back_to_khashab_taarat_names$'),
            CallbackQueryHandler(button)
        ]
    )

    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler)
    dp.add_handler(box_handler)
    dp.add_handler(tray_handler)
    dp.add_handler(khashab_tray_handler)
    dp.add_handler(akerik_taarat_handler) 
    dp.add_handler(khashab_taarat_handler) 
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()