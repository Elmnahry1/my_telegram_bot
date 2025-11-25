import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# تم استيراد Updater بدلاً من Application
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات الواتساب ورقم فودافون كاش
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
GET_AKRILIK_TAARAT_DATE = 10 # حالة تاريخ طارات اكليريك
GET_KHASHAB_TAARAT_NAMES = 11 # حالة أسماء طارات خشب
GET_KHASHAB_TAARAT_DATE = 12 # حالة تاريخ طارات خشب
GET_BSAMAT_NAMES = 13  # حالة كتابة أسماء العرسان للبصامات
GET_BSAMAT_DATE = 14   # حالة كتابة التاريخ للبصامات
GET_TISSUE_NAMES = 15  # حالة كتابة أسماء العرسان للمناديل
GET_TISSUE_DATE = 16   # حالة كتابة التاريخ للمناديل

# 🔥 الحالة الجديدة لطلب إيصال الدفع
GET_PAYMENT_RECEIPT = 17 

# 🔥 الحالة الجديدة لطلب صور المجات (أبيض/سحري)
GET_MUG_PHOTOS = 18

# 🔥🔥 الحالة الجديدة لاسم المج الديجتال
GET_DIGITAL_MUG_NAME = 19

# 🔥 الحالة الجديدة لاسم يد الهوايا
GET_HWAYA_NAME = 20


# --------------------
# 2. بيانات القوائم والمنتجات (تم إضافة السعر لكل منتج)
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

# 🔥 قائمة مستلزمات سبلميشن الجديدة
sublimation_supplies_submenu = [
    {"label": "مج سحري فارغ (درجة أولي)", "callback": "subli_magic_mug", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "مج سيراميك سحري فارغ جاهز للطباعة الحرارية، درجة أولي ممتاز.", "price": "60 ج"},
    {"label": "تيشيرت قطن جاهز للسبلميشن", "callback": "subli_tshirt_cotton", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "تيشيرت قطن مجهز بطبقة سبلميشن، متوفر بجميع المقاسات.", "price": "100 ج"}
]

# 🔥 قائمة يد الهوايا الجديدة
hwaya_Wedding_submenu = [
    {"label": "يد هوايا موديل 1", "callback": "hwaya_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف يد هوايا موديل 1، تصميم مزخرف.", "price": "150 ج"},
    {"label": "يد هوايا موديل 2", "callback": "hwaya_m2", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "وصف يد هوايا موديل 2، تصميم عصري.", "price": "180 ج"}
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
    {"label": "💍 مرايا محفورة بأسم العروسة", "callback": "Miror_Wedding"},
    {"label": "💍 يد هوايا محفورة بأسم العروسة", "callback": "hwaya_Wedding"},
    {"label": "🗄️ هرم مكتب", "callback": "haram"},
    {"label": "🏆 دروع", "callback": "doro3"},
    {"label": "💡 اباجورات", "callback": "abajorat"}, 
    {"label": "✏️ اقلام", "callback": "aqlam"}, 
    {"label": "☕ مجات", "callback": "mugat"},
    {"label": "ساعات زجاج بالصورة", "callback": "clock"},
    {"label": "تابلوهات", "callback": "tablue"},
    {"label": "مباخر", "callback": "mbakher"},
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"}, 
    {"label": "🖨️ مستلزمات سبلميشن", "callback": "sublimation"} # 🔥 الزر الجديد
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
    "sublimation": sublimation_supplies_submenu, # 🔥 إضافة القائمة الجديدة
    "hwaya_Wedding": hwaya_Wedding_submenu, # 🔥 إضافة قائمة يد الهوايا
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box", "sublimation", "hwaya_Wedding"]: # 🔥 إضافة 'hwaya_Wedding'
        # للقوائم المباشرة، نضيف كل منتج مباشرة
        for product in submenu_list:
            # بالنسبة للأقلام والمحافظ (التي تبدأ محادثة مباشرة) يجب أن يتم معالجتها
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

# 🛑 الدالة الجديدة: لإلغاء أي محادثة جارية والعودة للقائمة الرئيسية
def cancel_and_end(update, context):
    query = update.callback_query
    if query:
        # إشعار سريع للمستخدم
        query.answer("تم إلغاء العملية الحالية. يرجى اختيار طلبك مرة أخرى.", show_alert=True)
        # محاولة حذف الرسالة القديمة لتجنب ارتباك المستخدم
        try:
            query.message.delete()
        except Exception:
            pass
    
    # مسح حالة المحادثة المؤقتة
    context.user_data.clear()
    
    # العودة للقائمة الرئيسية لبدء عملية جديدة نظيفة
    start(update, context) 
    
    # إنهاء المحادثة بشكل صريح
    return ConversationHandler.END


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
        # ⚠️ ملاحظة: لا نستخدم buy_ هنا بل نستخدم callback_data لتمكين زر الشراء لاحقاً
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
        

def show_product_page(update, product_callback_data, product_list, is_direct_list=False):
    query = update.callback_query
    if query:
        query.answer()

    # نحذف رسالة القائمة السابقة
    if query and query.message:
        try:
            query.message.delete()
        except Exception:
            pass
    
    # ⚠️ product_list هنا هي قائمة المنتجات المراد عرضها
    for item in product_list:
        # هنا كان يتم إظهار زر الشراء الذي ينفذ مسار المحادثة
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
    
    # تحديد زر الرجوع
    
    # 1. إذا كانت قائمة مباشرة من القائمة الرئيسية (مثل بصمات، أباجورات)
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation", "hwaya_Wedding"]: # 🔥 إضافة 'hwaya_Wedding'
        back_callback = "main_menu"
        back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
    # 2. قوائم المستوى الثاني (مثل صواني اكليريك/خشب) تعود للقائمة الأم (صواني)
    elif product_to_submenu_map.get(product_callback_data) in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        back_callback = product_to_submenu_map.get(product_callback_data)
        back_text = "🔙 اضغط للرجوع إلى القائمة الفرعية"
    # 3. الافتراضي
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


# --- [دوال المحادثات الخاصة بالبصامات] ---
def get_bsamat_items():
    return bsamat_submenu

def start_bsamat_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_bsamat_m1
    product_callback = data.replace("buy_", "")
    
    # 1. Get product data
    items_list = get_bsamat_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['bsamat_product'] = selected_product
    context.user_data['state'] = GET_BSAMAT_NAMES
    
    # 2. Prepare keyboard (Back button to bsamat menu)
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="bsamat")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # 3. Send message asking for names
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        # Fallback in case of image error
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    return GET_BSAMAT_NAMES

def back_to_bsamat_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear() # نمسح أي بيانات قديمة
    # نحاكي عملية العودة للقائمة الفرعية
    try:
        query.message.delete()
    except Exception:
        pass
    # إعادة عرض قائمة البصامات
    show_product_page(update, "bsamat", get_bsamat_items(), is_direct_list=True)
    return ConversationHandler.END


def save_bsamat_names_ask_date(update, context):
    names = update.message.text
    context.user_data['bsamat_names'] = names
    
    selected_product = context.user_data.get('bsamat_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END
        
    # زر الرجوع هنا يعود لطلب الأسماء مرة أخرى
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_bsamat_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_BSAMAT_DATE

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
        
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="من فضلك أعد كتابة **اسم العريس والعروسة**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_BSAMAT_NAMES

def receive_bsamat_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['bsamat_date'] = date_text
    return prompt_for_payment_and_receipt(update, context, product_type="بصامة")


# --- [دوال المحادثات الخاصة بمناديل كتب الكتاب] ---
def get_wedding_tissues_items():
    return wedding_tissues_submenu

def start_tissue_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_tissue_m1
    product_callback = data.replace("buy_", "")
    
    # 1. Get product data
    items_list = get_wedding_tissues_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['tissue_product'] = selected_product
    context.user_data['state'] = GET_TISSUE_NAMES
    
    # 2. Prepare keyboard (Back button to tissues menu)
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="wedding_tissues")]] # wedding_tissues will be handled by the fallback back_to_tissue_menu
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # 3. Send message asking for names
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        # Fallback in case of image error
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    return GET_TISSUE_NAMES

def back_to_tissue_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear() # نمسح أي بيانات قديمة
    # نحاكي عملية العودة للقائمة الفرعية
    try:
        query.message.delete()
    except Exception:
        pass
    # إعادة عرض قائمة مناديل كتب الكتاب
    show_product_page(update, "wedding_tissues", get_wedding_tissues_items(), is_direct_list=True)
    return ConversationHandler.END
    

def save_tissue_names_ask_date(update, context):
    names = update.message.text
    context.user_data['tissue_names'] = names
    
    selected_product = context.user_data.get('tissue_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END
        
    # زر الرجوع هنا يعود لطلب الأسماء مرة أخرى
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_tissue_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_TISSUE_DATE

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
        
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="من فضلك أعد كتابة **اسم العريس والعروسة**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_TISSUE_NAMES
    

def receive_tissue_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['tissue_date'] = date_text
    return prompt_for_payment_and_receipt(update, context, product_type="منديل كتب كتاب")


# --- [دوال المحادثات الخاصة بيد الهوايا] ---
def get_hwaya_items():
    return hwaya_Wedding_submenu

def back_to_hwaya_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear() 
    try:
        query.message.delete()
    except Exception:
        pass
    # إعادة عرض قائمة يد الهوايا
    show_product_page(update, "hwaya_Wedding", get_hwaya_items(), is_direct_list=True)
    return ConversationHandler.END

def start_hwaya_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_hwaya_m1 or buy_hwaya_m2
    product_callback = data.replace("buy_", "")
    
    # 1. Get product data
    items_list = get_hwaya_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['hwaya_product'] = selected_product
    context.user_data['state'] = GET_HWAYA_NAME
    
    # 2. Prepare keyboard (Back button to hwaya menu)
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="hwaya_Wedding")]] # hwaya_Wedding will be handled by the fallback back_to_hwaya_menu
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # 3. Send message asking for the name
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك **اكتب اسم العروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة للقائمة السابقة:"
    )
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest:
        # Fallback in case of image error or if it's too large/not accessible
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    return GET_HWAYA_NAME

def receive_hwaya_name_and_finish(update, context):
    bride_name = update.message.text
    context.user_data['hwaya_bride_name'] = bride_name
    return prompt_for_payment_and_receipt(update, context, product_type="يد هوايا")


# --- [دوال المحافظ] ---

def get_wallet_items():
    return engraved_wallet_submenu

def back_to_wallets_color(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear() # نمسح أي بيانات قديمة
    # نحاكي عملية العودة للقائمة الفرعية
    try:
        query.message.delete()
    except Exception:
        pass
    # إعادة عرض قائمة المحافظ
    show_product_page(update, "engraved_wallet", get_wallet_items(), is_direct_list=True)
    return ConversationHandler.END


def prompt_for_wallet_name(update, context):
    query = update.callback_query
    data = query.data # wallet_bege, wallet_brown, wallet_black
    query.answer()
    
    selected_wallet_data = next((item for item in engraved_wallet_submenu if item["callback"] == data), None)
    context.user_data['wallet_data'] = selected_wallet_data
    context.user_data['state'] = GET_WALLET_NAME
    
    try:
        # حذف رسالة القائمة الفرعية للمحافظ
        query.message.delete()
    except Exception:
        pass
    
    # زر الرجوع يعود إلى قائمة المحافظ الفرعية (لإعادة اختيار اللون)
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="engraved_wallet")]] 
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    caption_text = (
        f"**اختيارك: {selected_wallet_data['label']}** (السعر: *{selected_wallet_data.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك، **اكتب الاسم الذي تريد حفره** على المحفظة في رسالة نصية بالأسفل.\n"
        "او اضغط زر رجوع للعودة الي القائمة السابقة."
    )
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_wallet_data['image'],
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
        
    return GET_WALLET_NAME

def receive_wallet_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    context.user_data['wallet_engraving_name'] = engraving_name
    return prompt_for_payment_and_receipt(update, context, product_type="محافظ")

# دوال الأقلام
def get_pen_items():
    return aqlam_submenu

def back_to_pen_types(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    try:
        query.message.delete()
    except Exception:
        pass
    # 🔥 نستخدم دالة show_submenu لعرض الأزرار الفرعية للأقلام
    show_product_page(update, "aqlam", get_pen_items(), is_direct_list=True)
    # بما أن show_product_page ترسل رسالة جديدة، لا نحتاج لإرسال رسالة هنا
    return ConversationHandler.END


def prompt_for_pen_name(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    # نستخدم data مباشرة لأنها تحمل callback للأقلام (aqlam_metal/aqlam_luminous)
    selected_pen_data = next((item for item in aqlam_submenu if item["callback"] == data), None)
    context.user_data['pen_data'] = selected_pen_data
    context.user_data['state'] = GET_PEN_NAME
    
    try:
        # حذف رسالة القائمة الفرعية للأقلام
        query.message.delete()
    except Exception:
        pass
    
    # زر الرجوع يعود إلى قائمة الأقلام الفرعية
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="aqlam")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    caption_text = (
        f"**اختيارك: {selected_pen_data['label']}** (السعر: *{selected_pen_data.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك، **اكتب الاسم الذي تريد حفره** على القلم في رسالة نصية بالأسفل.\n"
        "او اضغط زر رجوع للعودة الي القائمة السابقة."
    )
    
    try:
        context.bot.send_photo(
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

def receive_pen_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    context.user_data['pen_engraving_name'] = engraving_name
    return prompt_for_payment_and_receipt(update, context, product_type="قلم")

# دوال بوكس كتب الكتاب
def get_box_items():
    return katb_kitab_box_submenu

def start_box_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_box_m1
    product_callback = data.replace("buy_", "")
    
    # 1. Get product data
    items_list = get_box_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['box_product'] = selected_product
    context.user_data['state'] = GET_BOX_COLOR # تبدأ المحادثة بطلب اللون
    
    # 2. Prepare keyboard (Colors + Back button)
    keyboard = [
        [InlineKeyboardButton("أبيض", callback_data="color_white"), InlineKeyboardButton("بيج (هافان)", callback_data="color_bege")],
        [InlineKeyboardButton("أسود", callback_data="color_black"), InlineKeyboardButton("رمادي", callback_data="color_gray")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")] # الرجوع للقائمة الرئيسية للبوكسات
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # 3. Send message asking for the color
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك **اختر لون البوكس**:"
    )
    
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=selected_product['image'],
        caption=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_BOX_COLOR

def back_to_box_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear() # نمسح أي بيانات قديمة
    # نحاكي عملية العودة للقائمة الفرعية للبوكسات
    try:
        query.message.delete()
    except Exception:
        pass
    # إعادة عرض قائمة بوكسات كتب الكتاب
    show_product_page(update, "katb_kitab_box", katb_kitab_box_submenu, is_direct_list=True)
    return ConversationHandler.END


def save_box_color_ask_names(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    selected_box = context.user_data.get('box_product')
    if not selected_box:
        start(update, context)
        return ConversationHandler.END
        
    color_callback = data.replace("color_", "")
    color_name = {
        'white': 'الأبيض',
        'bege': 'البيج (هافان)',
        'black': 'الأسود',
        'gray': 'الرمادي'
    }.get(color_callback, 'غير محدد')
    
    context.user_data['box_color'] = color_name
    context.user_data['state'] = GET_BOX_NAMES
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_box_color")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ اختيارك: **{selected_box['label']}** باللون **{color_name}**\n\nمن فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_BOX_NAMES


def receive_box_names_and_finish(update, context):
    names_text = update.message.text
    context.user_data['box_names'] = names_text
    return prompt_for_payment_and_receipt(update, context, product_type="بوكس كتب كتاب")


# دوال صواني اكليريك
def get_akerik_tray_items():
    # صواني شبكة اكليريك هي العنصر الأول في قائمة صواني
    return sawany_submenu[0]['items']

def start_akerik_tray_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_akerik_m1
    product_callback = data.replace("buy_", "")
    
    items_list = get_akerik_tray_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['tray_product'] = selected_product
    context.user_data['state'] = GET_TRAY_NAMES
    
    # زر الرجوع يعود لقائمة صواني اكليريك
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_akerik")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        # Fallback in case of image error
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
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
        
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_TRAY_NAMES


def save_tray_names_ask_date(update, context):
    names = update.message.text
    context.user_data['tray_names'] = names
    
    selected_product = context.user_data.get('tray_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END
        
    # زر الرجوع هنا يعود لطلب الأسماء مرة أخرى
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
    date_text = update.message.text
    context.user_data['tray_date'] = date_text
    return prompt_for_payment_and_receipt(update, context, product_type="صينية شبكة اكليريك")


# دوال صواني خشب
def get_khashab_tray_items():
    # صواني شبكة خشب هي العنصر الثاني في قائمة صواني
    return sawany_submenu[1]['items']

def start_khashab_tray_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_khashab_m1
    product_callback = data.replace("buy_", "")
    
    items_list = get_khashab_tray_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['khashab_tray_product'] = selected_product
    context.user_data['state'] = GET_KHASHAB_TRAY_NAMES
    
    # زر الرجوع يعود لقائمة صواني خشب
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_khashab")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        # Fallback in case of image error
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
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
        
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_KHASHAB_TRAY_NAMES


def save_khashab_tray_names_ask_date(update, context):
    names = update.message.text
    context.user_data['khashab_tray_names'] = names
    
    selected_product = context.user_data.get('khashab_tray_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END
        
    # زر الرجوع هنا يعود لطلب الأسماء مرة أخرى
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
    date_text = update.message.text
    context.user_data['khashab_tray_date'] = date_text
    return prompt_for_payment_and_receipt(update, context, product_type="صينية شبكة خشب")


# دوال طارات اكليريك
def get_akerik_taarat_items():
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
    
    # زر الرجوع يعود لقائمة طارات اكليريك
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_akerik")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        # Fallback in case of image error
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
    
    selected_product = context.user_data.get('taarat_akerik_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END
        
    # زر الرجوع هنا يعود لطلب الأسماء مرة أخرى
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
    context.user_data['taarat_akerik_date'] = date_text
    return prompt_for_payment_and_receipt(update, context, product_type="طارة اكليريك")


# دوال طارات خشب
def get_khashab_taarat_items():
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
    
    # زر الرجوع يعود لقائمة طارات خشب
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_khashab")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        # Fallback in case of image error
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
    
    selected_product = context.user_data.get('taarat_khashab_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END
        
    # زر الرجوع هنا يعود لطلب الأسماء مرة أخرى
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
    context.user_data['taarat_khashab_date'] = date_text
    return prompt_for_payment_and_receipt(update, context, product_type="طارة خشب")

# دوال المج الديجتال
def get_digital_mug_items():
    return mugat_submenu[2]['items'] # المج الديجتال هو العنصر الثالث في قائمة المجات

def start_digital_mug_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_mugat_digital_m1
    product_callback = data.replace("buy_", "")
    
    items_list = get_digital_mug_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['digital_mug_product'] = selected_product
    context.user_data['state'] = GET_DIGITAL_MUG_NAME
    
    # زر الرجوع يعود لقائمة المجات الديجتال
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="mugat_digital")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اكتب الاسم الذي تريد حفره** على المج في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        # Fallback in case of image error
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    return GET_DIGITAL_MUG_NAME

def back_to_digital_mug_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    # نحاكي عملية العودة للقائمة الفرعية
    try:
        query.message.delete()
    except Exception:
        pass
    # إعادة عرض قائمة المجات الديجتال
    
    # نستخدم دالة show_product_page لعرض منتجات مج ديجتال
    # أولاً نحصل على القائمة الأم للمجات
    mugat_list = all_submenus.get("mugat")
    # ثم نجد قائمة منتجات المج الديجتال
    digital_mug_items = next((item['items'] for item in mugat_list if item['callback'] == "mugat_digital"), None)
    if digital_mug_items:
        show_product_page(update, "mugat_digital", digital_mug_items, is_direct_list=False)
    else:
        # إذا لم يتم العثور على القائمة نعود للقائمة الرئيسية
        start(update, context) 
        
    return ConversationHandler.END


def receive_digital_mug_name_and_finish(update, context):
    name = update.message.text
    context.user_data['digital_mug_name'] = name
    return prompt_for_payment_and_receipt(update, context, product_type="مج ديجتال")

# 🔥 الدالة الجامعة لمعالجة أزرار القائمة الرئيسية والقوائم الفرعية
def handle_main_menu_clicks(update, context):
    query = update.callback_query
    data = query.data
    query.answer()

    # 1. معالجة زر الرجوع للقائمة الرئيسية
    if data == "main_menu":
        start(update, context)
        return

    # 2. معالجة فتح قوائم المستوى الأول المتداخلة (sawany, taarat, haram, doro3, mugat, aqlam, engraved_wallet)
    if data in ["sawany", "taarat", "haram", "doro3", "mugat", "aqlam", "engraved_wallet"]:
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus[data], clean_title, back_callback="main_menu")
        return

    # 3. معالجة فتح قوائم المستوى الأول المباشرة (bsamat, wedding_tissues, abajorat, katb_kitab_box, sublimation, hwaya_Wedding)
    if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation", "hwaya_Wedding"]: # 🔥 إضافة 'hwaya_Wedding'
        # Find the correct submenu list
        submenu_list = all_submenus.get(data)
        # إذا كانت "بصمات" أو أي قائمة أخرى تحتاج عرض المنتجات أولاً
        if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation", "hwaya_Wedding"]: # 🔥 إضافة 'hwaya_Wedding'
            show_product_page(update, data, submenu_list, is_direct_list=True)
            return
            
    # 4. معالجة عرض صفحات المنتجات مباشرة (قوائم المستوى الثاني)
    product_list_keys = [
        "sawany_akerik", "sawany_khashab", 
        "taarat_akerik", "taarat_khashab",
        "haram_akerik", "haram_metal", "haram_khashab",
        "doro3_akerik", "doro3_metal", "doro3_qatifah", "doro3_khashab",
        "mugat_white", "mugat_magic", "mugat_digital"
    ]
    if data in product_list_keys:
        # البحث عن القائمة الفرعية المناسبة في all_submenus
        submenu_list = next((item['items'] for menu_list in all_submenus.values() for item in menu_list if item['callback'] == data), None)
        if submenu_list:
            show_product_page(update, data, submenu_list, is_direct_list=False)
            return

    # 5. معالجة أزرار الشراء الفردية (للمنتجات التي لا تحتاج محادثة)
    if data.startswith("buy_"):
        # يجب أن يصل إلى هنا المنتجات التي لا تحتاج بيانات (مثل الأباجورات، الدروع، الهرم، المج الأبيض/السحري، مستلزمات السبلميشن)
        # نحتاج دالة لتجهيز رابط الواتساب مباشرة
        return prepare_whatsapp_link_for_direct_buy(update, context) 

    # 6. معالجة الأزرار التي تبدأ محادثة (تم حذفها من هنا، حيث يتم معالجتها كـ entry_points في ConversationHandler)

    # إذا لم يتم التعرف على الـ callback data
    query.answer("عذراً، حدث خطأ غير متوقع.", show_alert=True)


# --------------------------------------------------------------------------------
# 🔥 دالة تجهيز رابط الواتساب للدفع المباشر (للمنتجات التي لا تتطلب محادثة)
# --------------------------------------------------------------------------------
def prepare_whatsapp_link_for_direct_buy(update, context):
    query = update.callback_query
    data = query.data  # buy_abajora_m1
    product_callback = data.replace("buy_", "")
    
    product_data = None
    product_type = "طلب مباشر" # الافتراضي
    
    # 1. البحث في قوائم المنتجات المباشرة (اباجورات, بصمات, مناديل...)
    # *البصامات والمحافظ والأقلام والمناديل والبوكسات والمج الديجتال تعالجها الـ ConversationHandler الخاصة بها*

    # 🔥 البحث في الأباجورات
    items_list = abajorat_submenu
    product_data = next((item for item in items_list if item["callback"] == product_callback), None)
    if product_data:
        product_type = "اباجورة"
        
    # 🔥 البحث في مستلزمات سبلميشن الجديدة
    if not product_data:
        items_list = sublimation_supplies_submenu
        product_data = next((item for item in items_list if item["callback"] == product_callback), None)
        if product_data:
            product_type = "مستلزمات سبلميشن"
            
    # 2. البحث في القوائم المتداخلة (هرم مكتب، دروع، مجات)
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

    # 3. حفظ البيانات وإرسال رسالة الدفع
    context.user_data['direct_product'] = product_data # حفظ بيانات المنتج
    # يجب حذف رسالة الزر القديمة
    try:
        query.message.delete()
    except:
        pass
        
    # 🔥 إذا كان مج أبيض أو سحري، ننتقل لطلب الصور
    if product_callback.startswith("mugat_white") or product_callback.startswith("mugat_magic"):
        context.user_data['state'] = GET_MUG_PHOTOS
        
        caption_text = (
            f"✅ **{product_data['label']}** (السعر: *{product_data.get('price', 'غير متوفر')}*)\n\n"
            "لتنفيذ هذا الطلب، نحتاج إلى **3 صور** للتصميم.\n\n"
            "📸 من فضلك أرسل **الصورة الأولى** الآن:"
        )
        
        back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=product_to_submenu_map.get(product_callback, "main_menu"))]]
        reply_markup = InlineKeyboardMarkup(back_keyboard)
        
        # محاولة إرسال صورة المنتج
        try:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=product_data['image'],
                caption=caption_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        except telegram.error.BadRequest:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=caption_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        
        return GET_MUG_PHOTOS # الانتقال إلى حالة استقبال الصور
    
    # 🔥 لأي منتج آخر يتم شراؤه مباشرة (أباجورات، دروع، أهرامات، سبلميشن)
    return prompt_for_payment_and_receipt(update, context, product_type=product_type)
    

# --------------------------------------------------------------------------------
# 🔥 دالة معالجة أزرار مرحلة الدفع (تم تعديلها لحذف معالج زر النسخ)
# --------------------------------------------------------------------------------
def handle_payment_buttons(update, context):
    """ تعالج أزرار النسخ والإلغاء في مرحلة انتظار الإيصال. """
    query = update.callback_query
    data = query.data
    
    if data == "cancel":
        # الإلغاء
        return cancel_and_end(update, context) # returns ConversationHandler.END
        
    query.answer("تم تنفيذ الإجراء")
    return GET_PAYMENT_RECEIPT # البقاء في نفس الحالة بانتظار إيصال الدفع

# --------------------------------------------------------------------------------
# 🔥 دالة إرسال رسالة الدفع (تُستدعى من كل دالة إنهاء محادثة)
# --------------------------------------------------------------------------------
def prompt_for_payment_and_receipt(update, context, product_type):
    
    # 1. تجميع بيانات الطلب النهائية
    product_data = context.user_data.get('direct_product')
    names_details = context.user_data.get('bsamat_names') or context.user_data.get('tissue_names') or context.user_data.get('box_names') or context.user_data.get('wallet_engraving_name') or context.user_data.get('pen_engraving_name') or context.user_data.get('tray_names') or context.user_data.get('khashab_tray_names') or context.user_data.get('taarat_akerik_names') or context.user_data.get('taarat_khashab_names') or context.user_data.get('digital_mug_name') or context.user_data.get('hwaya_bride_name') # 🔥 إضافة 'hwaya_bride_name'

    date_details = context.user_data.get('bsamat_date') or context.user_data.get('tissue_date') or context.user_data.get('tray_date') or context.user_data.get('khashab_tray_date') or context.user_data.get('taarat_akerik_date') or context.user_data.get('taarat_khashab_date')
    
    # 2. تحديد المنتج والسعر (للتحديثات الأخيرة)
    
    if product_type == "بصامة":
        product_data = context.user_data.get('bsamat_product')
        product_type = f"{product_type} - {product_data['label']}"
    elif product_type == "منديل كتب كتاب":
        product_data = context.user_data.get('tissue_product')
        product_type = f"{product_type} - {product_data['label']}"
    elif product_type == "محافظ":
        product_data = context.user_data.get('wallet_data')
        product_type = f"{product_type} - {product_data['label']}"
    elif product_type == "قلم":
        product_data = context.user_data.get('pen_data')
        product_type = f"{product_type} - {product_data['label']}"
    elif product_type == "يد هوايا": # 🔥 حالة يد الهوايا
        product_data = context.user_data.get('hwaya_product')
        product_type = f"{product_type} - {product_data['label']}"
    elif product_type == "بوكس كتب كتاب":
        product_data = context.user_data.get('box_product')
        color_details = context.user_data.get('box_color')
        product_type = f"{product_type} - {product_data['label']} - {color_details}"
    elif product_type == "صينية شبكة اكليريك":
        product_data = context.user_data.get('tray_product')
        names_details = context.user_data.get('tray_names')
        date_details = context.user_data.get('tray_date')
    elif product_type == "صينية شبكة خشب":
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
    elif product_type == "مج ديجتال": # 🔥 إضافة حالة المج الديجتال
        product_data = context.user_data.get('digital_mug_product')
        names_details = context.user_data.get('digital_mug_name')
        # product_type remains "مج ديجتال"
    elif 'direct_product' in context.user_data: 
        # الأهرامات، الدروع، المجات، الأباجورات، السبلميشن
        product_data = context.user_data.get('direct_product')
        # product_type is already set from prepare_whatsapp_link_for_direct_buy
    else:
        update.effective_chat.send_message("حدث خطأ في تجهيز الطلب. يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ابدأ", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    product_label = product_data.get('label', 'غير متوفر')
    product_price = product_data.get('price', 'غير متوفر')
    product_image_url = product_data.get('image', 'https://example.com/placeholder.jpg')

    # 3. حفظ بيانات الطلب النهائية في الذاكرة لتستخدم في إرسال الواتساب
    context.user_data['final_product_type'] = product_type
    context.user_data['final_product_label'] = product_label
    context.user_data['final_price'] = product_price
    context.user_data['final_names'] = names_details if names_details else 'غير مطلوب'
    context.user_data['final_date'] = date_details if date_details else 'غير مطلوب'
    context.user_data['final_product_image'] = product_image_url
    
    # 4. بناء رسالة العرض للعميل
    details_text = f"**اسم/أسماء العرسان:** {names_details}" if names_details and product_type not in ["يد هوايا", "محافظ", "قلم", "مج ديجتال"] else ""
    if product_type == "يد هوايا":
        details_text = f"**اسم العروسة:** {names_details}"
    elif product_type in ["محافظ", "قلم", "مج ديجتال"]:
        details_text = f"**الاسم للحفر:** {names_details}"
        
    date_text = f"**التاريخ:** {date_details}" if date_details else ""
    
    if details_text or date_text:
        details_text = f"\n\nتفاصيل الطلب: \n{details_text}\n{date_text}"

    payment_message = (
        f"✅ تم تأكيد طلبك: **{product_type}**\n"
        f"السعر الإجمالي: **{product_price}**{details_text}\n\n"
        f"لإتمام الطلب: يرجى تحويل المبلغ المطلوب إلى رقم محفظة فودافون كاش التالي:\n"
        f"📱 **{VODAFONE_CASH_NUMBER}**\n\n"
        f"⚠️ **هام**: بعد التحويل، يرجى **إرسال صورة إيصال الدفع** في رسالة مستقلة لإثبات عملية التحويل والمتابعة في تنفيذ طلبك."
    )
    
    keyboard = [
        [InlineKeyboardButton("🚫 إلغاء الطلب", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # 5. إرسال رسالة الدفع وتغيير الحالة
    update.effective_chat.send_message(
        text=payment_message, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    # 6. تحديث حالة المحادثة
    return GET_PAYMENT_RECEIPT

# --------------------------------------------------------------------------------
# 🔥 دالة استقبال إيصال الدفع وإنهاء الطلب (يتم استدعاؤها من ConversationHandler)
# --------------------------------------------------------------------------------
def handle_payment_photo(update, context):
    # مسح جميع البيانات المتعلقة بمسار الشراء بعد اكتماله
    context.user_data.clear()
    
    # 1. الحصول على رابط إيصال الدفع من تليجرام
    if not (update.message and update.message.photo):
        # ليس صورة، اطلب منه الصورة مرة أخرى
        update.effective_chat.send_message("عفواً، يرجى إرسال صورة الإيصال فقط في هذه الخطوة.")
        return GET_PAYMENT_RECEIPT
        
    try:
        # الحصول على الصورة بأعلى دقة
        photo_file_id = update.message.photo[-1].file_id
        new_file = context.bot.get_file(photo_file_id)
        # هذا هو رابط الصورة المطلوب إرساله إلى الواتساب
        receipt_url = new_file.file_path
    except Exception as e:
        context.bot.send_message(update.effective_chat.id, f"حدث خطأ أثناء محاولة الحصول على رابط الصورة: {e}")
        return ConversationHandler.END

    # 2. استرجاع بيانات الطلب النهائية
    product_type = context.user_data.get('final_product_type', 'غير متوفر')
    product_label = context.user_data.get('final_product_label', 'غير متوفر')
    paid_amount = context.user_data.get('final_price', 'غير متوفر')
    names_text = context.user_data.get('final_names', 'غير مطلوب')
    date_text = context.user_data.get('final_date', 'غير مطلوب')
    product_image_url = context.user_data.get('final_product_image', 'غير متوفر')
    
    # 🔥🔥 استرجاع روابط صور المجات (إن وجدت)
    mug_photos = context.user_data.get('mug_photos_links', [])
    mug_photos_text = ""
    if mug_photos:
        mug_photos_text = "\n\n🔗 **صور التصميم المرفقة:**\n"
        for i, link in enumerate(mug_photos):
            mug_photos_text += f"- الصورة {i+1}: {link}\n"
            
    # 3. بناء رسالة الواتساب النهائية
    whatsapp_text = (
        f"✅ *تم إثبات طلب جديد*\n\n"
        f"**نوع المنتج:** {product_type}\n"
        f"**المنتج:** {product_label}\n"
        f"**السعر المدفوع:** {paid_amount}\n"
        f"**الاسم/الأسماء:** {names_text}\n"
        f"**التاريخ:** {date_text}\n\n"
        f"🔗 **رابط صورة المنتج (للتأكد):** {product_image_url}\n"
        f"🔗 **رابط إيصال الدفع (للتأكيد):** {receipt_url}"
        f"{mug_photos_text}"
    )

    # 4. بناء رابط الواتساب المشفر
    encoded_text = quote_plus(whatsapp_text)
    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    # 5. إرسال رسالة التأكيد للعميل مع رابط الواتساب
    confirmation_message = (
        f"✅ تم استلام الإيصال بنجاح. شكراً لك!\n\n"
        "لإنهاء الطلب وتأكيد موعد التسليم والمتابعة مع فريق التنفيذ، **يرجى الضغط على زر المتابعة** أدناه للتحدث معنا عبر الواتساب:"
    )
    
    whatsapp_keyboard = [[InlineKeyboardButton("📲 المتابعة عبر الواتساب", url=whatsapp_url)]]
    reply_markup = InlineKeyboardMarkup(whatsapp_keyboard)
    
    update.effective_chat.send_message(
        text=confirmation_message, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    # إرسال رسالة التلخيص إلى المشرف (Admin)
    context.bot.send_message(
        chat_id=update.effective_chat.id, # يمكنك تغييرها لـ chat_id المشرف
        text=f"🚨 **إيصال دفع جديد - مطلوب تأكيد** 🚨\n\n{whatsapp_text}",
        parse_mode="Markdown"
    )
    
    # إنهاء المحادثة
    return ConversationHandler.END


# --------------------------------------------------------------------------------
# 4. دالة main لتشغيل البوت وإضافة المعالجات
# --------------------------------------------------------------------------------

def main():
    # 🔥 قم بتعيين توكن البوت الخاص بك هنا أو من متغيرات البيئة
    TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE') 
    if TOKEN == 'YOUR_BOT_TOKEN_HERE':
        # رسالة خطأ أو استخدام قيمة placeholder إذا لم يتم العثور على التوكن
        print("Error: BOT_TOKEN environment variable is not set. Please set it or hardcode the token.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # تعريف معالجات المحادثات
    # جميع المحادثات تنتهي في حالة GET_PAYMENT_RECEIPT
    
    # 1. بوكس كتب الكتاب
    box_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_box_purchase, pattern='^buy_box_.*')],
        states={
            GET_BOX_COLOR: [
                CallbackQueryHandler(save_box_color_ask_names, pattern='^color_.*$'),
                CallbackQueryHandler(back_to_box_menu, pattern='^katb_kitab_box$') # الرجوع من اختيار اللون
            ],
            GET_BOX_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, receive_box_names_and_finish),
                CallbackQueryHandler(back_to_box_menu, pattern='^katb_kitab_box$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_box_menu, pattern='^katb_kitab_box$'), # زر الرجوع في أي حالة يعود للقائمة الرئيسية
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 2. صواني شبكة اكليريك
    tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_tray_purchase, pattern='^buy_akerik_.*')],
        states={
            GET_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tray_names_ask_date),
                CallbackQueryHandler(handle_main_menu_clicks, pattern='^sawany_akerik$') # زر الرجوع يعود لصفحة المنتجات
            ],
            GET_TRAY_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_tray_date_and_finish),
                CallbackQueryHandler(back_to_tray_names, pattern='^back_to_tray_names$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(handle_main_menu_clicks, pattern='^sawany_akerik$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # صواني شبكة خشب
    khashab_tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_tray_purchase, pattern='^buy_khashab_.*')],
        states={
            GET_KHASHAB_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_tray_names_ask_date),
                CallbackQueryHandler(handle_main_menu_clicks, pattern='^sawany_khashab$')
            ],
            GET_KHASHAB_TRAY_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_khashab_tray_date_and_finish),
                CallbackQueryHandler(back_to_khashab_tray_names, pattern='^back_to_khashab_tray_names$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(handle_main_menu_clicks, pattern='^sawany_khashab$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # طارات اكليريك
    akerik_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_taarat_purchase, pattern='^buy_taarat_akerik_.*')],
        states={
            GET_AKRILIK_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_akerik_taarat_names_ask_date),
                CallbackQueryHandler(handle_main_menu_clicks, pattern='^taarat_akerik$')
            ],
            GET_AKRILIK_TAARAT_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_akerik_taarat_date_and_finish),
                CallbackQueryHandler(back_to_akerik_taarat_names, pattern='^back_to_akerik_taarat_names$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(handle_main_menu_clicks, pattern='^taarat_akerik$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # طارات خشب
    khashab_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_taarat_purchase, pattern='^buy_taarat_khashab_.*')],
        states={
            GET_KHASHAB_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_taarat_names_ask_date),
                CallbackQueryHandler(handle_main_menu_clicks, pattern='^taarat_khashab$')
            ],
            GET_KHASHAB_TAARAT_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_khashab_taarat_date_and_finish),
                CallbackQueryHandler(back_to_khashab_taarat_names, pattern='^back_to_khashab_taarat_names$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(handle_main_menu_clicks, pattern='^taarat_khashab$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # بصامات
    bsamat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_bsamat_purchase, pattern='^buy_bsamat_.*')],
        states={
            GET_BSAMAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_bsamat_names_ask_date),
                CallbackQueryHandler(back_to_bsamat_menu, pattern='^bsamat$')
            ],
            GET_BSAMAT_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_bsamat_date_and_finish),
                CallbackQueryHandler(back_to_bsamat_names, pattern='^back_to_bsamat_names$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_bsamat_menu, pattern='^bsamat$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # مناديل كتب الكتاب
    tissue_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tissue_purchase, pattern='^buy_tissue_.*')],
        states={
            GET_TISSUE_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tissue_names_ask_date),
                CallbackQueryHandler(back_to_tissue_menu, pattern='^wedding_tissues$')
            ],
            GET_TISSUE_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_tissue_date_and_finish),
                CallbackQueryHandler(back_to_tissue_names, pattern='^back_to_tissue_names$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_tissue_menu, pattern='^wedding_tissues$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # يد هوايا محفورة بالاسم 🔥
    hwaya_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_hwaya_purchase, pattern='^buy_hwaya_.*')],
        states={
            GET_HWAYA_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_hwaya_name_and_finish),
                # زر الرجوع من مرحلة كتابة الاسم يعود لصفحة المنتجات
                CallbackQueryHandler(back_to_hwaya_menu, pattern='^hwaya_Wedding$') 
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            # زر الرجوع الرئيسي يعود لصفحة المنتجات
            CallbackQueryHandler(back_to_hwaya_menu, pattern='^hwaya_Wedding$'), 
            CallbackQueryHandler(cancel_and_end)
        ]
    )


    # محافظ محفورة بالاسم
    engraved_wallet_handler = ConversationHandler(
        # تبدأ المحادثة عند اختيار اللون من القائمة الفرعية
        entry_points=[CallbackQueryHandler(prompt_for_wallet_name, pattern='^wallet_.*')],
        states={
            GET_WALLET_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_wallet_name_and_prepare_whatsapp)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            # زر الرجوع يعود إلى قائمة اختيار المحافظ
            CallbackQueryHandler(back_to_wallets_color, pattern='^engraved_wallet$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # اقلام محفورة بالاسم
    engraved_pen_handler = ConversationHandler(
        # تبدأ المحادثة عند اختيار نوع القلم من القائمة الفرعية
        entry_points=[CallbackQueryHandler(prompt_for_pen_name, pattern='^aqlam_metal$|^aqlam_luminous$')],
        states={
            GET_PEN_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_pen_types, pattern='^aqlam$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # معالج استقبال صور المجات (الابيض والسحري)
    mug_photos_handler = ConversationHandler(
        entry_points=[], # لا تبدأ بشكل مباشر، يتم الدخول إليها من prepare_whatsapp_link_for_direct_buy
        states={
            GET_MUG_PHOTOS: [MessageHandler(Filters.photo, receive_mug_photos)],
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
    
    # معالج المج الديجتال (لطلب الاسم)
    digital_mug_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_digital_mug_purchase, pattern='^buy_mugat_digital_.*')],
        states={
            GET_DIGITAL_MUG_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_digital_mug_name_and_finish),
                CallbackQueryHandler(back_to_digital_mug_menu, pattern='^mugat_digital$') # الرجوع لصفحة المج الديجتال
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_digital_mug_menu, pattern='^mugat_digital$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # معالج الطلبات المباشرة (هرم، دروع، أباجورات، سبلميشن، مج أبيض/سحري)
    # يستخدم للطلبات التي لا تحتاج جمع بيانات إضافية (الاسم والتاريخ) باستثناء المج الذي يحتاج صور
    direct_buy_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prepare_whatsapp_link_for_direct_buy, 
                                           pattern='^buy_(abajora|haram|doro3|mugat_white|mugat_magic|subli)_.*')], 
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
    
    # 🔥 إضافة معالجات المجات الجديدة
    dp.add_handler(mug_photos_handler)
    dp.add_handler(digital_mug_handler) # 🔥 إضافة معالج المج الديجتال
    dp.add_handler(hwaya_handler) # 🔥 إضافة معالج يد الهوايا الجديد
    
    dp.add_handler(direct_buy_handler) 

    
    # 5. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 6. معالج لجميع ضغطات الأزرار (يجب وضعه في النهاية بعد الـ ConversationHandlers)
    dp.add_handler(CallbackQueryHandler(handle_main_menu_clicks))

    # بدء تشغيل البوت
    updater.start_polling()
    updater.idle()

# التأكد من عدم وجود دالة main_menu_handler أخرى
# يتم استخدام handle_main_menu_clicks لمعالجة جميع أزرار الـ InlineKeyboard التي لا تبدأ ConversationHandler.

if __name__ == '__main__':
    main()