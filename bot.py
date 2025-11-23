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
GET_PEN_NAME = 2    # حالة الأقلام (تم تعريفها مسبقاً في الكود الأصلي)
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
GET_BSAMAT_NAMES = 13 # حالة أسماء البصامات
GET_TISSUE_NAMES = 14 # حالة أسماء مناديل كتب الكتاب
GET_TISSUE_DATE = 15 # حالة تاريخ مناديل كتب الكتاب


# --------------------
# 2. بيانات القوائم والمنتجات
# --------------------

# --- قوائم فرعية مباشرة (تعرض منتجاتها مباشرة) ---
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
engraved_wallet_submenu = [
    {"label": "محفظة بيج (هافان)", "callback": "wallet_bege", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بيج (هافان)."},
    {"label": "محفظة بني", "callback": "wallet_brown", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بني."},
    {"label": "محفظة سوداء", "callback": "wallet_black", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون أسود."}
]

# 🛑 قائمة الأقلام (تم دمجها)
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


# --- القوائم المتداخلة (sawany, taarat, haram, doro3, mugat) تبقى كما هي ---
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
    "aqlam": aqlam_submenu, # تم تحديث هذا الجزء ليشمل الأقلام
    "mugat": mugat_submenu,
    "bsamat": bsamat_submenu, 
    "wedding_tissues": wedding_tissues_submenu, 
    "abajorat": abajorat_submenu,
    "engraved_wallet": engraved_wallet_submenu
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam"]: # تم تحديث هذا الجزء ليشمل الأقلام
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
    if context.user_data.get('state') in [GET_WALLET_NAME, GET_PEN_NAME, GET_BOX_COLOR, GET_BOX_NAMES, GET_TRAY_NAMES, GET_TRAY_DATE, GET_KHASHAB_TRAY_NAMES, GET_KHASHAB_TRAY_DATE, GET_AKRILIK_TAARAT_NAMES, GET_AKRILIK_TAARAT_DATE, GET_KHASHAB_TAARAT_NAMES, GET_KHASHAB_TAARAT_DATE, GET_BSAMAT_NAMES, GET_TISSUE_NAMES, GET_TISSUE_DATE]:
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
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat"]:
        back_callback = "main_menu"
        back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
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
# دوال المحافظ (Engraved Wallet Handlers)
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

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *محافظ محفورة بالاسم*:\n\nمن فضلك اختر اللون المطلوب:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

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

    # 💡 زر الرجوع
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_wallets_color")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
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
    
    return GET_WALLET_NAME

def receive_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    product_data = context.user_data.get('wallet_data')
    
    if not product_data:
        update.effective_chat.send_message("عفواً، حدث خطأ في استرجاع بيانات المنتج. يرجى البدء من القائمة الرئيسية.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        context.user_data.clear()
        return ConversationHandler.END

    user_info = update.message.from_user
    
    product_label = product_data['label']
    try:
        color = product_label.split('محفظة ', 1)[1].strip() 
        wallet_type = "محفظة سافوكس الاصلية التقيلة" 
    except IndexError:
        color = product_label
        wallet_type = product_label

    message_body = (
        f"🔔 *طلب شراء جديد (محافظ محفورة بالاسم)* 🔔\n\n"
        f"المنتج: {wallet_type}\n"
        f"اللون: {color}\n" 
        f" الاسم المطلوب حفره: *{engraving_name}*\n" 
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name} {user_info.last_name if user_info.last_name else ''}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}\n"
        f"رابط التواصل عبر التليجرام: tg://user?id={user_info.id}"
    )
    
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
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

# ------------------------------------
# دوال الأقلام (Pen Handlers) - تم إضافتها
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

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *اقلام محفورة بالاسم*:\n\nمن فضلك اختر نوع القلم المطلوب:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    return ConversationHandler.END 

def prompt_for_pen_name(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    # العثور على بيانات القلم الذي تم اختياره
    selected_pen_data = next((item for item in aqlam_submenu if item["callback"] == data), None)
    context.user_data['pen_data'] = selected_pen_data
    context.user_data['state'] = GET_PEN_NAME

    try:
        query.message.delete()
    except Exception:
        pass

    # 💡 يتم إنشاء زر الرجوع هنا
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_pen_types")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    caption_text = (
        f"**اختيارك: {selected_pen_data['label']}**\n\n"
        f"من فضلك، **اكتب الاسم الذي تريد حفره** على القلم في رسالة نصية بالأسفل.\n"
        f"أو اضغط زر الرجوع لتغيير نوع القلم."
    )
    
    # 🛑 إرسال صورة القلم مع رسالة طلب الاسم وزر الرجوع
    update.effective_chat.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=selected_pen_data['image'],
        caption=caption_text,
        reply_markup=back_reply_markup, 
        parse_mode="Markdown"
    )
    
    return GET_PEN_NAME

def receive_pen_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    product_data = context.user_data.get('pen_data')
    
    if not product_data:
        update.effective_chat.send_message("عفواً، حدث خطأ في استرجاع بيانات المنتج. يرجى البدء من القائمة الرئيسية.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        context.user_data.clear()
        return ConversationHandler.END

    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (اقلام محفورة بالاسم)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f" الاسم المطلوب حفره: *{engraving_name}*\n" 
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name} {user_info.last_name if user_info.last_name else ''}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}\n"
        f"رابط التواصل عبر التليجرام: tg://user?id={user_info.id}"
    )
    
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
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

# الدوال الأخرى (cancel_and_end, prompt_for_names_bsamat, receive_names_bsamat_and_finish, إلخ) موجودة كما هي في الكود الأصلي.

# ------------------------------------
# الدالة الرئيسية لمعالجة ضغطات الأزرار (تم تعديلها فقط لإضافة منطق الأقلام)
# ------------------------------------
# هنا يجب أن تكون هناك دوال لمعالجة:
# - box_color
# - prompt_for_names_box
# - receive_names_box_and_finish
# - ... (باقي الدوال لـ tray, taarat, bsamat, tissue)
# لن أدرجها هنا لأنها ليست جزءاً من طلب الدمج، ولكن الكود يفترض وجودها.

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
        
    # 3. معالجة فتح قائمة الأقلام (محادثة) - تم تعديلها هنا
    if data == "aqlam":
        show_submenu(update, context, aqlam_submenu, "اقلام محفورة بالاسم", back_callback="main_menu")
        return 
        
    # 4. معالجة اختيار المنتج المحفور (سواء محفظة أو قلم) - تم تعديلها هنا
    if data in [item["callback"] for item in engraved_wallet_submenu]:
        return prompt_for_name(update, context) 
    
    # 🛑 معالجة اختيار نوع القلم (معدن أو مضئ) - تم إضافتها هنا
    if data in [item["callback"] for item in aqlam_submenu]:
        return prompt_for_pen_name(update, context) # ⬅️ توجيه مباشر لبدء المحادثة وطلب الاسم

    # 5. معالجة فتح القوائم الفرعية المتداخلة (Sawany, Taarat, Haram, Doro3, Mugat)
    if data in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus[data], clean_title, back_callback="main_menu") 
        return
        
    # 6. معالجة القوائم الفرعية التي تعرض المنتجات مباشرة (Bsamat, Wedding_Tissues, Abajorat)
    if data in ["bsamat", "wedding_tissues", "abajorat"]:
        product_list = all_submenus[data]
        show_product_page(update, data, product_list, is_direct_list=True)
        return

    # 7. معالجة ضغط زر المنتج للذهاب لصفحة الشراء أو لفتح قائمة فرعية متداخلة (المنتجات غير المحفورة)
    if data in product_to_submenu_map:
        product_data = None
        
        for submenu_key, submenu_list in all_submenus.items():
            for item in submenu_list:
                # الحالة 1: المنتج هو قائمة فرعية متداخلة (مثل 'sawany_akerik')
                if data == item.get("callback") and 'items' in item:
                    product_data = item
                    break 
                # الحالة 2: المنتج هو عنصر مباشر أو موديل داخل قائمة متداخلة
                if data == item.get("callback") and 'items' not in item:
                    product_data = item
                    break
                # الحالة 3: البحث داخل الـ 'items'
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

    # 8. حالة زر الشراء (المنتجات العادية غير المحفورة)
    if data.startswith("buy_"):
        product_key = data.replace("buy_", "")
        product_data = None
        
        # منطق البحث عن بيانات المنتج للشراء (باقي المنتجات)
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
# 4. إعداد البوت 
# --------------------

# دوال المعالجة الأخرى (مثل الدوال الخاصة بالبوكس والصواني والطارات) يجب أن تكون معرفة هنا.
# بما أنها موجودة في الكود الذي أرسلته، سنفترض وجودها ونكمل من دالة main.

def main():
    # 💡 استبدل بتوكن البوت الخاص بك
    # يتم قراءة التوكن عادةً من متغيرات البيئة 
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN) في بيئة العمل. يرجى التأكد من تعيينه.")
        # يرجى وضع التوكن الخاص بك هنا مؤقتاً إذا لم تستخدم متغيرات البيئة:
        # TOKEN = "YOUR_BOT_TOKEN_HERE" 
        return
    
    if WHATSAPP_NUMBER == "201288846355":
        print("⚠️ يرجى استبدال WHATSAPP_NUMBER برقمك الحقيقي.")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # 1. مُعالج المحادثة لـ "محافظ محفورة بالاسم"
    engraved_wallet_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                prompt_for_name, 
                pattern='^(' + '|'.join([item['callback'] for item in engraved_wallet_submenu]) + ')$'
            )
        ],
        states={
            GET_WALLET_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_name_and_prepare_whatsapp),
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_wallets_color, pattern='^back_to_wallets_color$'),
            CallbackQueryHandler(button) 
        ]
    )

    # 2. مُعالج المحادثة لـ "اقلام" - تم إضافته
    engraved_pen_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                prompt_for_pen_name, 
                pattern='^(' + '|'.join([item['callback'] for item in aqlam_submenu]) + ')$'
            )
        ],
        states={
            GET_PEN_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp),
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_pen_types, pattern='^back_to_pen_types$'),
            CallbackQueryHandler(button) 
        ]
    )
    
    # مُعالجات المحادثة الأخرى (نفترض أنها معرفة في الكود الأصلي)
    # box_handler = ConversationHandler(...)
    # tray_handler = ConversationHandler(...)
    # ...

    # إضافة مُعالجات المحادثة (بما في ذلك الموجودة في الكود الأصلي)
    # سنلتزم بترتيب الإضافة الموجود في كودك الأصلي
    # dp.add_handler(box_handler)
    # dp.add_handler(tray_handler)
    # dp.add_handler(khashab_tray_handler)
    # dp.add_handler(akerik_taarat_handler) 
    # dp.add_handler(khashab_taarat_handler) 
    # dp.add_handler(bsamat_handler) 
    # dp.add_handler(tissue_handler) 
    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler) # تم إضافة مُعالج الأقلام

    # إضافة معالجات الأوامر والأزرار الأخرى
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    #os.environ["TOKEN"] = "YOUR_BOT_TOKEN_HERE" 
    main()