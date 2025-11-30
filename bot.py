import os
import re 
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات الواتساب ورقم فودافون كاش
WHATSAPP_NUMBER = "201288846355" 
VODAFONE_CASH_NUMBER = "01032328500" 


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

GET_PAYMENT_RECEIPT = 17 
GET_MUG_PHOTOS = 18
GET_DIGITAL_MUG_NAME = 19
GET_MIRROR_SIZE = 20
GET_MIRROR_NAME = 21
GET_FAN_NAME = 22
GET_CLOCK_SIZE = 23
GET_CLOCK_PHOTO = 24
GET_TABLOH_SIZE = 25
GET_MABKHARA_DETAILS = 26
GET_HASALA_TYPE = 27
GET_HASALA_NAME = 28
GET_DELIVERY_METHOD = 29
# 🔥 الحالة الجديدة لعنوان التوصيل
GET_DELIVERY_ADDRESS = 30


# --------------------
# 2. بيانات القوائم والمنتجات
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

# 🔥 قائمة المرايا
mirrors_submenu = [
    {"label": "مرايا موديل 1", "callback": "mirror_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "مرايا موديل 1 بتصميم أنيق.", "price": "حسب المقاس"},
    {"label": "مرايا موديل 2", "callback": "mirror_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "مرايا موديل 2 بتصميم عصري.", "price": "حسب المقاس"}
]

# 🔥🔥🔥 قائمة يد الهوايا
fans_submenu = [
    {"label": "يد هوايا موديل 1", "callback": "fan_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "يد هوايا مميزة موديل 1.", "price": "150 ج"},
    {"label": "يد هوايا موديل 2", "callback": "fan_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "يد هوايا مميزة موديل 2.", "price": "180 ج"}
]

# 🔥🔥🔥 قائمة ساعات الزجاج
clocks_submenu = [
    {"label": "ساعة زجاج مطبوعة", "callback": "clock_glass", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "ساعة زجاجية أنيقة يمكن طباعة صورتك المفضلة عليها، متوفرة بمقاسين.", "price": "حسب المقاس"}
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

# 🔥 قائمة المباخر
mabakher_submenu = [
    {
        "label": "مبخرة موديل 1", 
        "callback": "mabkhara_m1", 
        "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", 
        "description": "مبخرة خشبية بتصميم إسلامي مميز، مناسبة للإهداء.", 
        "price": "250 ج"
    },
    {
        "label": "مبخرة موديل 2", 
        "callback": "mabkhara_m2", 
        "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", 
        "description": "مبخرة اكليريك مع خشب بتصميم عصري وكتابة الاسم.", 
        "price": "300 ج"
    }
]

# 🔥 قائمة الحصالات
hasalat_submenu = [
    {
        "label": "حصالة خشبية مميزة", 
        "callback": "hasala_product", 
        "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", 
        "description": "حصالة خشبية أنيقة لتوفير المال، متوفرة بعدة فئات (5000 - 1000 - 2000) مع إمكانية كتابة الاسم.", 
        "price": "حسب الفئة"
    }
]

aqlam_submenu = [
    {
        "label": "قلم تاتش معدن", 
        "callback": "aqlam_metal", 
        "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", 
        "description": "قلم تاتش معدن عالي الجودة ومناسب للحفر بالليزر.", "price": "120 ج"
    },
    {
        "label": "قلم تاتش مضئ", 
        "callback": "aqlam_luminous", 
        "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", 
        "description": "قلم تاتش مضئ بتقنية متطورة ومناسب للحفر بالليزر.", "price": "150 ج"
    }
]

# 🔥 قائمة مستلزمات سبلميشن
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
    {"label": "🪞 مرايا محفورة بأسم العروسة", "callback": "mirrors"}, 
    {"label": "💃 يد هوايا محفورة بأسم العروسة", "callback": "fans"}, 
    {"label": "🗄️ هرم مكتب", "callback": "haram"},
    {"label": "🏆 دروع", "callback": "doro3"},
    {"label": "💡 اباجورات", "callback": "abajorat"}, 
    {"label": "✏️ اقلام", "callback": "aqlam"}, 
    {"label": "☕ مجات", "callback": "mugat"},
    {"label": "🕰️ ساعات زجاج بالصورة", "callback": "clocks"}, 
    {"label": "🖼️ تابلوهات", "callback": "tablohat"}, 
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"}, 
    {"label": "♨️ مباخر", "callback": "mabakher"}, 
    {"label": "💰 حصالات", "callback": "hasalat"}, 
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
    "mirrors": mirrors_submenu,
    "fans": fans_submenu, 
    "clocks": clocks_submenu, 
    "abajorat": abajorat_submenu,
    "engraved_wallet": engraved_wallet_submenu,
    "mabakher": mabakher_submenu, 
    "hasalat": hasalat_submenu, 
    "sublimation": sublimation_supplies_submenu 
}

# بناء خريطة المنتجات 
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box", "mirrors", "fans", "sublimation", "clocks", "mabakher", "hasalat"]: 
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

# دالة مساعدة لحساب السعر النهائي
def get_total_price_string(price_str, delivery_cost):
    match = re.search(r'\d+', price_str)
    if match and delivery_cost > 0:
        try:
            val = int(match.group())
            new_val = val + delivery_cost
            return f"{new_val} ج"
        except:
            pass
    
    if delivery_cost > 0:
        return f"{price_str} + {delivery_cost} ج (توصيل)"
    return price_str


# 🛑 الدالة لإلغاء أي محادثة جارية والعودة للقائمة الرئيسية
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
    
    user_name = update.effective_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختر طلبك من القائمة:"
    
    keyboard = []
    for i in range(0, len(main_menu), 2):
        row = [InlineKeyboardButton(main_menu[i]["label"], callback_data=main_menu[i]["callback"])]
        if i + 1 < len(main_menu):
            row.append(InlineKeyboardButton(main_menu[i+1]["label"], callback_data=main_menu[i+1]["callback"]))
        keyboard.append(row)
        
    reply_markup = InlineKeyboardMarkup(keyboard)

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
        try:
            query.message.delete()
        except Exception:
            pass 
        
    keyboard = []
    for item in submenu_list:
        keyboard.append([InlineKeyboardButton(item["label"], callback_data=item["callback"])]) 

    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = f"✅ {title}\n\nمن فضلك اختر طلبك من القائمة:"
    update.effective_chat.send_message(text=message_text, reply_markup=reply_markup, parse_mode="Markdown")
        

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
    
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "mirrors", "fans", "sublimation", "clocks", "mabakher", "hasalat"]: 
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
        
    update.effective_message.bot.send_message(chat_id=update.effective_chat.id, text="---", reply_markup=back_reply_markup)


# --- [دوال المحادثات الخاصة بالبصامات] ---
def get_bsamat_items():
    return bsamat_submenu

def start_bsamat_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = get_bsamat_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['bsamat_product'] = selected_product
    context.user_data['state'] = GET_BSAMAT_NAMES
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="bsamat")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
        
    return GET_BSAMAT_NAMES

def back_to_bsamat_names(update, context):
    query = update.callback_query
    query.answer()
    selected_product = context.user_data.get('bsamat_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="bsamat")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_BSAMAT_NAMES

def save_bsamat_names_ask_date(update, context):
    names = update.message.text
    context.user_data['bsamat_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_bsamat_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_BSAMAT_DATE

def receive_bsamat_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['bsamat_date'] = date_text
    return prompt_for_delivery_method(update, context, product_type="بصامة")

# --- [دوال المحادثات الخاصة بمناديل كتب الكتاب] --- 
def get_wedding_tissues_items():
    return wedding_tissues_submenu

def start_tissue_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = get_wedding_tissues_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['tissue_product'] = selected_product
    context.user_data['state'] = GET_TISSUE_NAMES
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="wedding_tissues")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
        
    return GET_TISSUE_NAMES

def back_to_tissue_names(update, context):
    query = update.callback_query
    query.answer()
    selected_product = context.user_data.get('tissue_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="wedding_tissues")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_TISSUE_NAMES

def save_tissue_names_ask_date(update, context):
    names = update.message.text
    context.user_data['tissue_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_tissue_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_TISSUE_DATE

def receive_tissue_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['tissue_date'] = date_text
    return prompt_for_delivery_method(update, context, product_type="منديل كتب كتاب")

# --- [دوال المحادثات الخاصة بالمرايا] --- 
def get_mirrors_items():
    return mirrors_submenu

def start_mirror_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = get_mirrors_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['mirror_product'] = selected_product
    context.user_data['state'] = GET_MIRROR_SIZE
    
    keyboard = [
        [InlineKeyboardButton("مقاس 1 (سعر 100 ج)", callback_data="size_1")],
        [InlineKeyboardButton("مقاس 2 (سعر 200 ج)", callback_data="size_2")],
        [InlineKeyboardButton("مقاس 3 (سعر 300 ج)", callback_data="size_3")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="mirrors")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}**\n\nبرجاء **تحديد المقاس المطلوب** من القائمة التالية:"
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    return GET_MIRROR_SIZE

def back_to_mirrors_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    try:
        query.message.delete()
    except Exception:
        pass
    show_product_page(update, "mirrors", mirrors_submenu, is_direct_list=True)
    return ConversationHandler.END

def save_mirror_size_ask_name(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    size_price = ""
    size_label = ""
    
    if data == "size_1":
        size_price = "100 ج"
        size_label = "مقاس 1"
    elif data == "size_2":
        size_price = "200 ج"
        size_label = "مقاس 2"
    elif data == "size_3":
        size_price = "300 ج"
        size_label = "مقاس 3"
    else:
        return GET_MIRROR_SIZE

    if 'mirror_product' in context.user_data:
        context.user_data['mirror_product']['price'] = size_price
        
    context.user_data['mirror_size'] = size_label
    context.user_data['state'] = GET_MIRROR_NAME
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="mirrors")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ تم اختيار **{size_label}** بسعر **{size_price}**.\n\nمن فضلك الآن **اكتب اسم العروسة المطلوب حفره على المرايا** في رسالة نصية بالأسفل، أو اضغط زر رجوع للإلغاء:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_MIRROR_NAME

def receive_mirror_name_and_finish(update, context):
    name = update.message.text
    context.user_data['mirror_name'] = name
    return prompt_for_delivery_method(update, context, product_type="مرايا")


# --- [🔥 دوال المحادثات الخاصة بـ يد الهوايا] ---
def get_fans_items():
    return fans_submenu

def start_fan_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = get_fans_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['fan_product'] = selected_product
    context.user_data['state'] = GET_FAN_NAME
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="fans")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\nبرجاء كتابة **اسم العروسة المطلوب كتابته علي يد الهوايا** في رسالة نصية بالأسفل،\nأو اضغط رجوع للعودة الي القائمة السابقة."
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
        
    return GET_FAN_NAME

def back_to_fans_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    try:
        query.message.delete()
    except Exception:
        pass
    show_product_page(update, "fans", fans_submenu, is_direct_list=True)
    return ConversationHandler.END

def receive_fan_name_and_finish(update, context):
    name = update.message.text
    context.user_data['fan_name'] = name
    return prompt_for_delivery_method(update, context, product_type="يد هوايا")


# --- [🔥 دوال المحادثات الخاصة بـ ساعات الزجاج] ---

def get_clocks_items():
    return clocks_submenu

def start_clock_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = get_clocks_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['clock_product'] = selected_product
    context.user_data['state'] = GET_CLOCK_SIZE
    
    keyboard = [
        [InlineKeyboardButton("مقاس 1 (سعر 100 ج)", callback_data="clock_size_1")],
        [InlineKeyboardButton("مقاس 2 (سعر 200 ج)", callback_data="clock_size_2")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="clocks")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}**\n\nبرجاء **تحديد المقاس المطلوب** من القائمة التالية:"
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
        
    return GET_CLOCK_SIZE

def back_to_clocks_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    try:
        query.message.delete()
    except Exception:
        pass
    show_product_page(update, "clocks", clocks_submenu, is_direct_list=True)
    return ConversationHandler.END

def save_clock_size_ask_photo(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    size_price = ""
    size_label = ""
    
    if data == "clock_size_1":
        size_price = "100 ج"
        size_label = "مقاس 1"
    elif data == "clock_size_2":
        size_price = "200 ج"
        size_label = "مقاس 2"
    else:
        return GET_CLOCK_SIZE

    if 'clock_product' in context.user_data:
        context.user_data['clock_product']['price'] = size_price
        
    context.user_data['clock_size'] = size_label
    context.user_data['state'] = GET_CLOCK_PHOTO
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="clocks")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ تم اختيار **{size_label}** بسعر **{size_price}**.\n\nمن فضلك الآن **أرفق الصورة المطلوب طباعتها على الساعة**، أو اضغط زر رجوع للإلغاء:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_CLOCK_PHOTO

def receive_clock_photo_and_finish(update, context):
    if not update.message.photo:
        update.effective_message.reply_text("⛔️ عذراً، يجب إرسال صورة فقط. يرجى إرسال الصورة المطلوب طباعتها.")
        return GET_CLOCK_PHOTO

    photo_file = update.message.photo[-1].get_file()
    photo_link = photo_file.file_path
    
    context.user_data['clock_photo_link'] = photo_link
    return prompt_for_delivery_method(update, context, product_type="ساعة زجاج")


# --- [🔥 دوال المحادثات الخاصة بـ التابلوهات] ---

def start_tabloh_purchase(update, context):
    query = update.callback_query
    query.answer()
    
    context.user_data['state'] = GET_TABLOH_SIZE
    
    keyboard = [
        [InlineKeyboardButton("مقاس 1 (سعر 100 ج)", callback_data="tabloh_100")],
        [InlineKeyboardButton("مقاس 2 (سعر 200 ج)", callback_data="tabloh_200")],
        [InlineKeyboardButton("مقاس 3 (سعر 300 ج)", callback_data="tabloh_300")],
        [InlineKeyboardButton("مقاس 4 (سعر 400 ج)", callback_data="tabloh_400")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    message_text = "🖼️ **قسم التابلوهات**\n\nيرجي اختيار المقاس المطلوب من القائمة التالية:"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_text, reply_markup=reply_markup, parse_mode="Markdown")
    return GET_TABLOH_SIZE

def save_tabloh_size_and_finish(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    price = ""
    size_label = ""
    
    if data == "tabloh_100":
        price = "100 ج"
        size_label = "مقاس 1"
    elif data == "tabloh_200":
        price = "200 ج"
        size_label = "مقاس 2"
    elif data == "tabloh_300":
        price = "300 ج"
        size_label = "مقاس 3"
    elif data == "tabloh_400":
        price = "400 ج"
        size_label = "مقاس 4"
    else:
        if data == "main_menu":
            start(update, context)
            return ConversationHandler.END
        return GET_TABLOH_SIZE

    context.user_data['tabloh_size'] = size_label
    context.user_data['tabloh_price'] = price
    
    try:
        query.message.delete()
    except:
        pass
        
    note_text = "⚠️ **ملحوظة :** سيتم طلب صورة التصميم المطلوب والصور المطلوب تنفيذها علي التصميم في متابعة الطلب علي الواتساب"
    context.bot.send_message(chat_id=update.effective_chat.id, text=note_text, parse_mode="Markdown")
    
    return prompt_for_delivery_method(update, context, product_type="تابلوه")


# --- [🔥 دوال المحادثات الخاصة بالمباخر] ---

def get_mabakher_items():
    return mabakher_submenu

def start_mabkhara_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = get_mabakher_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['mabkhara_product'] = selected_product
    context.user_data['state'] = GET_MABKHARA_DETAILS
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="mabakher")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        "📝 من فضلك **اكتب هنا أي تفاصيل إضافية خاصة بك** (مثل الاسم المطلوب كتابته).\n\n"
        "أو اكتب **'لا يوجد'** إذا لم يكن لديك أي تفاصيل إضافية.\n\n"
        "أو اضغط زر **رجوع** للعودة إلى القائمة السابقة."
    )
    
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
        
    return GET_MABKHARA_DETAILS

def back_to_mabakher_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    try:
        query.message.delete()
    except Exception:
        pass
    show_product_page(update, "mabakher", mabakher_submenu, is_direct_list=True)
    return ConversationHandler.END

def receive_mabkhara_details_and_finish(update, context):
    details = update.message.text
    context.user_data['mabkhara_details'] = details
    return prompt_for_delivery_method(update, context, product_type="مبخرة")


# --- [🔥 دوال المحادثات الخاصة بالحصالات] ---

def start_hasala_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = hasalat_submenu 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['hasala_product'] = selected_product
    context.user_data['state'] = GET_HASALA_TYPE
    
    keyboard = [
        [InlineKeyboardButton("حصالة 5000 (سعر 150 ج)", callback_data="hasala_5000")],
        [InlineKeyboardButton("حصالة 1000 (سعر 100 ج)", callback_data="hasala_1000")],
        [InlineKeyboardButton("حصالة 2000 (سعر 120 ج)", callback_data="hasala_2000")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="hasalat")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}**\n\nبرجاء **تحديد فئة الحصالة المطلوبة** من القائمة التالية:"
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
        
    return GET_HASALA_TYPE

def back_to_hasalat_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    try:
        query.message.delete()
    except Exception:
        pass
    show_product_page(update, "hasalat", hasalat_submenu, is_direct_list=True)
    return ConversationHandler.END

def save_hasala_type_ask_name(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    price = ""
    type_label = ""
    
    if data == "hasala_5000":
        price = "150 ج"
        type_label = "حصالة 5000"
    elif data == "hasala_1000":
        price = "100 ج"
        type_label = "حصالة 1000"
    elif data == "hasala_2000":
        price = "120 ج"
        type_label = "حصالة 2000"
    else:
        return GET_HASALA_TYPE

    if 'hasala_product' in context.user_data:
        context.user_data['hasala_product']['price'] = price
        
    context.user_data['hasala_type'] = type_label
    context.user_data['state'] = GET_HASALA_NAME
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="hasalat")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ تم اختيار **{type_label}** بسعر **{price}**.\n\nمن فضلك الآن **اكتب الاسم المطلوب طباعته على الحصالة** في رسالة نصية بالأسفل، أو اضغط زر رجوع للإلغاء:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_HASALA_NAME

def receive_hasala_name_and_finish(update, context):
    name = update.message.text
    context.user_data['hasala_name'] = name
    return prompt_for_delivery_method(update, context, product_type="حصالة")


# --- [دوال المحادثات الأخرى] --- 
# دوال المحافظ
def back_to_wallets_color(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    show_submenu(update, context, engraved_wallet_submenu, "محافظ محفورة بالاسم", back_callback="main_menu")
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
    
    caption_text = (f"**اختيارك: {selected_wallet_data['label']}** (السعر: *{selected_wallet_data.get('price', 'غير متوفر')}*)\n\nمن فضلك، **اكتب الاسم الذي تريد حفره** على المحفظة في رسالة نصية بالأسفل.او اضغط زر رجوع للعودة الي القائمة السابقة\nأو اضغط زر الرجوع لتغيير لون المحفظة.")
    
    try:
        update.effective_chat.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_wallet_data['image'], caption=caption_text, reply_markup=back_reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest as e:
         update.effective_chat.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=back_reply_markup, parse_mode="Markdown")

    return GET_WALLET_NAME

def receive_wallet_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    context.user_data['wallet_engraving_name'] = engraving_name
    return prompt_for_delivery_method(update, context, product_type="محافظ")


# دوال الأقلام
def back_to_pen_types(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    try:
        query.message.delete()
    except Exception:
        pass
    show_submenu(update, context, aqlam_submenu, "اقلام", back_callback="main_menu")
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
    
    caption_text = (f"**اختيارك: {selected_pen_data['label']}** (السعر: *{selected_pen_data.get('price', 'غير متوفر')}*)\n\nمن فضلك، **اكتب الاسم الذي تريد حفره** على القلم في رسالة نصية بالأسفل.او اضغط زر رجوع للعودة الي القائمة السابقة\nأو اضغط زر الرجوع لتغيير نوع القلم.")
    
    try:
        update.effective_chat.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_pen_data['image'], caption=caption_text, reply_markup=back_reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest as e:
         update.effective_chat.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=back_reply_markup, parse_mode="Markdown")

    return GET_PEN_NAME

def receive_pen_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    context.user_data['pen_engraving_name'] = engraving_name
    return prompt_for_delivery_method(update, context, product_type="اقلام")


# دوال بوكس كتب الكتاب
def get_box_items():
    return katb_kitab_box_submenu

def start_box_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = get_box_items() 
    selected_box = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_box:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['box_product'] = selected_box
    context.user_data['state'] = GET_BOX_COLOR
    
    keyboard = [
        [InlineKeyboardButton("أسود في ذهبي", callback_data="color_black_gold")],
        [InlineKeyboardButton("أبيض في ذهبي", callback_data="color_white_gold")]
    ]
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")]) 
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ **{selected_box['label']}** (السعر: *{selected_box.get('price', 'غير متوفر')}*)\n\nمن فضلك اختر **لون البوكس**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_BOX_COLOR

def save_box_color_ask_names(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    if data == "katb_kitab_box":
        return back_to_box_menu(update, context)

    color_name = "أسود في ذهبي" if data == "color_black_gold" else "أبيض في ذهبي" if data == "color_white_gold" else "غير محدد"
    context.user_data['box_color'] = color_name
    
    selected_box = context.user_data.get('box_product')
    if not selected_box:
        start(update, context)
        return ConversationHandler.END
        
    context.user_data['state'] = GET_BOX_NAMES
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_box_color")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ اختيارك: **{selected_box['label']}** باللون **{color_name}**\n\nمن فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    return GET_BOX_NAMES

def back_to_box_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    try:
        query.message.delete()
    except Exception:
        pass
    show_product_page(update, "katb_kitab_box", katb_kitab_box_submenu, is_direct_list=True)
    return ConversationHandler.END

def receive_box_names_and_finish(update, context):
    names_text = update.message.text
    context.user_data['box_names'] = names_text
    return prompt_for_delivery_method(update, context, product_type="بوكس كتب كتاب")

# دوال صواني اكليريك
def get_akerik_tray_items():
    return sawany_submenu[0]['items']

def start_akerik_tray_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = get_akerik_tray_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['tray_product'] = selected_product
    context.user_data['state'] = GET_TRAY_NAMES
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_akerik")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
        
    return GET_TRAY_NAMES

def back_to_tray_names(update, context):
    query = update.callback_query
    query.answer()
    selected_tray = context.user_data.get('tray_product')
    if not selected_tray:
        start(update, context)
        return ConversationHandler.END
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_akerik")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_TRAY_NAMES

def save_tray_names_ask_date(update, context):
    names = update.message.text
    context.user_data['tray_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_tray_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_TRAY_DATE

def receive_tray_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['tray_date'] = date_text
    return prompt_for_delivery_method(update, context, product_type="صواني شبكة اكليريك")


# دوال صواني خشب
def get_khashab_tray_items():
    return sawany_submenu[1]['items']

def start_khashab_tray_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = get_khashab_tray_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['khashab_tray_product'] = selected_product
    context.user_data['state'] = GET_KHASHAB_TRAY_NAMES
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_khashab")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
        
    return GET_KHASHAB_TRAY_NAMES

def back_to_khashab_tray_names(update, context):
    query = update.callback_query
    query.answer()
    selected_tray = context.user_data.get('khashab_tray_product')
    if not selected_tray:
        start(update, context)
        return ConversationHandler.END
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_khashab")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_KHASHAB_TRAY_NAMES

def save_khashab_tray_names_ask_date(update, context):
    names = update.message.text
    context.user_data['khashab_tray_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_khashab_tray_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_KHASHAB_TRAY_DATE

def receive_khashab_tray_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['khashab_tray_date'] = date_text
    return prompt_for_delivery_method(update, context, product_type="صواني شبكة خشب")


# دوال طارات اكليريك
def get_akerik_taarat_items():
    return taarat_submenu[0]['items']

def start_akerik_taarat_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = get_akerik_taarat_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['taarat_akerik_product'] = selected_product
    context.user_data['state'] = GET_AKRILIK_TAARAT_NAMES
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_akerik")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
        
    return GET_AKRILIK_TAARAT_NAMES

def back_to_akerik_taarat_names(update, context):
    query = update.callback_query
    query.answer()
    selected_taara = context.user_data.get('taarat_akerik_product')
    if not selected_taara:
        start(update, context)
        return ConversationHandler.END
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_akerik")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_AKRILIK_TAARAT_NAMES

def save_akerik_taarat_names_ask_date(update, context):
    names = update.message.text
    context.user_data['taarat_akerik_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_akerik_taarat_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_AKRILIK_TAARAT_DATE

def receive_akerik_taarat_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['taarat_akerik_date'] = date_text
    return prompt_for_delivery_method(update, context, product_type="طارة اكليريك")


# دوال طارات خشب
def get_khashab_taarat_items():
    return taarat_submenu[1]['items']

def start_khashab_taarat_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = get_khashab_taarat_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['taarat_khashab_product'] = selected_product
    context.user_data['state'] = GET_KHASHAB_TAARAT_NAMES
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_khashab")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
        
    return GET_KHASHAB_TAARAT_NAMES

def back_to_khashab_taarat_names(update, context):
    query = update.callback_query
    query.answer()
    selected_taara = context.user_data.get('taarat_khashab_product')
    if not selected_taara:
        start(update, context)
        return ConversationHandler.END
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_khashab")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_KHASHAB_TAARAT_NAMES

def save_khashab_taarat_names_ask_date(update, context):
    names = update.message.text
    context.user_data['taarat_khashab_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_khashab_taarat_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_KHASHAB_TAARAT_DATE

def receive_khashab_taarat_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['taarat_khashab_date'] = date_text
    return prompt_for_delivery_method(update, context, product_type="طارة خشب")


# --- 🔥🔥 دوال خاصة بالمجات الأبيض والسحري (تتطلب صور) 🔥🔥 ---
def start_mug_photos_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")

    product_data = None
    
    for item in mugat_submenu:
        for sub_item in item['items']:
            if sub_item['callback'] == product_callback:
                product_data = sub_item
                break
        if product_data:
            break
            
    if not product_data:
        query.answer("خطأ في المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['direct_product'] = product_data 
    context.user_data['mug_photos_links'] = [] 
    try:
        query.message.delete()
    except:
        pass

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ **{product_data['label']}**\n\nلتنفيذ هذا الطلب، نحتاج إلى **3 صور** للتصميم.\n\n📸 من فضلك أرسل **الصورة الأولى** الآن:",
        parse_mode="Markdown"
    )
    
    return GET_MUG_PHOTOS

def receive_mug_photos(update, context):
    if not update.message.photo:
        update.effective_message.reply_text("⛔️ عذراً، يجب إرسال صورة فقط. يرجى إرسال الصورة المطلوبة.")
        return GET_MUG_PHOTOS

    photo_file = update.message.photo[-1].get_file()
    photo_link = photo_file.file_path
    
    current_photos = context.user_data.get('mug_photos_links', [])
    current_photos.append(photo_link)
    context.user_data['mug_photos_links'] = current_photos
    
    count = len(current_photos)
    
    if count < 3:
        remaining = 3 - count
        update.effective_message.reply_text(f"✅ تم استلام الصورة رقم {count}.\n📸 متبقي {remaining} صور. من فضلك أرسل الصورة التالية:")
        return GET_MUG_PHOTOS
    else:
        update.effective_message.reply_text("✅ تم استلام الصور الثلاث بنجاح.\nجاري تحضير تفاصيل الدفع...")
        
        p_type = "مج (تصميم خاص)" 
        return prompt_for_delivery_method(update, context, product_type=p_type)


# --- 🔥🔥 دوال خاصة بالمج الديجتال (تتطلب اسم الحفر) 🔥🔥 ---

def start_digital_mug_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    product_callback = data.replace("buy_", "")
    
    items_list = mugat_submenu[2]['items']
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['digital_mug_product'] = selected_product
    context.user_data['state'] = GET_DIGITAL_MUG_NAME
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="mugat_digital")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\nمن فضلك **اكتب الاسم الذي تريد حفره** على المج الديجتال في رسالة نصية بالأسفل، أو اضغط زر رجوع للعودة:"
    try:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=selected_product['image'], caption=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    except telegram.error.BadRequest as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    
    return GET_DIGITAL_MUG_NAME

def receive_digital_mug_name(update, context):
    name = update.message.text
    context.user_data['digital_mug_name'] = name
    return prompt_for_delivery_method(update, context, product_type="مج ديجتال")


# دوال الشراء التي لا تحتاج محادثة (تم تعديلها لتطلب إيصال الدفع)
def prepare_whatsapp_link_for_direct_buy(update, context):
    query = update.callback_query
    data = query.data 
    query.answer()
    
    product_callback = data.replace("buy_", "")
    product_data = None
    product_type = ""
    
    items_list = abajorat_submenu
    product_data = next((item for item in items_list if item["callback"] == product_callback), None)
    if product_data:
        product_type = "اباجورة"
        
    if not product_data:
        items_list = sublimation_supplies_submenu
        product_data = next((item for item in items_list if item["callback"] == product_callback), None)
        if product_data:
            product_type = "مستلزمات سبلميشن"
    
    if not product_data:
        for menu_key, menu_label in [("haram", "هرم مكتب"), ("doro3", "درع"), ("mugat", "مج")]:
            for item in all_submenus.get(menu_key, []):
                if item['callback'] == product_callback:
                    product_data = item
                    product_type = menu_label 
                    break 
                if 'items' in item:
                    sub_item = next((si for si in item['items'] if si['callback'] == product_callback), None)
                    if sub_item:
                        product_data = sub_item
                        product_type = menu_label 
                        break
            if product_data:
                break
                
    if not product_data:
        query.answer("عفواً، لا يمكن إتمام هذا الطلب حالياً.", show_alert=True)
        start(update, context)
        return
    
    context.user_data['direct_product'] = product_data
    try:
        query.message.delete()
    except:
        pass

    return prompt_for_delivery_method(update, context, product_type=product_type)

# --------------------------------------------------------------------------------
# 🔥 دالة معالجة أزرار مرحلة الدفع
# --------------------------------------------------------------------------------
def handle_payment_buttons(update, context):
    query = update.callback_query
    data = query.data
    
    if data == "cancel":
        return cancel_and_end(update, context) 

    query.answer("يرجى إرسال إيصال الدفع لإتمام الطلب.", show_alert=True)
    return GET_PAYMENT_RECEIPT


# --------------------------------------------------------------------------------
# 🔥 دوال اختيار طريقة الاستلام والعنوان
# --------------------------------------------------------------------------------

def prompt_for_delivery_method(update, context, product_type):
    context.user_data['temp_product_type_for_delivery'] = product_type
    context.user_data['state'] = GET_DELIVERY_METHOD
    
    keyboard = [
        [InlineKeyboardButton("🏪 استلام من متجرنا (مجاناً)", callback_data="deliv_store")],
        [InlineKeyboardButton("🛵 دليفري داخل مركز البلينا (+30 ج)", callback_data="deliv_balyana")]
    ]
    keyboard.append([InlineKeyboardButton("❌ إلغاء الطلب", callback_data="cancel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg_text = (
        "🚚 **طريقة الاستلام**\n\n"
        "برجاء اختيار طريقة استلام الطلب:\n"
        "1️⃣ **استلام من المتجر:** بدون مصاريف إضافية.\n"
        "2️⃣ **دليفري داخل مركز البلينا:** يتم إضافة 30 ج إلى إجمالي الطلب."
    )
    
    if update.callback_query:
        try:
            update.callback_query.message.delete()
        except:
            pass
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        update.effective_message.reply_text(msg_text, reply_markup=reply_markup, parse_mode="Markdown")

    return GET_DELIVERY_METHOD


def handle_delivery_selection(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    if data == "cancel":
        return cancel_and_end(update, context)
        
    if data == "deliv_store":
        # استلام من المتجر -> لا يحتاج عنوان -> اذهب للدفع مباشرة
        context.user_data['delivery_cost'] = 0
        context.user_data['delivery_method_name'] = "استلام من المتجر (مجاناً)"
        context.user_data['delivery_address'] = "استلام من المتجر" # عنوان افتراضي
        
        product_type = context.user_data.get('temp_product_type_for_delivery', 'منتج')
        return prompt_for_payment_and_receipt(update, context, product_type)
        
    elif data == "deliv_balyana":
        # دليفري -> يحتاج عنوان -> اسأل عن العنوان
        context.user_data['delivery_cost'] = 30
        context.user_data['delivery_method_name'] = "دليفري داخل مركز البلينا (+30 ج)"
        
        try:
            query.message.delete()
        except:
            pass
            
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="📍 **عنوان التوصيل**\n\nيرجي كتابة عنوان الاستلام بوضوح في رسالة نصية:",
            parse_mode="Markdown"
        )
        return GET_DELIVERY_ADDRESS
        
    else:
        return GET_DELIVERY_METHOD


def save_address_and_proceed_payment(update, context):
    address_text = update.message.text
    context.user_data['delivery_address'] = address_text
    
    product_type = context.user_data.get('temp_product_type_for_delivery', 'منتج')
    
    return prompt_for_payment_and_receipt(update, context, product_type)


# --------------------------------------------------------------------------------
# 🔥 دالة طلب الدفع
# --------------------------------------------------------------------------------
def prompt_for_payment_and_receipt(update, context, product_type):
    
    product_data = None
    names_details = ""
    date_details = ""
    
    if product_type == "بصامة":
        product_data = context.user_data.get('bsamat_product')
        names_details = context.user_data.get('bsamat_names')
        date_details = context.user_data.get('bsamat_date')
    elif product_type == "منديل كتب كتاب":
        product_data = context.user_data.get('tissue_product')
        names_details = context.user_data.get('tissue_names')
        date_details = context.user_data.get('tissue_date')
    elif "محافظ" in str(product_type) or product_type == "محافظ": 
        product_data = context.user_data.get('wallet_data')
        names_details = context.user_data.get('wallet_engraving_name')
        if not " - " in str(product_type): 
             product_type = f"محافظ - {product_data['label']}"
    elif "اقلام" in str(product_type) or product_type == "اقلام":
        product_data = context.user_data.get('pen_data')
        names_details = context.user_data.get('pen_engraving_name')
        if not " - " in str(product_type):
             product_type = f"اقلام - {product_data['label']}"
    elif product_type == "بوكس كتب كتاب":
        product_data = context.user_data.get('box_product')
        names_details = context.user_data.get('box_names')
        color_details = context.user_data.get('box_color')
        product_type = f"{product_type} - {product_data['label']} - {color_details}"
    elif product_type == "صواني شبكة اكليريك":
        product_data = context.user_data.get('tray_product')
        names_details = context.user_data.get('tray_names')
        date_details = context.user_data.get('tray_date')
    elif product_type == "صواني شبكة خشب":
        product_data = context.user_data.get('khashab_tray_product')
        names_details = context.user_data.get('khashab_tray_names')
        date_details = context.user_data.get('khashab_tray_date')
    elif product_type == "طارة اكليريك":
        product_data = context.user_data.get('taarat_akerik_product')
        names_details = context.user_data.get('taarat_akerik_names')
        date_details = context.user_data.get('taarat_akerik_date')
    elif product_type == "طارة خشب":
        product_data = context.user_data.get('taarat_khashab_product')
        names_details = context.user_data.get('taarat_khashab_names')
        date_details = context.user_data.get('taarat_khashab_date')
    elif product_type == "مج ديجتال": 
        product_data = context.user_data.get('digital_mug_product')
        names_details = context.user_data.get('digital_mug_name')
    elif "مرايا" in str(product_type) or product_type == "مرايا": 
        product_data = context.user_data.get('mirror_product')
        size_label = context.user_data.get('mirror_size')
        names_details = context.user_data.get('mirror_name')
        if not " - " in str(product_type):
             product_type = f"مرايا - {size_label}"
    elif product_type == "يد هوايا": 
        product_data = context.user_data.get('fan_product')
        names_details = context.user_data.get('fan_name')
    elif "ساعة زجاج" in str(product_type) or product_type == "ساعة زجاج": 
        product_data = context.user_data.get('clock_product')
        size_label = context.user_data.get('clock_size')
        if not " - " in str(product_type):
             product_type = f"ساعة زجاج - {size_label}"
    elif "تابلوه" in str(product_type) or product_type == "تابلوه": 
        size_label = context.user_data.get('tabloh_size')
        price = context.user_data.get('tabloh_price')
        product_data = {'label': 'تابلوه', 'price': price, 'callback': 'tablohat', 'image': 'غير متوفر'}
        if not " - " in str(product_type):
             product_type = f"تابلوه - {size_label}"
    elif product_type == "مبخرة": 
        product_data = context.user_data.get('mabkhara_product')
        names_details = context.user_data.get('mabkhara_details')
    elif "حصالة" in str(product_type) or product_type == "حصالة": 
        product_data = context.user_data.get('hasala_product')
        type_label = context.user_data.get('hasala_type')
        names_details = context.user_data.get('hasala_name')
        if not " - " in str(product_type):
             product_type = f"حصالة - {type_label}"
    elif 'direct_product' in context.user_data: 
        product_data = context.user_data.get('direct_product')
    else:
        update.effective_chat.send_message("حدث خطأ في تجهيز الطلب. يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        context.user_data.clear()
        return ConversationHandler.END

    delivery_cost = context.user_data.get('delivery_cost', 0)
    original_price = product_data.get('price', 'غير محدد')
    final_price_str = get_total_price_string(original_price, delivery_cost)

    context.user_data['final_product_type'] = product_type
    context.user_data['final_product_label'] = product_data.get('label', product_type)
    context.user_data['final_price'] = final_price_str 
    context.user_data['final_names'] = names_details if names_details else 'غير مطلوب'
    context.user_data['final_date'] = date_details if date_details else 'غير مطلوب'
    context.user_data['final_code'] = product_data.get('callback', 'N/A')
    context.user_data['final_product_image'] = product_data.get('image', 'غير متوفر') 
    
    delivery_msg = f"\n🚚 *طريقة الاستلام:* {context.user_data.get('delivery_method_name', '')}"
    address_msg = ""
    if context.user_data.get('delivery_address') and context.user_data.get('delivery_address') != "استلام من المتجر":
        address_msg = f"\n📍 *العنوان:* {context.user_data.get('delivery_address')}"

    payment_message = (
        f"✅ *طلبك جاهز:* {context.user_data['final_product_label']}\n"
        f"{delivery_msg}{address_msg}\n"
        f"💰 *السعر الإجمالي:* {context.user_data['final_price']}\n\n"
        f"⚠️ **ملحوظة : سيتم تجهيز الاوردر الخاص بك خلال يومين من تاكيد عملية الدفع**\n\n"
        f"من فضلك قم بتحويل المبلغ على محفظة فودافون كاش علي رقم <u><code>{VODAFONE_CASH_NUMBER}</code></u>.\n\n"
        f"👇 **اضغط على زر النسخ بالأسفل ليظهر الرقم في خانة الرسالة لنسخه بسهولة**.\n\n"
        f"بعد التحويل، **يرجى إرسال صورة إيصال التحويل في رسالة بالأسفل** لإتمام الطلب.\n\n"
        f"أو اضغط إلغاء للعودة للقائمة الرئيسية."
    )
    
    keyboard = [
        [InlineKeyboardButton("📞 نسخ رقم المحفظة مباشرة (اضغط هنا)", switch_inline_query_current_chat=f" {VODAFONE_CASH_NUMBER}")],
        [InlineKeyboardButton("❌ إلغاء الطلب", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        try:
            update.callback_query.message.delete()
        except:
            pass
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=payment_message, reply_markup=reply_markup, parse_mode="HTML")

    context.user_data['state'] = GET_PAYMENT_RECEIPT
    return GET_PAYMENT_RECEIPT


# --------------------------------------------------------------------------------
# 🔥 دالة معالجة إيصال الدفع
# --------------------------------------------------------------------------------
def handle_payment_photo(update, context):
    
    if context.user_data.get('state') != GET_PAYMENT_RECEIPT:
        update.effective_chat.send_message("عفواً، لا يمكنني معالجة هذه الصورة الآن. يرجى البدء بطلب جديد.")
        context.user_data.clear()
        return ConversationHandler.END

    if not (update.message and update.message.photo):
        update.effective_chat.send_message("عفواً، يرجى إرسال صورة الإيصال فقط في هذه الخطوة.")
        return GET_PAYMENT_RECEIPT
        
    try:
        photo_file_id = update.message.photo[-1].file_id
        new_file = context.bot.get_file(photo_file_id)
        receipt_url = new_file.file_path 
    except Exception as e:
        context.bot.send_message(update.effective_chat.id, f"حدث خطأ أثناء محاولة الحصول على رابط الصورة: {e}")
        return ConversationHandler.END

    product_type = context.user_data.get('final_product_type', 'غير متوفر')
    product_label = context.user_data.get('final_product_label', 'غير متوفر')
    paid_amount = context.user_data.get('final_price', 'غير متوفر')
    names_text = context.user_data.get('final_names', 'غير مطلوب')
    date_text = context.user_data.get('final_date', 'غير مطلوب')
    product_code = context.user_data.get('final_code', 'N/A')
    delivery_info = context.user_data.get('delivery_method_name', 'غير محدد')
    delivery_addr = context.user_data.get('delivery_address', 'غير محدد')
    
    product_image_url = context.user_data.get('final_product_image', 'غير متوفر') 

    mug_photos = context.user_data.get('mug_photos_links', [])
    mug_photos_text = ""
    if mug_photos:
        mug_photos_text = "\n\n🔗 **صور التصميم المرفقة:**\n"
        for i, link in enumerate(mug_photos):
            mug_photos_text += f" صورة {i+1}: {link}\n"
            
    clock_photo = context.user_data.get('clock_photo_link', None)
    if clock_photo:
        mug_photos_text += f"\n🔗 **الصورة المطلوب طباعتها على الساعة:**\n {clock_photo}\n"
    
    user_info = update.message.from_user
    telegram_contact_link = f"tg://user?id={user_info.id}" 

    message_body = (
        f"🔔 *طلب شراء جديد (مدفوع)* 🔔\n\n"
        f"نوع المنتج: {product_type.replace('-', ' - ')}\n"
        f"المنتج: {product_label}\n"
        f"طريقة الاستلام: {delivery_info}\n"
        f"العنوان: {delivery_addr}\n"
        f"السعر المدفوع: *{paid_amount}*\n\n"
        f"الأسماء (أو الحفر): {names_text}\n"
        f"التاريخ: {date_text}\n"
        f"{mug_photos_text}\n" 
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
        text=f"تم استلام إيصال الدفع بنجاح. تفاصيل الطلب جاهزة:\n\nالمنتج: {product_label}\nالاستلام: {delivery_info}\nالسعر: {paid_amount}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    
    context.user_data.clear()
    return ConversationHandler.END

# --------------------------------------------------------------------------------
# 4. دالة button لمعالجة الأزرار (Callback Queries) 
# --------------------------------------------------------------------------------
def button(update, context):
    query = update.callback_query
    data = query.data
    
    if data == "cancel":
        return cancel_and_end(update, context)

    if data == "main_menu":
        start(update, context)
        return
        
    if data in ["sawany", "taarat", "haram", "doro3", "mugat", "aqlam", "engraved_wallet"]: 
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        show_submenu(update, context, all_submenus[data], title, back_callback="main_menu")
        return
        
    if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "mirrors", "fans", "sublimation", "clocks", "mabakher", "hasalat"]: 
        submenu_list = all_submenus.get(data)
        if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "mirrors", "fans", "sublimation", "clocks", "mabakher", "hasalat"]: 
            show_product_page(update, data, submenu_list, is_direct_list=True)
            return

    product_list_keys = [
        "sawany_akerik", "sawany_khashab", "taarat_akerik", "taarat_khashab", 
        "haram_akerik", "haram_metal", "haram_khashab", "doro3_akerik", 
        "doro3_metal", "doro3_qatifah", "doro3_khashab", "mugat_white", 
        "mugat_magic", "mugat_digital"
    ]
    if data in product_list_keys:
        submenu_list = next((item['items'] for menu_list in all_submenus.values() for item in menu_list if item['callback'] == data), None)
        if submenu_list:
            show_product_page(update, data, submenu_list, is_direct_list=False)
            return

    if data.startswith("buy_"):
        
        if "mugat_white" in data or "mugat_magic" in data:
             start_mug_photos_purchase(update, context)
             return

        if "mugat_digital" in data:
             start_digital_mug_purchase(update, context)
             return
             
        if "mirror" in data:
             start_mirror_purchase(update, context)
             return
        
        if "fan" in data:
             start_fan_purchase(update, context)
             return

        if "clock" in data:
             start_clock_purchase(update, context)
             return

        if "mabkhara" in data:
             start_mabkhara_purchase(update, context)
             return

        if "hasala" in data:
             start_hasala_purchase(update, context)
             return
             
        prepare_whatsapp_link_for_direct_buy(update, context)
        return
        
    if data in ["back_to_pen_types", "back_to_wallets_color"]:
        query.answer("يرجى إتمام العملية الجارية أو الضغط على /start للبدء من جديد.", show_alert=True)
        return
        
    query.answer("إجراء غير معروف.", show_alert=True)
    start(update, context) 

def handle_messages(update, context):
    user_name = update.effective_user.first_name
    update.effective_message.reply_text(
        f"عفواً {user_name}، لا يمكنني فهم طلبك حالياً. يمكنك استخدام /start للبدء من جديد أو اختيار منتج من القوائم.", 
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]])
    )
    

# --------------------
# 5. دالة main لتشغيل البوت
# --------------------

def main():
    TOKEN = os.environ.get('TOKEN') 
    if not TOKEN:
         print("Error: BOT_TOKEN environment variable is not set. Please set it or hardcode the token.")
         return
         
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # تعريف معالجات المحادثات
    # الترتيب: GET_DELIVERY_METHOD -> (GET_DELIVERY_ADDRESS if needed) -> GET_PAYMENT_RECEIPT
    
    # 1. بوكس كتب الكتاب
    box_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_box_purchase, pattern='^buy_box_.*')],
        states={
            GET_BOX_COLOR: [CallbackQueryHandler(save_box_color_ask_names, pattern='^color_.*$|^katb_kitab_box$')],
            GET_BOX_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, receive_box_names_and_finish),
                CallbackQueryHandler(back_to_box_menu, pattern='^katb_kitab_box$')
            ],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_box_menu, pattern='^back_to_box_color$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 2. صواني شبكة اكليريك
    tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_tray_purchase, pattern='^buy_akerik_.*')],
        states={
            GET_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_akerik$') 
            ],
            GET_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_tray_date_and_finish)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_tray_names, pattern='^back_to_tray_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # صواني شبكة خشب
    khashab_tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_tray_purchase, pattern='^buy_khashab_.*')],
        states={
            GET_KHASHAB_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_khashab$') 
            ],
            GET_KHASHAB_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_khashab_tray_date_and_finish)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_khashab_tray_names, pattern='^back_to_khashab_tray_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # طارات اكليريك
    akerik_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_taarat_purchase, pattern='^buy_taarat_akerik_.*')],
        states={
            GET_AKRILIK_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_akerik_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_akerik$')
            ],
            GET_AKRILIK_TAARAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_akerik_taarat_date_and_finish)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_akerik_taarat_names, pattern='^back_to_akerik_taarat_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # طارات خشب
    khashab_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_taarat_purchase, pattern='^buy_taarat_khashab_.*')],
        states={
            GET_KHASHAB_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_khashab$')
            ],
            GET_KHASHAB_TAARAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_khashab_taarat_date_and_finish)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_khashab_taarat_names, pattern='^back_to_khashab_taarat_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # بصامات
    bsamat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_bsamat_purchase, pattern='^buy_bsamat_.*')],
        states={
            GET_BSAMAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_bsamat_names_ask_date),
                CallbackQueryHandler(button, pattern='^bsamat$')
            ],
            GET_BSAMAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_bsamat_date_and_finish)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_bsamat_names, pattern='^back_to_bsamat_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # مناديل كتب الكتاب
    tissue_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tissue_purchase, pattern='^buy_tissue_.*')],
        states={
            GET_TISSUE_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tissue_names_ask_date),
                CallbackQueryHandler(button, pattern='^wedding_tissues$') 
            ],
            GET_TISSUE_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_tissue_date_and_finish)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_tissue_names, pattern='^back_to_tissue_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # محافظ محفورة بالاسم
    engraved_wallet_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prompt_for_name, pattern='^wallet_.*$')],
        states={
            GET_WALLET_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_wallet_name_and_prepare_whatsapp)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_wallets_color, pattern='^back_to_wallets_color$|^engraved_wallet$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # اقلام محفورة بالاسم
    engraved_pen_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prompt_for_pen_name, pattern='^aqlam_metal$|^aqlam_luminous$')],
        states={
            GET_PEN_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_pen_types, pattern='^back_to_pen_types$|^aqlam$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 🔥🔥 معالج خاص للمجات الأبيض والسحري
    mug_photos_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_mug_photos_purchase, pattern='^buy_mugat_(white|magic)_.*')],
        states={
            GET_MUG_PHOTOS: [MessageHandler(Filters.photo, receive_mug_photos)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
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
    
    # 🔥🔥 معالج خاص للمج الديجتال
    digital_mug_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_digital_mug_purchase, pattern='^buy_mugat_digital_.*')],
        states={
            GET_DIGITAL_MUG_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_digital_mug_name),
                CallbackQueryHandler(button, pattern='^mugat_digital$') 
            ],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
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

    # 🔥🔥 معالج خاص للمرايا
    mirrors_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_mirror_purchase, pattern='^buy_mirror_.*')],
        states={
            GET_MIRROR_SIZE: [CallbackQueryHandler(save_mirror_size_ask_name, pattern='^size_.*')],
            GET_MIRROR_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_mirror_name_and_finish)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_mirrors_menu, pattern='^mirrors$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 🔥🔥 معالج خاص ليد الهوايا
    fans_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_fan_purchase, pattern='^buy_fan_.*')],
        states={
            GET_FAN_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_fan_name_and_finish)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_fans_menu, pattern='^fans$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 🔥🔥 معالج خاص لساعات الزجاج
    clocks_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_clock_purchase, pattern='^buy_clock_.*')],
        states={
            GET_CLOCK_SIZE: [CallbackQueryHandler(save_clock_size_ask_photo, pattern='^clock_size_.*')],
            GET_CLOCK_PHOTO: [MessageHandler(Filters.photo, receive_clock_photo_and_finish)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_clocks_menu, pattern='^clocks$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 🔥🔥 معالج خاص للتابلوهات
    tablohat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tabloh_purchase, pattern='^tablohat$')],
        states={
            GET_TABLOH_SIZE: [CallbackQueryHandler(save_tabloh_size_and_finish, pattern='^tabloh_.*')],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
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

    # 🔥🔥 معالج خاص للمباخر
    mabakher_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_mabkhara_purchase, pattern='^buy_mabkhara_.*')],
        states={
            GET_MABKHARA_DETAILS: [MessageHandler(Filters.text & ~Filters.command, receive_mabkhara_details_and_finish)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_mabakher_menu, pattern='^mabakher$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 🔥🔥 معالج خاص للحصالات
    hasalat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_hasala_purchase, pattern='^buy_hasala_.*')],
        states={
            GET_HASALA_TYPE: [CallbackQueryHandler(save_hasala_type_ask_name, pattern='^hasala_.*')],
            GET_HASALA_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_hasala_name_and_finish)],
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_hasalat_menu, pattern='^hasalat$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # معالج الطلبات المباشرة
    direct_buy_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prepare_whatsapp_link_for_direct_buy, pattern='^buy_(abajora|haram|doro3|subli)_.*')], 
        states={
            GET_DELIVERY_METHOD: [CallbackQueryHandler(handle_delivery_selection, pattern='^deliv_.*$|^cancel$')],
            GET_DELIVERY_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address_and_proceed_payment)],
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
    
    dp.add_handler(box_handler)
    dp.add_handler(tray_handler)
    dp.add_handler(khashab_tray_handler)
    dp.add_handler(akerik_taarat_handler) 
    dp.add_handler(khashab_taarat_handler) 
    dp.add_handler(bsamat_handler) 
    dp.add_handler(tissue_handler) 
    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler)
    
    dp.add_handler(mug_photos_handler)
    dp.add_handler(digital_mug_handler) 

    dp.add_handler(mirrors_handler)
    dp.add_handler(fans_handler)
    dp.add_handler(clocks_handler)
    dp.add_handler(tablohat_handler)
    dp.add_handler(mabakher_handler)
    dp.add_handler(hasalat_handler)
    
    dp.add_handler(direct_buy_handler) 

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button)) 
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()