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

# 🔥 حالات تمت إضافتها لإعادة الأزرار إلى وضع المحادثة
GET_ABAJORAT_TEXT = 18  # حالة كتابة النص للأباجورات (تم استعادته)
GET_SUBLI_TEXT = 19     # حالة كتابة النص لمستلزمات سبلميشن (تم استعادته)
GET_MUGAT_PHOTO_1 = 20  # حالة صورة التصميم الأولي للمجات (تمت إضافتها للحفاظ على طلب 3 صور)
GET_MUGAT_PHOTO_2 = 21  # حالة صورة التصميم الثاني للمجات (تمت إضافتها للحفاظ على طلب 3 صور)
GET_MUGAT_PHOTO_3 = 22  # حالة صورة التصميم الثالث للمجات (تمت إضافتها للحفاظ على طلب 3 صور)


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

# 🔥 قائمة مستلزمات سبلميشن الجديدة (تم استعادتها لوضع المحادثة)
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
    {"label": "💡 اباجورات", "callback": "abajorat"}, # تم استعادته
    {"label": "✏️ اقلام", "callback": "aqlam"}, 
    {"label": "☕ مجات", "callback": "mugat"}, # تم استعادته
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"}, 
    {"label": "🖨️ مستلزمات سبلميشن", "callback": "sublimation"} # تم استعادته
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
    "sublimation": sublimation_supplies_submenu # 🔥 إضافة القائمة الجديدة
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box", "sublimation"]: # 🔥 تم تعديلها لتشمل القوائم المباشرة
        # للقوائم المباشرة، نضيف كل منتج مباشرة
        for product in submenu_list:
            # بالنسبة للأقلام والمحافظ (التي تبدأ محادثة مباشرة) يجب أن يتم معالجتها
            product_to_submenu_map[product["callback"]] = menu_key
    else:
        # للقوائم المتداخلة (sawany, taarat, mugat, ...)
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

def show_product_page(update, context, list_callback, items_list, is_direct_list=False):
    query = update.callback_query
    query.answer()
    
    # تحديد القائمة الأم للرجوع إليها
    # 1. إذا كانت قائمة مباشرة (bsamat, aqlam, ...) فترجع لـ main_menu
    if is_direct_list:
        back_callback = "main_menu"
    # 2. إذا كانت قائمة متداخلة (sawany_akerik, taarat_khashab, ...) فترجع للقائمة الفرعية (sawany, taarat, ...)
    else: 
        back_callback = product_to_submenu_map.get(list_callback, "main_menu")

    # بناء الأزرار (اسم المنتج + زر الشراء)
    keyboard = []
    
    for item in items_list:
        # إضافة زر الشراء بنمط 'buy_callback' لتمييزه عن زر عرض القائمة
        buy_callback = f"buy_{item['callback']}" 
        # نستخدم اسم المنتج كنص للزر، وفي النهاية سعر المنتج
        button_text = f"{item['label']} ({item.get('price', 'غير متوفر')})"
        # ⚠️ نستخدم اسم المنتج مباشرة لـ الأقلام والمحافظ للبدء بالمحادثة
        if list_callback in ["engraved_wallet", "aqlam"]:
             keyboard.append([InlineKeyboardButton(button_text, callback_data=item["callback"])])
        else:
            keyboard.append([InlineKeyboardButton(button_text, callback_data=buy_callback)])

    # إضافة زر الرجوع
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    # منطق عرض المنتجات: نرسل صورة المنتج الأول مع وصف القائمة العامة 
    first_item = items_list[0]
    
    # نحذف الرسالة القديمة ونرسل رسالة جديدة بالكامل
    try:
        query.message.delete()
    except Exception:
        pass 
        
    caption_text = f"✅ **{first_item['label']} والموديلات الأخرى**:\n\nمن فضلك اختر الموديل الذي تريده للبدء في التخصيص/الشراء:"

    try:
        # إرسال صورة المنتج الأول مع قائمة الأزرار
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=first_item['image'], 
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        # في حالة فشل إرسال الصورة
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text + "\n(لم نتمكن من عرض صورة العرض التوضيحية لهذا المنتج)",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# --------------------------------------------------------------------------------
# دوال شراء المنتجات المباشرة (هرم مكتب، دروع)
# --------------------------------------------------------------------------------

def prepare_whatsapp_link_for_direct_buy(update, context):
    """
    تُستخدم لشراء المنتجات التي لا تحتاج إلى محادثة تخصيص (مثل بعض أنواع الدروع والهرامات).
    بعدها يتجه العميل لصفحة الدفع مباشرة.
    """
    query = update.callback_query
    data = query.data # buy_haram_metal_m1
    product_callback = data.replace("buy_", "")

    # 1. البحث عن بيانات المنتج
    product_data = None
    product_type = ""
    # نمر على كل القوائم المتداخلة التي بقيت في الشراء المباشر
    for menu_key in ["haram", "doro3"]: # تم حذف mugat و abajorat و sublimation
        submenu_list = all_submenus[menu_key]
        for item in submenu_list:
            if 'items' in item:
                for sub_item in item['items']:
                    if sub_item["callback"] == product_callback:
                        product_data = sub_item
                        product_type = item["label"] # نستخدم اسم القائمة الفرعية كنوع للمنتج
                        break
            if product_data:
                break
        if product_data:
            break
            
    if not product_data:
        query.answer("عفواً، لا يمكن إتمام هذا الطلب حالياً.", show_alert=True)
        start(update, context)
        return

    # 3. حفظ البيانات وإرسال رسالة الدفع
    context.user_data['direct_product'] = product_data
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
    """ الدالة الجديدة التي تطلب من العميل الدفع وتحويل الحالة إلى انتظار صورة الإيصال. """
    
    # 1. إعداد تفاصيل الطلب حسب نوع المنتج
    product_data = None
    names_details = ""
    date_details = ""
    mugat_photo_details = "" # 🔥 تفاصيل إضافية للمجات
    
    if product_type == "بصامة":
        product_data = context.user_data.get('bsamat_product')
        names_details = context.user_data.get('bsamat_names')
        date_details = context.user_data.get('bsamat_date')
    elif product_type == "منديل كتب كتاب":
        product_data = context.user_data.get('tissue_product')
        names_details = context.user_data.get('tissue_names')
        date_details = context.user_data.get('tissue_date')
    elif product_type == "بوكس كتب كتاب (مخصص)":
        product_data = context.user_data.get('box_product')
        color = context.user_data.get('box_color', 'غير محدد')
        names_details = f"الأسماء: {context.user_data.get('box_names')}\nاللون المختار: {color}"
        product_type = "بوكس كتب كتاب (مخصص)"
    elif product_type == "أباجورة": # 🔥 New handler
        product_data = context.user_data.get('abajorat_product')
        names_details = context.user_data.get('abajorat_text')
        product_type = "أباجورة (مخصصة)"
    elif product_type == "مستلزم سبلميشن": # 🔥 New handler
        product_data = context.user_data.get('subli_product')
        names_details = context.user_data.get('subli_notes')
        product_type = "مستلزم سبلميشن (بملاحظات)"
    elif product_type == "مج (3 صور تصميم)": # 🔥 New handler
        product_data = context.user_data.get('mugat_product')
        photos_ids = context.user_data.get('mugat_photos', [])
        names_details = f"تم استلام 3 صور تصميم في التليجرام. (Photo IDs: {', '.join(photos_ids)})"
        product_type = "مج مخصص (3 صور)"
        mugat_photo_details = "⚠️ يرجى مراجعة آخر 3 ملفات وسائط تم استلامها من العميل قبل هذه الرسالة مباشرة."
    elif product_type == "صينية اكليريك":
        product_data = context.user_data.get('tray_product')
        names_details = context.user_data.get('tray_names')
        date_details = context.user_data.get('tray_date')
    elif product_type == "صينية خشب":
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
    elif product_type.startswith("محفظة"):
        product_data = context.user_data.get('wallet_data')
        names_details = context.user_data.get('wallet_engraving_name')
        product_type = f"محفظة ({product_data.get('label', 'محفورة')})"
    elif product_type.startswith("قلم"):
        product_data = context.user_data.get('pen_data')
        names_details = context.user_data.get('pen_engraving_name')
        product_type = f"قلم ({product_data.get('label', 'محفور')})"
    elif product_data is None: # للمنتجات المباشرة (دروع، هرامات)
        product_data = context.user_data.get('direct_product')
        # product_type يتم تمريرها للدالة
    
    # 2. حفظ تفاصيل الطلب بشكل موحد لـ handle_payment_photo
    context.user_data['final_product_type'] = product_type
    context.user_data['final_product_label'] = product_data.get('label', product_type)
    context.user_data['final_price'] = product_data.get('price', 'غير محدد')
    context.user_data['final_names'] = names_details if names_details else 'غير مطلوب'
    context.user_data['final_date'] = date_details if date_details else 'غير مطلوب'
    context.user_data['final_code'] = product_data.get('callback', 'N/A')
    # 🔥 حفظ رابط صورة المنتج
    context.user_data['final_product_image'] = product_data.get('image', 'غير متوفر')
    context.user_data['final_mugat_photos'] = context.user_data.get('mugat_photos', []) # 🔥 حفظ صور المجات

    # 3. إرسال رسالة الدفع (تم التعديل)
    payment_message = (
        f"✅ *طلبك جاهز:* {context.user_data['final_product_label']}\n"
        f"💰 *السعر الإجمالي:* {context.user_data['final_price']}\n\n"
        f"{mugat_photo_details}\n\n" # 🔥 تفاصيل المجات الإضافية
        f"من فضلك قم بتحويل المبلغ على محفظة فودافون كاش.\n\n"
        f"👇 **اضغط على زر النسخ بالأسفل ليظهر الرقم في خانة الرسالة لنسخه بسهولة**.\n\n"
        f"بعد التحويل، **يرجى إرسال صورة إيصال التحويل في رسالة بالأسفل** لإتمام الطلب.\n\n"
        f"أو اضغط إلغاء للعودة للقائمة الرئيسية."
    )
    
    # 🔥 التعديل الرئيسي: استخدام switch_inline_query_current_chat لتمكين النسخ المباشر
    keyboard = [
        # هذا الزر سيضع الرقم مباشرة في خانة إدخال المستخدم
        [InlineKeyboardButton("📞 نسخ رقم المحفظة مباشرة (اضغط هنا)", switch_inline_query_current_chat=f" {VODAFONE_CASH_NUMBER}")],
        [InlineKeyboardButton("❌ إلغاء الطلب", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # نحول الحالة إلى انتظار الإيصال
    context.user_data['state'] = GET_PAYMENT_RECEIPT
    update.effective_chat.send_message(
        text=payment_message, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_PAYMENT_RECEIPT

# --------------------------------------------------------------------------------
# 🔥 دالة معالجة إيصال الدفع (تم التعديل لإضافة رابط صورة المنتج وصور التصميم)
# --------------------------------------------------------------------------------
def handle_payment_photo(update, context):
    if not update.message.photo:
        update.message.reply_text("عفواً، يرجى إرسال صورة الإيصال فقط.")
        return GET_PAYMENT_RECEIPT

    # 1. استخراج البيانات المحفوظة
    product_type = context.user_data.get('final_product_type', 'طلب مخصص')
    product_label = context.user_data.get('final_product_label', 'منتج غير محدد')
    paid_amount = context.user_data.get('final_price', 'غير محدد')
    names_text = context.user_data.get('final_names', 'غير مطلوب')
    date_text = context.user_data.get('final_date', 'غير مطلوب')
    product_image_url = context.user_data.get('final_product_image', 'غير متوفر') # 🔥 رابط صورة المنتج
    product_code = context.user_data.get('final_code', 'N/A')
    
    # 2. الحصول على رابط الإيصال (رابط صورة التليجرام)
    receipt_file_id = update.message.photo[-1].file_id
    receipt_file = context.bot.get_file(receipt_file_id)
    receipt_url = receipt_file.file_path

    user_info = update.effective_user
    telegram_contact_link = f"tg://user?id={user_info.id}"

    # ⚠️ استخراج تفاصيل الصور الإضافية (مخصص للمجات)
    mugat_photo_details = ""
    if product_type == "مج مخصص (3 صور)":
        mugat_photo_details = (
            "⚠️ تم استلام 3 صور تصميم في التليجرام. يرجى مراجعة ملفات الوسائط الأخيرة في محادثة التليجرام.\n"
        )
    
    # 3. إعداد نص رسالة الواتساب (تم التعديل)
    message_body = (
        f"🔔 *طلب شراء جديد (مدفوع)* 🔔\n\n"
        f"نوع المنتج: {product_type.replace('-', ' - ')}\n"
        f"المنتج: {product_label}\n"
        f"السعر المدفوع: *{paid_amount}*\n\n"
        f"{mugat_photo_details}" # 🔥 إضافة تفاصيل صور المجات
        f"الأسماء والتفاصيل: {names_text}\n"
        f"التاريخ/النص الإضافي: {date_text}\n\n"
        f"🔗 رابط صورة المنتج: {product_image_url}\n" # 🔥 إضافة رابط صورة المنتج
        f"🔗 رابط إيصال الدفع: {receipt_url}\n"
        f"الكود: {product_code}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"رابط التواصل عبر التليجرام: {telegram_contact_link}" # 🔥 إضافة رابط التواصل
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"

    # 4. إرسال رسالة التأكيد في تليجرام
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"تم استلام إيصال الدفع بنجاح. تفاصيل الطلب جاهزة:\n\nالمنتج: {product_label}\nالسعر: {paid_amount}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )

    # 5. إنهاء المحادثة ومسح البيانات المؤقتة
    context.user_data.clear()
    return ConversationHandler.END

# --------------------------------------------------------------------------------
# 4. دالة button لمعالجة الأزرار (Callback Queries)
# --------------------------------------------------------------------------------

def button(update, context):
    query = update.callback_query
    data = query.data

    # 0. معالجة إلغاء المحادثة (فقط في حال لم يكن داخل ConversationHandler)
    if data == "cancel":
        return cancel_and_end(update, context)

    # 1. زر الرجوع إلى القائمة الرئيسية
    if data == "main_menu":
        start(update, context)
        return

    # 2. أزرار القوائم المتداخلة (صواني، طارات، هرم مكتب، دروع، مجات)
    elif data in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        title = next(item["label"] for item in main_menu if item["callback"] == data)
        show_submenu(update, context, all_submenus[data], title)
        return

    # 3. أزرار القوائم الفرعية المتداخلة (sawany_akerik, taarat_khashab, mugat_white, ...)
    elif data in product_to_submenu_map and product_to_submenu_map[data] in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        # إذا كانت قائمة منتجات نهائية (مثل صواني اكليريك)
        current_list = next((item['items'] for item in all_submenus[product_to_submenu_map[data]] if item['callback'] == data), None)
        if current_list:
            show_product_page(update, context, data, current_list, is_direct_list=False)
        else:
            query.answer("عفواً، لا توجد موديلات متاحة حالياً.", show_alert=True)
        return

    # 4. أزرار القوائم المباشرة (بصامات، مناديل كتب الكتاب، بوكس كتب الكتاب، اباجورات، اقلام، محافظ، سبلميشن)
    elif data in ["bsamat", "wedding_tissues", "katb_kitab_box", "abajorat", "engraved_wallet", "aqlam", "sublimation"]:
        # عرض قائمة المنتجات النهائية مباشرة من القائمة الرئيسية
        show_product_page(update, context, data, all_submenus[data], is_direct_list=True)
        return 

    # 5. معالجة أزرار الشراء الفردية (للمنتجات التي لا تحتاج محادثة)
    if data.startswith("buy_"):
        # يجب أن يصل إلى هنا فقط الهرامات والدروع التي تستخدم الشراء المباشر
        # تمت إزالة اباجورات والمجات والسبلميشن من هذا المسار
        if any(prod_type in data for prod_type in ["haram", "doro3"]):
             prepare_whatsapp_link_for_direct_buy(update, context)
             return
        # إذا كان المنتج من النوع الذي يجب أن يبدأ محادثة (مثل buy_bsamat_m1)
        # سيتم التعامل معه بواسطة ConversationHandler في دالة main
        
        
    # 6. معالجة الأزرار التي تعيد المستخدم إلى قائمة فرعية سابقة
    if data in ["back_to_pen_types", "back_to_wallets_color"]:
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
    
# --------------------------------------------------------------------------------
# 5. دوال الإرجاع للمحادثات (الحالات المفقودة والمسترجعة)
# --------------------------------------------------------------------------------

def get_product_items(menu_key):
    """Retrieves the full list of products from a top-level or sub-level menu key."""
    if menu_key in ["bsamat", "wedding_tissues", "katb_kitab_box", "abajorat", "engraved_wallet", "aqlam", "sublimation"]:
        return all_submenus.get(menu_key, [])
    
    # For nested menus (sawany, taarat, mugat, haram, doro3)
    # The menu_key passed here should be the item's parent key (e.g. 'sawany_akerik')
    parent_menu_key = product_to_submenu_map.get(menu_key)
    if parent_menu_key in all_submenus:
        for item in all_submenus[parent_menu_key]:
            if item['callback'] == menu_key:
                return item.get('items', [])
    return []

def generic_start_purchase(update, context, menu_key, state_names, prompt_text, product_data_key):
    query = update.callback_query
    query.answer()
    data = query.data.replace("buy_", "")
    
    # Determine the correct items list (could be direct submenu or nested submenu)
    parent_callback = product_to_submenu_map.get(data)
    if parent_callback in ["sawany", "taarat", "mugat", "haram", "doro3"]: # Nested menus
         # In nested menus, the parent_callback is the top level ('sawany'), 
         # but the item list is under the sub-level key ('sawany_akerik')
         list_key = product_to_submenu_map.get(data)
         items_list = get_product_items(list_key)
         back_to_menu = list_key
    else: # Direct menus (bsamat, tissues, abajorat, subli, etc.)
         list_key = product_to_submenu_map.get(data)
         items_list = get_product_items(list_key)
         back_to_menu = menu_key

    selected_product = next((item for item in items_list if item["callback"] == data), None)
    
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
    
    context.user_data[product_data_key] = selected_product
    context.user_data['state'] = state_names[0]

    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_to_menu)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try: query.message.delete()
    except: pass
    
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        f"{prompt_text}"
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
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    return state_names[0]


def generic_save_names_ask_date(update, context, names_key, date_state, next_state, product_data_key, prompt_text):
    names = update.message.text
    context.user_data[names_key] = names
    context.user_data['state'] = next_state
    
    product = context.user_data.get(product_data_key)
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=date_state)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    update.message.reply_text(
        f"✅ تم حفظ الأسماء. \n\nالآن من فضلك **{prompt_text}**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return next_state
    
def generic_receive_date_and_finish(update, context, date_key, product_type):
    date_text = update.message.text
    context.user_data[date_key] = date_text
    
    return prompt_for_payment_and_receipt(update, context, product_type=product_type)

def generic_back_to_names(update, context, product_data_key, names_state, back_callback_data, prompt_text):
    query = update.callback_query
    query.answer()
    
    selected_product = context.user_data.get(product_data_key)
    if not selected_product:
        start(update, context)
        return ConversationHandler.END

    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_callback_data)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try: query.message.delete()
    except: pass

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"من فضلك أعد كتابة **{prompt_text}**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return names_state

# --- بوكس كتب الكتاب (Logic: Product -> Color Selection -> Names Input -> Payment) ---

def get_box_items():
    return katb_kitab_box_submenu

def start_box_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data.replace("buy_", "")
    items_list = get_box_items()
    selected_product = next((item for item in items_list if item["callback"] == data), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
    
    context.user_data['box_product'] = selected_product
    context.user_data['state'] = GET_BOX_COLOR

    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try: query.message.delete()
    except: pass
    
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        f"من فضلك اختر لون البوكس المطلوب (أسود في دهبي / أبيض في دهبي):"
    )
    
    color_keyboard = [
        [InlineKeyboardButton("أسود في دهبي", callback_data="color_اسود في دهبي")],
        [InlineKeyboardButton("أبيض في دهبي", callback_data="color_ابيض في دهبي")]
    ]
    color_keyboard.extend(back_keyboard)
    color_reply_markup = InlineKeyboardMarkup(color_keyboard)

    try:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=color_reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=color_reply_markup,
            parse_mode="Markdown"
        )
    return GET_BOX_COLOR

def save_box_color_ask_names(update, context):
    query = update.callback_query
    
    if query:
        query.answer()
        color = query.data.replace("color_", "")
        context.user_data['box_color'] = color
        
        # محاولة حذف رسالة اختيار اللون
        try: query.message.delete()
        except: pass
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # رسالة طلب الأسماء
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ تم اختيار اللون: *{context.user_data['box_color']}*\n\n"
             f"الآن من فضلك **اكتب اسم العريس واسم العروسة** (على سطرين منفصلين أو بفاصل واضح):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_BOX_NAMES

def receive_box_names_and_finish(update, context):
    names = update.message.text
    context.user_data['box_names'] = names
    # الانتقال لطلب الدفع مباشرة بعد استلام الأسماء
    return prompt_for_payment_and_receipt(update, context, product_type="بوكس كتب كتاب (مخصص)")

def back_to_box_menu(update, context):
    query = update.callback_query
    query.answer()
    # العودة لخطوة اختيار اللون (يجب أن يتم إعادة تهيئة عرض المنتج واختيار اللون)
    return start_box_purchase(update, context)

# --- بصامات (Logic: Product -> Names Input -> Date Input -> Payment) ---
def start_bsamat_purchase(update, context):
    return generic_start_purchase(update, context, "bsamat", [GET_BSAMAT_NAMES, GET_BSAMAT_DATE], "من فضلك **اكتب اسم العريس واسم العروسة**:", 'bsamat_product')
def save_bsamat_names_ask_date(update, context):
    return generic_save_names_ask_date(update, context, 'bsamat_names', 'back_to_bsamat_names', GET_BSAMAT_DATE, 'bsamat_product', 'اكتب التاريخ الذي تريده')
def receive_bsamat_date_and_finish(update, context):
    return generic_receive_date_and_finish(update, context, 'bsamat_date', "بصامة")
def back_to_bsamat_names(update, context):
    return generic_back_to_names(update, context, 'bsamat_product', GET_BSAMAT_NAMES, 'bsamat', 'اسم العريس واسم العروسة')

# --- مناديل كتب الكتاب (Logic: Product -> Names Input -> Date Input -> Payment) ---
def start_tissue_purchase(update, context):
    return generic_start_purchase(update, context, "wedding_tissues", [GET_TISSUE_NAMES, GET_TISSUE_DATE], "من فضلك **اكتب اسم العريس واسم العروسة**:", 'tissue_product')
def save_tissue_names_ask_date(update, context):
    return generic_save_names_ask_date(update, context, 'tissue_names', 'back_to_tissue_names', GET_TISSUE_DATE, 'tissue_product', 'اكتب التاريخ الذي تريده')
def receive_tissue_date_and_finish(update, context):
    return generic_receive_date_and_finish(update, context, 'tissue_date', "منديل كتب كتاب")
def back_to_tissue_names(update, context):
    return generic_back_to_names(update, context, 'tissue_product', GET_TISSUE_NAMES, 'wedding_tissues', 'اسم العريس واسم العروسة')

# --- صواني شبكة اكليريك (Logic: Product -> Names Input -> Date Input -> Payment) ---
def start_akerik_tray_purchase(update, context):
    return generic_start_purchase(update, context, "sawany", [GET_TRAY_NAMES, GET_TRAY_DATE], "من فضلك **اكتب اسم العريس واسم العروسة**:", 'tray_product')
def save_tray_names_ask_date(update, context):
    return generic_save_names_ask_date(update, context, 'tray_names', 'back_to_tray_names', GET_TRAY_DATE, 'tray_product', 'اكتب التاريخ الذي تريده')
def receive_tray_date_and_finish(update, context):
    return generic_receive_date_and_finish(update, context, 'tray_date', "صينية اكليريك")
def back_to_tray_names(update, context):
    return generic_back_to_names(update, context, 'tray_product', GET_TRAY_NAMES, 'sawany_akerik', 'اسم العريس واسم العروسة')


# --- صواني شبكة خشب (Logic: Product -> Names Input -> Date Input -> Payment) ---
def start_khashab_tray_purchase(update, context):
    return generic_start_purchase(update, context, "sawany", [GET_KHASHAB_TRAY_NAMES, GET_KHASHAB_TRAY_DATE], "من فضلك **اكتب اسم العريس واسم العروسة**:", 'khashab_tray_product')
def save_khashab_tray_names_ask_date(update, context):
    return generic_save_names_ask_date(update, context, 'khashab_tray_names', 'back_to_khashab_tray_names', GET_KHASHAB_TRAY_DATE, 'khashab_tray_product', 'اكتب التاريخ الذي تريده')
def receive_khashab_tray_date_and_finish(update, context):
    return generic_receive_date_and_finish(update, context, 'khashab_tray_date', "صينية خشب")
def back_to_khashab_tray_names(update, context):
    return generic_back_to_names(update, context, 'khashab_tray_product', GET_KHASHAB_TRAY_NAMES, 'sawany_khashab', 'اسم العريس واسم العروسة')

# --- طارات اكليريك (Logic: Product -> Names Input -> Date Input -> Payment) ---
def start_akerik_taarat_purchase(update, context):
    return generic_start_purchase(update, context, "taarat", [GET_AKRILIK_TAARAT_NAMES, GET_AKRILIK_TAARAT_DATE], "من فضلك **اكتب اسم العريس واسم العروسة**:", 'taarat_akerik_product')
def save_akerik_taarat_names_ask_date(update, context):
    return generic_save_names_ask_date(update, context, 'taarat_akerik_names', 'back_to_akerik_taarat_names', GET_AKRILIK_TAARAT_DATE, 'taarat_akerik_product', 'اكتب التاريخ الذي تريده')
def receive_akerik_taarat_date_and_finish(update, context):
    return generic_receive_date_and_finish(update, context, 'taarat_akerik_date', "طارة اكليريك")
def back_to_akerik_taarat_names(update, context):
    return generic_back_to_names(update, context, 'taarat_akerik_product', GET_AKRILIK_TAARAT_NAMES, 'taarat_akerik', 'اسم العريس واسم العروسة')

# --- طارات خشب (Logic: Product -> Names Input -> Date Input -> Payment) ---
def start_khashab_taarat_purchase(update, context):
    return generic_start_purchase(update, context, "taarat", [GET_KHASHAB_TAARAT_NAMES, GET_KHASHAB_TAARAT_DATE], "من فضلك **اكتب اسم العريس واسم العروسة**:", 'taarat_khashab_product')
def save_khashab_taarat_names_ask_date(update, context):
    return generic_save_names_ask_date(update, context, 'taarat_khashab_names', 'back_to_khashab_taarat_names', GET_KHASHAB_TAARAT_DATE, 'taarat_khashab_product', 'اكتب التاريخ الذي تريده')
def receive_khashab_taarat_date_and_finish(update, context):
    return generic_receive_date_and_finish(update, context, 'taarat_khashab_date', "طارة خشب")
def back_to_khashab_taarat_names(update, context):
    return generic_back_to_names(update, context, 'taarat_khashab_product', GET_KHASHAB_TAARAT_NAMES, 'taarat_khashab', 'اسم العريس واسم العروسة')


# --- محافظ محفورة بالاسم (Logic: Product -> Name Input -> Payment) ---
def get_wallet_items():
    return engraved_wallet_submenu

def prompt_for_wallet_name(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # wallet_bege, wallet_brown, etc.
    
    items_list = get_wallet_items()
    selected_product = next((item for item in items_list if item["callback"] == data), None)
    
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['wallet_data'] = selected_product
    context.user_data['state'] = GET_WALLET_NAME

    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="engraved_wallet")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try: query.message.delete()
    except: pass
    
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        f"من فضلك **اكتب الاسم الذي تريد حفره** على المحفظة (الاسم الأول فقط أو أول حرفين):"
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
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    return GET_WALLET_NAME

def receive_wallet_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    context.user_data['wallet_engraving_name'] = engraving_name
    return prompt_for_payment_and_receipt(update, context, product_type=f"محفظة")

# --- أقلام (Logic: Product -> Name Input -> Payment) ---
def get_pen_items():
    return aqlam_submenu

def prompt_for_pen_name(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # aqlam_metal, aqlam_luminous, etc.
    
    items_list = get_pen_items()
    selected_product = next((item for item in items_list if item["callback"] == data), None)
    
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['pen_data'] = selected_product
    context.user_data['state'] = GET_PEN_NAME

    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="aqlam")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try: query.message.delete()
    except: pass
    
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        f"من فضلك **اكتب الاسم/النص الذي تريد حفره** على القلم:"
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
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    return GET_PEN_NAME

def receive_pen_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    context.user_data['pen_engraving_name'] = engraving_name
    return prompt_for_payment_and_receipt(update, context, product_type=f"قلم")

# --- أباجورات (تم استرجاعه لمحادثة التخصيص) ---
def get_abajorat_items():
    return abajorat_submenu

def start_abajorat_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data.replace("buy_", "")
    items_list = get_abajorat_items()
    selected_product = next((item for item in items_list if item["callback"] == data), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
    
    context.user_data['abajorat_product'] = selected_product
    context.user_data['state'] = GET_ABAJORAT_TEXT

    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="abajorat")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try: query.message.delete()
    except: pass
    
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        f"من فضلك **اكتب النص الذي تريد حفره/طباعته** على الأباجورة في رسالة نصية بالأسفل "
        f"أو اضغط زر رجوع للعودة إلى القائمة السابقة:"
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
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    return GET_ABAJORAT_TEXT

def save_abajorat_text_and_finish(update, context):
    custom_text = update.message.text
    context.user_data['abajorat_text'] = custom_text
    return prompt_for_payment_and_receipt(update, context, product_type="أباجورة")
    
def back_to_abajorat_text(update, context):
    query = update.callback_query
    query.answer()
    selected_product = context.user_data.get('abajorat_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="abajorat")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try: query.message.delete()
    except: pass
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"من فضلك أعد كتابة **النص الذي تريده على الأباجورة**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_ABAJORAT_TEXT

# --- مستلزمات سبلميشن (تم استرجاعه لمحادثة التخصيص) ---
def get_subli_items():
    return sublimation_supplies_submenu

def start_subli_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data.replace("buy_", "")
    items_list = get_subli_items()
    selected_product = next((item for item in items_list if item["callback"] == data), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
    
    context.user_data['subli_product'] = selected_product
    context.user_data['state'] = GET_SUBLI_TEXT

    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sublimation")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try: query.message.delete()
    except: pass
    
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        f"من فضلك **اكتب ملاحظاتك بخصوص التصميم/المنتج (إن وجدت)** في رسالة نصية بالأسفل "
        f"أو اضغط زر رجوع للعودة إلى القائمة السابقة:\n\n"
        f"*(سيتم التواصل معك لاحقاً لتأكيد تفاصيل التصميم)*"
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
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    return GET_SUBLI_TEXT

def save_subli_text_and_finish(update, context):
    custom_text = update.message.text
    context.user_data['subli_notes'] = custom_text
    return prompt_for_payment_and_receipt(update, context, product_type="مستلزم سبلميشن")

def back_to_subli_text(update, context):
    query = update.callback_query
    query.answer()
    selected_product = context.user_data.get('subli_product')
    if not selected_product:
        start(update, context)
        return ConversationHandler.END
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sublimation")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    try: query.message.delete()
    except: pass
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"من فضلك أعد كتابة **ملاحظاتك بخصوص التصميم/المنتج**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_SUBLI_TEXT

# --- مجات (تم تعديلها لطلب 3 صور تصميم) ---
def get_mugat_items(list_callback):
    # mugat_white / mugat_magic / mugat_digital
    for menu in mugat_submenu:
        if menu['callback'] == list_callback:
            return menu['items']
    return []

def start_mugat_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data.replace("buy_", "") # mugat_white_m1, mugat_magic_m1, etc.
    
    # تحديد القائمة الأم للرجوع إليها
    if data.startswith("mugat_white"):
        list_callback = "mugat_white"
    elif data.startswith("mugat_magic"):
        list_callback = "mugat_magic"
    elif data.startswith("mugat_digital"):
        list_callback = "mugat_digital"
    else:
        query.answer("خطأ في تحديد نوع المج", show_alert=True)
        return ConversationHandler.END

    items_list = get_mugat_items(list_callback)
    selected_product = next((item for item in items_list if item["callback"] == data), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
    
    context.user_data['mugat_product'] = selected_product
    context.user_data['mugat_photos'] = [] # قائمة لحفظ الـ file_id
    context.user_data['state'] = GET_MUGAT_PHOTO_1
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=list_callback)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try: query.message.delete()
    except: pass
    
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        f"من فضلك أرسل **صورة التصميم الأولي (الصورة رقم 1)** الآن:"
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
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    return GET_MUGAT_PHOTO_1

def receive_mugat_photo_1(update, context):
    if not update.message.photo:
        update.message.reply_text("عفواً، يرجى إرسال **صورة** التصميم الأولي.")
        return GET_MUGAT_PHOTO_1
        
    context.user_data['mugat_photos'].append(update.message.photo[-1].file_id)
    
    list_callback = product_to_submenu_map.get(context.user_data['mugat_product']['callback'])
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=list_callback)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    update.message.reply_text("✅ تم استلام الصورة رقم 1. من فضلك أرسل **صورة التصميم الثاني (الصورة رقم 2)** الآن:", reply_markup=reply_markup)
    return GET_MUGAT_PHOTO_2

def receive_mugat_photo_2(update, context):
    if not update.message.photo:
        update.message.reply_text("عفواً، يرجى إرسال **صورة** التصميم الثاني.")
        return GET_MUGAT_PHOTO_2
        
    context.user_data['mugat_photos'].append(update.message.photo[-1].file_id)
    
    list_callback = product_to_submenu_map.get(context.user_data['mugat_product']['callback'])
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=list_callback)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    update.message.reply_text("✅ تم استلام الصورة رقم 2. من فضلك أرسل **صورة التصميم الثالث (الصورة رقم 3)** الآن:", reply_markup=reply_markup)
    return GET_MUGAT_PHOTO_3

def receive_mugat_photo_3_and_finish(update, context):
    if not update.message.photo:
        update.message.reply_text("عفواً، يرجى إرسال **صورة** التصميم الثالث.")
        return GET_MUGAT_PHOTO_3

    context.user_data['mugat_photos'].append(update.message.photo[-1].file_id)
    
    # يتم هنا الانتقال لطلب الدفع مباشرة بعد استلام الصور
    return prompt_for_payment_and_receipt(update, context, product_type="مج (3 صور تصميم)")


# --------------------
# 6. دالة main لتشغيل البوت (تم تعديل المعالجات)
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
    
    # 1. بوكس كتب الكتاب 
    box_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_box_purchase, pattern='^buy_box_.*')],
        states={
            GET_BOX_COLOR: [
                CallbackQueryHandler(save_box_color_ask_names, pattern='^color_.*$'), # تمت إزالة katb_kitab_box$ من هنا
                CallbackQueryHandler(button, pattern='^katb_kitab_box$')
            ],
            GET_BOX_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, receive_box_names_and_finish),
                CallbackQueryHandler(button, pattern='^katb_kitab_box$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_box_menu, pattern='^back_to_box_menu$'),
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
            GET_TRAY_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_tray_date_and_finish)
            ],
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
    
    # 3. صواني شبكة خشب
    khashab_tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_tray_purchase, pattern='^buy_khashab_.*')],
        states={
            GET_KHASHAB_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_khashab$')
            ],
            GET_KHASHAB_TRAY_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_khashab_tray_date_and_finish)
            ],
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

    # 4. طارات اكليريك
    akerik_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_taarat_purchase, pattern='^buy_taarat_akerik_.*')],
        states={
            GET_AKRILIK_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_akerik_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_akerik$')
            ],
            GET_AKRILIK_TAARAT_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_akerik_taarat_date_and_finish)
            ],
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

    # 5. طارات خشب
    khashab_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_taarat_purchase, pattern='^buy_taarat_khashab_.*')],
        states={
            GET_KHASHAB_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_khashab$')
            ],
            GET_KHASHAB_TAARAT_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_khashab_taarat_date_and_finish)
            ],
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

    # 6. بصامات 
    bsamat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_bsamat_purchase, pattern='^buy_bsamat_.*')],
        states={
            GET_BSAMAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_bsamat_names_ask_date),
                CallbackQueryHandler(button, pattern='^bsamat$')
            ],
            GET_BSAMAT_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_bsamat_date_and_finish)
            ],
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

    # 7. مناديل كتب الكتاب
    tissue_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tissue_purchase, pattern='^buy_tissue_.*')],
        states={
            GET_TISSUE_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tissue_names_ask_date),
                CallbackQueryHandler(button, pattern='^wedding_tissues$')
            ],
            GET_TISSUE_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_tissue_date_and_finish)
            ],
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
    
    # 8. محافظ محفورة بالاسم
    engraved_wallet_handler = ConversationHandler(
        entry_points=[
            # entry_points تستخدم الـ callback_data بدون "buy_" هنا
            CallbackQueryHandler(prompt_for_wallet_name, pattern='^wallet_bege$|^wallet_brown$|^wallet_black$')
        ],
        states={
            GET_WALLET_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_wallet_name_and_prepare_whatsapp),
                # زر الرجوع يعود إلى قائمة المحافظ 
                CallbackQueryHandler(button, pattern='^engraved_wallet$') 
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
    
    # 9. أقلام
    engraved_pen_handler = ConversationHandler(
        entry_points=[
            # entry_points تستخدم الـ callback_data بدون "buy_" هنا
            CallbackQueryHandler(prompt_for_pen_name, pattern='^aqlam_metal$|^aqlam_luminous$')
        ],
        states={
            GET_PEN_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp),
                # زر الرجوع يعود إلى قائمة الأقلام 
                CallbackQueryHandler(button, pattern='^aqlam$')
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

    # 🔥 10. أباجورات (تمت استعادته لمحادثة التخصيص)
    abajorat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_abajorat_purchase, pattern='^buy_abajora_.*')],
        states={
            GET_ABAJORAT_TEXT: [
                MessageHandler(Filters.text & ~Filters.command, save_abajorat_text_and_finish),
                CallbackQueryHandler(button, pattern='^abajorat$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_abajorat_text, pattern='^back_to_abajorat_text$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 🔥 11. مستلزمات سبلميشن (تمت استعادته لمحادثة التخصيص)
    subli_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_subli_purchase, pattern='^buy_subli_.*')],
        states={
            GET_SUBLI_TEXT: [
                MessageHandler(Filters.text & ~Filters.command, save_subli_text_and_finish),
                CallbackQueryHandler(button, pattern='^sublimation$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_subli_text, pattern='^back_to_subli_text$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 🔥 12. مجات (تم تعديلها لطلب 3 صور)
    mugat_custom_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_mugat_purchase, pattern='^buy_mugat_white_.*'),
            CallbackQueryHandler(start_mugat_purchase, pattern='^buy_mugat_magic_.*'),
            CallbackQueryHandler(start_mugat_purchase, pattern='^buy_mugat_digital_.*')
        ],
        states={
            GET_MUGAT_PHOTO_1: [
                MessageHandler(Filters.photo & ~Filters.command, receive_mugat_photo_1),
                CallbackQueryHandler(button, pattern='^mugat_white$|^mugat_magic$|^mugat_digital$')
            ],
            GET_MUGAT_PHOTO_2: [
                MessageHandler(Filters.photo & ~Filters.command, receive_mugat_photo_2),
                CallbackQueryHandler(button, pattern='^mugat_white$|^mugat_magic$|^mugat_digital$')
            ],
            GET_MUGAT_PHOTO_3: [
                MessageHandler(Filters.photo & ~Filters.command, receive_mugat_photo_3_and_finish),
                CallbackQueryHandler(button, pattern='^mugat_white$|^mugat_magic$|^mugat_digital$')
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

    # 13. الشراء المباشر (متبقي فقط الهرامات والدروع)
    direct_buy_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prepare_whatsapp_link_for_direct_buy, pattern='^buy_(haram|doro3)_.*')], # 🔥 تم إزالة abajora, mugat, subli
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
    
    # 🔥 إضافة المعالجات المسترجعة والمعدلة
    dp.add_handler(abajorat_handler) # أباجورات
    dp.add_handler(subli_handler)    # سبلميشن
    dp.add_handler(mugat_custom_handler) # مجات (3 صور)

    dp.add_handler(direct_buy_handler) # الشراء المباشر (هرامات ودروع فقط)
    

    
    # 5. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 6. معالج أزرار الـ Inline
    dp.add_handler(CallbackQueryHandler(button))
    
    # 7. معالج الرسائل النصية المتبقية
    dp.add_handler(MessageHandler(Filters.text, handle_messages))

    # بدء تشغيل البوت
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()