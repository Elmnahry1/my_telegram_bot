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

# 🔥🔥🔥 الحالة الجديدة ليد الهوايا (تمت الإضافة)
GET_FAN_NAME = 22

# 🔥🔥🔥 الحالات الجديدة للساعات الزجاج (تمت الإضافة)
GET_CLOCK_SIZE = 23
GET_CLOCK_PHOTO = 24

# 🔥🔥🔥 الحالة الجديدة للتابلوهات (تمت الإضافة)
GET_TABLOH_SIZE = 25

# 🔥🔥🔥 الحالة الجديدة للمباخر
GET_MABAKHIR_DETAILS = 26 


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

# 🔥 قائمة المرايا
mirrors_submenu = [
    {"label": "مرايا موديل 1", "callback": "mirror_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "مرايا موديل 1 بتصميم أنيق.", "price": "حسب المقاس"},
    {"label": "مرايا موديل 2", "callback": "mirror_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "مرايا موديل 2 بتصميم عصري.", "price": "حسب المقاس"}
]

# 🔥🔥🔥 قائمة يد الهوايا (تمت الإضافة)
fans_submenu = [
    {"label": "يد هوايا موديل 1", "callback": "fan_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "يد هوايا مميزة موديل 1.", "price": "150 ج"},
    {"label": "يد هوايا موديل 2", "callback": "fan_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "يد هوايا مميزة موديل 2.", "price": "180 ج"}
]

# 🔥🔥🔥 قائمة ساعات الزجاج الجديدة (تمت الإضافة)
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

# 🔥🔥🔥 قائمة المباخر الجديدة
mabakhir_submenu = [
    {"label": "مبخرة موديل 1", "callback": "mabkhara_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف المبخرة موديل 1. مبخرة أنيقة عالية الجودة.", "price": "180 ج"},
    {"label": "مبخرة موديل 2", "callback": "mabkhara_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف المبخرة موديل 2. تصميم عصري ومميز.", "price": "230 ج"}
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
    {"label": "🖼️ تابلوهات", "callback": "tablohat"}, # 🔥 الزر الجديد (تمت الإضافة)
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"}, 
    {"label": "✨ مباخر", "callback": "mabakhir"}, # 🔥🔥🔥 الزر الجديد المطلوب
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
    "mabakhir": mabakhir_submenu, # 🔥🔥🔥 القائمة الجديدة
    "sublimation": sublimation_supplies_submenu 
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "mabakhir", "aqlam", "katb_kitab_box", "mirrors", "fans", "sublimation", "clocks"]: 
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
        # إذا كان العنصر يحتوي على قائمة فرعية متداخلة (مثل صواني اكليريك)
        if 'items' in item:
            keyboard.append([InlineKeyboardButton(item["label"], callback_data=item["callback"])])
        # إذا كان العنصر هو منتج مباشر (يتم عرضه في صفحة المنتج لاحقاً)
        else:
            keyboard.append([InlineKeyboardButton(item["label"], callback_data=item["callback"])])
            
    # إضافة زر الرجوع
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)])
    
    # إنشاء لوحة المفاتيح النهائية
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = f"✅ *{title}*:\n\nمن فضلك اختر طلبك من القائمة:"

    # إرسال رسالة جديدة
    if query:
        update.effective_chat.send_message(
            text=message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
         update.effective_message.reply_text(
            text=message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )


# 💡 دالة عرض صفحة المنتج/المنتجات
def show_product_page(update, list_callback_data, product_list, is_direct_list=False):
    query = update.callback_query
    if query:
        query.answer()
    
    # نحذف رسالة القائمة السابقة
    if query and query.message:
        try:
            query.message.delete()
        except Exception:
            pass
            
    # تحديد زر الرجوع (يعتمد على القائمة الأم)
    back_button_callback = product_to_submenu_map.get(list_callback_data, "main_menu")
    
    # ⚠️ product_list هنا هي قائمة المنتجات المراد عرضها
    for item in product_list:
        
        # إذا كانت قائمة مباشرة (مثل المحافظ أو الأقلام)، يتم استخدام buy_
        if is_direct_list:
            buy_callback = f"buy_{item['callback']}"
        else:
            # إذا كانت قائمة متداخلة (مثل صواني اكليريك)، يتم استخدام buy_
            buy_callback = f"buy_{item['callback']}"
            
        
        item_keyboard = [
            [InlineKeyboardButton("🛒 شراء", callback_data=buy_callback)],
        ]
        
        reply_markup = InlineKeyboardMarkup(item_keyboard)
        
        caption_text = (
            f"✅ **{item['label']}**\n\n"
            f"*{item['description']}*\n"
            f"💰 السعر: *{item['price']}*"
        )
        
        # إرسال رسالة لكل منتج
        try:
            update.effective_chat.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=item['image'],
                caption=caption_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        except telegram.error.BadRequest:
             update.effective_chat.bot.send_message(
                chat_id=update.effective_chat.id,
                text=caption_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )


    # إرسال زر الرجوع منفصلاً في النهاية
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_button_callback)]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    update.effective_chat.send_message(
        text="اضغط رجوع للعودة الى القائمة السابقة",
        reply_markup=back_reply_markup,
        parse_mode="Markdown"
    )
    
# 💡 دالة معالجة الشراء المباشر للمنتجات التي لا تحتاج خطوات إضافية (مثل الأهرامات، الدروع، الأباجورات، السبلميشن)
def handle_direct_buy(update, context):
    query = update.callback_query
    data = query.data # buy_haram_akerik_m1
    product_callback = data.replace("buy_", "")
    
    product_data = None
    product_type = "طلب مباشر" # القيمة الافتراضية

    # 1. البحث عن المنتج في القوائم المباشرة
    for menu_key, submenu_list in all_submenus.items():
        if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box", "mirrors", "fans", "sublimation", "clocks"]: 
            product_data = next((item for item in submenu_list if item["callback"] == product_callback), None)
            if product_data:
                product_type = product_data.get('label', product_data.get('callback'))
                # إذا كان المنتج هو مج يتطلب صور، أو قلم/محفظة يتطلب اسم، أو بصامة/منديل يتطلب أسماء وتاريخ، يتم تركه للمعالج الخاص به
                if menu_key in ["mugat", "engraved_wallet", "aqlam", "bsamat", "wedding_tissues", "katb_kitab_box", "mirrors", "fans", "clocks", "mabakhir"]:
                    # يجب أن يتم معالجة هذه الأنواع بواسطة المعالج الخاص بها، هنا نتركها فقط إذا لم يكن لها معالج شراء خاص بها
                    # إذا كان لها معالج شراء خاص (buy_...) لن تصل إلى هنا إذا تم تعريف المعالج بشكل صحيح
                    # ولكن إذا كانت من المجات العادية (white/magic) التي تحتاج صور، يجب أن تذهب إلى معالجها
                    if "mugat" in menu_key:
                         return # نتركها للمعالج الخاص بها (mug_photos_handler)
                    # وإذا كانت محفظة/قلم/بصامة/منديل/مباخر يجب أن تذهب لمعالجها
                    if menu_key in ["engraved_wallet", "aqlam", "bsamat", "wedding_tissues", "katb_kitab_box", "mirrors", "fans", "clocks", "mabakhir"]:
                        return # نتركها للمعالج الخاص بها
                        
                break

    # 2. البحث عن المنتج في القوائم المتداخلة (دروع، أهرامات)
    if not product_data:
        for menu_label, submenu in all_submenus.items():
            if menu_label in ["doro3", "haram", "sawany", "taarat", "mugat"]:
                for item in submenu:
                    sub_item = next((si for si in item['items'] if si['callback'] == product_callback), None)
                    if sub_item:
                        product_data = sub_item
                        product_type = item["label"]
                        break
                if product_data:
                    break

    if not product_data:
        query.answer("عفواً، لا يمكن إتمام هذا الطلب حالياً.", show_alert=True)
        start(update, context)
        return

    # 3. حفظ البيانات وإرسال رسالة الدفع
    context.user_data['direct_product'] = product_data
    # يجب حذف رسالة الزر القديمة
    try:
        query.message.delete()
    except Exception:
        pass
    
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

    # ⚠️ تم حذف جزء 'copy_voda_cash' هنا لأنه تم استبداله بزر 'switch_inline_query_current_chat'
    # والذي لا يحتاج إلى معالج CallbackQueryHandler
    
    # إذا تم الضغط على أي زر آخر في هذه المرحلة (فقط زر الإلغاء هو المتبقي)
    query.answer("يرجى إرسال إيصال الدفع لإتمام الطلب.", show_alert=True)
    return GET_PAYMENT_RECEIPT

# --------------------------------------------------------------------------------
# 🔥 دالة طلب الدفع (تم التعديل لتمكين النسخ المباشر)
# --------------------------------------------------------------------------------
def prompt_for_payment_and_receipt(update, context, product_type):
    """
    تجهز رسالة الدفع وتطلب إيصال الدفع من العميل.
    """
    # 1. استخلاص بيانات المنتج من الـ context
    product_data = {}
    names_details = ""
    date_text = ""
    price = "غير متوفر"

    if product_type == "محفظة":
        product_data = context.user_data.get('wallet_product')
        names_details = context.user_data.get('wallet_engraving_name')
    elif product_type == "قلم":
        product_data = context.user_data.get('pen_product')
        names_details = context.user_data.get('pen_engraving_name')
    elif product_type == "بوكس كتب كتاب":
        product_data = context.user_data.get('box_product')
        names_details = context.user_data.get('box_names')
        color = context.user_data.get('box_color')
        date_text = context.user_data.get('box_date')
        if color:
             names_details = f"الأسماء: {names_details} | اللون: {color}"
    elif "صينية اكليريك" in product_type:
        product_data = context.user_data.get('akerik_tray_product')
        names_details = context.user_data.get('akerik_tray_names')
        date_text = context.user_data.get('akerik_tray_date')
    elif "صينية خشب" in product_type:
        product_data = context.user_data.get('khashab_tray_product')
        names_details = context.user_data.get('khashab_tray_names')
        date_text = context.user_data.get('khashab_tray_date')
    elif "طارة اكليريك" in product_type:
        product_data = context.user_data.get('taarat_akerik_product')
        names_details = context.user_data.get('taarat_akerik_names')
        date_text = context.user_data.get('taarat_akerik_date')
    elif "طارة خشب" in product_type:
        product_data = context.user_data.get('taarat_khashab_product')
        names_details = context.user_data.get('taarat_khashab_names')
        date_text = context.user_data.get('taarat_khashab_date')
    elif product_type == "بصامة":
        product_data = context.user_data.get('bsamat_product')
        names_details = context.user_data.get('bsamat_names')
        date_text = context.user_data.get('bsamat_date')
    elif product_type == "منديل كتب كتاب":
        product_data = context.user_data.get('tissue_product')
        names_details = context.user_data.get('tissue_names')
        date_text = context.user_data.get('tissue_date')
    elif product_type == "مج (تصميم خاص)":
        # الصور تم حفظها مسبقاً في mug_photo_links
        product_data = context.user_data.get('direct_product')
        names_details = f"عدد الصور: {len(context.user_data.get('mug_photo_links', []))}"
        if product_data:
            price = product_data.get('price', 'غير متوفر')
            
    elif product_type == "مج ديجتال":
        product_data = context.user_data.get('digital_mug_product')
        names_details = context.user_data.get('digital_mug_name')
        # product_type remains "مج ديجتال"
    elif product_type == "مرايا": # 🔥 إضافة حالة المرايا
        product_data = context.user_data.get('mirror_product')
        size_label = context.user_data.get('mirror_size')
        names_details = context.user_data.get('mirror_name')
        product_type = f"{product_type} - {size_label}"
    elif product_type == "يد هوايا": # 🔥 إضافة حالة يد الهوايا
        product_data = context.user_data.get('fan_product')
        names_details = context.user_data.get('fan_name')
        # product_type remains "يد هوايا"
    elif product_type == "ساعة زجاج": # 🔥 إضافة حالة ساعات الزجاج
        product_data = context.user_data.get('clock_product')
        size_label = context.user_data.get('clock_size')
        product_type = f"{product_type} - {size_label}"
    elif product_type == "تابلوه": # 🔥 إضافة حالة التابلوهات (جديد)
        size_label = context.user_data.get('tabloh_size')
        price = context.user_data.get('tabloh_price')
        product_data = {'label': 'تابلوه', 'price': price, 'callback': 'tablohat', 'image': 'غير متوفر'}
        product_type = f"{product_type} - {size_label}"
    elif "مبخرة" in product_type: # 🔥🔥🔥 إضافة حالة المباخر
        product_data = context.user_data.get('mabkhara_product')
        names_details = context.user_data.get('mabkhara_details') # التفاصيل الإضافية
        # product_type remains "مبخرة"
    elif 'direct_product' in context.user_data: 
        # الأهرامات، الدروع، المجات، الأباجورات، السبلميشن
        product_data = context.user_data.get('direct_product')
        # product_type is already set from prepare_whatsapp_link_for_direct_buy
    else:
        update.effective_chat.send_message("حدث خطأ في تجهيز الطلب. يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        context.user_data.clear()
        return ConversationHandler.END


    # 2. استخراج البيانات المشتركة وتخزينها للمرحلة النهائية
    product_label = product_data.get('label', product_data.get('callback', 'غير متوفر'))
    price = product_data.get('price', price) # نستخدم السعر الذي تم استخراجه أو السعر العام

    context.user_data['final_product_type'] = product_type
    context.user_data['final_product_label'] = product_label
    context.user_data['final_price'] = price
    context.user_data['final_names'] = names_details
    context.user_data['final_date'] = date_text

    
    # 3. بناء رسالة الدفع
    
    # تفاصيل المنتج النهائية للعرض على المستخدم
    final_details_text = f"✅ نوع المنتج: **{product_type}**\n"
    if product_label != "غير متوفر":
        final_details_text += f"✅ الموديل/الاسم: **{product_label}**\n"
        
    final_details_text += f"💰 السعر: **{price}**\n"

    # ⚠️ تجميع جميع التفاصيل الإضافية (الأسماء، المقاسات، الألوان، إلخ)
    if names_details:
        final_details_text += f"\n- **التفاصيل الإضافية المطلوبة**: {names_details}"
    
    if date_text:
        final_details_text += f"\n- **التاريخ**: {date_text}"

    # إذا كانت ساعة زجاج، نطلب منه الصورة في خطوة سابقة، هنا نذكره
    if product_type == "ساعة زجاج":
        final_details_text += "\n\n**تم إرسال الصورة بالفعل في الخطوة السابقة.**"
    
    # إذا كان مج (تصميم خاص) نطلب منه الصور في خطوة سابقة
    if product_type == "مج (تصميم خاص)":
         final_details_text += "\n\n**تم إرسال الصور بالفعل في الخطوة السابقة.**"


    payment_message = (
        f"*{final_details_text}*\n\n"
        "-------------------------------------\n"
        "💳 *مرحلة الدفع (يرجى اختيار طريقة الدفع المناسبة):*\n"
        "1. **محفظة فودافون كاش:**\n"
        f"   - الرقم: `{VODAFONE_CASH_NUMBER}` (للدفع من محفظة فودافون كاش)\n"
        "   - للدفع من أي محفظة أو بنك آخر استخدم:\n"
        "     - رقم الحساب البنكي (IBAN): `01032328500`\n"
        "     - كود البنك: `000`\n"
        "   - **ملاحظة:** يرجى إضافة رسوم التحويل (عمولة الخدمة) للسعر الإجمالي عند الدفع فودافون كاش.\n\n"
        "2. **الدفع البنكي:** (لم يتم تفعيله بعد، يرجى استخدام فودافون كاش حالياً)\n"
        "-------------------------------------\n"
        "🚨 بعد إتمام عملية الدفع، *يرجى إرسال صورة إيصال الدفع في رسالة منفصلة لإكمال الطلب*."
    )
    
    # 4. بناء أزرار الدفع
    payment_keyboard = [
        # زر يتيح للعميل نسخ الرقم بشكل مباشر إلى شريط الرسائل
        [InlineKeyboardButton("نسخ رقم فودافون كاش (01032328500)", switch_inline_query_current_chat=VODAFONE_CASH_NUMBER)], 
        [InlineKeyboardButton("❌ إلغاء العملية", callback_data="cancel")]
    ]
    payment_reply_markup = InlineKeyboardMarkup(payment_keyboard)
    
    # 5. إرسال رسالة الدفع والانتظار لإيصال الدفع
    
    # حفظ حالة انتظار الإيصال
    context.user_data['state'] = GET_PAYMENT_RECEIPT 
    
    # إرسال الرسالة
    update.effective_chat.send_message(
        text=payment_message,
        reply_markup=payment_reply_markup,
        parse_mode="Markdown"
    )

    return GET_PAYMENT_RECEIPT

# --------------------------------------------------------------------------------
# 🔥 دالة معالجة صورة الإيصال (المرحلة الأخيرة)
# --------------------------------------------------------------------------------
def handle_payment_photo(update, context):
    """
    تستقبل صورة إيصال الدفع وتنهي المحادثة عن طريق إرسال رابط واتساب للمسؤول.
    """
    # التأكد من أننا في حالة انتظار الإيصال
    if context.user_data.get('state') != GET_PAYMENT_RECEIPT:
        update.effective_chat.send_message("عفواً، لا يمكنني معالجة هذه الصورة الآن. يرجى البدء بطلب جديد.")
        context.user_data.clear()
        return ConversationHandler.END

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
    
    
    # 3. بناء رسالة الواتساب النهائية
    whatsapp_message = f"💰 *طلب شراء جديد (تم إرسال إيصال الدفع):*\n"
    whatsapp_message += f"**- العميل**: @{update.effective_user.username} (ID: {update.effective_user.id})\n"
    whatsapp_message += f"**- المنتج**: {product_type}\n"
    whatsapp_message += f"**- الموديل/الاسم**: {product_label}\n"
    whatsapp_message += f"**- السعر المدفوع**: {paid_amount}\n"
    
    if names_text and names_text != "لا يوجد":
        whatsapp_message += f"**- التفاصيل الإضافية**: {names_text}\n"
    if date_text:
        whatsapp_message += f"**- التاريخ**: {date_text}\n"
    
    # إرفاق رابط الإيصال
    whatsapp_message += f"**- رابط إيصال الدفع**: {receipt_url}\n"
    
    # إذا كانت ساعة زجاج، إرفاق رابط الصورة
    if product_type.startswith("ساعة زجاج"):
        photo_link = context.user_data.get('clock_photo_link')
        if photo_link:
            whatsapp_message += f"**- رابط صورة الساعة**: {photo_link}\n"
            
    # إذا كان مج (تصميم خاص) نرفق روابط الصور
    if product_type == "مج (تصميم خاص)":
        photo_links = context.user_data.get('mug_photo_links', [])
        if photo_links:
             whatsapp_message += f"**- عدد الصور المرفقة**: {len(photo_links)}\n"
             for i, link in enumerate(photo_links):
                whatsapp_message += f"**- رابط صورة {i+1}**: {link}\n"


    # 4. تجهيز رابط الواتساب المشفر
    encoded_message = quote_plus(whatsapp_message)
    whatsapp_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"

    
    # 5. إرسال رسالة التأكيد النهائية للعميل
    confirmation_text = (
        "✅ **تم استلام إيصال الدفع بنجاح!**\n\n"
        "يتم الآن مراجعة طلبك من قبل فريق المبيعات.\n"
        "برجاء التواصل معنا على الواتساب عبر الزر بالأسفل لتأكيد الطلب وبدء التنفيذ:\n"
    )
    
    whatsapp_keyboard = [[InlineKeyboardButton("💬 تأكيد الطلب عبر الواتساب", url=whatsapp_link)]]
    whatsapp_reply_markup = InlineKeyboardMarkup(whatsapp_keyboard)
    
    update.effective_chat.send_message(
        text=confirmation_text,
        reply_markup=whatsapp_reply_markup,
        parse_mode="Markdown"
    )
    
    # 6. إنهاء المحادثة ومسح البيانات المؤقتة
    context.user_data.clear()
    return ConversationHandler.END


# --- [دوال المحادثات الخاصة بالمحافظ] ---
def get_wallet_items():
    return engraved_wallet_submenu

def prompt_for_name(update, context):
    query = update.callback_query
    query.answer()
    wallet_callback = query.data # wallet_bege, wallet_brown, wallet_black
    items_list = get_wallet_items()
    selected_wallet_data = next((item for item in items_list if item["callback"] == wallet_callback), None)

    if not selected_wallet_data:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['wallet_product'] = selected_wallet_data
    context.user_data['state'] = GET_WALLET_NAME

    back_keyboard = [
        [InlineKeyboardButton("🔙 رجوع", callback_data="engraved_wallet")]
    ]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # نحذف رسالة الأزرار القديمة
    try:
        query.message.delete()
    except Exception:
        pass
        
    caption_text = (
        f"✅ تم اختيار **{selected_wallet_data['label']}** (السعر: *{selected_wallet_data.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك، **اكتب الاسم الذي تريد حفره** على المحفظة في رسالة نصية بالأسفل."
        "او اضغط زر **رجوع** للعودة الي القائمة السابقة\n"
        "أو اضغط زر الرجوع لتغيير لون المحفظة."
    )
    
    try:
        update.effective_chat.bot.send_photo(
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
    
    return prompt_for_payment_and_receipt(update, context, product_type="محفظة")

# --- [دوال المحادثات الخاصة بالأقلام] ---
def get_pen_items():
    return aqlam_submenu

def start_pen_purchase(update, context):
    query = update.callback_query
    query.answer()
    pen_callback = query.data # buy_aqlam_metal or buy_aqlam_luminous
    product_callback = pen_callback.replace("buy_", "")
    items_list = get_pen_items()
    selected_pen_data = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_pen_data:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['pen_product'] = selected_pen_data
    context.user_data['state'] = GET_PEN_NAME

    back_keyboard = [
        [InlineKeyboardButton("🔙 رجوع", callback_data="aqlam")]
    ]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # نحذف رسالة الأزرار القديمة
    try:
        query.message.delete()
    except Exception:
        pass
        
    caption_text = (
        f"✅ تم اختيار **{selected_pen_data['label']}** (السعر: *{selected_pen_data.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك، **اكتب الاسم الذي تريد حفره** على القلم في رسالة نصية بالأسفل."
        "او اضغط زر **رجوع** للعودة الي القائمة السابقة\n"
        "أو اضغط زر الرجوع لتغيير نوع القلم."
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

def receive_pen_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    context.user_data['pen_engraving_name'] = engraving_name
    
    return prompt_for_payment_and_receipt(update, context, product_type="قلم")

# --- [دوال المحادثات الخاصة بالبوكس] ---
def get_box_items():
    return katb_kitab_box_submenu

def start_box_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_box_m1
    product_callback = data.replace("buy_", "")
    items_list = get_box_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['box_product'] = selected_product
    context.user_data['state'] = GET_BOX_COLOR
    
    # أزرار اختيار اللون (لنفترض لونين فقط)
    color_keyboard = [
        [InlineKeyboardButton("لون أبيض", callback_data="color_white")],
        [InlineKeyboardButton("لون بيج", callback_data="color_bege")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")] 
    ]
    reply_markup = InlineKeyboardMarkup(color_keyboard)

    # حذف الرسالة القديمة
    try:
        query.message.delete()
    except Exception:
        pass

    caption_text = (
        f"✅ تم اختيار **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك، **اختر لون البوكس** المطلوب من القائمة بالأسفل:"
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

    return GET_BOX_COLOR

def save_box_color_ask_names(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data.startswith("color_"):
        color = query.data.replace("color_", "")
        context.user_data['box_color'] = color
    else:
        # إذا تم الضغط على زر الرجوع في مرحلة اللون
        return back_to_box_menu(update, context)

    selected_product = context.user_data.get('box_product')
    
    # زر الرجوع يعود لقائمة الألوان
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_box_color")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # نحذف رسالة اللون
    try:
        query.message.delete()
    except Exception:
        pass

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ تم اختيار اللون **{context.user_data['box_color']}**.\n\nمن فضلك الآن **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_BOX_NAMES

def back_to_box_menu(update, context):
    query = update.callback_query
    # إعادة تشغيل عملية اختيار اللون
    return start_box_purchase(update, context)


def receive_box_names_and_finish(update, context):
    names = update.message.text
    context.user_data['box_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_box_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    return GET_BOX_DATE 

def back_to_box_names(update, context):
    query = update.callback_query
    query.answer()
    
    selected_product = context.user_data.get('box_product')
    # زر الرجوع يعود لقائمة الألوان
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except Exception:
        pass

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_BOX_NAMES

def receive_box_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['box_date'] = date_text
    
    return prompt_for_payment_and_receipt(update, context, product_type="بوكس كتب كتاب")


# --- [دوال المحادثات الخاصة بصواني اكليريك] ---
def get_akerik_tray_items():
    # نبحث عن قائمة صواني شبكة اكليريك
    return sawany_submenu[0]['items']

def start_akerik_tray_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_akerik_m1
    product_callback = data.replace("buy_", "")
    items_list = get_akerik_tray_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['akerik_tray_product'] = selected_product
    context.user_data['state'] = GET_TRAY_NAMES
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_akerik")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except Exception:
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
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    return GET_TRAY_NAMES

def back_to_akerik_tray_names(update, context):
    query = update.callback_query
    query.answer()
    
    selected_tray = context.user_data.get('akerik_tray_product')
    if not selected_tray:
        start(update, context)
        return ConversationHandler.END
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_akerik")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except Exception:
        pass

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_TRAY_NAMES


def save_akerik_tray_names_ask_date(update, context):
    names = update.message.text
    context.user_data['akerik_tray_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_akerik_tray_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_TRAY_DATE

def receive_akerik_tray_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['akerik_tray_date'] = date_text
    
    return prompt_for_payment_and_receipt(update, context, product_type="صينية اكليريك")


# --- [دوال المحادثات الخاصة بصواني خشب] ---
def get_khashab_tray_items():
    # نبحث عن قائمة صواني شبكة خشب
    return sawany_submenu[1]['items']

def start_khashab_tray_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_khashab_m1
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
    except Exception:
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
    except Exception:
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
    
    return prompt_for_payment_and_receipt(update, context, product_type="صينية خشب")


# --- [دوال المحادثات الخاصة بطارات اكليريك] ---
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
    except Exception:
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
    except Exception:
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


# --- [دوال المحادثات الخاصة بطارات خشب] ---
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
    except Exception:
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
    except Exception:
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


# --- [دوال المحادثات الخاصة بالبصامات] ---
def get_bsamat_items():
    return bsamat_submenu

def start_bsamat_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_bsamat_m1
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
    except Exception:
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
    except Exception:
        pass

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_BSAMAT_NAMES


def save_bsamat_names_ask_date(update, context):
    names = update.message.text
    context.user_data['bsamat_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_bsamat_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_BSAMAT_DATE

def receive_bsamat_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['bsamat_date'] = date_text
    
    return prompt_for_payment_and_receipt(update, context, product_type="بصامة")

# --- [دوال المحادثات الخاصة بالمناديل] ---
def get_tissue_items():
    return wedding_tissues_submenu

def start_tissue_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_tissue_m1
    product_callback = data.replace("buy_", "")
    items_list = get_tissue_items()
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
    except Exception:
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
    except Exception:
        pass

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_TISSUE_NAMES


def save_tissue_names_ask_date(update, context):
    names = update.message.text
    context.user_data['tissue_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_tissue_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_TISSUE_DATE

def receive_tissue_date_and_finish(update, context):
    date_text = update.message.text
    context.user_data['tissue_date'] = date_text
    
    return prompt_for_payment_and_receipt(update, context, product_type="منديل كتب كتاب")

# --- [دوال المحادثات الخاصة بالمرايا] ---
def get_mirrors_items():
    return mirrors_submenu

def start_mirror_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_mirror_m1
    product_callback = data.replace("buy_", "")
    items_list = get_mirrors_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['mirror_product'] = selected_product
    context.user_data['state'] = GET_MIRROR_SIZE # الحالة الأولي هي طلب المقاس
    
    # 3 أزرار للمقاسات (مقاس صغير، متوسط، كبير)
    keyboard = [
        [InlineKeyboardButton("مقاس صغير (سعر 100 ج)", callback_data="size_small_100")],
        [InlineKeyboardButton("مقاس متوسط (سعر 150 ج)", callback_data="size_medium_150")],
        [InlineKeyboardButton("مقاس كبير (سعر 200 ج)", callback_data="size_large_200")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="mirrors")] 
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # حذف الرسالة القديمة
    try:
        query.message.delete()
    except Exception:
        pass

    caption_text = (
        f"✅ تم اختيار **{selected_product['label']}**\n\n"
        "من فضلك، **اختر المقاس** المطلوب من القائمة بالأسفل:"
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

    return GET_MIRROR_SIZE

def save_mirror_size_ask_name(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data.startswith("size_"):
        # size_small_100
        size_data = query.data.replace("size_", "")
        size_label = size_data.split('_')[0]
        size_price = size_data.split('_')[1]

        context.user_data['mirror_size'] = size_label
        # نعدل سعر المنتج في الـ context
        context.user_data['mirror_product']['price'] = f"{size_price} ج"
    else:
        # إذا تم الضغط على زر الرجوع في مرحلة المقاس
        return back_to_mirror_menu(update, context)

    selected_product = context.user_data.get('mirror_product')
    size_label = context.user_data.get('mirror_size')
    
    # زر الرجوع يعود لقائمة المرايا
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="mirrors")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # نحذف رسالة المقاس
    try:
        query.message.delete()
    except Exception:
        pass
        
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ تم اختيار مقاس **{size_label}** بسعر **{selected_product['price']}**.\n\nمن فضلك الآن **اكتب الاسم الذي تريد حفره** على المرآة في رسالة نصية بالأسفل:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_MIRROR_NAME

def back_to_mirror_menu(update, context):
    query = update.callback_query
    # يتم إعادة تشغيل عملية اختيار المقاس
    return start_mirror_purchase(update, context)

def receive_mirror_name_and_finish(update, context):
    name = update.message.text
    context.user_data['mirror_name'] = name
    
    return prompt_for_payment_and_receipt(update, context, product_type="مرايا")


# --- [دوال المحادثات الخاصة بيد الهوايا] ---
def get_fans_items():
    return fans_submenu

def start_fan_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_fan_m1
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
    except Exception:
        pass
        
    caption_text = (
        f"✅ تم اختيار **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك، **اكتب الاسم الذي تريد حفره** على يد الهوايا في رسالة نصية بالأسفل."
        "او اضغط زر **رجوع** للعودة الي القائمة السابقة:"
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
        
    return GET_FAN_NAME

def back_to_fan_menu(update, context):
    query = update.callback_query
    # يتم العودة لقائمة المنتجات المباشرة (fans)
    fans_list = get_fans_items()
    show_product_page(update, "fans", fans_list, is_direct_list=True)
    return ConversationHandler.END 

def receive_fan_name_and_finish(update, context):
    name = update.message.text
    context.user_data['fan_name'] = name
    
    return prompt_for_payment_and_receipt(update, context, product_type="يد هوايا")

# --- [دوال المحادثات الخاصة بساعات الزجاج] ---
def get_clocks_items():
    return clocks_submenu

def start_clock_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_clock_glass
    product_callback = data.replace("buy_", "")
    items_list = get_clocks_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['clock_product'] = selected_product
    context.user_data['state'] = GET_CLOCK_SIZE # الحالة الأولي هي طلب المقاس
    
    # 2 أزرار للمقاسات
    keyboard = [
        [InlineKeyboardButton("مقاس صغير (سعر 200 ج)", callback_data="clock_size_small_200")],
        [InlineKeyboardButton("مقاس كبير (سعر 280 ج)", callback_data="clock_size_large_280")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="clocks")] 
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # حذف الرسالة القديمة
    try:
        query.message.delete()
    except Exception:
        pass

    caption_text = (
        f"✅ تم اختيار **{selected_product['label']}**\n\n"
        "من فضلك، **اختر المقاس** المطلوب من القائمة بالأسفل:"
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

    return GET_CLOCK_SIZE

def back_to_clocks_menu(update, context):
    query = update.callback_query
    # يتم العودة لقائمة المنتجات المباشرة (clocks)
    clocks_list = get_clocks_items()
    show_product_page(update, "clocks", clocks_list, is_direct_list=True)
    return ConversationHandler.END 


def save_clock_size_ask_photo(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data.startswith("clock_size_"):
        # clock_size_small_200
        size_data = query.data.replace("clock_size_", "")
        size_label = size_data.split('_')[0]
        size_price = size_data.split('_')[1]

        context.user_data['clock_size'] = size_label
        # نعدل سعر المنتج في الـ context
        context.user_data['clock_product']['price'] = f"{size_price} ج"
    else:
        # إذا تم الضغط على زر الرجوع
        return back_to_clocks_menu(update, context)

    selected_product = context.user_data.get('clock_product')
    size_label = context.user_data.get('clock_size')
    
    # زر الرجوع يعود لقائمة الساعات
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="clocks")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # نحذف رسالة المقاس
    try:
        query.message.delete()
    except Exception:
        pass

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ تم اختيار **{size_label}** بسعر **{selected_product['price']}**.\n\nمن فضلك الآن **أرفق الصورة المطلوب طباعتها على الساعة**، أو اضغط زر رجوع للإلغاء:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_CLOCK_PHOTO

def receive_clock_photo_and_finish(update, context):
    # التأكد من أن الرسالة صورة
    if not update.message.photo:
        update.effective_message.reply_text("⛔️ عذراً، يجب إرسال صورة فقط. يرجى إرسال الصورة المطلوب طباعتها.")
        return GET_CLOCK_PHOTO 

    # الحصول على رابط الصورة
    photo_file = update.message.photo[-1].get_file()
    photo_link = photo_file.file_path
    context.user_data['clock_photo_link'] = photo_link
    
    return prompt_for_payment_and_receipt(update, context, product_type="ساعة زجاج")


# --- [🔥 دوال المحادثات الخاصة بـ التابلوهات (تمت الإضافة)] ---
def start_tabloh_purchase(update, context):
    query = update.callback_query
    query.answer()
    
    # حالة التابلوهات
    context.user_data['state'] = GET_TABLOH_SIZE 
    
    # 4 أزرار للمقاسات
    keyboard = [
        [InlineKeyboardButton("مقاس 1 (سعر 100 ج)", callback_data="tabloh_100")],
        [InlineKeyboardButton("مقاس 2 (سعر 200 ج)", callback_data="tabloh_200")],
        [InlineKeyboardButton("مقاس 3 (سعر 300 ج)", callback_data="tabloh_300")],
        [InlineKeyboardButton("مقاس 4 (سعر 400 ج)", callback_data="tabloh_400")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")] 
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # حذف الرسالة القديمة
    try:
        query.message.delete()
    except Exception:
        pass

    message_text = "✅ *تابلوهات*\n\nمن فضلك، **اختر المقاس المطلوب** من القائمة بالأسفل (السعر شامل الطباعة):"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    return GET_TABLOH_SIZE

def save_tabloh_size_and_finish(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data.startswith("tabloh_"):
        # tabloh_100
        size_data = query.data.replace("tabloh_", "")
        price = size_data
        
        size_label = ""
        if price == "100": size_label = "مقاس 1"
        elif price == "200": size_label = "مقاس 2"
        elif price == "300": size_label = "مقاس 3"
        elif price == "400": size_label = "مقاس 4"
        else: size_label = "غير محدد"

        context.user_data['tabloh_size'] = size_label
        context.user_data['tabloh_price'] = f"{price} ج"
        
        # الانتقال إلى مرحلة الدفع مباشرة (هذا المنتج لا يحتاج صورة هنا، يفترض أن العميل سيرسلها لاحقاً في الواتساب)
        return prompt_for_payment_and_receipt(update, context, product_type="تابلوه")
    
    else:
        # إذا تم الضغط على زر الرجوع
        start(update, context)
        return ConversationHandler.END


# --- [🔥 دوال المحادثات الخاصة بـ المجات (تصميم خاص) ] ---
# قائمة المجات: mugat_submenu (فيها white/magic/digital)
# مج ديجتال له معالج خاص (digital_mug_handler)
# مج ابيض و سحري تحتاج صور، لذا يتم معالجتها هنا
def get_mug_design_items():
    # مج ابيض ومج سحري
    return mugat_submenu[0]['items'] + mugat_submenu[1]['items']

def start_mug_photos_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_mugat_white_m1
    product_callback = data.replace("buy_", "")
    items_list = get_mug_design_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['direct_product'] = selected_product
    context.user_data['mug_photo_links'] = [] # تهيئة قائمة الصور
    context.user_data['state'] = GET_MUG_PHOTOS # الحالة الأولي هي طلب الصورة
    
    # زر الرجوع يعود لقائمة المجات
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="mugat")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # حذف الرسالة القديمة
    try:
        query.message.delete()
    except Exception:
        pass

    caption_text = (
        f"✅ تم اختيار **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        "هذا المنتج يتطلب طباعة **3 صور** بحد أقصى.\n\n"
        "من فضلك، **أرسل الصورة رقم 1** في رسالة منفصلة بالأسفل، أو اضغط زر رجوع للإلغاء:"
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


def receive_mug_photos(update, context):
    # التأكد من أن الرسالة صورة
    if not update.message.photo:
        update.effective_message.reply_text("⛔️ عذراً، يجب إرسال صورة فقط. يرجى إرسال الصورة المطلوب طباعتها.")
        return GET_MUG_PHOTOS 

    # الحصول على رابط الصورة
    photo_file = update.message.photo[-1].get_file()
    photo_link = photo_file.file_path
    
    context.user_data['mug_photo_links'].append(photo_link)
    
    count = len(context.user_data['mug_photo_links'])
    remaining = 3 - count

    if remaining > 0:
        # ما زلنا ننتظر صور إضافية
        update.effective_message.reply_text(f"✅ تم استلام الصورة رقم {count}.\n📸 متبقي {remaining} صور. من فضلك أرسل الصورة التالية:")
        return GET_MUG_PHOTOS
    else:
        # تم استلام 3 صور
        update.effective_message.reply_text("✅ تم استلام الصور الثلاث بنجاح.\nجاري تحضير تفاصيل الدفع...")
        
        # الانتقال لمرحلة الدفع
        # بما أننا حفظنا المنتج في direct_product، يمكننا استخدام product_type المناسب
        p_data = context.user_data.get('direct_product')
        p_type = "مج (تصميم خاص)" 
        return prompt_for_payment_and_receipt(update, context, product_type=p_type)


# --- 🔥🔥 دوال خاصة بالمج الديجتال (تتطلب اسم الحفر) 🔥🔥 --- 
def start_digital_mug_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data
    product_callback = data.replace("buy_", "")
    
    # البحث عن المنتج داخل قائمة المج الديجتال
    items_list = mugat_submenu[2]['items'] # mugat_digital is index 2
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
    except Exception:
        pass
        
    caption_text = (
        f"✅ تم اختيار **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك، **اكتب الاسم الذي تريد حفره** على المج في رسالة نصية بالأسفل."
        "او اضغط زر **رجوع** للعودة الي القائمة السابقة:"
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
        
    return GET_DIGITAL_MUG_NAME

def receive_digital_mug_name_and_finish(update, context):
    name = update.message.text
    context.user_data['digital_mug_name'] = name
    
    return prompt_for_payment_and_receipt(update, context, product_type="مج ديجتال")


# --- [🔥🔥 دوال المحادثات الخاصة بالمباخر (الجديدة)] ---
def get_mabakhir_items():
    return mabakhir_submenu

def start_mabkhara_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_mabkhara_m1
    product_callback = data.replace("buy_", "")
    items_list = get_mabakhir_items()
    
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['mabkhara_product'] = selected_product
    context.user_data['state'] = GET_MABAKHIR_DETAILS
    
    # زر الرجوع يعود لقائمة المباخر
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="mabakhir")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # حذف الرسالة القديمة
    try:
        query.message.delete()
    except Exception:
        pass
        
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك **اكتب هنا اي تفاصيل اضافية خاصة بك** "
        "او اكتب **لا يوجد** اذا لم يكن لديك اي تفاصيل اضافية "
        "او اضغط **رجوع** للعودة الي القائمة السابقة:"
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
        # Fallback in case of image error or if no image URL is valid
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    return GET_MABAKHIR_DETAILS

def back_to_mabakhir_menu(update, context):
    query = update.callback_query
    query.answer()
    
    # نستخدم نفس طريقة عرض صفحة المنتج للقائمة المباشرة
    mabakhir_list = get_mabakhir_items()
    show_product_page(update, "mabakhir", mabakhir_list, is_direct_list=True)
    
    return ConversationHandler.END # نخرج من المحادثة ونعتمد على زر الرجوع في show_product_page ليعيدنا للقائمة الرئيسية

def receive_mabkhara_details_and_finish(update, context):
    details = update.message.text
    context.user_data['mabkhara_details'] = details
    
    # نجهز بيانات المنتج لنمررها لدالة الدفع
    product_data = context.user_data.get('mabkhara_product', {})
    product_type = product_data.get('label', 'مبخرة')
    
    # إضافة التفاصيل الإضافية كجزء من البيانات النهائية
    if details.strip() != "لا يوجد":
        context.user_data['final_names'] = details # نستخدم حقل الأسماء لتمرير التفاصيل الإضافية
    
    return prompt_for_payment_and_receipt(update, context, product_type=product_type)


# --------------------
# 4. دالة معالجة الأزرار (CallbackQueryHandler)
# --------------------

def button(update, context):
    query = update.callback_query
    data = query.data

    # 0. معالجة إلغاء المحادثة (فقط عندما لا نكون في محادثة ConversationHandler)
    if data == "cancel":
        return cancel_and_end(update, context)

    # 1. العودة للقائمة الرئيسية
    if data == "main_menu":
        start(update, context)
        return

    # 2. معالجة فتح قوائم المستوى الأول (sawany, taarat, haram, doro3, mugat, aqlam, engraved_wallet)
    # 🔥 ملاحظة: القوائم التي تحتاج عرض منتجات مباشرة تم معالجتها في الخطوة 3
    if data in ["sawany", "taarat", "haram", "doro3", "mugat", "aqlam", "engraved_wallet"]:
        # mugat و aqlam و engraved_wallet تحتوي على مستويين، لذا نستخدم show_submenu
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus[data], clean_title, back_callback="main_menu")
        return

    # 3. معالجة فتح قوائم المستوى الأول المباشرة (bsamat, wedding_tissues, abajorat, katb_kitab_box, mirrors, fans, sublimation, clocks, mabakhir)
    # 🔥 ملاحظة: تم حذف "tablohat" من هنا لأن لها معالج محادثة خاص بها
    if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "mirrors", "fans", "sublimation", "clocks", "mabakhir"]: # 🔥🔥🔥 تمت إضافة mabakhir
        # Find the correct submenu list
        submenu_list = all_submenus.get(data)
        
        # إذا كانت "بصمات" أو أي قائمة أخرى تحتاج عرض المنتجات أولاً
        if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "mirrors", "fans", "sublimation", "clocks", "mabakhir"]: # 🔥🔥🔥 تمت إضافة mabakhir
            show_product_page(update, data, submenu_list, is_direct_list=True)
            return

    # 4. معالجة فتح قوائم المستوى الثاني (sawany_akerik, taarat_khashab, haram_metal, mugat_white...)
    if data in product_to_submenu_map:
        parent_menu_key = product_to_submenu_map[data] 
        
        # البحث عن القائمة الفرعية المناسبة
        if parent_menu_key in ["sawany", "taarat", "haram", "doro3", "mugat"]: 
            # قوائم متداخلة
            parent_list = all_submenus.get(parent_menu_key, [])
            selected_list_info = next((item for item in parent_list if item["callback"] == data), None)

            if selected_list_info and 'items' in selected_list_info:
                # هذه قائمة منتجات داخل قائمة فرعية (مثل: صواني اكليريك)
                list_name = selected_list_info["label"]
                clean_name = list_name.split()[-1]
                show_product_page(update, data, selected_list_info['items'])
                return
        
        # إذا كانت القائمة هي mugat_digital (مجات ديجتال)، نعرض المنتجات
        if parent_menu_key == "mugat" and data == "mugat_digital":
            # Mugat digital index is 2 in mugat_submenu
            digital_list = all_submenus.get(parent_menu_key, [])[2]['items']
            show_product_page(update, data, digital_list)
            return
            
        # إذا كانت القائمة هي aqlam أو engraved_wallet، نعرض المنتجات
        if parent_menu_key == "aqlam" or parent_menu_key == "engraved_wallet":
            # هذه قوائم منتجات تحتاج لمعالج محادثة (لذا هي قائمة مباشرة وليست متداخلة)
            product_list = all_submenus.get(data)
            show_product_page(update, data, product_list, is_direct_list=True)
            return
            
            
    # إذا لم يتم العثور على إجراء، ننبه المستخدم ونعود للقائمة الرئيسية (احتياطي)
    if data in ["back_to_box_color", "back_to_box_names", "back_to_akerik_tray_names", "back_to_khashab_tray_names", "back_to_akerik_taarat_names", "back_to_khashab_taarat_names", "back_to_bsamat_names", "back_to_tissue_names", "back_to_pen_types", "back_to_wallets_color"]:
        query.answer("يرجى إتمام العملية الجارية أو الضغط على /start للبدء من جديد.", show_alert=True)
        return
        
    query.answer("إجراء غير معروف.", show_alert=True)
    start(update, context) # عودة للقائمة الرئيسية كإجراء احتياطي


def handle_messages(update, context):
    # وظيفة لمعالجة أي رسائل نصية لا تندرج تحت محادثة نشطة
    user_name = update.effective_user.first_name
    update.effective_message.reply_text(
        f"عفواً {user_name}، لا يمكنني فهم طلبك حالياً. يمكنك استخدام /start للبدء من جديد أو اختيار منتج من القوائم.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]])
    )

# --------------------
# 5. دالة main لتشغيل البوت
# --------------------
def main():
    # ⚠️ تم استعادة استخدام متغير البيئة BOT_TOKEN كما طلبت
    TOKEN = os.environ.get('TOKEN')
    if not TOKEN:
        # يفضل طباعة رسالة خطأ أو استخدام قيمة placeholder إذا لم يتم العثور على التوكن
        print("Error: BOT_TOKEN environment variable is not set. Please set it or hardcode the token.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # تعريف معالجات المحادثات
    # جميع المحادثات تنتهي في حالة GET_PAYMENT_RECEIPT

    # 1. بوكس كتب الكتاب
    box_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_box_purchase, pattern='^buy_box_.*$')],
        states={
            GET_BOX_COLOR: [
                CallbackQueryHandler(save_box_color_ask_names, pattern='^color_.*$|^katb_kitab_box$')
            ],
            GET_BOX_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, receive_box_names_and_finish),
                CallbackQueryHandler(back_to_box_menu, pattern='^katb_kitab_box$')
            ],
            GET_BOX_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_box_date_and_finish)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_box_names, pattern='^back_to_box_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # صواني شبكة اكليريك
    tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_tray_purchase, pattern='^buy_akerik_m.*$')],
        states={
            GET_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_akerik_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_akerik$') 
            ],
            GET_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_akerik_tray_date_and_finish)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_akerik_tray_names, pattern='^back_to_akerik_tray_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # صواني شبكة خشب
    khashab_tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_tray_purchase, pattern='^buy_khashab_m.*$')],
        states={
            GET_KHASHAB_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_khashab$') 
            ],
            GET_KHASHAB_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_khashab_tray_date_and_finish)],
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
        entry_points=[CallbackQueryHandler(start_akerik_taarat_purchase, pattern='^buy_taarat_akerik_m.*$')],
        states={
            GET_AKRILIK_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_akerik_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_akerik$') 
            ],
            GET_AKRILIK_TAARAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_akerik_taarat_date_and_finish)],
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
        entry_points=[CallbackQueryHandler(start_khashab_taarat_purchase, pattern='^buy_taarat_khashab_m.*$')],
        states={
            GET_KHASHAB_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_khashab$') 
            ],
            GET_KHASHAB_TAARAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_khashab_taarat_date_and_finish)],
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
        entry_points=[CallbackQueryHandler(start_bsamat_purchase, pattern='^buy_bsamat_m.*$')],
        states={
            GET_BSAMAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_bsamat_names_ask_date),
                CallbackQueryHandler(button, pattern='^bsamat$')
            ],
            GET_BSAMAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_bsamat_date_and_finish)],
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
        entry_points=[CallbackQueryHandler(start_tissue_purchase, pattern='^buy_tissue_m.*$')],
        states={
            GET_TISSUE_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tissue_names_ask_date),
                CallbackQueryHandler(button, pattern='^wedding_tissues$')
            ],
            GET_TISSUE_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_tissue_date_and_finish)],
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
    # تبدأ المحادثة عند اختيار اللون (wallet_bege/wallet_brown/wallet_black)
    engraved_wallet_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prompt_for_name, pattern='^wallet_.*$')],
        states={
            GET_WALLET_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_wallet_name_and_prepare_whatsapp),
                CallbackQueryHandler(button, pattern='^engraved_wallet$') # رجوع يعود لقائمة المحافظ (عرض المنتجات)
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

    # أقلام محفورة بالاسم
    engraved_pen_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_pen_purchase, pattern='^buy_aqlam_.*$')],
        states={
            GET_PEN_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp),
                CallbackQueryHandler(button, pattern='^aqlam$') # رجوع يعود لقائمة الأقلام (عرض المنتجات)
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

    # 🔥 معالج المرايا (يحتاج اختيار مقاس ثم اسم)
    mirrors_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_mirror_purchase, pattern='^buy_mirror_m.*$')],
        states={
            GET_MIRROR_SIZE: [CallbackQueryHandler(save_mirror_size_ask_name, pattern='^size_.*$|^mirrors$')],
            GET_MIRROR_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_mirror_name_and_finish)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_mirror_menu, pattern='^back_to_mirror_menu$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 🔥 معالج يد الهوايا (يحتاج اسم حفر)
    fans_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_fan_purchase, pattern='^buy_fan_m.*$')],
        states={
            GET_FAN_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_fan_name_and_finish),
                CallbackQueryHandler(back_to_fan_menu, pattern='^fans$') 
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

    # 🔥 معالج ساعات الزجاج (يحتاج مقاس ثم صورة)
    clocks_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_clock_purchase, pattern='^buy_clock_glass$')],
        states={
            GET_CLOCK_SIZE: [CallbackQueryHandler(save_clock_size_ask_photo, pattern='^clock_size_.*$|^clocks$')],
            GET_CLOCK_PHOTO: [MessageHandler(Filters.photo, receive_clock_photo_and_finish)],
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
    
    # 🔥 معالج التابلوهات (يحتاج مقاس فقط)
    tablohat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tabloh_purchase, pattern='^tablohat$')],
        states={
            GET_TABLOH_SIZE: [CallbackQueryHandler(save_tabloh_size_and_finish, pattern='^tabloh_.*$')],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(button, pattern='^main_menu$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 🔥 معالج المجات (تصميم خاص) - يحتاج صور
    mug_photos_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_mug_photos_purchase, pattern='^buy_mugat_(white|magic)_m.*$')],
        states={
            GET_MUG_PHOTOS: [
                MessageHandler(Filters.photo, receive_mug_photos),
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

    # 🔥 معالج المج الديجتال - يحتاج اسم حفر
    digital_mug_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_digital_mug_purchase, pattern='^buy_mugat_digital_m.*$')],
        states={
            GET_DIGITAL_MUG_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_digital_mug_name_and_finish),
                CallbackQueryHandler(button, pattern='^mugat_digital$') 
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

    # 🔥🔥🔥 معالج المباخر الجديد (يحتاج تفاصيل إضافية)
    mabakhir_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_mabkhara_purchase, pattern='^buy_mabkhara_.*$')],
        states={
            GET_MABAKHIR_DETAILS: [
                MessageHandler(Filters.text & ~Filters.command, receive_mabkhara_details_and_finish),
                CallbackQueryHandler(back_to_mabakhir_menu, pattern='^mabakhir$') # الرجوع من التفاصيل الإضافية يعود لقائمة المباخر
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

    # معالج الشراء المباشر (للمنتجات التي لا تحتاج خطوات إضافية في التليجرام: الأهرامات، الدروع، الأباجورات، السبلميشن)
    direct_buy_handler = CallbackQueryHandler(handle_direct_buy, pattern='^buy_.*')

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
    
    # 🔥 إضافة معالج ساعات الزجاج الجديد
    dp.add_handler(clocks_handler)

    # 🔥🔥🔥 إضافة معالج المباخر الجديد
    dp.add_handler(mabakhir_handler) 

    # 🔥 إضافة معالج التابلوهات الجديد
    dp.add_handler(tablohat_handler)
    
    dp.add_handler(direct_buy_handler) 

    
    # 5. إضافة المعالجات الأساسية
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text, handle_messages))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()