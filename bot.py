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

GET_PAYMENT_RECEIPT = 17 # 🔥 الحالة الجديدة لطلب إيصال الدفع
GET_MUG_PHOTO = 18    # 🔥 الحالة الجديدة لجمع صور الطباعة للمجات


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
             {"label": "مج ابيض موديل 1", "callback": "mugat_white_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "مج أبيض عالي الجودة جاهز للطباعة الحرارية.", "price": "100 ج"},
             {"label": "مج ابيض موديل 2", "callback": "mugat_white_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "مج أبيض بتصميم مميز للطباعة الحرارية.", "price": "120 ج"}
        ]
    },
    {
        "label": "مج سحري", "callback": "mugat_magic", "items": [
             {"label": "مج سحري موديل 1", "callback": "mugat_magic_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "مج سحري عالي الجودة، يظهر التصميم بالحرارة.", "price": "150 ج"},
             {"label": "مج سحري موديل 2", "callback": "mugat_magic_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "مج سحري بتصميم فاخر، يظهر التصميم بالحرارة.", "price": "180 ج"}
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
    elif menu_key == "mugat":
        for item in submenu_list:
            product_to_submenu_map[item["callback"]] = menu_key
            for sub_item in item['items']:
                 product_to_submenu_map[sub_item["callback"]] = item["callback"] 
    else:
        for item in submenu_list:
            product_to_submenu_map[item["callback"]] = menu_key 
            if 'items' in item:
                for sub_item in item['items']:
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
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation", "engraved_wallet", "aqlam"]: 
        back_callback = "main_menu"
        back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
    # 2. قوائم المستوى الثاني (مثل صواني اكليريك/خشب/مج ابيض/مج سحري/مج ديجتال) تعود للقائمة الأم (صواني/طارات/هرم/دروع/مجات)
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
    
# 🔥 دالة مساعدة للحصول على بيانات المج
def get_mug_product_data(callback_data):
    for group in mugat_submenu:
        for item in group.get('items', []):
            if item['callback'] == callback_data:
                return item
    return None


# --------------------------------------------------------------------------------
# 🔥 [دوال المحادثات المضافة حديثاً للمجات]
# --------------------------------------------------------------------------------

def back_to_mug_type_menu(update, context):
    query = update.callback_query
    query.answer()
    product_callback = context.user_data.get('mug_product', {}).get('callback')
    
    if not product_callback:
        start(update, context)
        return ConversationHandler.END

    # الحصول على مفتاح القائمة الفرعية (mugat_white أو mugat_magic)
    parent_callback = product_to_submenu_map.get(product_callback)
    
    if not parent_callback:
        context.user_data.clear()
        start(update, context)
        return ConversationHandler.END
        
    # Find the correct submenu list for the parent
    mug_group = next((g for g in mugat_submenu if g['callback'] == parent_callback), None)
    
    if mug_group and 'items' in mug_group:
        # مسح بيانات المحادثة قبل العودة إلى قائمة الاختيار
        context.user_data.clear()
        
        # عرض صفحة المنتج للمج المحدد (مثل قائمة مج ابيض)
        show_product_page(update, parent_callback, mug_group['items'], is_direct_list=False)
        return ConversationHandler.END
    
    context.user_data.clear()
    start(update, context) 
    return ConversationHandler.END


def start_mug_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # e.g., buy_mugat_white_m1 or buy_mugat_magic_m2
    product_callback = data.replace("buy_", "")
    
    selected_product = get_mug_product_data(product_callback)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['mug_product'] = selected_product
    # 🔥 تم التعديل: نستخدم 'mug_photos_ids' لتخزين معرفات الصور بدلاً من الروابط
    context.user_data['mug_photos_ids'] = [] 
    
    # تحديد زر الرجوع (يعود إلى قائمة مج ابيض أو مج سحري)
    back_callback = product_to_submenu_map.get(product_callback) 
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        f"مطلوب 3 صور إجمالاً للطباعة على المج.\n\n"
        f"من فضلك **أرسل الصور الثلاث (3 صور)**. يمكنك إرسالهم في رسائل منفصلة أو جميعاً في رسالة واحدة (ألبوم).\n\n"
        f"اضغط زر رجوع للعودة الي القائمة السابقة."
    )
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_MUG_PHOTO 


def receive_mug_photo(update, context):
    # 1. Input Check (Ignore text messages, only process photos)
    if update.message.text:
        # 🔥 تم التعديل: استخدام 'mug_photos_ids'
        current_count = len(context.user_data.get('mug_photos_ids', []))
        message_text = f"عفواً، يرجى إرسال صور فقط. لقد أرسلت الآن **{current_count}/3** صور."
        
        product_callback = context.user_data.get('mug_product', {}).get('callback')
        if not product_callback: return ConversationHandler.END
        back_callback = product_to_submenu_map.get(product_callback) 
        
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)]])
        )
        return GET_MUG_PHOTO
        
    # 2. Process Photo
    if not (update.message and update.message.photo):
        return GET_MUG_PHOTO
    
    # 3. Store Photo ID (Efficient)
    try:
        photo_file_id = update.message.photo[-1].file_id
        
        # 🔥 تم التعديل: تخزين الـ file_id بدلاً من file_path لتسريع عملية العد
        # والتأكد من عدم تكرار نفس الصورة (حيث أن file_id فريد)
        if photo_file_id not in context.user_data.get('mug_photos_ids', []):
             # نستخدم setdefault للتأكد من وجود القائمة
            context.user_data.setdefault('mug_photos_ids', []).append(photo_file_id)
    except Exception as e:
        context.bot.send_message(update.effective_chat.id, "حدث خطأ أثناء حفظ الصورة. يرجى إعادة المحاولة.")
        return GET_MUG_PHOTO

    # 4. Check Count and Transition
    current_count = len(context.user_data['mug_photos_ids'])
    
    # Determine the back button
    product_callback = context.user_data['mug_product']['callback']
    back_callback = product_to_submenu_map.get(product_callback) 
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)]])
    
    if current_count < 3:
        # Still waiting for more photos
        is_media_group = update.message.media_group_id is not None
        
        # 🔥 تم التعديل: لا نرسل رسالة رد لكل صورة في الألبوم لتجنب الارتباك
        if not is_media_group: 
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"✅ تم استلام الصورة رقم {current_count}. \n\nمطلوب 3 صور إجمالاً. يرجى إرسال الصور المتبقية.",
                reply_markup=reply_markup
            )
        return GET_MUG_PHOTO
    
    elif current_count >= 3:
        # All 3 photos received (or more), proceed to payment prompt
        
        # نأخذ أول 3 معرفات صور
        final_file_ids = context.user_data['mug_photos_ids'][:3] 
        
        # 🔥 نجلب روابط الملفات (file_path) الآن، مرة واحدة للثلاث صور
        final_photo_paths = []
        for file_id in final_file_ids:
            try:
                new_file = context.bot.get_file(file_id)
                final_photo_paths.append(new_file.file_path)
            except Exception:
                # في حالة فشل الاتصال، نستخدم الـ ID كبديل
                final_photo_paths.append(f"File ID: {file_id}") 
                
        # تخزين قائمة الروابط/IDs النهائية
        context.user_data['final_mug_photos_links'] = final_photo_paths 
        
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="✅ تم استلام الصور الثلاث بنجاح. سننتقل الآن إلى مرحلة الدفع."
        )
        
        # مسح المعرفات المؤقتة
        del context.user_data['mug_photos_ids'] 
        return prompt_for_payment_and_receipt(update, context, product_type="مج طباعة")


# --------------------------------------------------------------------------------
# 🔥 [باقي دوال المحادثات (بوكس، صواني، طارات، بصامات، مناديل، محافظ، أقلام)]
# --------------------------------------------------------------------------------

def get_box_product_data(callback_data):
    return next((item for item in katb_kitab_box_submenu if item["callback"] == callback_data), None)

def back_to_box_menu(update, context):
    query = update.callback_query
    query.answer()
    show_product_page(update, "katb_kitab_box", katb_kitab_box_submenu, is_direct_list=True)
    context.user_data.clear()
    return ConversationHandler.END


def start_box_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data.replace("buy_", "")
    
    selected_product = get_box_product_data(data)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['box_product'] = selected_product
    
    keyboard = [
        [InlineKeyboardButton("أبيض", callback_data="color_أبيض")],
        [InlineKeyboardButton("أسود", callback_data="color_أسود")],
        [InlineKeyboardButton("بني (غامق)", callback_data="color_بني")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")]
    ]
    
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *{selected_product['label']}*\n\nمن فضلك اختر لون البوكس:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return GET_BOX_COLOR

def save_box_color_ask_names(update, context):
    query = update.callback_query
    query.answer()
    
    # إذا كانت CallBackQuery للرجوع
    if query.data == 'katb_kitab_box':
        return back_to_box_menu(update, context)

    color_data = query.data.replace("color_", "")
    context.user_data['box_color'] = color_data
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")]]
    
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ تم اختيار اللون: *{color_data}*\n\nمن فضلك أرسل *الاسمين* المراد كتابتهما على البوكس (على سبيل المثال: محمد ونورهان):",
        reply_markup=InlineKeyboardMarkup(back_keyboard),
        parse_mode="Markdown"
    )
    return GET_BOX_NAMES

def receive_box_names_and_finish(update, context):
    box_names = update.message.text
    context.user_data['box_names'] = box_names
    
    update.message.reply_text("✅ تم استلام الأسماء بنجاح. سننتقل الآن إلى مرحلة الدفع.")
    
    return prompt_for_payment_and_receipt(update, context, product_type="بوكس كتب كتاب")


# --------------------------------------------------------------------------------
# 🔥 [دوال المحادثات المضافة لتصحيح الخطأ: الصواني (اكليريك وخشب)]
# --------------------------------------------------------------------------------

def get_tray_product_data(callback_data):
    for group in sawany_submenu:
        if 'items' in group:
            item = next((i for i in group['items'] if i['callback'] == callback_data), None)
            if item: return item
    return None

def back_to_tray_names(update, context):
    # This function is used in fallbacks for GET_TRAY_DATE to re-prompt for names
    return start_akerik_tray_purchase(update, context, called_from_back=True) 

def start_akerik_tray_purchase(update, context, called_from_back=False):
    query = update.callback_query
    
    if query and not called_from_back: # Only run this if it's a fresh entry point
        query.answer()
        data = query.data.replace("buy_", "")
        
        selected_product = get_tray_product_data(data)
        if not selected_product:
            query.answer("خطأ في العثور على المنتج", show_alert=True)
            return ConversationHandler.END
            
        context.user_data['tray_product'] = selected_product

        try: query.message.delete()
        except: pass
            
    # If called from back_to_tray_names or fresh, product is in context.user_data
    selected_product = context.user_data.get('tray_product', {})

    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_akerik")]]
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *{selected_product.get('label', 'صينية شبكة اكليريك')}*\n\nمن فضلك أرسل *الاسمين* المراد كتابتهما على الصينية (مثال: علي وفاطمة):",
        reply_markup=InlineKeyboardMarkup(back_keyboard),
        parse_mode="Markdown"
    )
    return GET_TRAY_NAMES

def save_tray_names_ask_date(update, context):
    context.user_data['tray_names'] = update.message.text
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_tray_names")]]
    
    update.message.reply_text(
        "✅ تم استلام الأسماء بنجاح.\n\nالآن، من فضلك أرسل *التاريخ* المراد كتابته على الصينية (مثال: 15/07/2025):",
        reply_markup=InlineKeyboardMarkup(back_keyboard)
    )
    return GET_TRAY_DATE

def receive_tray_date_and_finish(update, context):
    context.user_data['tray_date'] = update.message.text
    
    update.message.reply_text("✅ تم استلام التاريخ بنجاح. سننتقل الآن إلى مرحلة الدفع.")
    
    return prompt_for_payment_and_receipt(update, context, product_type="صواني شبكة اكليريك")


# Khashab Tray Functions 
def back_to_khashab_tray_names(update, context):
    return start_khashab_tray_purchase(update, context, called_from_back=True)

def start_khashab_tray_purchase(update, context, called_from_back=False):
    query = update.callback_query
    if query and not called_from_back:
        query.answer()
        data = query.data.replace("buy_", "")
        selected_product = get_tray_product_data(data)
        if not selected_product:
            query.answer("خطأ في العثور على المنتج", show_alert=True)
            return ConversationHandler.END
        context.user_data['khashab_tray_product'] = selected_product
        try: query.message.delete()
        except: pass
    
    selected_product = context.user_data.get('khashab_tray_product', {})
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="sawany_khashab")]]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *{selected_product.get('label', 'صينية شبكة خشب')}*\n\nمن فضلك أرسل *الاسمين* المراد كتابتهما على الصينية (مثال: علي وفاطمة):",
        reply_markup=InlineKeyboardMarkup(back_keyboard),
        parse_mode="Markdown"
    )
    return GET_KHASHAB_TRAY_NAMES

def save_khashab_tray_names_ask_date(update, context):
    context.user_data['khashab_tray_names'] = update.message.text
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_khashab_tray_names")]]
    update.message.reply_text(
        "✅ تم استلام الأسماء بنجاح.\n\nالآن، من فضلك أرسل *التاريخ* المراد كتابته على الصينية (مثال: 15/07/2025):",
        reply_markup=InlineKeyboardMarkup(back_keyboard)
    )
    return GET_KHASHAB_TRAY_DATE

def receive_khashab_tray_date_and_finish(update, context):
    context.user_data['khashab_tray_date'] = update.message.text
    update.message.reply_text("✅ تم استلام التاريخ بنجاح. سننتقل الآن إلى مرحلة الدفع.")
    return prompt_for_payment_and_receipt(update, context, product_type="صواني شبكة خشب")


# --------------------------------------------------------------------------------
# 🔥 [دوال المحادثات المضافة لتصحيح الخطأ: الطارات (اكليريك وخشب)]
# --------------------------------------------------------------------------------

def get_taarat_product_data(callback_data):
    for group in taarat_submenu:
        if 'items' in group:
            item = next((i for i in group['items'] if i['callback'] == callback_data), None)
            if item: return item
    return None

def back_to_akerik_taarat_names(update, context):
    return start_akerik_taarat_purchase(update, context, called_from_back=True)

def start_akerik_taarat_purchase(update, context, called_from_back=False):
    query = update.callback_query
    if query and not called_from_back:
        query.answer()
        data = query.data.replace("buy_", "")
        selected_product = get_taarat_product_data(data)
        if not selected_product:
            query.answer("خطأ في العثور على المنتج", show_alert=True)
            return ConversationHandler.END
        context.user_data['taarat_akerik_product'] = selected_product
        try: query.message.delete()
        except: pass
    
    selected_product = context.user_data.get('taarat_akerik_product', {})
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_akerik")]]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *{selected_product.get('label', 'طارة اكليريك')}*\n\nمن فضلك أرسل *الاسمين* المراد كتابتهما على الطارة (مثال: علي وفاطمة):",
        reply_markup=InlineKeyboardMarkup(back_keyboard),
        parse_mode="Markdown"
    )
    return GET_AKRILIK_TAARAT_NAMES

def save_akerik_taarat_names_ask_date(update, context):
    context.user_data['taarat_akerik_names'] = update.message.text
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_akerik_taarat_names")]]
    update.message.reply_text(
        "✅ تم استلام الأسماء بنجاح.\n\nالآن، من فضلك أرسل *التاريخ* المراد كتابته على الطارة (مثال: 15/07/2025):",
        reply_markup=InlineKeyboardMarkup(back_keyboard)
    )
    return GET_AKRILIK_TAARAT_DATE

def receive_akerik_taarat_date_and_finish(update, context):
    context.user_data['taarat_akerik_date'] = update.message.text
    update.message.reply_text("✅ تم استلام التاريخ بنجاح. سننتقل الآن إلى مرحلة الدفع.")
    return prompt_for_payment_and_receipt(update, context, product_type="طارة اكليريك")


def back_to_khashab_taarat_names(update, context):
    return start_khashab_taarat_purchase(update, context, called_from_back=True)

def start_khashab_taarat_purchase(update, context, called_from_back=False):
    query = update.callback_query
    if query and not called_from_back:
        query.answer()
        data = query.data.replace("buy_", "")
        selected_product = get_taarat_product_data(data)
        if not selected_product:
            query.answer("خطأ في العثور على المنتج", show_alert=True)
            return ConversationHandler.END
        context.user_data['taarat_khashab_product'] = selected_product
        try: query.message.delete()
        except: pass
    
    selected_product = context.user_data.get('taarat_khashab_product', {})
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="taarat_khashab")]]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *{selected_product.get('label', 'طارة خشب')}*\n\nمن فضلك أرسل *الاسمين* المراد كتابتهما على الطارة (مثال: علي وفاطمة):",
        reply_markup=InlineKeyboardMarkup(back_keyboard),
        parse_mode="Markdown"
    )
    return GET_KHASHAB_TAARAT_NAMES

def save_khashab_taarat_names_ask_date(update, context):
    context.user_data['taarat_khashab_names'] = update.message.text
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_khashab_taarat_names")]]
    update.message.reply_text(
        "✅ تم استلام الأسماء بنجاح.\n\nالآن، من فضلك أرسل *التاريخ* المراد كتابته على الطارة (مثال: 15/07/2025):",
        reply_markup=InlineKeyboardMarkup(back_keyboard)
    )
    return GET_KHASHAB_TAARAT_DATE

def receive_khashab_taarat_date_and_finish(update, context):
    context.user_data['taarat_khashab_date'] = update.message.text
    update.message.reply_text("✅ تم استلام التاريخ بنجاح. سننتقل الآن إلى مرحلة الدفع.")
    return prompt_for_payment_and_receipt(update, context, product_type="طارة خشب")

# --------------------------------------------------------------------------------
# 🔥 [دوال المحادثات المضافة لتصحيح الخطأ: البصامات]
# --------------------------------------------------------------------------------

def get_bsamat_product_data(callback_data):
    return next((item for item in bsamat_submenu if item["callback"] == callback_data), None)

def back_to_bsamat_names(update, context):
    return start_bsamat_purchase(update, context, called_from_back=True)

def start_bsamat_purchase(update, context, called_from_back=False):
    query = update.callback_query
    if query and not called_from_back:
        query.answer()
        data = query.data.replace("buy_", "")
        selected_product = get_bsamat_product_data(data)
        if not selected_product:
            query.answer("خطأ في العثور على المنتج", show_alert=True)
            return ConversationHandler.END
        context.user_data['bsamat_product'] = selected_product
        try: query.message.delete()
        except: pass
    
    selected_product = context.user_data.get('bsamat_product', {})
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="bsamat")]]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *{selected_product.get('label', 'بصامة')}*\n\nمن فضلك أرسل *الاسمين* المراد كتابتهما على البصامة (مثال: علي وفاطمة):",
        reply_markup=InlineKeyboardMarkup(back_keyboard),
        parse_mode="Markdown"
    )
    return GET_BSAMAT_NAMES

def save_bsamat_names_ask_date(update, context):
    context.user_data['bsamat_names'] = update.message.text
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_bsamat_names")]]
    update.message.reply_text(
        "✅ تم استلام الأسماء بنجاح.\n\nالآن، من فضلك أرسل *التاريخ* المراد كتابته على البصامة (مثال: 15/07/2025):",
        reply_markup=InlineKeyboardMarkup(back_keyboard)
    )
    return GET_BSAMAT_DATE

def receive_bsamat_date_and_finish(update, context):
    context.user_data['bsamat_date'] = update.message.text
    update.message.reply_text("✅ تم استلام التاريخ بنجاح. سننتقل الآن إلى مرحلة الدفع.")
    return prompt_for_payment_and_receipt(update, context, product_type="بصامة")

# --------------------------------------------------------------------------------
# 🔥 [دوال المحادثات المضافة لتصحيح الخطأ: مناديل كتب الكتاب]
# --------------------------------------------------------------------------------

def get_tissue_product_data(callback_data):
    return next((item for item in wedding_tissues_submenu if item["callback"] == callback_data), None)

def back_to_tissue_names(update, context):
    return start_tissue_purchase(update, context, called_from_back=True)

def start_tissue_purchase(update, context, called_from_back=False):
    query = update.callback_query
    if query and not called_from_back:
        query.answer()
        data = query.data.replace("buy_", "")
        selected_product = get_tissue_product_data(data)
        if not selected_product:
            query.answer("خطأ في العثور على المنتج", show_alert=True)
            return ConversationHandler.END
        context.user_data['tissue_product'] = selected_product
        try: query.message.delete()
        except: pass
    
    selected_product = context.user_data.get('tissue_product', {})
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="wedding_tissues")]]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *{selected_product.get('label', 'منديل كتب كتاب')}*\n\nمن فضلك أرسل *الاسمين* المراد كتابتهما على المنديل (مثال: علي وفاطمة):",
        reply_markup=InlineKeyboardMarkup(back_keyboard),
        parse_mode="Markdown"
    )
    return GET_TISSUE_NAMES

def save_tissue_names_ask_date(update, context):
    context.user_data['tissue_names'] = update.message.text
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_tissue_names")]]
    update.message.reply_text(
        "✅ تم استلام الأسماء بنجاح.\n\nالآن، من فضلك أرسل *التاريخ* المراد كتابته على المنديل (مثال: 15/07/2025):",
        reply_markup=InlineKeyboardMarkup(back_keyboard)
    )
    return GET_TISSUE_DATE

def receive_tissue_date_and_finish(update, context):
    context.user_data['tissue_date'] = update.message.text
    update.message.reply_text("✅ تم استلام التاريخ بنجاح. سننتقل الآن إلى مرحلة الدفع.")
    return prompt_for_payment_and_receipt(update, context, product_type="منديل كتب كتاب")

# --------------------------------------------------------------------------------
# 🔥 [دوال المحادثات المضافة لتصحيح الخطأ: المحافظ]
# --------------------------------------------------------------------------------

def get_wallet_product_data(callback_data):
    return next((item for item in engraved_wallet_submenu if item["callback"] == callback_data), None)

def back_to_wallets_color(update, context):
    query = update.callback_query
    query.answer()
    show_product_page(update, "engraved_wallet", engraved_wallet_submenu, is_direct_list=True)
    context.user_data.clear()
    return ConversationHandler.END

def prompt_for_name(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    
    selected_product = get_wallet_product_data(data)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['wallet_data'] = selected_product
    
    try:
        query.message.delete()
    except:
        pass
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="engraved_wallet")]]
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *{selected_product['label']}* (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\nمن فضلك أرسل *الاسم* المراد حفره على المحفظة:",
        reply_markup=InlineKeyboardMarkup(back_keyboard),
        parse_mode="Markdown"
    )
    return GET_WALLET_NAME

def receive_wallet_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    context.user_data['wallet_engraving_name'] = engraving_name
    
    update.message.reply_text("✅ تم استلام الاسم بنجاح. سننتقل الآن إلى مرحلة الدفع.")
    
    return prompt_for_payment_and_receipt(update, context, product_type="محافظ")

# --------------------------------------------------------------------------------
# 🔥 [دوال المحادثات المضافة لتصحيح الخطأ: الأقلام]
# --------------------------------------------------------------------------------

def get_pen_product_data(callback_data):
    return next((item for item in aqlam_submenu if item["callback"] == callback_data), None)

def back_to_pen_types(update, context):
    query = update.callback_query
    query.answer()
    show_product_page(update, "aqlam", aqlam_submenu, is_direct_list=True)
    context.user_data.clear()
    return ConversationHandler.END


def prompt_for_pen_name(update, context):
    query = update.callback_query
    query.answer()
    data = query.data 
    
    selected_product = get_pen_product_data(data)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['pen_data'] = selected_product
    
    try:
        query.message.delete()
    except:
        pass
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="aqlam")]]
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ *{selected_product['label']}* (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\nمن فضلك أرسل *الاسم* المراد حفره على القلم:",
        reply_markup=InlineKeyboardMarkup(back_keyboard),
        parse_mode="Markdown"
    )
    return GET_PEN_NAME

def receive_pen_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    context.user_data['pen_engraving_name'] = engraving_name
    
    update.message.reply_text("✅ تم استلام الاسم بنجاح. سننتقل الآن إلى مرحلة الدفع.")
    
    return prompt_for_payment_and_receipt(update, context, product_type="اقلام")


# --------------------------------------------------------------------------------
# [دوال الشراء المباشر والدفع - تم تعديلها في النسخة السابقة]
# --------------------------------------------------------------------------------
def prepare_whatsapp_link_for_direct_buy(update, context):
    query = update.callback_query
    data = query.data # buy_callback_data
    query.answer()
    
    # 1. استخراج مفتاح المنتج
    product_callback = data.replace("buy_", "")
    
    # 2. البحث عن بيانات المنتج 
    product_data = None
    product_type = ""
    
    # قائمة الأباجورات (القائمة المباشرة)
    items_list = abajorat_submenu
    product_data = next((item for item in items_list if item["callback"] == product_callback), None)
    if product_data:
        product_type = "اباجورة"
        
    # البحث في مستلزمات سبلميشن الجديدة
    if not product_data:
        items_list = sublimation_supplies_submenu
        product_data = next((item for item in items_list if item["callback"] == product_callback), None)
        if product_data:
            product_type = "مستلزمات سبلميشن"
            
    # البحث في مجات ديجتال (التي لا تحتاج صور)
    if not product_data:
        items_list = mugat_submenu[2]['items'] # مج ديجتال
        product_data = next((item for item in items_list if item["callback"] == product_callback), None)
        if product_data:
            product_type = "مج ديجتال"
    
    if not product_data:
        # البحث في القوائم المتداخلة (هرم مكتب، دروع)
        for menu_key, menu_label in [("haram", "هرم مكتب"), ("doro3", "درع")]:
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
    context.user_data['direct_product'] = product_data
    
    # يجب حذف رسالة الزر القديمة
    try:
        query.message.delete()
    except:
        pass

    return prompt_for_payment_and_receipt(update, context, product_type=product_type)

# --------------------------------------------------------------------------------
# 🔥 دالة طلب الدفع (تم التعديل لإضافة بيانات صور المج)
# --------------------------------------------------------------------------------
def prompt_for_payment_and_receipt(update, context, product_type):
    
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
    elif product_type == "مج طباعة": # 🔥 مجات الطباعة الجديدة (مج ابيض وسحري)
        product_data = context.user_data.get('mug_product')
        product_type = f"{product_type} - {product_data['label']}"
        mug_photos = context.user_data.get('final_mug_photos_links', []) # 🔥 تم التعديل: استخدام المفتاح الجديد
        # تخزين روابط الصور في بيانات المحادثة النهائية كسلسلة نصية
        context.user_data['final_mug_photos_links_str'] = "\n".join(mug_photos) # 🔥 تم التعديل: مفتاح جديد لسلسلة الروابط
    elif 'direct_product' in context.user_data: # الأهرامات، الدروع، المجات الديجتال، الأباجورات، السبلميشن
        product_data = context.user_data.get('direct_product')
    else:
        update.effective_chat.send_message("حدث خطأ في تجهيز الطلب. يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        context.user_data.clear()
        return ConversationHandler.END

    # 2. حفظ تفاصيل الطلب بشكل موحد لـ handle_payment_photo
    context.user_data['final_product_type'] = product_type
    context.user_data['final_product_label'] = product_data.get('label', product_type)
    context.user_data['final_price'] = product_data.get('price', 'غير محدد')
    context.user_data['final_names'] = names_details if names_details else 'غير مطلوب'
    context.user_data['final_date'] = date_details if date_details else 'غير مطلوب'
    context.user_data['final_code'] = product_data.get('callback', 'N/A')
    # حفظ رابط صورة المنتج
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


def handle_payment_buttons(update, context):
    query = update.callback_query
    data = query.data
    
    if data == "cancel":
        return cancel_and_end(update, context)

    query.answer("يرجى إرسال إيصال الدفع لإتمام الطلب.", show_alert=True)
    return GET_PAYMENT_RECEIPT

# --------------------------------------------------------------------------------
# 🔥 دالة معالجة إيصال الدفع (تم التعديل لإضافة روابط صور المج)
# --------------------------------------------------------------------------------
def handle_payment_photo(update, context):
    
    if context.user_data.get('state') != GET_PAYMENT_RECEIPT:
        update.effective_chat.send_message("عفواً، لا يمكنني معالجة هذه الصورة الآن. يرجى البدء بطلب جديد.")
        context.user_data.clear()
        return ConversationHandler.END

    # 1. الحصول على رابط إيصال الدفع من تليجرام
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

    # 2. استرجاع بيانات الطلب النهائية
    product_type = context.user_data.get('final_product_type', 'غير متوفر')
    product_label = context.user_data.get('final_product_label', 'غير متوفر')
    paid_amount = context.user_data.get('final_price', 'غير متوفر')
    names_text = context.user_data.get('final_names', 'غير مطلوب')
    date_text = context.user_data.get('final_date', 'غير مطلوب')
    product_code = context.user_data.get('final_code', 'N/A')
    product_image_url = context.user_data.get('final_product_image', 'غير متوفر') 
    
    # 🔥 استرجاع روابط صور المج (إذا كانت موجودة)
    mug_photos_links = context.user_data.get('final_mug_photos_links_str') # 🔥 تم التعديل: استخدام المفتاح الجديد
    
    user_info = update.message.from_user
    telegram_contact_link = f"tg://user?id={user_info.id}" 

    # 3. بناء نص الرسالة للواتساب (تم التعديل)
    message_body = (
        f"🔔 *طلب شراء جديد (مدفوع)* 🔔\n\n"
        f"نوع المنتج: {product_type.replace('-', ' - ')}\n"
        f"المنتج: {product_label}\n"
        f"السعر المدفوع: *{paid_amount}*\n\n"
        f"الأسماء: {names_text}\n"
        f"التاريخ: {date_text}\n\n"
    )
    
    if mug_photos_links and mug_photos_links.strip(): # 🔥 إضافة روابط صور المج
        message_body += f"🔗 *روابط صور الطباعة للمج (3 صور):*\n{mug_photos_links}\n\n"
    
    message_body += (
        f"🔗 رابط صورة المنتج: {product_image_url}\n" 
        f"🔗 رابط إيصال الدفع: {receipt_url}\n" 
        f"الكود: {product_code}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"رابط التواصل عبر التليجرام: {telegram_contact_link}"
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


# --------------------
# 4. دالة button لمعالجة الأزرار (Callback Queries) 
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
    if data in ["sawany", "taarat", "haram", "doro3", "mugat", "aqlam", "engraved_wallet"]: 
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus[data], clean_title, back_callback="main_menu")
        return
        
    # 3. معالجة فتح قوائم المستوى الأول المباشرة (bsamat, wedding_tissues, abajorat, katb_kitab_box, sublimation)
    if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation"]: 
        submenu_list = all_submenus.get(data)
        if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation"]:
            show_product_page(update, data, submenu_list, is_direct_list=True)
            return

    # 4. معالجة عرض صفحات المنتجات مباشرة (قوائم المستوى الثاني)
    product_list_keys = [
        "sawany_akerik", "sawany_khashab", "taarat_akerik", "taarat_khashab", 
        "haram_akerik", "haram_metal", "haram_khashab", "doro3_akerik", 
        "doro3_metal", "doro3_qatifah", "doro3_khashab", 
        "mugat_white", "mugat_magic", "mugat_digital" # قوائم المجات
    ]
    if data in product_list_keys:
        submenu_list = next((item['items'] for menu_list in all_submenus.values() for item in menu_list if item['callback'] == data), None)
        if submenu_list:
            show_product_page(update, data, submenu_list, is_direct_list=False)
            return

    # 5. معالجة أزرار الشراء الفردية (للمنتجات التي لا تحتاج محادثة)
    # لا ينبغي أن يصل إلى هنا أي زر buy_.* إلا إذا لم يتم معالجته في ConversationHandler
    if data.startswith("buy_"):
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

    # 1.1 معالج مجات الطباعة (مج ابيض وسحري)
    mug_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_mug_purchase, pattern='^buy_mugat_(white|magic)_.*')],
        states={
            GET_MUG_PHOTO: [
                MessageHandler(Filters.photo, receive_mug_photo),
                MessageHandler(Filters.text & ~Filters.command, receive_mug_photo),
                CallbackQueryHandler(back_to_mug_type_menu, pattern='^mugat_(white|magic)$')
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_mug_type_menu, pattern='^mugat_(white|magic)$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 2. بوكس كتب الكتاب
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
            CallbackQueryHandler(back_to_box_menu, pattern='^katb_kitab_box$'), # زر الرجوع في حالة الاسماء
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 3. صواني شبكة اكليريك
    tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_tray_purchase, pattern='^buy_akerik_.*')],
        states={
            GET_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_akerik$') 
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
            CallbackQueryHandler(back_to_tray_names, pattern='^back_to_tray_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 4. صواني شبكة خشب
    khashab_tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_tray_purchase, pattern='^buy_khashab_.*')],
        states={
            GET_KHASHAB_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_khashab$') 
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
            CallbackQueryHandler(back_to_khashab_tray_names, pattern='^back_to_khashab_tray_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 5. طارات اكليريك
    akerik_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_taarat_purchase, pattern='^buy_taarat_akerik_.*')],
        states={
            GET_AKRILIK_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_akerik_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_akerik$')
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
            CallbackQueryHandler(back_to_akerik_taarat_names, pattern='^back_to_akerik_taarat_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 6. طارات خشب
    khashab_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_taarat_purchase, pattern='^buy_taarat_khashab_.*')],
        states={
            GET_KHASHAB_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_khashab$')
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
            CallbackQueryHandler(back_to_khashab_taarat_names, pattern='^back_to_khashab_taarat_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 7. بصامات
    bsamat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_bsamat_purchase, pattern='^buy_bsamat_.*')],
        states={
            GET_BSAMAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_bsamat_names_ask_date),
                CallbackQueryHandler(button, pattern='^bsamat$')
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
            CallbackQueryHandler(back_to_bsamat_names, pattern='^back_to_bsamat_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 8. مناديل كتب الكتاب
    tissue_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tissue_purchase, pattern='^buy_tissue_.*')],
        states={
            GET_TISSUE_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tissue_names_ask_date),
                CallbackQueryHandler(button, pattern='^wedding_tissues$') 
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
            CallbackQueryHandler(back_to_tissue_names, pattern='^back_to_tissue_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 9. محافظ محفورة بالاسم
    engraved_wallet_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prompt_for_name, pattern='^wallet_.*$')],
        states={
            GET_WALLET_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_wallet_name_and_prepare_whatsapp)],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_wallets_color, pattern='^engraved_wallet$'), # العودة الى قائمة المحافظ
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 10. اقلام محفورة بالاسم
    engraved_pen_handler = ConversationHandler(
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
            CallbackQueryHandler(back_to_pen_types, pattern='^aqlam$'), # العودة الى قائمة الاقلام
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 11. معالج الطلبات المباشرة (اباجورات، هرم، دروع، مجات ديجتال، مستلزمات سبلميشن)
    # ملاحظة: مجات ابيض وسحري تم استثناؤها ليعالجها mug_handler
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
    
    # 12. إضافة جميع ConversationHandler أولاً لضمان الأولوية
    dp.add_handler(mug_handler) 
    dp.add_handler(box_handler)
    dp.add_handler(tray_handler)
    dp.add_handler(khashab_tray_handler)
    dp.add_handler(akerik_taarat_handler) 
    dp.add_handler(khashab_taarat_handler) 
    dp.add_handler(bsamat_handler) 
    dp.add_handler(tissue_handler) 
    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler) 
    dp.add_handler(direct_buy_handler) 

    
    # 13. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 14. معالج أزرار القائمة والتنقل (يجب أن يأتي بعد معالجات المحادثة)
    dp.add_handler(CallbackQueryHandler(button)) 

    # 15. معالج للرسائل النصية التي لا تندرج تحت محادثة
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    # 16. بدء تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()