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

# 🔥🔥 الحالات الجديدة للمرايا
GET_MIRROR_SIZE = 20
GET_MIRROR_NAME = 21

# 🔥🔥🔥 الحالة الجديدة ليد الهوايا
GET_FAN_NAME = 22

# 🔥🔥🔥 الحالات الجديدة للساعات الزجاجية
GET_GLASS_CLOCK_SIZE = 23 # حالة اختيار مقاس الساعة
GET_GLASS_CLOCK_PHOTO = 24 # حالة انتظار صورة الساعة


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
    {"label": "منديل موديل 2", "callback": "tissue_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 2، خامة عالية الجودة.", "price": "400 ج"}
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

# 🔥🔥🔥 قائمة الساعات الزجاجية الجديدة (منتج واحد)
glass_clocks_submenu = [
    {
        "label": "ساعة زجاج بالصورة", 
        "callback": "glass_clock_m1", 
        "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", 
        "description": "ساعة زجاجية مدورة طباعة صورة، تصميم عالي الجودة.", 
        "price": "حسب المقاس"
    }
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
    {"label": "🕰️ ساعات زجاج بالصورة", "callback": "glass_clocks"}, # 🔥 الزر الجديد
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
    "glass_clocks": glass_clocks_submenu, # 🔥 إضافة قائمة الساعات الزجاجية
    "bsamat": bsamat_submenu, 
    "wedding_tissues": wedding_tissues_submenu,
    "katb_kitab_box": katb_kitab_box_submenu,
    "mirrors": mirrors_submenu,
    "fans": fans_submenu, 
    "abajorat": abajorat_submenu,
    "engraved_wallet": engraved_wallet_submenu,
    "sublimation": sublimation_supplies_submenu 
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box", "mirrors", "fans", "sublimation", "glass_clocks"]: # 🔥 إضافة 'glass_clocks'
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
    
    # 1. إذا كانت قائمة مباشرة من القائمة الرئيسية (مثل بصمات، أباجورات، مرايا، يد هوايا، ساعات زجاج)
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "mirrors", "fans", "sublimation", "glass_clocks"]: # 🔥 إضافة 'glass_clocks'
        back_callback = "main_menu"
        back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
    # 2. قوائم المستوى الثاني (مثل صواني اكليريك/خشب) تعود للقائمة الأم (صواني)
    elif product_to_submenu_map.get(product_callback_data) in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        back_callback = product_to_submenu_map.get(product_callback_data)
        back_text = f"🔙 رجوع إلى قائمة {next((item['label'] for item in main_menu if item['callback'] == back_callback), 'القائمة السابقة')}"
    else:
        # إذا لم يتم العثور على زر رجوع، نعود للقائمة الرئيسية كافتراض
        back_callback = "main_menu"
        back_text = "🔙 رجوع إلى القائمة الرئيسية"


    # زر الرجوع بعد عرض كل المنتجات
    back_keyboard = [[InlineKeyboardButton(back_text, callback_data=back_callback)]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # إرسال زر الرجوع في رسالة منفصلة في نهاية عرض المنتجات
    update.effective_chat.send_message(
        text=back_text, 
        reply_markup=back_reply_markup,
        parse_mode="Markdown"
    )
    # لا نرجع حالة محادثة هنا، بل نعتمد على الـ CallbackQueryHandler التالي
    return


# --------------------
# 4. دوال المحادثات المخصصة
# --------------------

# ... (بقية الدوال الرئيسية مثل دوال المحافظ، الأقلام، البوكس، الصواني، الطارات، البصمات، المناديل) ...

# --------------------------------------------------------------------------------
# 🔥🔥 دوال خاصة بالساعات الزجاجية بالصورة 🔥🔥
# --------------------------------------------------------------------------------

def get_glass_clock_items():
    return glass_clocks_submenu

def start_glass_clock_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_glass_clock_m1 
    product_callback = data.replace("buy_", "")
    items_list = get_glass_clock_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['glass_clock_product'] = selected_product
    context.user_data['state'] = GET_GLASS_CLOCK_SIZE

    # اختيار المقاس (2 أزرار + زر رجوع)
    keyboard = [
        [InlineKeyboardButton("مقاس 1 بسعر 100 ج", callback_data="size_1_price_100")],
        [InlineKeyboardButton("مقاس 2 بسعر 200 ج", callback_data="size_2_price_200")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="glass_clocks")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        query.message.delete()
    except:
        pass
    
    caption_text = f"✅ **{selected_product['label']}**\n\nبرجاء **تحديد المقاس المطلوب** من القائمة التالية:"
    
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
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
    return GET_GLASS_CLOCK_SIZE

def back_to_glass_clocks_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    try:
        query.message.delete()
    except Exception:
        pass
    # العودة إلى عرض منتجات الساعات
    show_product_page(update, "glass_clocks", glass_clocks_submenu, is_direct_list=True)
    return ConversationHandler.END

def back_to_glass_clock_size(update, context):
    query = update.callback_query
    query.answer()
    selected_product = context.user_data.get('glass_clock_product')
    
    if not selected_product:
        start(update, context)
        return ConversationHandler.END

    # اختيار المقاس (2 أزرار + زر رجوع)
    keyboard = [
        [InlineKeyboardButton("مقاس 1 بسعر 100 ج", callback_data="size_1_price_100")],
        [InlineKeyboardButton("مقاس 2 بسعر 200 ج", callback_data="size_2_price_200")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="glass_clocks")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        query.message.delete()
    except:
        pass
    
    caption_text = f"✅ **{selected_product['label']}**\n\nبرجاء **تحديد المقاس المطلوب** من القائمة التالية:"
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    # العودة لحالة اختيار المقاس
    return GET_GLASS_CLOCK_SIZE

def receive_glass_clock_size_ask_photo(update, context):
    query = update.callback_query
    query.answer()
    
    data = query.data # size_1_price_100 or size_2_price_200
    
    # استخراج المقاس والسعر
    if data == "size_1_price_100":
        size_label = "مقاس 1"
        price_value = "100 ج"
    elif data == "size_2_price_200":
        size_label = "مقاس 2"
        price_value = "200 ج"
    else:
        # خطأ غير متوقع
        query.answer("خطأ في اختيار المقاس", show_alert=True)
        return back_to_glass_clock_size(update, context) # الرجوع لاختيار المقاس
    
    context.user_data['glass_clock_size'] = size_label
    context.user_data['glass_clock_price'] = price_value
    
    selected_product = context.user_data.get('glass_clock_product')

    context.user_data['state'] = GET_GLASS_CLOCK_PHOTO

    # طلب الصورة
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع للعودة للقائمة السابقة", callback_data="back_to_glass_clock_size")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    try:
        query.message.delete()
    except:
        pass

    caption_text = (
        f"✅ تم اختيار: **{selected_product['label']} - {size_label}** (السعر: *{price_value}*)\n\n"
        "من فضلك، **أرسل الصورة المطلوب طباعتها علي الساعة** في رسالة بالأسفل.\n"
        "أو اضغط زر الرجوع للعودة للقائمة السابقة"
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_GLASS_CLOCK_PHOTO

def receive_glass_clock_photo_and_finish(update, context):
    # نستخدم نفس منطق الـ Mirrors أو الـ Mugs للحصول على رابط الصورة
    if not update.message.photo:
        update.message.reply_text("❌ من فضلك أرسل *صورة* لإتمام الطلب.", parse_mode="Markdown")
        return GET_GLASS_CLOCK_PHOTO

    # 1. حفظ file_id للصورة المرفقة
    photo_file = update.message.photo[-1]
    
    # 2. حفظ بيانات المنتج النهائية قبل مرحلة الدفع
    product_data = context.user_data['glass_clock_product']
    size_label = context.user_data['glass_clock_size']
    price_value = context.user_data['glass_clock_price']

    # إعداد البيانات لـ prompt_for_payment_and_receipt
    
    # نجهز بيانات الدفع النهائية 
    product_type_label = "ساعة زجاج بالصورة"
    context.user_data['final_product_type'] = product_type_label
    context.user_data['final_product_label'] = product_data['label']
    context.user_data['final_price'] = price_value
    context.user_data['final_names'] = size_label # استخدام حقل names لتخزين المقاس مبدئياً
    context.user_data['final_date'] = "صورة مرفقة"
    context.user_data['final_code'] = product_data['callback']
    
    # ⚠️ حقل جديد لحفظ file_id الصورة المرفقة لطباعتها
    context.user_data['printing_image_file_id'] = photo_file.file_id
    
    update.message.reply_text("✅ تم استلام الصورة بنجاح.\nجاري تحضير تفاصيل الدفع...")
    
    # الانتقال لمرحلة الدفع
    return prompt_for_payment_and_receipt(update, context, product_type=product_type_label)


# --------------------------------------------------------------------------------
# 🔥 دالة طلب الدفع (تم التعديل لتمكين النسخ المباشر ومعالجة رابط صورة الساعة)
# --------------------------------------------------------------------------------
def prompt_for_payment_and_receipt(update, context, product_type):
    """ الدالة الجديدة التي تطلب من العميل الدفع وتحويل الحالة إلى انتظار صورة الإيصال. """
    # 1. إعداد تفاصيل الطلب حسب نوع المنتج
    product_data = None
    names_details = ""
    date_details = ""
    
    if product_type == "محفظة":
        # ... (بقية دوال المحافظ)
    elif product_type == "اقلام":
        # ... (بقية دوال الأقلام)
    elif product_type == "بوكس كتب كتاب":
        # ... (بقية دوال البوكس)
    elif product_type == "صواني شبكة اكليريك":
        # ... (بقية دوال الصواني)
    elif product_type == "صواني شبكة خشب":
        # ... (بقية دوال الصواني)
    elif product_type == "طارات اكليريك":
        # ... (بقية دوال الطارات)
    elif product_type == "طارات خشب":
        # ... (بقية دوال الطارات)
    elif product_type == "بصامة":
        # ... (بقية دوال البصمات)
    elif product_type == "منديل كتب كتاب":
        # ... (بقية دوال المناديل)
    elif product_type == "مج أبيض" or product_type == "مج سحري":
        # ... (بقية دوال المجات)
    elif product_type == "مج ديجتال":
        # ... (بقية دوال المج الديجتال)
    elif product_type == "مرايا":
        # ... (بقية دوال المرايا)
    elif product_type == "يد هوايا":
        # ... (بقية دوال يد الهوايا)
    elif product_type == "ساعة زجاج بالصورة": # 🔥 إضافة حالة الساعة الزجاجية
        product_data = context.user_data.get('glass_clock_product')
        size_label = context.user_data.get('glass_clock_size')
        product_price = context.user_data.get('glass_clock_price')
        
        # ⚠️ هنا نحتاج للحصول على رابط الصورة من Telegram file_id
        image_file_id = context.user_data.get('printing_image_file_id')
        
        if image_file_id:
            try:
                # الحصول على كائن الملف من file_id
                new_file = context.bot.get_file(image_file_id)
                # ⚠️ حفظ رابط الصورة المطلوب طباعتها (يحتوي على التوكن ويجب استخدامه مباشرة)
                context.user_data['printing_image_url'] = new_file.file_path 
                
                # تحديث تفاصيل الاسم/المقاس لتظهر في رسالة الدفع (مؤقتا)
                names_details = f"المقاس: {size_label}" # الرابط سيتم إضافته في النهاية في handle_payment_photo
                product_data['price'] = product_price # تحديث السعر الفعلي
            except Exception as e:
                names_details = f"المقاس: {size_label}\n❌ فشل الحصول على رابط الصورة: {e}"
                context.user_data['printing_image_url'] = "فشل الحصول على الرابط"
        else:
            names_details = f"المقاس: {size_label}"
        
        # نضبط البيانات النهائية مرة أخرى للتأكد من استخدام السعر الصحيح
        context.user_data['final_price'] = product_data.get('price', 'غير محدد')
        context.user_data['final_names'] = names_details if names_details else 'غير مطلوب'
        context.user_data['final_date'] = date_details if date_details else 'غير مطلوب'
        context.user_data['final_product_image'] = product_data.get('image', 'غير متوفر')
        context.user_data['final_product_type'] = product_type
        context.user_data['final_product_label'] = product_data.get('label', product_type)
        context.user_data['final_code'] = product_data.get('callback', 'N/A')
        
    elif 'direct_product' in context.user_data:
        # الأهرامات، الدروع، الأباجورات، السبلميشن
        product_data = context.user_data.get('direct_product')
        
    else:
        update.effective_chat.send_message("حدث خطأ في تجهيز الطلب. يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        context.user_data.clear()
        return ConversationHandler.END

    # 2. حفظ تفاصيل الطلب بشكل موحد لـ handle_payment_photo (إذا لم تكن من نوع 'ساعة زجاج بالصورة')
    if product_type != "ساعة زجاج بالصورة":
        context.user_data['final_product_type'] = product_type
        context.user_data['final_product_label'] = product_data.get('label', product_type)
        context.user_data['final_price'] = product_data.get('price', 'غير محدد')
        context.user_data['final_names'] = names_details if names_details else 'غير مطلوب'
        context.user_data['final_date'] = date_details if date_details else 'غير مطلوب'
        context.user_data['final_code'] = product_data.get('callback', 'N/A')
        context.user_data['final_product_image'] = product_data.get('image', 'غير متوفر')

    # ... (بقية كود دالة prompt_for_payment_and_receipt) ...

    context.user_data['state'] = GET_PAYMENT_RECEIPT
    
    final_price = context.user_data['final_price']
    
    # 3. إعداد رسالة الدفع
    message_text = (
        f"✅ تم تأكيد طلبك لمنتج **{context.user_data['final_product_label']}** "
        f"بسعر إجمالي **{final_price}**.\n\n"
        "لإتمام الطلب، برجاء تحويل المبلغ على رقم فودافون كاش:\n"
        f"💰 **{VODAFONE_CASH_NUMBER}**\n\n"
        "⚠️ بعد إتمام عملية التحويل، يرجى إرسال **صورة إيصال الدفع** في رسالة بالأسفل. "
        "بدونها لن يتم تأكيد الطلب. شكرًا لتعاونكم."
    )
    
    # زر نسخ رقم المحفظة وزر إلغاء
    keyboard = [
        # زر نسخ (يستخدم الـ inline query)
        [InlineKeyboardButton("📋 نسخ رقم فودافون كاش", switch_inline_query_current_chat=VODAFONE_CASH_NUMBER)],
        [InlineKeyboardButton("❌ إلغاء الطلب والعودة للرئيسية", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # إرسال الرسالة
    update.effective_chat.send_message(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_PAYMENT_RECEIPT


# --------------------------------------------------------------------------------
# 🔥 دالة معالجة صورة الإيصال (تم التعديل لإضافة رابط صورة الطباعة لرسالة الواتساب)
# --------------------------------------------------------------------------------
def handle_payment_photo(update, context):
    # ... (بقية كود دالة handle_payment_photo) ...

    # 1. حفظ صورة الإيصال والحصول على رابط الصورة
    if not update.message.photo:
        update.message.reply_text("❌ من فضلك أرسل *صورة* الإيصال لإتمام الطلب.", parse_mode="Markdown")
        return GET_PAYMENT_RECEIPT
    
    # ... (بقية كود دالة handle_payment_photo) ...
    
    # 2. استرجاع بيانات الطلب النهائية
    product_type = context.user_data.get('final_product_type', 'غير متوفر')
    product_label = context.user_data.get('final_product_label', 'غير متوفر')
    paid_amount = context.user_data.get('final_price', 'غير متوفر')
    names_text = context.user_data.get('final_names', 'غير مطلوب')
    date_text = context.user_data.get('final_date', 'غير مطلوب')
    product_code = context.user_data.get('final_code', 'N/A')
    
    # 🔥 استرجاع رابط صورة المنتج
    product_image_url = context.user_data.get('final_product_image', 'غير متوفر')
    
    # 🔥🔥 استرجاع روابط صور المجات (إن وجدت)
    mug_photos = context.user_data.get('mug_photos_links', [])
    mug_photos_text = ""
    if mug_photos:
        mug_photos_text = "\n\n🔗 **صور التصميم المرفقة:**\n"
        for i, link in enumerate(mug_photos):
            mug_photos_text += f" صورة {i+1}: {link}\n"
            
    # 🔥🔥🔥 استرجاع رابط الصورة المطلوب طباعتها على الساعة (الحالة الجديدة)
    printing_image_url = context.user_data.get('printing_image_url')
    image_to_print_text = ""
    if printing_image_url and product_type == "ساعة زجاج بالصورة":
        # إضافة رابط الصورة المطلوب طباعتها ضمن تفاصيل الطلب
        image_to_print_text = f"\n🔗 *رابط الصورة المطلوب طباعتها علي الساعة:* {printing_image_url}\n"
        
        # يتم دمج المقاس مع اسم المنتج في حقل product_type
        # names_text already holds the size and is enough
        
    user_info = update.message.from_user
    # 🔥 إنشاء رابط التواصل عبر التليجرام
    telegram_contact_link = f"tg://user?id={user_info.id}"

    # 3. بناء نص الرسالة للواتساب (تم التعديل)
    message_body = (
        f"🔔 *طلب منتج جديد* 🔔\n\n"
        f"👤 *العميل:* {user_info.first_name} {user_info.last_name if user_info.last_name else ''} (ID: {user_info.id})\n"
        f"📞 *للتواصل عبر تليجرام:* {telegram_contact_link}\n\n"
        f"📦 *المنتج:* {product_label} ({product_type})\n"
        f"💰 *السعر المتفق عليه:* {paid_amount}\n"
        
        # 🔥 إضافة رابط الصورة المطلوب طباعتها هنا
        f"{image_to_print_text}" # يتم إضافته هنا إذا كانت ساعة زجاج
        
        f"📝 *تفاصيل الطلب (الأسماء/المقاس):* {names_text}\n"
        f"🗓️ *التاريخ:* {date_text}\n"
        f"🔗 *رابط صورة الإيصال:* {receipt_url}\n"
        f"📷 *رابط صورة المنتج المعروض:* {product_image_url}\n"
        f"🔢 *كود المنتج:* {product_code}\n"
        f"{mug_photos_text}"
        "\n--- رسالة تلقائية من البوت ---"
    )

    # ... (بقية كود دالة handle_payment_photo) ...
    
    return ConversationHandler.END

# --------------------
# 5. دالة إضافة المعالجات (setup_handlers)
# --------------------
def setup_handlers(dp):
    # ... (بقية كود دالة setup_handlers) ...

    # دوال المحافظ
    engraved_wallet_handler = ConversationHandler(
    # ...
    )

    # اقلام محفورة بالاسم
    engraved_pen_handler = ConversationHandler(
    # ...
    )

    # 🔥🔥 دوال خاصة بالمجات التي تتطلب صور (أبيض / سحري)
    mug_photos_handler = ConversationHandler(
    # ...
    )

    # 🔥🔥 دوال خاصة بالمج الديجتال (تتطلب اسم الحفر)
    digital_mug_handler = ConversationHandler(
    # ...
    )
    
    # 🔥🔥 دوال المرايا
    mirrors_handler = ConversationHandler(
    # ...
    )

    # 🔥🔥 دوال يد الهوايا
    fans_handler = ConversationHandler(
    # ...
    )
    
    # 🔥🔥🔥 دوال الساعات الزجاجية بالصورة (المعالج الجديد)
    glass_clock_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_glass_clock_purchase, pattern='^buy_glass_clock_.*')],
        states={
            GET_GLASS_CLOCK_SIZE: [
                CallbackQueryHandler(receive_glass_clock_size_ask_photo, pattern='^size_1_price_100$|^size_2_price_200$'),
                CallbackQueryHandler(back_to_glass_clocks_menu, pattern='^glass_clocks$')
            ],
            GET_GLASS_CLOCK_PHOTO: [
                MessageHandler(Filters.photo, receive_glass_clock_photo_and_finish),
                CallbackQueryHandler(back_to_glass_clock_size, pattern='^back_to_glass_clock_size$')
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

    # 3. معالج الشراء المباشر للمنتجات التي لا تحتاج محادثة
    direct_buy_handler = CallbackQueryHandler(
    # ...
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
    dp.add_handler(digital_mug_handler) 

    # 🔥 إضافة معالج المرايا الجديد
    dp.add_handler(mirrors_handler)

    # 🔥 إضافة معالج يد الهوايا الجديد
    dp.add_handler(fans_handler)
    
    # 🔥 إضافة معالج الساعات الزجاجية الجديد
    dp.add_handler(glass_clock_handler) # 🔥🔥🔥 إضافة المعالج الجديد
    
    dp.add_handler(direct_buy_handler) 

    
    # 5. أوامر /start
    dp.add_handler(CommandHandler('start', start))
    
    # 6. معالج أزرار القوائم الفرعية 
    # ... (بقية كود دالة setup_handlers) ...

if __name__ == '__main__':
    main()