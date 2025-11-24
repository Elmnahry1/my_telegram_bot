import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات الواتساب ورقم فودافون كاش
WHATSAPP_NUMBER = "201288846355" 
VODAFONE_CASH_NUMBER = "01032328500" 
VODAFONE_CASH_ACCOUNT_NAME = "اسم حساب فودافون كاش" # (افتراضي - يرجى تغييره)

# --------------------
# 1. تعريف حالات المحادثة
# --------------------

GET_WALLET_NAME = 1 
GET_PEN_NAME = 2    
GET_BOX_COLOR = 3   
GET_BOX_NAMES = 4   
GET_TRAY_NAMES = 5  
GET_TRAY_DATE = 6   
GET_KHASHAB_TRAY_NAMES = 7 
GET_KHASHAB_TRAY_DATE = 8  
GET_AKRILIK_TAARAT_NAMES = 9 
GET_AKRILIK_TAARAT_DATE = 10 
GET_KHASHAB_TAARAT_NAMES = 11 
GET_KHASHAB_TAARAT_DATE = 12 
GET_BSAMAT_NAMES = 13  
GET_BSAMAT_DATE = 14   
GET_TISSUE_NAMES = 15  
GET_TISSUE_DATE = 16   

# 🔥 الحالة الجديدة لطلب إيصال الدفع
GET_PAYMENT_RECEIPT = 17 
# 🔥 الحالة الجديدة لطلب صور المج (إضافة جديدة)
GET_MUG_PHOTOS = 18 


# --------------------
# 2. بيانات القوائم والمنتجات (تم الاحتفاظ بها كما هي لضمان التكامل)
# --------------------

# --- قوائم فرعية مباشرة ---
bsamat_submenu = [
    {"label": "بصامة موديل 1", "callback": "bsamat_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 1.", "price": "180 ج"},
    {"label": "بصامة موديل 2", "callback": "bsamat_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 2.", "price": "220 ج"}
]
wedding_tissues_submenu = [
    {"label": "منديل موديل 1", "callback": "tissue_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 1.", "price": "350 ج"},
    {"label": "منديل موديل 2", "callback": "tissue_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 2.", "price": "400 ج"}
]
katb_kitab_box_submenu = [
    {"label": "بوكس كتب كتاب موديل 1", "callback": "box_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف بوكس كتب الكتاب موديل 1، يحتوي على تصميم مميز.", "price": "550 ج"},
    {"label": "بوكس كتب كتاب موديل 2", "callback": "box_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف بوكس كتب الكتاب موديل 2، خامة عالية الجودة.", "price": "620 ج"}
]
abajorat_submenu = [
    {"label": "أباجورة موديل 1", "callback": "abajora_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف الأباجورة موديل 1.", "price": "450 ج"},
    {"label": "أباجورة موديل 2", "callback": "abajora_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف الأباجورة موديل 2.", "price": "480 ج"}
]
engraved_wallet_submenu = [
    {"label": "محفظة بيج (هافان)", "callback": "wallet_bege", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بيج (هافان).", "price": "200 ج"},
    {"label": "محفظة بني", "callback": "wallet_brown", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بني.", "price": "200 ج"},
    {"label": "محفظة سوداء", "callback": "wallet_black", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون أسود.", "price": "200 ج"}
]
aqlam_submenu = [
    {
        "label": "قلم تاتش معدن", 
        "callback": "aqlam_metal", 
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/475773348_986832329974720_6197915277469223378_n.jpg?stp=dst-jpg_s720x720_tt6&_nc_cat=107&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=KrebndL4u2oQ7kNvwH3smA2&_nc_oc=AdkT6T_o5SpJKdr9FQ5OhX2vuI5Cp3WjQl0pV9vRotIn9csOIX1DX-I9dC3FpvlBLJM&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=JFYgN-MxG5oy8y3q9Os6Ew&oh=00_AfhJxajOEm9owiAqd00_zEZ4Hy4qz7DYATV6p4tWdRxeA&oe=6923BE1B", 
        "description": "قلم تاتش معدن عالي الجودة ومناسب للحفر بالليزر.", "price": "120 ج"
    },
    {
        "label": "قلم تاتش مضئ", 
        "callback": "aqlam_luminous", 
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/489809156_1164483322357054_6286791651911010777_n.jpg?stp=dst-jpg_s590x590_tt6&_nc_cat=107&ccb=1-7&_nc_sid=833d8c&_nc_ohc=ELb9pciSoD0Q7kNvwG_rdLE&_nc_oc=AdkDWLOZBcjZp9AbNO2Fs-zK-suPtGc1D-KC3JP7NlzhwgJB3WZeGQQfCQIsfxZgvrg&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=U5_JMOw_cSsgrQQLv77j7g&oh=00_Afg-wJrTmoGZo5m1kVVh2IU0227UQ7pUtKSjRx_YEFoGWg&oe=6923B3BA", 
        "description": "قلم تاتش مضئ بتقنية متطورة ومناسب للحفر بالليزر.", "price": "150 ج"
    }
]

# قائمة مستلزمات سبلميشن 
sublimation_supplies_submenu = [
    {"label": "مج سحري فارغ (درجة أولي)", "callback": "subli_magic_mug", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "مج سيراميك سحري فارغ جاهز للطباعة الحرارية، درجة أولي ممتاز.", "price": "60 ج"},
    {"label": "تيشيرت قطن جاهز للسبلميشن", "callback": "subli_tshirt_cotton", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "تيشيرت قطن مجهز بطبقة سبلميشن، متوفر بجميع المقاسات.", "price": "100 ج"}
]


# --- القوائم المتداخلة ---
sawany_submenu = [
    {
        "label": "صواني شبكة اكليريك", "callback": "sawany_akerik", 
        "items": [ 
            {"label": "صينية اكليريك موديل 1", "callback": "akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "صينية اكليريك: وصف المنتج الأول.", "price": "800 ج"},
            {"label": "صينية اكليريك موديل 2", "callback": "akerik_m2", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "صينية اكليريك: وصف المنتج الثاني.", "price": "950 ج"}
        ]
    },
    {
        "label": "صواني شبكة خشب", "callback": "sawany_khashab", 
        "items": [ 
            {"label": "صينية خشب موديل 1", "callback": "khashab_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "صينية خشب: وصف المنتج الأول.", "price": "700 ج"},
            {"label": "صينية خشب موديل 2", "callback": "khashab_m2", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "صينية خشب: وصف المنتج الثاني.", "price": "850 ج"}
        ]
    }
]
taarat_submenu = [
    {
        "label": "طارات اكليريك", "callback": "taarat_akerik", "items": [
             {"label": "طارة اكليريك موديل 1", "callback": "taarat_akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة اكليريك موديل 1", "price": "300 ج"},
             {"label": "طارة اكليريك موديل 2", "callback": "taarat_akerik_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة اكليريك موديل 2", "price": "380 ج"}
        ]
    },
    {
        "label": "طارات خشب", "callback": "taarat_khashab", "items": [
            {"label": "طارة خشب موديل 1", "callback": "taarat_khashab_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة خشب موديل 1", "price": "250 ج"},
            {"label": "طارة خشب موديل 2", "callback": "taarat_khashab_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة خشب موديل 2", "price": "320 ج"}
        ]
    }
]
haram_submenu = [
    {
        "label": "هرم مكتب اكليريك", "callback": "haram_akerik", "items": [
             {"label": "هرم اكليريك موديل 1", "callback": "haram_akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم اكليريك موديل 1", "price": "350 ج"},
             {"label": "هرم اكليريك موديل 2", "callback": "haram_akerik_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم اكليريك موديل 2", "price": "420 ج"}
        ]
    },
    {
        "label": "هرم مكتب معدن بديل", "callback": "haram_metal", "items": [
             {"label": "هرم معدن موديل 1", "callback": "haram_metal_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم معدن موديل 1", "price": "300 ج"},
             {"label": "هرم معدن موديل 2", "callback": "haram_metal_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم معدن موديل 2", "price": "380 ج"}
        ]
    },
    {
        "label": "هرم مكتب خشب", "callback": "haram_khashab", "items": [
             {"label": "هرم خشب موديل 1", "callback": "haram_khashab_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم خشب موديل 1", "price": "280 ج"},
             {"label": "هرم خشب موديل 2", "callback": "haram_khashab_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف هرم خشب موديل 2", "price": "330 ج"}
        ]
    }
]
doro3_submenu = [
    {
        "label": "دروع اكليريك", "callback": "doro3_akerik", "items": [
             {"label": "درع اكليريك موديل 1", "callback": "doro3_akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع اكليريك موديل 1", "price": "200 ج"},
             {"label": "درع اكليريك موديل 2", "callback": "doro3_akerik_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع اكليريك موديل 2", "price": "250 ج"}
        ]
    },
    {
        "label": "دروع معدن بديل", "callback": "doro3_metal", "items": [
             {"label": "درع معدن موديل 1", "callback": "doro3_metal_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع معدن موديل 1", "price": "180 ج"},
             {"label": "درع معدن موديل 2", "callback": "doro3_metal_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع معدن موديل 2", "price": "220 ج"}
        ]
    },
    {
        "label": "دروع قطيفة", "callback": "doro3_qatifah", "items": [
             {"label": "درع قطيفة موديل 1", "callback": "doro3_qatifah_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع قطيفة موديل 1", "price": "280 ج"},
             {"label": "درع قطيفة موديل 2", "callback": "doro3_qatifah_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع قطيفة موديل 2", "price": "330 ج"}
        ]
    },
    {
        "label": "دروع خشب", "callback": "doro3_khashab", "items": [
             {"label": "درع خشب موديل 1", "callback": "doro3_khashab_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع خشب موديل 1", "price": "150 ج"},
             {"label": "درع خشب موديل 2", "callback": "doro3_khashab_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف درع خشب موديل 2", "price": "190 ج"}
        ]
    }
]
mugat_submenu = [
    {
        "label": "مج ابيض", "callback": "mugat_white", "items": [
             {"label": "مج ابيض موديل 1", "callback": "mugat_white_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج ابيض موديل 1", "price": "100 ج"},
             {"label": "مج ابيض موديل 2", "callback": "mugat_white_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج ابيض موديل 2", "price": "120 ج"}
        ]
    },
    {
        "label": "مج سحري", "callback": "mugat_magic", "items": [
             {"label": "مج سحري موديل 1", "callback": "mugat_magic_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج سحري موديل 1", "price": "150 ج"},
             {"label": "مج سحري موديل 2", "callback": "mugat_magic_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج سحري موديل 2", "price": "180 ج"}
        ]
    },
    {
        "label": "مج ديجتال", "callback": "mugat_digital", "items": [
             {"label": "مج ديجتال موديل 1", "callback": "mugat_digital_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج ديجتال موديل 1", "price": "220 ج"},
             {"label": "مج ديجتال موديل 2", "callback": "mugat_digital_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف مج ديجتال موديل 2", "price": "250 ج"}
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
    "engraved_wallet": engraved_wallet_submenu,
    "sublimation": sublimation_supplies_submenu
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box", "sublimation"]:
        for product in submenu_list:
            product_to_submenu_map[product["callback"]] = menu_key
    else:
        for item in submenu_list:
            product_to_submenu_map[item["callback"]] = menu_key 
            if 'items' in item:
                for sub_item in item['items']:
                    product_to_submenu_map[sub_item["callback"]] = item["callback"] 


# --------------------
# 3. الدوال الرئيسية والمساعدة
# --------------------

def get_file_link(context, file_id):
    """دالة مساعدة للحصول على رابط مباشر للملف (الصورة)."""
    try:
        file = context.bot.get_file(file_id)
        return f"https://api.telegram.org/file/bot{context.bot.token}/{file.file_path}"
    except Exception as e:
        print(f"Error getting file link: {e}")
        return "غير متوفر"


def cancel_and_end(update, context):
    query = update.callback_query
    if query:
        query.answer("تم إلغاء العملية الحالية. يرجى اختيار طلبك مرة أخرى.", show_alert=True)
        try:
            query.message.delete()
        except Exception:
            pass
    
    context.user_data.clear()
    
    start(update, context) 
    
    return ConversationHandler.END


def start(update, context):
    query = update.callback_query
    if context.user_data.get('state'):
        context.user_data.clear()
        context.user_data['state'] = None
        
    if query:
        query.answer()
    
    user_name = update.effective_user.first_name if update.effective_user else "عميلنا"
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
    
    return ConversationHandler.END

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

def show_product_page(update, product_callback_data, product_list, is_direct_list=False):
    query = update.callback_query
    if query:
        query.answer()

    if query and query.message:
        try:
            query.message.delete()
        except Exception:
            pass
    
    for item in product_list:
        item_keyboard = [[InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{item['callback']}")]]
        item_reply_markup = InlineKeyboardMarkup(item_keyboard)
        
        caption_text = f"**{item['label']}**\n\nالسعر: *{item.get('price', 'غير متوفر')}*\n\n{item['description']}"
        
        update.effective_message.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=item['image'],
            caption=caption_text,
            reply_markup=item_reply_markup,
            parse_mode="Markdown"
        )
    
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation", "aqlam", "engraved_wallet"]:
        back_callback = "main_menu"
        back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
    elif product_to_submenu_map.get(product_callback_data) in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        back_callback = product_to_submenu_map.get(product_callback_data)
        back_text = "🔙 اضغط للرجوع إلى القائمة الفرعية"
    else:
        back_callback = "main_menu"
        back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"


    back_keyboard = [[InlineKeyboardButton(back_text, callback_data=back_callback)]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
        
    update.effective_message.bot.send_message(
        chat_id=update.effective_chat.id,
        text="---", 
        reply_markup=back_reply_markup
    )


# --------------------------------------------------------------------------------
# 🔥 دوال المجّات المعدلة (إضافة GET_MUG_PHOTOS)
# --------------------------------------------------------------------------------

def get_mug_items():
    """دالة مساعدة للحصول على قائمة المج الأبيض والسحري فقط."""
    white_mugs = mugat_submenu[0]['items']
    magic_mugs = mugat_submenu[1]['items']
    return white_mugs + magic_mugs


def start_mug_purchase(update, context):
    """تبدأ محادثة المج، وتطلب إرفاق 3 صور للطباعة."""
    query = update.callback_query
    query.answer()
    data = query.data 

    product_callback = data.replace("buy_", "")
    
    # 1. جلب بيانات المنتج
    all_mug_items = get_mug_items() 
    selected_product = next((item for item in all_mug_items if item["callback"] == product_callback), None)
    
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['mug_product'] = selected_product
    context.user_data['mug_photos_links'] = [] # تهيئة قائمة لتخزين روابط الصور
    context.user_data['state'] = GET_MUG_PHOTOS 
    
    # 2. إعداد لوحة المفاتيح (زر الرجوع)
    back_callback = "mugat" # العودة إلى قائمة تصنيفات المجّات
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # 3. إرسال رسالة طلب الصور
    try:
        query.message.delete()
    except:
        pass

    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        f"من فضلك، **يرجى إرسال 3 صور** في رسائل متتالية لطباعتهم على المج.\n"
        f"سيتم إرسال رابط الصور إلينا ضمن طلب الشراء.\n\n"
        f"أو اضغط زر رجوع للعودة الي القائمة السابقة."
    )
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    return GET_MUG_PHOTOS


def receive_mug_photos_and_finish(update, context):
    """تستقبل الصور وتنتقل لمرحلة الدفع بعد استلام 3 صور."""
    
    if not update.message.photo:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="❌ يجب إرسال **صورة**. يرجى إرفاق صورة للطباعة.",
            parse_mode="Markdown"
        )
        return GET_MUG_PHOTOS # البقاء في نفس الحالة
        
    # الحصول على ملف الصورة بأعلى دقة
    photo_file_id = update.message.photo[-1].file_id 
    
    # تحويل معرف الملف إلى رابط مباشر
    photo_link = get_file_link(context, photo_file_id)
        
    
    mug_photos_links = context.user_data.get('mug_photos_links', [])
    mug_photos_links.append(photo_link)
    context.user_data['mug_photos_links'] = mug_photos_links
    
    # التحقق من اكتمال 3 صور
    count = len(mug_photos_links)
    remaining = 3 - count
    
    if remaining > 0:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"تم استلام الصورة رقم {count} بنجاح. يرجى إرسال **{remaining} صور إضافية** لطباعتهم."
        )
        return GET_MUG_PHOTOS # البقاء في نفس الحالة
    else:
        # تم استلام جميع الصور، الانتقال إلى مرحلة الدفع
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="✅ تم استلام الثلاث صور بنجاح! سيتم الآن الانتقال لخطوة الدفع."
        )
        # الانتقال إلى مرحلة الدفع وتمرير نوع المنتج الجديد
        return prompt_for_payment_and_receipt(update, context, product_type="مج (طباعة 3 صور)")


# --------------------------------------------------------------------------------
# دوال الدفع (تم تعديلها لدمج تفاصيل المج)
# --------------------------------------------------------------------------------

def handle_payment_photo(update, context):
    """يعالج إيصال الدفع ويرسل طلب الشراء عبر الواتساب."""
    chat_id = update.message.chat_id
    
    if not update.message.photo:
        context.bot.send_message(chat_id=chat_id, text="يرجى إرسال صورة إيصال الدفع فقط.")
        return GET_PAYMENT_RECEIPT

    receipt_photo_id = update.message.photo[-1].file_id
    receipt_url = get_file_link(context, receipt_photo_id)

    # استخراج البيانات النهائية
    product_type = context.user_data.get('final_product_type', 'غير محدد')
    product_label = context.user_data.get('final_product_label', 'منتج غير معروف')
    paid_amount = context.user_data.get('final_price', 'غير محدد')
    names_text = context.user_data.get('final_names', 'غير مطلوب')
    date_text = context.user_data.get('final_date', 'غير مطلوب')
    product_code = context.user_data.get('final_code', 'N/A')
    product_image_url = context.user_data.get('final_product_image', 'غير متوفر')
    user_info = update.message.from_user
    
    telegram_contact_link = f"tg://user?id={user_info.id}"

    # بناء رسالة الواتساب النهائية (تم دمج تفاصيل المج هنا)
    message_body = (
        f"🔔 *طلب شراء جديد (مدفوع)* 🔔\n\n"
        f"نوع المنتج: {product_type.replace('-', ' - ')}\n"
        f"المنتج: {product_label}\n"
        f"السعر المدفوع: *{paid_amount}*\n\n"
        f"الأسماء/التفاصيل:\n{names_text}\n" # هذا سيشمل روابط صور المج
        f"التاريخ: {date_text}\n\n"
        f"🔗 رابط صورة المنتج: {product_image_url}\n" 
        f"🔗 رابط إيصال الدفع: {receipt_url}\n"
        f"الكود: {product_code}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"رابط التواصل عبر التليجرام: {telegram_contact_link}"
    )
    
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"تم استلام إيصال الدفع بنجاح. تفاصيل الطلب جاهزة:\n\nالمنتج: {product_label}\nالسعر: {paid_amount}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    
    context.user_data.clear()
    return ConversationHandler.END


def handle_payment_buttons(update, context):
    """يعالج أزرار مرحلة الدفع (مثل الإلغاء)."""
    query = update.callback_query
    data = query.data
    
    if data == "cancel":
        return cancel_and_end(update, context)

    query.answer("يرجى إرسال إيصال الدفع لإتمام الطلب.", show_alert=True)
    return GET_PAYMENT_RECEIPT


def prompt_for_payment_and_receipt(update, context, product_type):
    """
    الدالة التي تطلب من العميل الدفع وتحويل الحالة إلى انتظار صورة الإيصال.
    """
    
    product_data = None
    names_details = ""
    date_details = ""
    
    # 1. إعداد تفاصيل الطلب حسب نوع المنتج
    if product_type == "بصامة":
        product_data = context.user_data.get('bsamat_product')
        names_details = context.user_data.get('bsamat_names')
        date_details = context.user_data.get('bsamat_date')
    elif product_type == "مج (طباعة 3 صور)": # 🔥 الحالة الجديدة لطلب المج
        product_data = context.user_data.get('mug_product')
        mug_photos_links = context.user_data.get('mug_photos_links', [])
        # يتم تحويل روابط الصور إلى نص واحد وإدراجه في حقل الأسماء لإرساله عبر الواتساب
        names_details = "روابط صور الطباعة:\n" + "\n".join([f"🔗 صورة {i+1}: {link}" for i, link in enumerate(mug_photos_links)])
        date_details = 'غير مطلوب'
    # ... (باقي حالات المنتجات التي تحتاج إدخال - مثل: محافظ, اقلام, صواني, طارات, مناديل, بوكسات)
    # ⚠️ في هذا الإصدار، تم افتراض أن المنتجات الأخرى تستخدم 'product_data' المحفوظة مسبقًا
    elif 'product_data' in context.user_data: # حالة الشراء المباشر (أباجورات، دروع، أهرام، مج ديجتال، سبلميشن)
        product_data = context.user_data.get('product_data', {})
        names_details = context.user_data.get('names_details', 'غير مطلوب') # قد تكون محفوظة من محادثات أخرى
        date_details = context.user_data.get('date_details', 'غير مطلوب')
    else:
        if update.callback_query:
            update.callback_query.answer("خطأ: لم يتم تحديد المنتج لإتمام عملية الدفع.", show_alert=True)
        return ConversationHandler.END

    # 2. حفظ تفاصيل الطلب بشكل موحد لـ handle_payment_photo
    context.user_data['final_product_type'] = product_type
    context.user_data['final_product_label'] = product_data.get('label', product_type)
    context.user_data['final_price'] = product_data.get('price', 'غير محدد')
    context.user_data['final_names'] = names_details if names_details else 'غير مطلوب'
    context.user_data['final_date'] = date_details if date_details else 'غير مطلوب'
    context.user_data['final_code'] = product_data.get('callback', 'N/A')
    context.user_data['final_product_image'] = product_data.get('image', 'غير متوفر')
    
    # 3. إرسال رسالة الدفع
    payment_message = (
        f"✅ *طلبك جاهز:* {context.user_data['final_product_label']}\n"
        f"💰 *السعر الإجمالي:* {context.user_data['final_price']}\n\n"
        f"من فضلك قم بتحويل المبلغ على محفظة فودافون كاش.\n\n"
        f"👇 **اضغط على زر النسخ بالأسفل ليظهر الرقم في خانة الرسالة لنسخه بسهولة**.\n\n"
        f"بعد التحويل، **يرجى إرسال صورة إيصال التحويل في رسالة بالأسفل** لإتمام الطلب.\n\n"
        f"أو اضغط إلغاء للعودة للقائمة الرئيسية."
    )
    
    keyboard = [
        [InlineKeyboardButton("📞 نسخ رقم المحفظة مباشرة (اضغط هنا)", switch_inline_query_current_chat=f" {VODAFONE_CASH_NUMBER}")],
        [InlineKeyboardButton("❌ إلغاء الطلب", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    chat_id = update.effective_chat.id 
    
    if update.callback_query:
        try:
            update.callback_query.edit_message_text(text=payment_message, reply_markup=reply_markup, parse_mode="Markdown")
        except:
            context.bot.send_message(chat_id=chat_id, text=payment_message, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        context.bot.send_message(chat_id=chat_id, text=payment_message, reply_markup=reply_markup, parse_mode="Markdown")
        
    context.user_data['state'] = GET_PAYMENT_RECEIPT
    return GET_PAYMENT_RECEIPT

def prepare_whatsapp_link_for_direct_buy(update, context):
    """يعالج المنتجات ذات الشراء المباشر (مج ديجتال، اباجورات، دروع، اهرام، سبلميشن) وينتقل لمرحلة الدفع."""
    query = update.callback_query
    query.answer()
    data = query.data 

    product_callback = data.replace("buy_", "")
    
    selected_product = None
    product_type = ""
    
    # البحث في قوائم الشراء المباشر (أباجورات، سبلميشن)
    direct_list_keys = ["abajorat", "sublimation"]
    for key in direct_list_keys:
        for item in all_submenus.get(key, []):
            if item["callback"] == product_callback:
                selected_product = item
                product_type = item['label']
                break
        if selected_product: break

    # البحث في قوائم متداخلة (دروع، أهرام، مج ديجتال)
    if not selected_product:
        for menu_key in ["doro3", "haram", "mugat"]:
            for item in all_submenus.get(menu_key, []):
                if 'items' in item:
                    for sub_item in item['items']:
                        if sub_item["callback"] == product_callback:
                            selected_product = sub_item
                            product_type = item['label']
                            break
                if selected_product:
                    break
            if selected_product:
                break

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['product_data'] = selected_product
    
    try: 
        query.message.delete()
    except: 
        pass 
        
    # الانتقال إلى مرحلة الدفع
    return prompt_for_payment_and_receipt(update, context, product_type=selected_product.get('label', product_type))

def button(update, context):
    query = update.callback_query
    data = query.data

    if data == "cancel":
        return cancel_and_end(update, context) 

    if data == "main_menu":
        start(update, context)
        return 

    # 1. معالجة فتح قوائم المستوى الأول (sawany, taarat, haram, doro3, mugat, aqlam, engraved_wallet, ...)
    if data in all_submenus:
        menu_data = all_submenus[data]
        menu_title = next(item['label'] for item in main_menu if item['callback'] == data)
        
        # قوائم المستوى الأول التي تفتح صفحة منتجات مباشرة (مثل بصمات، أباجورات)
        if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation", "aqlam", "engraved_wallet"]:
            show_product_page(update, data, menu_data, is_direct_list=True)
        # قوائم المستوى الأول التي تفتح قائمة فرعية (مثل صواني، طارات، دروع)
        else:
            show_submenu(update, context, menu_data, menu_title, back_callback="main_menu")
        return 

    # 2. معالجة قوائم المستوى الثاني (sawany_akerik, taarat_khashab, ...)
    parent_menu_key = product_to_submenu_map.get(data)
    if parent_menu_key in ["sawany", "taarat", "haram", "doro3", "mugat"]: 
        parent_menu = next(item for item in all_submenus.get(parent_menu_key, []) if item['callback'] == data)
        if parent_menu and 'items' in parent_menu:
            show_product_page(update, data, parent_menu['items'])
            return

    # 3. معالجة أزرار الشراء الفردية التي لم تبدأ محادثة (يتم معالجتها في direct_buy_handler)
    if data.startswith("buy_"):
        prepare_whatsapp_link_for_direct_buy(update, context)
        return
        
    query.answer("إجراء غير معروف.", show_alert=True)
    start(update, context)


# --------------------
# 5. تعريف الدوال الناقصة (لضمان عمل البوت وعدم انهياره)
# --------------------

# دوال محادثات الصواني والطارات والبوكسات والمناديل والبصامات والمحافظ والأقلام:
# ⚠️ تم ترك المنطق الداخلي فارغًا (`pass`) هنا، ويجب أن تضيف المنطق الخاص بها من ملفك الأصلي.

def start_box_purchase(update, context): pass 
def save_box_color_ask_names(update, context): pass 
def back_to_box_menu(update, context): return button(update, context) # استخدام الدالة button للرجوع
def receive_box_names_and_finish(update, context): pass 

def start_akerik_tray_purchase(update, context): pass 
def save_tray_names_ask_date(update, context): pass 
def receive_tray_date_and_finish(update, context): pass 

def start_khashab_tray_purchase(update, context): pass 
def save_khashab_tray_names_ask_date(update, context): pass 
def receive_khashab_tray_date_and_finish(update, context): pass 

def start_akerik_taarat_purchase(update, context): pass 
def save_akerik_taarat_names_ask_date(update, context): pass 
def receive_akerik_taarat_date_and_finish(update, context): pass 

def start_khashab_taarat_purchase(update, context): pass 
def save_khashab_taarat_names_ask_date(update, context): pass 
def receive_khashab_taarat_date_and_finish(update, context): pass 

def start_bsamat_purchase(update, context): pass 
def save_bsamat_names_ask_date(update, context): pass 
def receive_bsamat_date_and_finish(update, context): pass 

def start_tissue_purchase(update, context): pass 
def save_tissue_names_ask_date(update, context): pass 
def receive_tissue_date_and_finish(update, context): pass 

def start_wallet_purchase(update, context): pass 
def receive_wallet_name_and_prepare_whatsapp(update, context): pass 
def back_to_wallet_name(update, context): pass

def start_pen_purchase(update, context): pass 
def receive_pen_name_and_prepare_whatsapp(update, context): pass 
def back_to_pen_types(update, context): pass


# --------------------
# 6. دالة main لتشغيل البوت
# --------------------

def main():
    """تشغيل البوت وإضافة جميع المعالجات."""
    # ⚠️ يجب التأكد من ضبط متغير البيئة TOKEN
    TOKEN = os.environ.get('TOKEN', "YOUR_BOT_TOKEN_HERE") 

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # 1. بوكس كتب الكتاب
    box_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_box_purchase, pattern='^buy_box_.*')],
        states={
            GET_BOX_COLOR: [CallbackQueryHandler(save_box_color_ask_names, pattern='^color_.*$|^katb_kitab_box$')],
            GET_BOX_NAMES: [ 
                MessageHandler(Filters.text & ~Filters.command, receive_box_names_and_finish),
                CallbackQueryHandler(back_to_box_menu, pattern='^katb_kitab_box$') 
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[ CommandHandler('start', start), CallbackQueryHandler(back_to_box_menu, pattern='^back_to_box_menu$'), CallbackQueryHandler(cancel_and_end) ]
    )

    # 2. صواني شبكة اكليريك
    tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_tray_purchase, pattern='^buy_akerik_m[12]$')],
        states={
            GET_TRAY_NAMES: [ MessageHandler(Filters.text & ~Filters.command, save_tray_names_ask_date), CallbackQueryHandler(button, pattern='^sawany_akerik$') ],
            GET_TRAY_DATE: [ MessageHandler(Filters.text & ~Filters.command, receive_tray_date_and_finish) ],
            GET_PAYMENT_RECEIPT: [ MessageHandler(Filters.photo, handle_payment_photo), CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') ]
        }, fallbacks=[ CommandHandler('start', start), CallbackQueryHandler(cancel_and_end) ]
    )

    # 3. صواني شبكة خشب
    khashab_tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_tray_purchase, pattern='^buy_khashab_m[12]$')],
        states={
            GET_KHASHAB_TRAY_NAMES: [ MessageHandler(Filters.text & ~Filters.command, save_khashab_tray_names_ask_date), CallbackQueryHandler(button, pattern='^sawany_khashab$') ],
            GET_KHASHAB_TRAY_DATE: [ MessageHandler(Filters.text & ~Filters.command, receive_khashab_tray_date_and_finish) ],
            GET_PAYMENT_RECEIPT: [ MessageHandler(Filters.photo, handle_payment_photo), CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') ]
        }, fallbacks=[ CommandHandler('start', start), CallbackQueryHandler(cancel_and_end) ]
    )

    # 4. طارات اكليريك
    akerik_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_taarat_purchase, pattern='^buy_taarat_akerik_m[12]$')],
        states={
            GET_AKRILIK_TAARAT_NAMES: [ MessageHandler(Filters.text & ~Filters.command, save_akerik_taarat_names_ask_date), CallbackQueryHandler(button, pattern='^taarat_akerik$') ],
            GET_AKRILIK_TAARAT_DATE: [ MessageHandler(Filters.text & ~Filters.command, receive_akerik_taarat_date_and_finish) ],
            GET_PAYMENT_RECEIPT: [ MessageHandler(Filters.photo, handle_payment_photo), CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') ]
        }, fallbacks=[ CommandHandler('start', start), CallbackQueryHandler(cancel_and_end) ]
    )

    # 5. طارات خشب
    khashab_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_taarat_purchase, pattern='^buy_taarat_khashab_m[12]$')],
        states={
            GET_KHASHAB_TAARAT_NAMES: [ MessageHandler(Filters.text & ~Filters.command, save_khashab_taarat_names_ask_date), CallbackQueryHandler(button, pattern='^taarat_khashab$') ],
            GET_KHASHAB_TAARAT_DATE: [ MessageHandler(Filters.text & ~Filters.command, receive_khashab_taarat_date_and_finish) ],
            GET_PAYMENT_RECEIPT: [ MessageHandler(Filters.photo, handle_payment_photo), CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') ]
        }, fallbacks=[ CommandHandler('start', start), CallbackQueryHandler(cancel_and_end) ]
    )

    # 6. بصامات
    bsamat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_bsamat_purchase, pattern='^buy_bsamat_.*')],
        states={
            GET_BSAMAT_NAMES: [ MessageHandler(Filters.text & ~Filters.command, save_bsamat_names_ask_date), CallbackQueryHandler(button, pattern='^bsamat$') ],
            GET_BSAMAT_DATE: [ MessageHandler(Filters.text & ~Filters.command, receive_bsamat_date_and_finish) ],
            GET_PAYMENT_RECEIPT: [ MessageHandler(Filters.photo, handle_payment_photo), CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') ]
        }, fallbacks=[ CommandHandler('start', start), CallbackQueryHandler(cancel_and_end) ]
    )

    # 7. مناديل كتب الكتاب
    tissue_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tissue_purchase, pattern='^buy_tissue_.*')],
        states={
            GET_TISSUE_NAMES: [ MessageHandler(Filters.text & ~Filters.command, save_tissue_names_ask_date), CallbackQueryHandler(button, pattern='^wedding_tissues$') ],
            GET_TISSUE_DATE: [ MessageHandler(Filters.text & ~Filters.command, receive_tissue_date_and_finish) ],
            GET_PAYMENT_RECEIPT: [ MessageHandler(Filters.photo, handle_payment_photo), CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') ]
        }, fallbacks=[ CommandHandler('start', start), CallbackQueryHandler(cancel_and_end) ]
    )

    # 8. محفظة محفورة
    engraved_wallet_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_wallet_purchase, pattern='^buy_wallet_.*')],
        states={
            GET_WALLET_NAME: [ MessageHandler(Filters.text & ~Filters.command, receive_wallet_name_and_prepare_whatsapp) ],
            GET_PAYMENT_RECEIPT: [ MessageHandler(Filters.photo, handle_payment_photo), CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') ]
        }, fallbacks=[ CommandHandler('start', start), CallbackQueryHandler(back_to_wallet_name, pattern='^back_to_wallets_color$'), CallbackQueryHandler(cancel_and_end) ]
    )
    
    # 9. قلم محفور
    engraved_pen_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_pen_purchase, pattern='^buy_aqlam_.*')],
        states={
            GET_PEN_NAME: [ MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp) ],
            GET_PAYMENT_RECEIPT: [ MessageHandler(Filters.photo, handle_payment_photo), CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') ]
        }, fallbacks=[ CommandHandler('start', start), CallbackQueryHandler(back_to_pen_types, pattern='^back_to_pen_types$'), CallbackQueryHandler(cancel_and_end) ]
    )
    
    # 10. محادثة المج الأبيض والسحري (طلب 3 صور) 🔥 الإضافة الرئيسية
    mug_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_mug_purchase, pattern='^buy_mugat_white_.*$'),
            CallbackQueryHandler(start_mug_purchase, pattern='^buy_mugat_magic_.*$')
        ],
        states={
            GET_MUG_PHOTOS: [
                # يستقبل رسائل الصور
                MessageHandler(Filters.photo & ~Filters.command, receive_mug_photos_and_finish),
                # زر الرجوع يعود إلى قائمة المجّات الرئيسية
                CallbackQueryHandler(button, pattern='^mugat$') 
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

    # 11. محادثة الشراء المباشر (أباجورات، دروع، أهرام، مج ديجتال، سبلميشن)
    # 🔥 تم تعديل النمط لاستبعاد المج الأبيض والسحري
    direct_buy_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prepare_whatsapp_link_for_direct_buy, pattern='^buy_(abajora|haram|doro3|subli|mugat_digital)_.*')], 
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

    # 5. إضافة جميع ConversationHandler أولاً لضمان الأولوية
    dp.add_handler(box_handler)
    dp.add_handler(tray_handler)
    dp.add_handler(khashab_tray_handler)
    dp.add_handler(akerik_taarat_handler) 
    dp.add_handler(khashab_taarat_handler) 
    dp.add_handler(bsamat_handler) 
    dp.add_handler(tissue_handler) 
    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler) 
    
    # 🔥 إضافة معالج المجّات الجديد
    dp.add_handler(mug_handler) 
    # إضافة معالج الشراء المباشر (يجب أن يكون بعد معالجات المجّات الخاصة)
    dp.add_handler(direct_buy_handler) 

    
    # 6. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 7. معالج أزرار القائمة العامة (يجب أن يكون في النهاية)
    dp.add_handler(CallbackQueryHandler(button))

    # 8. تشغيل البوت
    print("Bot started...")
    updater.start_polling()
    updater.idle() 

if __name__ == '__main__':
    main()