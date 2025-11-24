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
GET_MUG_PHOTOS = 18 # 🔥 الحالة الجديدة لطلب ارفاق الصور للمجات


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
    "sublimation": sublimation_supplies_submenu # 🔥 إضافة القائمة الجديدة
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box", "sublimation"]: # 🔥 إضافة 'sublimation'
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
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation"]: # 🔥 إضافة 'sublimation'
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
    
    # 3. Send message
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

# دوال مناديل كتب الكتاب
def get_tissue_items():
    return wedding_tissues_submenu

def start_tissue_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_tissue_m1
    product_callback = data.replace("buy_", "")
    
    # 1. Get product data
    items_list = get_tissue_items()
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['tissue_product'] = selected_product
    context.user_data['state'] = GET_TISSUE_NAMES
    
    # 2. Prepare keyboard (Back button to tissues menu)
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="wedding_tissues")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # 3. Send message
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


# دوال المحافظ
def get_wallet_items():
    return engraved_wallet_submenu

def start_wallet_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_wallet_bege
    product_callback = data.replace("buy_", "")
    
    selected_wallet_data = next((item for item in engraved_wallet_submenu if item["callback"] == product_callback), None)
    context.user_data['wallet_data'] = selected_wallet_data
    context.user_data['state'] = GET_WALLET_NAME
    
    try:
        query.message.delete()
    except Exception:
        pass
        
    # زر الرجوع يعود إلى قائمة ألوان المحافظ
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_wallets_color")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    caption_text = (f"**اختيارك: {selected_wallet_data['label']}** (السعر: *{selected_wallet_data.get('price', 'غير متوفر')}*)\n\n"
                    f"من فضلك، **اكتب الاسم الذي تريد حفره** على المحفظة في رسالة نصية بالأسفل.او اضغط زر رجوع للعودة الي القائمة السابقة\n"
                    f"أو اضغط زر الرجوع لتغيير نوع المحفظة.")
    
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

def back_to_wallets_color(update, context):
    query = update.callback_query
    query.answer()
    
    # نحاكي عملية العودة للقائمة الفرعية للمحافظ
    show_product_page(update, "engraved_wallet", engraved_wallet_submenu, is_direct_list=True)
    return ConversationHandler.END


def receive_wallet_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    context.user_data['wallet_engraving_name'] = engraving_name
    return prompt_for_payment_and_receipt(update, context, product_type="محافظ")

# دوال الأقلام
def get_pen_items():
    return aqlam_submenu

def start_pen_purchase(update, context):
    query = update.callback_query
    data = query.data  # buy_aqlam_metal
    product_callback = data.replace("buy_", "")
    
    selected_pen_data = next((item for item in aqlam_submenu if item["callback"] == product_callback), None)
    context.user_data['pen_data'] = selected_pen_data
    context.user_data['state'] = GET_PEN_NAME
    
    # زر الرجوع يعود إلى قائمة الأقلام الفرعية
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_pen_types")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    caption_text = (f"**اختيارك: {selected_pen_data['label']}** (السعر: *{selected_pen_data.get('price', 'غير متوفر')}*)\n\n"
                    f"من فضلك، **اكتب الاسم الذي تريد حفره** على القلم في رسالة نصية بالأسفل.او اضغط زر رجوع للعودة الي القائمة السابقة\n"
                    f"أو اضغط زر الرجوع لتغيير نوع القلم.")
    
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


def back_to_pen_types(update, context):
    query = update.callback_query
    query.answer()
    
    # نحاكي عملية العودة للقائمة الفرعية للأقلام
    show_product_page(update, "aqlam", aqlam_submenu, is_direct_list=True)
    return ConversationHandler.END


def receive_pen_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    context.user_data['pen_engraving_name'] = engraving_name
    return prompt_for_payment_and_receipt(update, context, product_type="اقلام")

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
    context.user_data['state'] = GET_BOX_COLOR
    
    # 2. Prepare keyboard (Colors)
    keyboard = [
        [InlineKeyboardButton("أبيض", callback_data="color_white"), InlineKeyboardButton("بيج", callback_data="color_bege")],
        [InlineKeyboardButton("أسود", callback_data="color_black"), InlineKeyboardButton("بني", callback_data="color_brown")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")] 
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # 3. Send message
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n من فضلك **اختر لون البوكس**:"
    
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
        
    return GET_BOX_COLOR

def save_box_color_ask_names(update, context):
    query = update.callback_query
    query.answer()
    
    color = query.data.replace("color_", "")
    context.user_data['box_color'] = color
    context.user_data['state'] = GET_BOX_NAMES
    
    box_product = context.user_data.get('box_product', {})
    
    # زر الرجوع يعود إلى قائمة البوكسات وليس خطوة اللون
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = (
        f"✅ تم اختيار اللون: **{color}**\n"
        f"**المنتج**: {box_product.get('label', 'بوكس كتب كتاب')}\n\n"
        f"من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_BOX_NAMES

def back_to_box_menu(update, context):
    query = update.callback_query
    query.answer()
    context.user_data.clear()
    
    # نحاكي عملية العودة للقائمة الفرعية للبوكسات
    try:
        query.message.delete()
    except Exception:
        pass
        
    # إعادة عرض قائمة بوكسات كتب الكتاب
    show_product_page(update, "katb_kitab_box", katb_kitab_box_submenu, is_direct_list=True)
    return ConversationHandler.END

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
    return prompt_for_payment_and_receipt(update, context, product_type="صواني شبكة اكليريك")


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
    return prompt_for_payment_and_receipt(update, context, product_type="صواني شبكة خشب")


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
    return prompt_for_payment_and_receipt(update, context, product_type="طارات اكليريك")


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
    return prompt_for_payment_and_receipt(update, context, product_type="طارات خشب")


# --- [دوال المجات الجديدة] --- 🔥🔥🔥
def get_mug_items():
    # مج ابيض موديل 1/2 + مج سحري موديل 1/2
    white_mugs = mugat_submenu[0]['items']
    magic_mugs = mugat_submenu[1]['items']
    return white_mugs + magic_mugs

def start_mug_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # e.g., buy_mugat_white_m1
    product_callback = data.replace("buy_", "")
    
    # 1. Get product data
    items_list = get_mug_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['mug_product'] = selected_product
    context.user_data['mug_photos'] = [] # قائمة لتخزين معرفات الصور
    context.user_data['state'] = GET_MUG_PHOTOS
    
    # 2. Prepare keyboard (Back button to mugat menu)
    # الرجوع سيكون إلى قائمة المجات الفرعية (mugat)
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="mugat")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # 3. Send message
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        f"من فضلك **قم بإرسال 3 صور** واحدة تلو الأخرى لطباعتها على المج. بعد إرسال الصورة الثالثة، سيتم استكمال عملية الشراء.\n\n"
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
        # Fallback in case of image error
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    return GET_MUG_PHOTOS

def back_to_mug_types(update, context):
    # دالة للعودة إلى قائمة مجات (مج ابيض/سحري/ديجتال)
    query = update.callback_query
    query.answer()
    context.user_data.clear() 
    try:
        query.message.delete()
    except Exception:
        pass
    
    # إعادة عرض قائمة المجات
    show_submenu(update, context, mugat_submenu, "مج سحري ومج ابيض وديجيتال", back_callback="main_menu") 
    return ConversationHandler.END


def handle_mug_photos(update, context):
    # 1. Store photo file_id
    # نستخدم photo[-1] للحصول على أكبر نسخة من الصورة (أعلى دقة)
    photo_file_id = update.message.photo[-1].file_id
    
    if 'mug_photos' not in context.user_data:
        context.user_data['mug_photos'] = []
    
    context.user_data['mug_photos'].append(photo_file_id)
    
    photos_count = len(context.user_data['mug_photos'])

    if photos_count < 3:
        # 2. Ask for remaining photos
        remaining = 3 - photos_count
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"تم استقبال الصورة رقم {photos_count}/3 بنجاح. يرجى إرسال **{remaining} صور** متبقية."
        )
        return GET_MUG_PHOTOS
    else:
        # 3. All 3 photos received, proceed to payment
        mug_product = context.user_data.get('mug_product', {})
        product_label = mug_product.get('label', 'المج المطلوب')
        
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"✅ تم استلام الصور الثلاثة بنجاح.\n\nسيتم الآن استكمال عملية الشراء لمنتج: **{product_label}**.",
            parse_mode="Markdown"
        )
        
        # ننتقل إلى مرحلة الدفع
        return prompt_for_payment_and_receipt(update, context, product_type="مج (طباعة صور)") 

def handle_text_in_photo_state(update, context):
    # دالة للتعامل مع الرسائل النصية عند انتظار الصور
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="عفواً، يرجى إرسال صور لطباعتها على المج، وليس نصاً. يتبقى لك إرسال **%d صور**." % (3 - len(context.user_data.get('mug_photos', []))),
        parse_mode="Markdown"
    )
    return GET_MUG_PHOTOS
# --- [نهاية دوال المجات الجديدة] ---


# دوال الشراء المباشر لمنتجات لا تحتاج إدخال بيانات (مثل الأباجورات، الدروع، الهرم، مستلزمات سبلميشن)
def get_direct_buy_items():
    # جمع قوائم المنتجات المباشرة التي لا تحتاج محادثة قبل الدفع
    items_list = []
    for menu_key in ["abajorat", "haram", "doro3", "sublimation"]: # تم حذف mugat
        submenu_list = all_submenus.get(menu_key, [])
        if menu_key in ["abajorat", "sublimation"]: # قوائم مستوى واحد
            items_list.extend(submenu_list)
        else: # قوائم متداخلة (دروع، هرم)
            for sub_menu in submenu_list:
                items_list.extend(sub_menu.get('items', []))
    return items_list

def prepare_whatsapp_link_for_direct_buy(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_abajora_m1
    product_callback = data.replace("buy_", "")
    
    # 1. Find product type and product data
    product_data = None
    product_type = None
    items_list = get_direct_buy_items()
    for product in items_list:
        if product["callback"] == product_callback:
            # نستنتج نوع المنتج من قائمة المنتجات الأصلية
            for menu_label, submenu_list in all_submenus.items():
                if menu_label in ["abajorat", "sublimation"]:
                    if product in submenu_list:
                        product_type = submenu_list[0]['label']
                        break
                elif menu_label in ["haram", "doro3"]:
                    for sub_menu in submenu_list:
                        if product in sub_menu['items']:
                            product_type = sub_menu['label'] # مثل دروع اكليريك
                            break
            product_data = product
            
            # محاولة أفضل لاستنتاج اسم القائمة الأم للمنتجات المباشرة
            if not product_type:
                for menu_key, submenu_list in all_submenus.items():
                    if menu_key in ["abajorat", "doro3", "haram", "sublimation"]:
                        for item in submenu_list:
                            if product_callback.startswith(item["callback"]):
                                product_type = item["label"]
                                break
                    if product_type:
                        break
            
            if product_type == "اباجورات": # نأخذ العنوان الرئيسي
                menu_label = "اباجورات"
                break
            elif product_type == "مستلزمات سبلميشن": # نأخذ العنوان الرئيسي
                menu_label = "مستلزمات سبلميشن"
                break
                
            menu_label = product_to_submenu_map.get(product_callback)
            if menu_label:
                # نستخدم اسم القائمة الفرعية كنوع للمنتج (مثل: دروع اكليريك)
                for item in all_submenus.get(menu_label, []):
                    if item.get('callback') == product_to_submenu_map.get(product_callback):
                        product_type = item['label']
                        break
            
            if not product_type: # Fallback if specific submenu label is not found
                product_type = menu_label
                
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
    except:
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
    """ الدالة الجديدة التي تطلب من العميل الدفع وتحويل الحالة إلى انتظار صورة الإيصال. """
    
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
        date_details = 'غير مطلوب'
    elif product_type == "اقلام":
        product_data = context.user_data.get('pen_data')
        names_details = context.user_data.get('pen_engraving_name')
        date_details = 'غير مطلوب'
    elif product_type == "بوكس كتب كتاب":
        product_data = context.user_data.get('box_product')
        color = context.user_data.get('box_color', 'غير محدد')
        names_details = context.user_data.get('box_names')
        date_details = f"اللون: {color}"
    elif product_type == "صواني شبكة اكليريك":
        product_data = context.user_data.get('tray_product')
        names_details = context.user_data.get('tray_names')
        date_details = context.user_data.get('tray_date')
    elif product_type == "صواني شبكة خشب":
        product_data = context.user_data.get('khashab_tray_product')
        names_details = context.user_data.get('khashab_tray_names')
        date_details = context.user_data.get('khashab_tray_date')
    elif product_type == "طارات اكليريك":
        product_data = context.user_data.get('taarat_akerik_product')
        names_details = context.user_data.get('taarat_akerik_names')
        date_details = context.user_data.get('taarat_akerik_date')
    elif product_type == "طارات خشب":
        product_data = context.user_data.get('taarat_khashab_product')
        names_details = context.user_data.get('taarat_khashab_names')
        date_details = context.user_data.get('taarat_khashab_date')
    elif product_type == "مج (طباعة صور)": # 🔥 إضافة النوع الجديد
        product_data = context.user_data.get('mug_product')
        mug_photos = context.user_data.get('mug_photos', [])
        # تحويل قائمة معرفات الصور إلى نص واحد مفصول بفاصلة منقوطة
        names_details = "؛".join(mug_photos) 
        date_details = 'غير مطلوب' # التاريخ غير مطلوب للمجات
    else: 
        # لمنتجات الشراء المباشر (اباجورات، دروع، هرم، سبلميشن)
        product_data = context.user_data.get('direct_product')
        names_details = 'غير مطلوب'
        date_details = 'غير مطلوب'
    
    if not product_data:
        # إذا لم يتم العثور على بيانات المنتج، العودة للقائمة الرئيسية
        if update.callback_query:
            update.callback_query.answer("خطأ: لم يتم تحديد المنتج. يرجى البدء من جديد.", show_alert=True)
        return start(update, context)

    # 2. حفظ تفاصيل الطلب بشكل موحد لـ handle_payment_photo
    context.user_data['final_product_type'] = product_type
    context.user_data['final_product_label'] = product_data.get('label', product_type)
    context.user_data['final_price'] = product_data.get('price', 'غير محدد')
    context.user_data['final_names'] = names_details if names_details else 'غير مطلوب'
    context.user_data['final_date'] = date_details if date_details else 'غير مطلوب'
    context.user_data['final_code'] = product_data.get('callback', 'N/A')
    # 🔥 حفظ رابط صورة المنتج
    context.user_data['final_product_image'] = product_data.get('image', 'غير متوفر') 
    
    # 3. إرسال رسالة الدفع (تم التعديل)
    payment_message = (
        f"✅ *طلبك جاهز:* {context.user_data['final_product_label']}\n"
        f"💰 *السعر الإجمالي:* {context.user_data['final_price']}\n\n"
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
    
    update.effective_chat.send_message(
        text=payment_message, 
        reply_markup=reply_markup, 
        parse_mode="Markdown"
    )
    
    # 4. تغيير الحالة لانتظار الصورة
    context.user_data['state'] = GET_PAYMENT_RECEIPT
    return GET_PAYMENT_RECEIPT

# --------------------------------------------------------------------------------
# 🔥 دالة معالجة صورة الإيصال (وإرسال طلب الواتساب)
# --------------------------------------------------------------------------------
def handle_payment_photo(update, context):
    # 1. حفظ صورة الإيصال
    receipt_file_id = update.message.photo[-1].file_id
    receipt_file = context.bot.get_file(receipt_file_id)
    # ⚠️ نستخدم مسار ملف مؤقت لغرض إرساله في رابط (هذا الرابط يعمل مؤقتاً).
    # يفضل في بيئة الإنتاج استخدام خدمة تخزين سحابي لضمان الروابط الدائمة.
    receipt_url = receipt_file.file_path 
    
    # 2. استخراج بيانات الطلب
    user_info = update.effective_user
    product_type = context.user_data.get('final_product_type', 'غير محدد')
    product_label = context.user_data.get('final_product_label', 'غير محدد')
    paid_amount = context.user_data.get('final_price', 'غير محدد')
    names_text = context.user_data.get('final_names', 'غير مطلوب')
    date_text = context.user_data.get('final_date', 'غير مطلوب')
    product_image_url = context.user_data.get('final_product_image', 'غير متوفر')
    product_code = context.user_data.get('final_code', 'N/A')
    
    telegram_contact_link = f"tg://user?id={user_info.id}"

    # 🔥 تعديل لنص الواتساب إذا كان المنتج هو مج يتطلب صور
    mug_photo_details = ""
    if product_type == "مج (طباعة صور)":
        # names_text هنا يحتوي على معرفات الصور مفصولة بـ "؛"
        file_ids = names_text.split("؛")
        
        mug_photo_details = "--- صور الطباعة ---\n"
        mug_photo_details += "⚠️ *ملاحظة لمسؤول المبيعات: الروابط المباشرة التالية مؤقتة (صالحة لحوالي ساعة)، يرجى حفظ الصور فوراً.* \n"
        
        # 🆕 التعديل هنا: جلب رابط الملف الفعلي لكل صورة
        photo_urls = []
        for file_id in file_ids:
            try:
                photo_file = context.bot.get_file(file_id)
                # استخدام file_path لجلب الرابط الكامل المؤقت
                photo_urls.append(photo_file.file_path) 
            except Exception as e:
                # في حالة فشل جلب الرابط، نستخدم معرف الملف كاحتياطي
                photo_urls.append(f"❌ خطأ في الرابط (ID: {file_id})")

        for i, url in enumerate(photo_urls):
            mug_photo_details += f"🔗 رابط الصورة {i+1}: {url}\n"
            
        mug_photo_details += "-----------------------\n"
        
        # نغير محتوى حقلي الأسماء والتاريخ لرسالة الواتساب
        names_text = "تم ارفاق 3 صور، يرجى مراجعة تفاصيل الصور أعلاه."
        date_text = "غير مطلوب"
        

    # 3. بناء رسالة الواتساب (تم التعديل)
    message_body = (
        f"🔔 *طلب شراء جديد (مدفوع)* 🔔\n\n"
        f"نوع المنتج: {product_type.replace('-', ' - ')}\n"
        f"المنتج: {product_label}\n"
        f"السعر المدفوع: *{paid_amount}*\n\n"
        
        f"{mug_photo_details}" # 🔥 الآن يحتوي على الروابط الكاملة
        
        f"الأسماء: {names_text}\n"
        f"التاريخ: {date_text}\n\n"
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
    
    # 0. معالجة إلغاء المحادثة (فقط عندما لا نكون في محادثة ConversationHandler)
    if data == "cancel":
        return cancel_and_end(update, context)
    
    # 1. العودة للقائمة الرئيسية
    if data == "main_menu":
        start(update, context)
        return
        
    # 2. معالجة فتح قوائم المستوى الأول (sawany, taarat, haram, doro3, mugat, aqlam, engraved_wallet)
    if data in all_submenus:
        submenu_list = all_submenus[data]
        title = next(item["label"] for item in main_menu if item["callback"] == data) # البحث عن العنوان في القائمة الرئيسية
        show_submenu(update, context, submenu_list, title)
        return
        
    # 3. معالجة فتح قوائم المستوى الثاني (sawany_akerik, taarat_khashab, etc.)
    # البحث عنها في القوائم المتداخلة فقط (sawany, taarat, haram, doro3, mugat)
    is_nested_submenu = False
    for menu_key in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        for item in all_submenus.get(menu_key, []):
            if item["callback"] == data:
                # هذه هي قائمة منتجات (مثل صواني اكليريك)
                show_product_page(update, data, item["items"], is_direct_list=False)
                is_nested_submenu = True
                return
    if is_nested_submenu: return
    
    # 4. معالجة فتح قوائم المستوى الأول المباشرة (bsamat, wedding_tissues, abajorat, engraved_wallet, aqlam, katb_kitab_box, sublimation)
    if data in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box", "sublimation"]:
        # هذه قائمة منتجات مباشرة (مثل بصمات)
        show_product_page(update, data, all_submenus[data], is_direct_list=True)
        return
    
    # 5. معالجة أزرار الشراء الفردية (للمنتجات التي لا تحتاج محادثة)
    if data.startswith("buy_"):
        # يجب أن يصل إلى هنا فقط الأباجورات والهرامات والدروع والسبلميشن (بعد إزالة المجات)
        prepare_whatsapp_link_for_direct_buy(update, context)
        return
    
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
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_box_menu, pattern='^katb_kitab_box$'), # للرجوع من خطوة الأسماء
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 2. صواني اكليريك
    tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_tray_purchase, pattern='^buy_akerik_.*')],
        states={
            GET_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_akerik$')
            ],
            GET_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_tray_date_and_finish)],
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

    # 3. صواني خشب
    khashab_tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_tray_purchase, pattern='^buy_khashab_.*')],
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

    # 4. طارات اكليريك
    akerik_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_taarat_purchase, pattern='^buy_taarat_akerik_.*')],
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

    # 5. طارات خشب
    khashab_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_taarat_purchase, pattern='^buy_taarat_khashab_.*')],
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

    # 6. بصامات
    bsamat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_bsamat_purchase, pattern='^buy_bsamat_.*')],
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
    
    # 7. مناديل كتب الكتاب
    tissue_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tissue_purchase, pattern='^buy_tissue_.*')],
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
    
    # 8. محافظ محفورة بالاسم
    engraved_wallet_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_wallet_purchase, pattern='^buy_wallet_.*')],
        states={
            GET_WALLET_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_wallet_name_and_prepare_whatsapp),
                CallbackQueryHandler(back_to_wallets_color, pattern='^back_to_wallets_color$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_wallets_color, pattern='^back_to_wallets_color$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 9. اقلام
    engraved_pen_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_pen_purchase, pattern='^buy_aqlam_.*')],
        states={
            GET_PEN_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp),
                CallbackQueryHandler(back_to_pen_types, pattern='^back_to_pen_types$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_pen_types, pattern='^back_to_pen_types$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 10. معالج المجات الجديد (يجمع 3 صور ثم ينتقل للدفع) 🔥🔥🔥
    mug_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_mug_purchase, pattern='^buy_mugat_(white|magic)_m[12]$')
        ],
        states={
            GET_MUG_PHOTOS: [
                MessageHandler(Filters.photo, handle_mug_photos),
                MessageHandler(Filters.text & ~Filters.command, handle_text_in_photo_state), # للتعامل مع النصوص المدخلة خطأً
                CallbackQueryHandler(back_to_mug_types, pattern='^mugat$') # زر الرجوع من قائمة الصور
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_mug_types, pattern='^mugat$'), # للرجوع من خطوة الصور
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    

    # 11. معالج الشراء المباشر (للمنتجات التي لا تحتاج محادثة)
    # ⚠️ تم حذف 'mugat' من النمط لتمكين عمل 'mug_handler' بدلاً منه.
    direct_buy_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prepare_whatsapp_link_for_direct_buy, pattern='^buy_(abajora|haram|doro3|subli)_.*')], # 🔥 تم حذف 'mugat'
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
    dp.add_handler(mug_handler) # 🔥 إضافة معالج المجات
    dp.add_handler(direct_buy_handler) 

    
    # 5. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 6. معالج أزرار الـ Inline Keyboard (يجب أن يكون بعد الـ ConversationHandlers)
    dp.add_handler(CallbackQueryHandler(button))
    
    # 7. معالج الرسائل النصية التي لا تقع ضمن أي محادثة (يجب أن يكون في النهاية)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()