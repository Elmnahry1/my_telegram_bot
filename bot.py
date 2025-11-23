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

# حالات البصامات
GET_BSAMAT_NAMES = 13  # حالة كتابة أسماء العرسان للبصامات
GET_BSAMAT_DATE = 14   # حالة كتابة التاريخ للبصامات

# حالات مناديل كتب الكتاب
GET_TISSUE_NAMES = 15  # حالة كتابة أسماء العرسان للمناديل
GET_TISSUE_DATE = 16   # حالة كتابة التاريخ للمناديل


# --------------------
# 2. بيانات القوائم والمنتجات
# --------------------

# --- قوائم فرعية مباشرة ---
bsamat_submenu = [
    {"label": "بصامة موديل 1", "callback": "bsamat_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 1."},
    {"label": "بصامة موديل 2", "callback": "bsamat_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 2."}
]
wedding_tissues_submenu = [
    {"label": "منديل موديل 1", "callback": "tissue_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 1."},
    {"label": "منديل موديل 2", "callback": "tissue_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 2."}
]
katb_kitab_box_submenu = [
    {"label": "بوكس كتب كتاب موديل 1", "callback": "box_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف بوكس كتب الكتاب موديل 1، يحتوي على تصميم مميز."},
    {"label": "بوكس كتب كتاب موديل 2", "callback": "box_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف بوكس كتب الكتاب موديل 2، خامة عالية الجودة."}
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
# 🌟 القائمة المضافة: مستلزمات سبلميشن
sublimation_submenu = [
    {"label": "تيشيرت سبلميشن", "callback": "subli_tshirt", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "تيشيرت قطن بوليستر مجهز للطباعة الحرارية."},
    {"label": "غطاء هاتف سبلميشن", "callback": "subli_phonecase", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "غطاء هاتف بلاستيك للطباعة الحرارية."}
]


# --- القوائم المتداخلة ---
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
    {"label": "🎁 بوكس كتب الكتاب", "callback": "katb_kitab_box"},
    {"label": "🗄️ هرم مكتب", "callback": "haram"},
    {"label": "🏆 دروع", "callback": "doro3"},
    {"label": "💡 اباجورات", "callback": "abajorat"}, 
    {"label": "✏️ اقلام", "callback": "aqlam"}, 
    {"label": "☕ مجات", "callback": "mugat"},
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"},
    {"label": "🖨️ مستلزمات سبلميشن", "callback": "sublimation"} # موجودة هنا
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
    "sublimation": sublimation_submenu # 🌟 تمت إضافة قائمة السبلميشن هنا
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box", "sublimation"]: # 🌟 تمت إضافة sublimation هنا
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

# ⚠️ دالة عرض المنتج الواحد للمحافظ
def show_single_wallet_product(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # wallet_bege, wallet_brown, etc.

    # 1. البحث عن بيانات المنتج
    product_data = next((item for item in engraved_wallet_submenu if item["callback"] == data), None)
    if not product_data:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return

    # 2. حذف رسالة القائمة الفرعية
    if query and query.message:
        try:
            query.message.delete()
        except Exception:
            pass

    # 3. إعداد الأزرار (شراء يبدأ المحادثة، رجوع يعود لقائمة الألوان)
    keyboard = [
        [InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{data}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="engraved_wallet")] # العودة لقائمة الألوان
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 4. إرسال الصورة والوصف
    update.effective_message.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=product_data['image'],
        caption=f"**{product_data['label']}**\n\n{product_data['description']}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ⚠️ دالة عرض المنتج الواحد للأقلام (جديدة)
def show_single_pen_product(update, context):
    query = update.callback_query
    query.answer()
    data = query.data # aqlam_metal, aqlam_luminous, etc.

    # 1. البحث عن بيانات المنتج
    product_data = next((item for item in aqlam_submenu if item["callback"] == data), None)
    if not product_data:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return

    # 2. حذف رسالة القائمة الفرعية
    if query and query.message:
        try:
            query.message.delete()
        except Exception:
            pass

    # 3. إعداد الأزرار (شراء يبدأ المحادثة، رجوع يعود لقائمة أنواع الأقلام)
    keyboard = [
        [InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{data}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="aqlam")] # العودة لقائمة أنواع الأقلام
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 4. إرسال الصورة والوصف
    update.effective_message.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=product_data['image'],
        caption=f"**{product_data['label']}**\n\n{product_data['description']}",
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
        
        update.effective_message.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=item['image'],
            caption=f"**{item['label']}**\n\n{item['description']}",
            reply_markup=item_reply_markup,
            parse_mode="Markdown"
        )
    
    # تحديد زر الرجوع
    
    # 1. إذا كانت قائمة مباشرة من القائمة الرئيسية (مثل بصمات، أباجورات، سبلميشن)
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation"]: # 🌟 تمت إضافة sublimation هنا
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
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
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
    product_data = context.user_data.get('bsamat_product')
    names_text = context.user_data.get('bsamat_names')
    
    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (بصامة)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الأسماء: *{names_text}*\n"
        f"التاريخ: *{date_text}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n✋ المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    context.user_data.clear()
    return ConversationHandler.END


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
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="wedding_tissues")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # 3. Send message
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
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
    product_data = context.user_data.get('tissue_product')
    names_text = context.user_data.get('tissue_names')
    
    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (منديل كتب كتاب)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الأسماء: *{names_text}*\n"
        f"التاريخ: *{date_text}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n📜 المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    context.user_data.clear()
    return ConversationHandler.END


# --- [دوال المحادثات الخاصة بالمحافظ] --- 

def get_wallet_items():
    return engraved_wallet_submenu

def back_to_wallet_product_page(update, context):
    # للرجوع من خطوة إدخال الاسم إلى صفحة المنتج
    query = update.callback_query
    query.answer()
    
    product_data = context.user_data.get('wallet_product')
    if not product_data:
        cancel_and_end(update, context)
        return ConversationHandler.END
        
    product_callback = product_data['callback']

    # مسح حالة المحادثة
    context.user_data.clear() # Clear all user_data to end conversation and state
    
    # حذف الرسالة الحالية (رسالة طلب الاسم)
    try:
        query.message.delete()
    except Exception:
        pass
        
    # إعادة عرض صفحة المنتج الواحد
    keyboard = [
        [InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{product_callback}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="engraved_wallet")] # الرجوع لقائمة الألوان
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.effective_message.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=product_data['image'],
        caption=f"**{product_data['label']}**\n\n{product_data['description']}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END # ننهي المحادثة هنا لأننا عدنا لواجهة الأزرار


def start_wallet_purchase(update, context):
    # نقطة بدء المحادثة من زر "🛒 شراء"
    query = update.callback_query
    query.answer()
    data = query.data  # buy_wallet_bege
    product_callback = data.replace("buy_", "")
    
    items_list = get_wallet_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['wallet_product'] = selected_product
    context.user_data['state'] = GET_WALLET_NAME
    
    # زر الرجوع يعود إلى صفحة المنتج المحدد (مثلاً wallet_bege)
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_wallet_product_page")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except Exception:
        pass
        
    # المطالبة بالاسم
    prompt_text = (
        f"✅ اختيارك: **{selected_product['label']}**\n\n"
        f"من فضلك، **اكتب الاسم الذي تريد حفره** على المحفظة في رسالة نصية بالأسفل.\n"
        f"أو اضغط زر **رجوع** للعودة إلى القائمة السابقة."
    )
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=prompt_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_WALLET_NAME


def receive_wallet_name_and_prepare_whatsapp(update, context):
    # معالجة إدخال الاسم وإظهار رابط الواتساب
    engraving_name = update.message.text
    product_data = context.user_data.get('wallet_product')
    
    if not product_data:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        context.user_data.clear()
        return ConversationHandler.END

    # تجهيز رسالة الواتساب
    user_info = update.message.from_user
    message_body = (
        f"🔔 *طلب شراء جديد (محفظة محفورة)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الاسم للحفر: *{engraving_name}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"

    # إعداد أزرار الانتهاء (واتساب ورجوع)
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # إرسال رسالة التأكيد
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n👝 المنتج: {product_data['label']}\n✍️ الاسم المراد حفره: {engraving_name}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    context.user_data.clear()
    return ConversationHandler.END


# --- [دوال المحادثات الخاصة بالأقلام] --- 

# ⚠️ دالة الرجوع من إدخال اسم القلم لصفحة المنتج الواحد
def back_to_single_pen_product_page(update, context):
    query = update.callback_query
    query.answer()
    
    product_data = context.user_data.get('pen_data')
    if not product_data:
        cancel_and_end(update, context)
        return ConversationHandler.END
        
    product_callback = product_data['callback']

    # مسح حالة المحادثة المؤقتة
    context.user_data.clear() # Clear all user_data to end conversation and state
    
    # حذف الرسالة الحالية (رسالة طلب الاسم)
    try:
        query.message.delete()
    except Exception:
        pass
        
    # إعادة عرض صفحة المنتج الواحد (باستخدام منطق show_single_pen_product)
    keyboard = [
        [InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{product_callback}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="aqlam")] # الرجوع لقائمة أنواع الأقلام
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.effective_message.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=product_data['image'],
        caption=f"**{product_data['label']}**\n\n{product_data['description']}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END # ننهي المحادثة هنا لأننا عدنا لواجهة الأزرار


def start_pen_purchase(update, context):
    # نقطة بدء المحادثة من زر "🛒 شراء"
    query = update.callback_query
    data = query.data # buy_aqlam_metal
    query.answer()
    
    product_callback = data.replace("buy_", "") # aqlam_metal
    selected_pen_data = next((item for item in aqlam_submenu if item["callback"] == product_callback), None)
    
    if not selected_pen_data:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['pen_data'] = selected_pen_data
    context.user_data['state'] = GET_PEN_NAME
    
    try:
        query.message.delete()
    except Exception:
        pass

    # زر الرجوع يعود لصفحة المنتج الواحد
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_pen_product_page")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    caption_text = (f"**اختيارك: {selected_pen_data['label']}**\n\nمن فضلك، **اكتب الاسم الذي تريد حفره** على القلم في رسالة نصية بالأسفل.\nأو اضغط زر الرجوع للعودة إلى القائمة السابقة.")

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=caption_text,
        reply_markup=back_reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_PEN_NAME

def receive_pen_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    product_data = context.user_data.get('pen_data')
    
    if not product_data:
        update.effective_chat.send_message("عفواً، حدث خطأ. يرجى البدء من القائمة الرئيسية.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END

    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (اقلام)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الاسم للحفر: *{engraving_name}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n✏️ المنتج: {product_data['label']}\n✍️ الاسم المراد حفره: {engraving_name}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    context.user_data.clear()
    return ConversationHandler.END


# دوال بوكسات كتب الكتاب

def get_box_items():
    return katb_kitab_box_submenu

def start_box_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  # buy_box_m1
    product_callback = data.replace("buy_", "")
    
    items_list = get_box_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['box_product'] = selected_product
    context.user_data['state'] = GET_BOX_COLOR
    
    try:
        query.message.delete()
    except:
        pass
        
    # خيارات الألوان (المصححة)
    keyboard = [
        [InlineKeyboardButton("أسود في ذهبي", callback_data="color_black_gold")],
        [InlineKeyboardButton("أبيض في ذهبي", callback_data="color_white_gold")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")] # يعود لقائمة موديلات البوكسات
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ **{selected_product['label']}**\n\nمن فضلك اختر **لون البوكس**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_BOX_COLOR

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

def save_box_color_ask_names(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    # Check for explicit return to previous menu
    if data == "katb_kitab_box":
        return back_to_box_menu(update, context)

    # Extract color name from callback_data
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

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return GET_BOX_NAMES

def back_to_box_color(update, context):
    query = update.callback_query
    query.answer()
    selected_box = context.user_data.get('box_product')
    if not selected_box:
        start(update, context)
        return ConversationHandler.END
        
    # إعادة عرض خيارات الألوان (باستخدام الكيبورد المصحح)
    keyboard = [
        [InlineKeyboardButton("أسود في ذهبي", callback_data="color_black_gold")],
        [InlineKeyboardButton("أبيض في ذهبي", callback_data="color_white_gold")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")] 
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ **{selected_box['label']}**\n\nمن فضلك اختر **لون البوكس**:", reply_markup=reply_markup, parse_mode="Markdown")
    
    return GET_BOX_COLOR

def receive_box_names_and_finish(update, context):
    names_text = update.message.text
    product_data = context.user_data.get('box_product')
    color_name = context.user_data.get('box_color')
    
    if not product_data or not color_name:
        update.effective_chat.send_message("حدث خطأ.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (بوكس كتب كتاب)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"اللون: *{color_name}*\n"
        f"الأسماء: *{names_text}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n🎁 المنتج: {product_data['label']}\n🎨 اللون: {color_name}\n✍️ الأسماء: {names_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    context.user_data.clear()
    return ConversationHandler.END


# دوال صواني شبكة اكليريك
def get_akerik_tray_items():
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
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
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
    product_data = context.user_data.get('tray_product')
    names_text = context.user_data.get('tray_names')
    
    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (صواني شبكة اكليريك)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الأسماء: *{names_text}*\n"
        f"التاريخ: *{date_text}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n💍 المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    context.user_data.clear()
    return ConversationHandler.END


# دوال صواني شبكة خشب
def get_khashab_tray_items():
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
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
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
    product_data = context.user_data.get('khashab_tray_product')
    names_text = context.user_data.get('khashab_tray_names')
    
    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (صواني شبكة خشب)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الأسماء: *{names_text}*\n"
        f"التاريخ: *{date_text}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n💍 المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    context.user_data.clear()
    return ConversationHandler.END


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
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
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
    product_data = context.user_data.get('taarat_akerik_product')
    names_text = context.user_data.get('taarat_akerik_names')
    
    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (طارة اكليريك)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الأسماء: *{names_text}*\n"
        f"التاريخ: *{date_text}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n💍 المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    context.user_data.clear()
    return ConversationHandler.END


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
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
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
    product_data = context.user_data.get('taarat_khashab_product')
    names_text = context.user_data.get('taarat_khashab_names')
    
    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (طارة خشب)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الأسماء: *{names_text}*\n"
        f"التاريخ: *{date_text}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n💍 المنتج: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    context.user_data.clear()
    return ConversationHandler.END


# دوال الشراء التي لا تحتاج محادثة
def prepare_whatsapp_link_for_direct_buy(update, context):
    query = update.callback_query
    data = query.data  # buy_callback_data
    query.answer()

    # 1. استخراج مفتاح المنتج
    product_callback = data.replace("buy_", "")

    # 2. البحث عن بيانات المنتج (هذه الدالة تستخدم لـ: أباجورات، أهرامات، دروع، مجات، سبلميشن)
    product_data = None
    
    # القوائم المباشرة (أباجورات، سبلميشن)
    direct_lists = [abajorat_submenu, sublimation_submenu] # 🌟 إضافة sublimation_submenu
    for items_list in direct_lists:
        product_data = next((item for item in items_list if item["callback"] == product_callback), None)
        if product_data:
            break

    if not product_data:
        # البحث في القوائم المتداخلة (هرم مكتب، دروع، مجات)
        for menu_key in ["haram", "doro3", "mugat"]:
            for item in all_submenus.get(menu_key, []):
                if item['callback'] == product_callback:
                    product_data = item
                    break # وجد المنتج في المستوى الأول (ليس في هذا السيناريو)
                
                if 'items' in item:
                    sub_item = next((si for si in item['items'] if si['callback'] == product_callback), None)
                    if sub_item:
                        product_data = sub_item
                        break 
            if product_data:
                break


    if not product_data:
        query.answer("عفواً، لا يمكن إتمام هذا الطلب حالياً.", show_alert=True)
        start(update, context)
        return

    user_info = query.from_user
    message_body = (
        f"🔔 *طلب شراء جديد (شراء مباشر)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    # إعداد أزرار الانتهاء (واتساب ورجوع)
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # حذف الرسالة السابقة لتجنب الازدواجية
    try:
        query.message.delete()
    except Exception:
        pass
        
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n📦 المنتج: {product_data['label']}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def button(update, context):
    data = update.callback_query.data
    
    # 1. معالجة زر الرجوع للقائمة الرئيسية
    if data == 'main_menu':
        start(update, context)
        return

    # 2. معالجة فتح قوائم المستوى الأول (مثل: sawany, taarat, haram, ...) 
    # 🌟 تم حذف "sublimation" من هذه القائمة ليعمل كمنتجات مباشرة
    if data in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        submenu_list = all_submenus.get(data)
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus[data], clean_title, back_callback="main_menu")
        return

    # 3. معالجة فتح قوائم المستوى الأول المباشرة (engraved_wallet, aqlam, bsamat, etc.)
    # 🌟 تم إضافة "sublimation" هنا ليعمل كمنتجات مباشرة
    if data in ["engraved_wallet", "aqlam", "bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation"]:
        # Find the correct submenu list
        submenu_list = all_submenus.get(data)
        
        # ⚠️ المحافظ (engraved_wallet) تفتح قائمة فرعية من الأزرار
        if data == "engraved_wallet":
             show_submenu(update, context, submenu_list, "محافظ محفورة بالاسم", back_callback="main_menu")
             return
             
        # ⚠️ الأقلام (aqlam) تفتح قائمة فرعية من الأزرار 
        if data == "aqlam":
            show_submenu(update, context, submenu_list, "اقلام محفورة بالاسم", back_callback="main_menu")
            return
             
        # القوائم الأخرى التي تعرض المنتجات مباشرة 
        if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "sublimation"]: # 🌟 sublimation يعرض المنتجات مباشرة
            show_product_page(update, data, submenu_list, is_direct_list=True)
            return

    # ⚠️ معالجة أزرار ألوان المحافظ الفردية لفتح صفحة المنتج
    wallet_product_keys = [item["callback"] for item in engraved_wallet_submenu]
    if data in wallet_product_keys:
        show_single_wallet_product(update, context)
        return

    # ⚠️ معالجة أزرار أنواع الأقلام الفردية لفتح صفحة المنتج 
    pen_product_keys = [item["callback"] for item in aqlam_submenu]
    if data in pen_product_keys:
        show_single_pen_product(update, context)
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
        # يجب أن يصل إلى هنا الأباجورات والهرامات والدروع والمجات والسبلميشن
        prepare_whatsapp_link_for_direct_buy(update, context)
        return
        
    update.callback_query.answer("إجراء غير معروف.", show_alert=True)
    start(update, context) # عودة للقائمة الرئيسية كإجراء احتياطي


def handle_messages(update, context):
    # وظيفة لمعالجة الرسائل النصية التي لا تبدأ بأمر
    if context.user_data.get('state'):
        # إذا كانت هناك محادثة جارية، يتم تجاهل الرسالة هنا ويتم معالجتها بواسطة MessageHandler في ConversationHandler
        return
        
    update.effective_chat.send_message("من فضلك، اختر طلبك من الأزرار.", 
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))


def main():
    # ⚠️ تم استعادة استخدام متغير البيئة BOT_TOKEN كما طلبت
    TOKEN = os.environ.get('TOKEN') 
    if not TOKEN:
         # يفضل طباعة رسالة خطأ أو استخدام قيمة placeholder إذا لم يتم العثور على التوكن
         print("Error: BOT_TOKEN environment variable is not set. Please set it or hardcode the token.")
         return
         
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # 1. تعريف ConversationHandler للمحافظ
    engraved_wallet_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_wallet_purchase, pattern='^buy_wallet_.*')],
        states={
            GET_WALLET_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_wallet_name_and_prepare_whatsapp),
                # زر الرجوع يعود لصفحة المنتج الواحد
                CallbackQueryHandler(back_to_wallet_product_page, pattern='^back_to_wallet_product_page$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 2. تعريف ConversationHandler للأقلام 
    engraved_pen_handler = ConversationHandler(
        # تم تعديل نمط الدخول ليبدأ من زر الشراء
        entry_points=[CallbackQueryHandler(start_pen_purchase, pattern='^buy_aqlam_.*')],
        states={
            GET_PEN_NAME: [
                MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp),
                # تم تغيير نمط الرجوع ليعود لصفحة المنتج الواحد
                CallbackQueryHandler(back_to_single_pen_product_page, pattern='^back_to_pen_product_page$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(cancel_and_end)
        ]
    )


    # 3. تعريف ConversationHandler لبوكسات كتب الكتاب
    box_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_box_purchase, pattern='^buy_box_.*')],
        states={
            GET_BOX_COLOR: [
                # أزرار اختيار اللون
                CallbackQueryHandler(save_box_color_ask_names, pattern='^color_.*$'),
                # زر الرجوع من قائمة الألوان يعود لقائمة المنتجات (بوكس موديل 1/2)
                CallbackQueryHandler(back_to_box_menu, pattern='^katb_kitab_box$'), 
            ],
            GET_BOX_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, receive_box_names_and_finish),
                # زر الرجوع من إدخال الاسم يعود لاختيار اللون
                CallbackQueryHandler(back_to_box_color, pattern='^back_to_box_color$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 4. تعريف ConversationHandler لصواني شبكة اكليريك
    tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_tray_purchase, pattern='^buy_akerik_.*')],
        states={
            GET_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tray_names_ask_date),
                # الرجوع من إدخال الأسماء يعود لقائمة منتجات الاكليريك
                CallbackQueryHandler(button, pattern='^sawany_akerik$') 
            ],
            GET_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_tray_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_tray_names, pattern='^back_to_tray_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 5. تعريف ConversationHandler لصواني شبكة خشب
    khashab_tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_tray_purchase, pattern='^buy_khashab_.*')],
        states={
            GET_KHASHAB_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_khashab$')
            ],
            GET_KHASHAB_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_khashab_tray_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_khashab_tray_names, pattern='^back_to_khashab_tray_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 6. تعريف ConversationHandler لطارات اكليريك
    akerik_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_akerik_taarat_purchase, pattern='^buy_taarat_akerik_.*')],
        states={
            GET_AKRILIK_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_akerik_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_akerik$')
            ],
            GET_AKRILIK_TAARAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_akerik_taarat_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_akerik_taarat_names, pattern='^back_to_akerik_taarat_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 7. تعريف ConversationHandler لطارات خشب
    khashab_taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_khashab_taarat_purchase, pattern='^buy_taarat_khashab_.*')],
        states={
            GET_KHASHAB_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_khashab_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_khashab$')
            ],
            GET_KHASHAB_TAARAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_khashab_taarat_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_khashab_taarat_names, pattern='^back_to_khashab_taarat_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 8. تعريف ConversationHandler للبصامات
    bsamat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_bsamat_purchase, pattern='^buy_bsamat_.*')],
        states={
            GET_BSAMAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_bsamat_names_ask_date),
                CallbackQueryHandler(button, pattern='^bsamat$')
            ],
            GET_BSAMAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_bsamat_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_bsamat_names, pattern='^back_to_bsamat_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 9. تعريف ConversationHandler لمناديل كتب الكتاب
    tissue_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tissue_purchase, pattern='^buy_tissue_.*')],
        states={
            GET_TISSUE_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tissue_names_ask_date),
                CallbackQueryHandler(button, pattern='^wedding_tissues$') 
            ],
            GET_TISSUE_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_tissue_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_tissue_names, pattern='^back_to_tissue_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 10. إضافة جميع ConversationHandler أولاً لضمان الأولوية
    dp.add_handler(box_handler)
    dp.add_handler(tray_handler)
    dp.add_handler(khashab_tray_handler)
    dp.add_handler(akerik_taarat_handler) 
    dp.add_handler(khashab_taarat_handler) 
    dp.add_handler(bsamat_handler) 
    dp.add_handler(tissue_handler) 
    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler)
    
    
    # 11. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 12. معالج أزرار القائمة والتنقل (يجب أن يأتي بعد معالجات المحادثة)
    dp.add_handler(CallbackQueryHandler(button)) 

    # 13. معالج للرسائل النصية غير المرتبطة بمحادثة
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    # ابدأ البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()