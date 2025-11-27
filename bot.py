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

# 🔥🔥🔥 الحالة الجديدة للمباخر (تمت الإضافة)
GET_MABKHARA_DETAILS = 26

# 🔥🔥🔥 الحالات الجديدة للحصالات (تمت الإضافة)
GET_PIGGYBANK_TYPE = 27 
GET_PIGGYBANK_NAME = 28 


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

# 🔥 قائمة المباخر الجديدة (تمت الإضافة)
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

# 🔥🔥🔥 قائمة الحصالات الجديدة (تمت الإضافة)
piggybanks_submenu = [
    {
        "label": "حصالة سادة (يمكن تخصيصها)", 
        "callback": "piggybank_m1", 
        "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", 
        "description": "حصالة خشبية بجودة عالية، يتم حفر الاسم المطلوب عليها بالليزر.", 
        "price": "200 ج" 
    }
]


aqlam_submenu = [
    {
        "label": "قلم تاتش معدن", 
        "callback": "aqlam_metal", 
        "image": "https://instagram.fcai17-1.fna.fbcdn.net/v/t51.29350-15/469489804_558427536910090_6244832033802616988_n.webp?stp=dst-jpg_e35_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0uaW1hZ2VfdXJsZ2VuLjEwODB4MTA4MC5zZHIuZjI5MzUwLmRlZmF1bHRfaW1hZ2UuYzIifQ&_nc_ht=instagram.fcai17-1.fna.fbcdn.net&_nc_cat=110&_nc_oc=Q6cZ2QEv1Z3QLfB8iF1DqV4UOohEqOeWCOudYmrDOVct4UhOUBy5mGVp9ixk8PBZ0e05AWQ&_nc_ohc=y0KDwmDicIQQ7kNvwGt-trw&_nc_gid=NMNKuwn67_oNmN6Kpv7dRg&edm=APs17CUBAAAA&ccb=7-5&ig_cache_key=MzUxNzM5ODI2NjY2NjI2MjY3Ng%3D%3D.3-ccb7-5&oh=00_Afi2fCP-T5-Yu1en7IxAseMfRj4ePL5qG26VQHgtFRjtjQ&oe=692D99FE&_nc_sid=10d13b", 
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
    {"label": "🕰️ ساعات زجاج بالصورة", "callback": "clocks"}, 
    {"label": "🖼️ تابلوهات", "callback": "tablohat"}, # 🔥 الزر الجديد (تمت الإضافة)
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"}, 
    {"label": "♨️ مباخر", "callback": "mabakher"}, # 🔥 الزر الجديد (تمت الإضافة)
    {"label": "🐷 حصالات", "callback": "piggybanks"}, # 🔥🔥🔥 الزر الجديد (تمت الإضافة أسفل مباخر)
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
    "mabakher": mabakher_submenu, # 🔥 تمت الإضافة
    "piggybanks": piggybanks_submenu, # 🔥🔥🔥 تمت الإضافة
    "sublimation": sublimation_supplies_submenu 
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box", "mirrors", "fans", "sublimation", "clocks", "mabakher", "piggybanks"]: # 🔥🔥🔥 تمت إضافة "piggybanks"
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
        keyboard.append([InlineKeyboardButton(item["label"], callback_data=item["callback"])])
    
    # إضافة زر الرجوع
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)])
    
    # إنشاء لوحة المفاتيح النهائية
    reply_markup = InlineKeyboardMarkup(keyboard)

    # إرسال الرسالة
    message_text = f"**{title}**\n\nمن فضلك اختر المنتج المطلوب:"
    update.effective_chat.send_message(message_text, reply_markup=reply_markup, parse_mode="Markdown")


# 🛍️ دالة عرض صفحة المنتج (للقوائم الفرعية المباشرة مثل المرايا، الأقلام، إلخ)
def show_product_page(update, back_callback_data, products_list, is_direct_list=False):
    query = update.callback_query
    query.answer()
    
    # حذف الرسالة السابقة لتجنب الإزعاج
    try:
        query.message.delete()
    except Exception:
        pass
        
    # إرسال المنتجات كرسائل منفصلة (صورة + وصف + زر شراء)
    for product in products_list:
        # بناء لوحة المفاتيح للمنتج الواحد
        product_keyboard = [
            [InlineKeyboardButton("🛒 زر شراء", callback_data=f"buy_{product['callback']}")],
        ]
        
        # إذا كانت قائمة مباشرة، نضيف زر رجوع لكل رسالة (غير مرغوب، يفضل أن يكون في رسالة واحدة)
        # لكن سنلتزم بالنموذج المتبع في الكود الحالي لإضافة زر الشراء
        
        caption_text = (
            f"**{product['label']}**\n"
            f"*الوصف*: {product['description']}\n"
            f"*السعر*: **{product.get('price', 'غير متوفر')}**"
        )
        
        try:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=product['image'],
                caption=caption_text,
                reply_markup=InlineKeyboardMarkup(product_keyboard),
                parse_mode="Markdown"
            )
        except telegram.error.BadRequest as e:
            # إذا فشل إرسال الصورة (رابط خاطئ أو غير متوفر)، نرسل رسالة نصية فقط
            caption_text += "\n\n(تعذر عرض الصورة)"
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=caption_text,
                reply_markup=InlineKeyboardMarkup(product_keyboard),
                parse_mode="Markdown"
            )

    # إرسال زر الرجوع في رسالة منفصلة
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_callback_data)]]
    reply_markup_back = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="اضغط رجوع لاختيار منتج آخر:",
        reply_markup=reply_markup_back
    )

    # لا ننهي المحادثة هنا، بل ننتظر إما Buy أو Back.
    return 

# --------------------------------------------------------------------------------
# 🔥🔥🔥 دوال المحادثات الخاصة بالحصالات (تمت الإضافة)
# --------------------------------------------------------------------------------

def get_piggybanks_items():
    return piggybanks_submenu

def start_piggybank_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # buy_piggybank_m1
    product_callback = data.replace("buy_", "")

    # 1. الحصول على بيانات المنتج
    items_list = get_piggybanks_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
    
    context.user_data['piggybank_product'] = selected_product
    context.user_data['state'] = GET_PIGGYBANK_TYPE
    
    # 2. إعداد أزرار اختيار نوع الحصالة
    keyboard = [
        [InlineKeyboardButton("حصالة 5000", callback_data="piggybank_5000")],
        [InlineKeyboardButton("حصالة 1000", callback_data="piggybank_1000")],
        [InlineKeyboardButton("حصالة 2000", callback_data="piggybank_2000")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="piggybanks")] # العودة للقائمة السابقة (قائمة الحصالات)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 3. إرسال الرسالة
    try:
        query.message.delete()
    except Exception:
        pass
    
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك **اختر نوع الحصالة** لتحديد مواصفات طلبك:"
    )

    # محاولة إرسال الصورة أولاً
    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest:
        # في حالة فشل الصورة
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    return GET_PIGGYBANK_TYPE


def back_to_piggybank_types(update, context):
    query = update.callback_query
    query.answer()
    
    selected_product = context.user_data.get('piggybank_product')
    
    if not selected_product:
        start(update, context)
        return ConversationHandler.END

    context.user_data['state'] = GET_PIGGYBANK_TYPE
    
    # إعداد أزرار اختيار نوع الحصالة مرة أخرى
    keyboard = [
        [InlineKeyboardButton("حصالة 5000", callback_data="piggybank_5000")],
        [InlineKeyboardButton("حصالة 1000", callback_data="piggybank_1000")],
        [InlineKeyboardButton("حصالة 2000", callback_data="piggybank_2000")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="piggybanks")] 
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        query.message.delete()
    except Exception:
        pass
    
    caption_text = (
        f"✅ تم اختيار: **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        "من فضلك **اختر نوع الحصالة** لتحديد مواصفات طلبك:"
    )
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    return GET_PIGGYBANK_TYPE


def prompt_for_piggybank_name(update, context):
    query = update.callback_query
    data = query.data # piggybank_5000, piggybank_1000, piggybank_2000
    query.answer()

    piggybank_type_label = ""
    if data == "piggybank_5000":
        piggybank_type_label = "حصالة 5000"
    elif data == "piggybank_1000":
        piggybank_type_label = "حصالة 1000"
    elif data == "piggybank_2000":
        piggybank_type_label = "حصالة 2000"
    else:
        # خطأ غير متوقع، نعود للقائمة السابقة
        return back_to_piggybank_types(update, context)

    context.user_data['piggybank_type'] = piggybank_type_label
    context.user_data['state'] = GET_PIGGYBANK_NAME

    # زر رجوع للعودة إلى قائمة الأنواع (باستخدام callback_data: back_to_piggybank_types)
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_piggybank_types")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    try:
        query.message.delete()
    except Exception:
        pass

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f"✅ تم اختيار: **{piggybank_type_label}**\n\n"
            "من فضلك **اكتب الاسم المطلوب طباعته علي الحصالة** في رسالة نصية بالأسفل.\n"
            "او اضغط زر رجوع للعودة الي القائمة السابقة."
        ),
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_PIGGYBANK_NAME


def receive_piggybank_name_and_finish(update, context):
    engraving_name = update.message.text
    context.user_data['piggybank_engraving_name'] = engraving_name
    
    # تجهيز النوع والتفاصيل للدفع
    piggybank_type = context.user_data.get('piggybank_type', 'حصالة سادة')
    product_type_with_details = f"حصالة - {piggybank_type}"
    
    return prompt_for_payment_and_receipt(update, context, product_type=product_type_with_details)


# --------------------------------------------------------------------------------
# ... (باقي الدوال)
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# 🔥 دالة طلب الدفع (تم التعديل لتمكين النسخ المباشر)
# --------------------------------------------------------------------------------
def prompt_for_payment_and_receipt(update, context, product_type):
    """
    الدالة الجديدة التي تطلب من العميل الدفع وتحويل الحالة إلى انتظار صورة الإيصال.
    """
    # 1. إعداد تفاصيل الطلب حسب نوع المنتج
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
    elif product_type == "محافظ":
        product_data = context.user_data.get('wallet_data')
        names_details = context.user_data.get('wallet_engraving_name')
        product_type = f"{product_type} - {product_data['label']}"
    elif product_type == "اقلام":
        product_data = context.user_data.get('pen_data')
        names_details = context.user_data.get('pen_engraving_name')
        product_type = f"{product_type} - {product_data['label']}"
    # ... (باقي حالات المنتجات)
    elif product_type == "مبخرة": # 🔥 إضافة حالة المباخر
        product_data = context.user_data.get('mabkhara_product')
        names_details = context.user_data.get('mabkhara_details')
    elif product_type.startswith("حصالة"): # 🔥🔥🔥 إضافة حالة الحصالات
        product_data = context.user_data.get('piggybank_product')
        names_details = context.user_data.get('piggybank_engraving_name')
        # product_type is already formatted as "حصالة - النوع"
    elif 'direct_product' in context.user_data: 
        # ... (باقي حالات المنتجات المباشرة)
    else:
        update.effective_chat.send_message("حدث خطأ في تجهيز الطلب. يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        context.user_data.clear()
        return ConversationHandler.END
        
    # 2. حفظ تفاصيل الطلب بشكل موحد لـ handle_payment_photo
    context.user_data['final_product_type'] = product_type
    context.user_data['final_product_label'] = product_data.get('label', product_type)
    context.user_data['final_price'] = product_data.get('price', 'غير محدد')
    # سيتم استخدام names_details هنا لتخزين اسم الحفر في حالة المج الديجتال أو المرايا أو يد الهوايا أو الحصالة
    context.user_data['final_names'] = names_details if names_details else 'غير مطلوب'
    context.user_data['final_date'] = date_details if date_details else 'غير مطلوب'
    context.user_data['final_code'] = product_data.get('callback', 'N/A')
    # 🔥 حفظ رابط صورة المنتج
    context.user_data['final_product_image'] = product_data.get('image', 'غير متوفر')
    
    # 3. إعداد رسالة الدفع وأزرارها
    # ... (باقي كود إعداد رسالة الدفع)

    # 4. تغيير الحالة إلى انتظار صورة الإيصال
    context.user_data['state'] = GET_PAYMENT_RECEIPT
    return GET_PAYMENT_RECEIPT


# --------------------
# 4. دالة button للتعامل مع ضغطات الأزرار
# --------------------

def button(update, context):
    # ... (كود دالة button الأصلي)

    # 3. معالجة فتح قوائم المستوى الأول المباشرة (bsamat, wedding_tissues, abajorat, katb_kitab_box, mirrors, fans, sublimation, clocks, mabakher, piggybanks)
    # 🔥 ملاحظة: تم حذف "tablohat" من هنا لأن لها معالج محادثة خاص بها
    if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "mirrors", "fans", "sublimation", "clocks", "mabakher", "piggybanks"]: # 🔥🔥🔥 تمت إضافة "piggybanks"
        # Find the correct submenu list
        submenu_list = all_submenus.get(data)
        # إذا كانت "بصمات" أو أي قائمة أخرى تحتاج عرض المنتجات أولاً
        if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "mirrors", "fans", "sublimation", "clocks", "mabakher", "piggybanks"]: # 🔥🔥🔥 تمت إضافة "piggybanks"
            show_product_page(update, data, submenu_list, is_direct_list=True)
            return

    # ... (باقي كود دالة button الأصلي)
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
    # ... (باقي الـ handlers)

    # 🔥 إضافة معالج المباخر الجديد (تمت الإضافة)
    mabakher_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_mabkhara_purchase, pattern='^buy_mabkhara_.*')],
        states={
            GET_MABKHARA_DETAILS: [MessageHandler(Filters.text & ~Filters.command, receive_mabkhara_details_and_finish)],
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

    # 🔥🔥🔥 معالج الحصالات الجديد (تمت الإضافة)
    piggybank_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_piggybank_purchase, pattern='^buy_piggybank_.*')],
        states={
            GET_PIGGYBANK_TYPE: [
                # انتقال لحالة طلب الاسم عند اختيار نوع الحصالة
                CallbackQueryHandler(prompt_for_piggybank_name, pattern='^piggybank_5000$|^piggybank_1000$|^piggybank_2000$'),
                # الرجوع إلى قائمة المنتجات عند الضغط على "رجوع" من صفحة اختيار النوع
                CallbackQueryHandler(button, pattern='^piggybanks$') 
            ],
            GET_PIGGYBANK_NAME: [
                # استقبال الاسم المطلوب طباعته والانتقال للدفع
                MessageHandler(Filters.text & ~Filters.command, receive_piggybank_name_and_finish),
                # زر رجوع من صفحة طلب الاسم إلى صفحة اختيار النوع
                CallbackQueryHandler(back_to_piggybank_types, pattern='^back_to_piggybank_types$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            # لمعالجة زر الرجوع من رسالة طلب الاسم إلى اختيار النوع
            CallbackQueryHandler(back_to_piggybank_types, pattern='^back_to_piggybank_types$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 4. إضافة جميع ConversationHandler أولاً لضمان الأولوية
    dp.add_handler(box_handler)
    dp.add_handler(tray_handler)
    # ... (باقي الـ handlers)
    dp.add_handler(mabakher_handler)
    dp.add_handler(piggybank_handler) # 🔥🔥🔥 إضافة معالج الحصالات الجديد
    
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.all, unknown))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()