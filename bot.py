import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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
GET_BSAMAT_NAMES = 13  # حالة كتابة أسماء العرسان للبصامات
GET_BSAMAT_DATE = 14   # حالة كتابة التاريخ للبصامات
GET_TISSUE_NAMES = 15  # حالة كتابة أسماء العرسان للمناديل
GET_TISSUE_DATE = 16   # حالة كتابة التاريخ للمناديل


# --------------------
# 2. بيانات القوائم والمنتجات (لا تغيير)
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
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/475773348_986832329974720_6197915277469223378_n.jpg?stp=dst-jpg_s720x720_tt6&_nc_cat=107&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=KrebndL4u2oQ7kNvwH3smA2&_nc_oc=AdkT6T_o5SpJKdr9FQ5OhX2vuI5Cp3WjQl0pV9vRotIn9csOIX1DX-I9dC3FpvlBLJM&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=JFYgN-MxG5oy8y3q9Os6Ew&oh=00_AfhJxajOEm9owiAqd00_zEZ4Hy4qz7DYATV6p4tWdRxeA&oe=6923BE1B", 
        "description": "قلم تاتش معدن عالي الجودة ومناسب للحفر بالليزر."
    },
    {
        "label": "قلم تاتش مضئ", 
        "callback": "aqlam_luminous", 
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/489809156_1164483322357054_6286791651911010777_n.jpg?stp=dst-jpg_s590x590_tt6&_nc_cat=107&ccb=1-7&_nc_sid=833d8c&_nc_ohc=ELb9pciSoD0Q7kNvwG_rdLE&_nc_oc=AdkDWLOZBcjZp9AbNO2Fs-zK-suPtGc1D-KC3JP7NlzhwgJB3WZeGQQfCQIsfxZgvrg&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=U5_JMOw_cSsgrQQLv77j7g&oh=00_Afg-wJrTmoGZo5m1kVVh2IU0227UQ7pUtKSjRx_YEFoGWg&oe=6923B3BA", 
        "description": "قلم تاتش مضئ بتقنية متطورة ومناسب للحفر بالليزر."
    }
]

# --- القوائم المتداخلة (كما هي) ---
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
    "engraved_wallet": engraved_wallet_submenu
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box"]: 
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
# 3. الدوال الرئيسية والمساعدة (معظمها كما هو)
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
        # ⚠️ جميع أزرار الشراء هنا يتم معالجتها لاحقا بواسطة CallbackQueryHandler
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
    
    # 1. إذا كانت قائمة مباشرة من القائمة الرئيسية (مثل بصمات، أباجورات)
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "engraved_wallet", "aqlam"]:
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


# ----------------------------------------------------
# 4. الدوال المفقودة لجميع محادثات المنتجات الأخرى 
# ----------------------------------------------------

# --- [دوال محادثات المحافظ] ---

def get_wallet_item(callback_data):
    return next((item for item in engraved_wallet_submenu if item["callback"] == callback_data), None)

def prompt_for_name(update, context):
    query = update.callback_query
    query.answer()
    
    product_callback = query.data
    selected_product = get_wallet_item(product_callback)

    if not selected_product:
        query.answer("خطأ في العثور على المحفظة", show_alert=True)
        return ConversationHandler.END

    context.user_data['wallet_product'] = selected_product
    
    # ⚠️ تم التعديل: تغيير اسم الـ callback لزر الرجوع
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_wallets_list")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    # ⚠️ تم التعديل: نص الرسالة يطابق طلب المستخدم
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب الاسم المراد حفره على المحفظة** في رسالة نصية بالأسفل."
    
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=selected_product['image'],
        caption=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    return GET_WALLET_NAME

def receive_name_and_prepare_whatsapp(update, context):
    name_text = update.message.text
    product_data = context.user_data.get('wallet_product')
    
    if not product_data:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (محفظة محفورة)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"النص المراد حفره: *{name_text}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    # ⚠️ تم التعديل: إظهار زر الواتساب بعد استلام الاسم
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n👝 المحفظة: {product_data['label']}\n✍️ النص: {name_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    context.user_data.clear()
    return ConversationHandler.END

# ⚠️ تم التعديل: لتصبح وظيفة الرجوع للمحافظ
def back_to_wallets_list(update, context):
    # رجوع إلى صفحة المحافظ
    query = update.callback_query
    query.answer()
    query.data = 'engraved_wallet'
    button(update, context) 
    return ConversationHandler.END

# --- [دوال محادثات الأقلام] ---

def get_pen_item(callback_data):
    return next((item for item in aqlam_submenu if item["callback"] == callback_data), None)

def prompt_for_pen_name(update, context):
    query = update.callback_query
    query.answer()
    
    product_callback = query.data
    selected_product = get_pen_item(product_callback)
    if not selected_product:
        query.answer("خطأ في العثور على القلم", show_alert=True)
        return ConversationHandler.END

    context.user_data['pen_product'] = selected_product
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_pen_types")]] 
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب الاسم أو النص المراد حفره على القلم** في رسالة نصية بالأسفل."
    
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=selected_product['image'],
        caption=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    return GET_PEN_NAME

def receive_pen_name_and_prepare_whatsapp(update, context):
    name_text = update.message.text
    product_data = context.user_data.get('pen_product')
    
    if not product_data:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (قلم محفور)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"النص المراد حفره: *{name_text}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n✏️ القلم: {product_data['label']}\n✍️ النص: {name_text}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    context.user_data.clear()
    return ConversationHandler.END

def back_to_pen_types(update, context):
    # رجوع إلى صفحة الأقلام
    query = update.callback_query
    query.answer()
    query.data = 'aqlam'
    button(update, context) 
    return ConversationHandler.END

# --- [دوال محادثات بوكس كتب الكتاب] ---
def get_box_item(callback_data):
    return next((item for item in katb_kitab_box_submenu if item["callback"] == callback_data.replace("buy_", "")), None)

def start_box_purchase(update, context):
    query = update.callback_query
    query.answer()
    product_callback = query.data 
    selected_product = get_box_item(product_callback)
    
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['box_product'] = selected_product
    
    # رسالة اختيار اللون
    color_keyboard = [
        [InlineKeyboardButton("أبيض", callback_data="color_white")],
        [InlineKeyboardButton("أسود", callback_data="color_black")],
        [InlineKeyboardButton("بيج", callback_data="color_beige")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="katb_kitab_box")] # العودة لصفحة البوكس
    ]
    reply_markup = InlineKeyboardMarkup(color_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ **{selected_product['label']}**\n\nمن فضلك اختر اللون المطلوب للبوكس:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_BOX_COLOR

def save_box_color_ask_names(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data == 'katb_kitab_box':
        # رجوع لصفحة المنتجات
        return back_to_box_color(update, context)

    color = query.data.split('_')[-1]
    context.user_data['box_color'] = color
    product_data = context.user_data.get('box_product')
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_box_color")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"تم اختيار اللون **{color}**.\n\nمن فضلك الآن **اكتب اسم العريس والعروسة** (حسب الشكل المطلوب):",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return GET_BOX_NAMES

def receive_box_names_and_finish(update, context):
    names = update.message.text
    product_data = context.user_data.get('box_product')
    color = context.user_data.get('box_color')
    
    if not product_data:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (
        f"🔔 *طلب شراء جديد (بوكس كتب كتاب)* 🔔\n\n"
        f"المنتج: {product_data['label']}\n"
        f"اللون: *{color}*\n"
        f"الأسماء: *{names}*\n"
        f"الكود: {product_data['callback']}\n\n"
        f"اسم العميل: {user_info.first_name}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}"
    )
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"شكراً لك! تفاصيل الطلب:\n\n🎁 البوكس: {product_data['label']}\n🎨 اللون: {color}\n✍️ الأسماء: {names}\n\nلإتمام الطلب، اضغط على الزر التالي:",
        reply_markup=reply_markup
    )
    context.user_data.clear()
    return ConversationHandler.END

def back_to_box_color(update, context):
    # رجوع لصفحة المنتجات
    query = update.callback_query
    query.answer()
    query.data = 'katb_kitab_box'
    button(update, context) 
    return ConversationHandler.END


# --- [دوال محادثات الصواني (اكليريك وخشب)] ---
# تم تبسيط هذه الدوال لضمان التعريف، واعتمدت على نفس نمط المناديل لطلب الاسم والتاريخ

def get_tray_item(callback_data):
    # للبحث في الصواني الاكليريك
    tray_list = next((s['items'] for s in sawany_submenu if s['callback'] == 'sawany_akerik'), [])
    # للبحث في الصواني الخشب
    tray_list += next((s['items'] for s in sawany_submenu if s['callback'] == 'sawany_khashab'), [])
    return next((item for item in tray_list if item["callback"] == callback_data.replace("buy_", "")), None)

def start_tray_purchase(update, context):
    query = update.callback_query
    query.answer()
    product_callback = query.data.replace("buy_", "")
    selected_product = get_tray_item(query.data) 
    
    if not selected_product:
        query.answer("خطأ في العثور على الصينية", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['tray_product'] = selected_product
    
    back_callback = "sawany_akerik" if "akerik" in product_callback else "sawany_khashab"
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة**:"
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    return GET_TRAY_NAMES # يستخدم لكلا النوعين (اكليريك وخشب) حسب السياق

def save_tray_names_ask_date(update, context):
    names = update.message.text
    context.user_data['tray_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_tray_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(chat_id=update.message.chat_id, text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_TRAY_DATE

def receive_tray_date_and_finish(update, context):
    date_text = update.message.text
    product_data = context.user_data.get('tray_product')
    names_text = context.user_data.get('tray_names')
    
    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (f"🔔 *طلب شراء جديد (صينية شبكة)* 🔔\n\nالمنتج: {product_data['label']}\nالأسماء: *{names_text}*\nالتاريخ: *{date_text}*\nالكود: {product_data['callback']}")
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(chat_id=update.message.chat_id, text=f"شكراً لك! تفاصيل الطلب:\n\n💍 الصينية: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:", reply_markup=reply_markup)
    context.user_data.clear()
    return ConversationHandler.END

def back_to_tray_names(update, context):
    query = update.callback_query
    query.answer()
    selected_product = context.user_data.get('tray_product')
    
    back_callback = "sawany_akerik" if "akerik" in selected_product['callback'] else "sawany_khashab"
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_TRAY_NAMES

# (ملاحظة: الدوال الأخرى start_khashab_tray_purchase, save_khashab_tray_names_ask_date, receive_khashab_tray_date_and_finish تم توحيدها مع دوال الاكليريك في نمط start_tray_purchase لتقليل التكرار. وسنستخدم الآن دوال الـ TRAY لنوعي الصواني)

# --- [دوال محادثات الطارات (اكليريك وخشب)] ---
# تم تبسيط هذه الدوال أيضًا واعتمدت على نمط المناديل لطلب الاسم والتاريخ.
# نظرًا لتكرار نمط طلب (الاسم > التاريخ)، سنستخدم نفس الدوال مع تعديل بسيط لنقاط الدخول.

def get_taarat_item(callback_data):
    # للبحث في طارات اكليريك
    taarat_list = next((s['items'] for s in taarat_submenu if s['callback'] == 'taarat_akerik'), [])
    # للبحث في طارات خشب
    taarat_list += next((s['items'] for s in taarat_submenu if s['callback'] == 'taarat_khashab'), [])
    return next((item for item in taarat_list if item["callback"] == callback_data.replace("buy_", "")), None)


def start_taarat_purchase(update, context):
    query = update.callback_query
    query.answer()
    product_callback = query.data.replace("buy_", "")
    selected_product = get_taarat_item(query.data) 
    
    if not selected_product:
        query.answer("خطأ في العثور على الطارة", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['taarat_product'] = selected_product
    
    back_callback = "taarat_akerik" if "akerik" in product_callback else "taarat_khashab"
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة**:"
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=caption_text, reply_markup=reply_markup, parse_mode="Markdown")
    return GET_AKRILIK_TAARAT_NAMES # سنستخدم هذا الحالة لكلا النوعين

def save_taarat_names_ask_date(update, context):
    names = update.message.text
    context.user_data['taarat_names'] = names
    
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_taarat_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(chat_id=update.message.chat_id, text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_AKRILIK_TAARAT_DATE

def receive_taarat_date_and_finish(update, context):
    date_text = update.message.text
    product_data = context.user_data.get('taarat_product')
    names_text = context.user_data.get('taarat_names')
    
    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (f"🔔 *طلب شراء جديد (طارة)* 🔔\n\nالمنتج: {product_data['label']}\nالأسماء: *{names_text}*\nالتاريخ: *{date_text}*\nالكود: {product_data['callback']}")
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(chat_id=update.message.chat_id, text=f"شكراً لك! تفاصيل الطلب:\n\n💍 الطارة: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:", reply_markup=reply_markup)
    context.user_data.clear()
    return ConversationHandler.END

def back_to_taarat_names(update, context):
    query = update.callback_query
    query.answer()
    selected_product = context.user_data.get('taarat_product')
    
    back_callback = "taarat_akerik" if "akerik" in selected_product['callback'] else "taarat_khashab"
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    try:
        query.message.delete()
    except:
        pass
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"من فضلك أعد كتابة **اسم العريس والعروسة**:", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_AKRILIK_TAARAT_NAMES

# (ملاحظة: تم توحيد جميع دوال الطارات بنفس نمط الصواني لضمان التشغيل)
# سنقوم بتعريف الدوال المطلوبة تحديداً في دالة main() باستخدام اسم دالة واحدة لكل وظيفة (مثلاً start_taarat_purchase بدلاً من start_akerik_taarat_purchase و start_khashab_taarat_purchase) 

# --- [دوال محادثات البصامات] ---
# تم تبسيط هذه الدوال أيضًا واعتمدت على نمط المناديل لطلب الاسم والتاريخ.

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
        
    caption_text = f"✅ **{selected_product['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** او اضغط زر رجوع للعودة الي القائمة السابقة:"
    
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
    
    context.bot.send_message(chat_id=update.message.chat_id, text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1):", reply_markup=reply_markup, parse_mode="Markdown")
    return GET_BSAMAT_DATE

def receive_bsamat_date_and_finish(update, context):
    date_text = update.message.text
    product_data = context.user_data.get('bsamat_product')
    names_text = context.user_data.get('bsamat_names')
    
    if not product_data or not names_text:
        update.effective_chat.send_message("حدث خطأ، يرجى البدء من جديد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        return ConversationHandler.END
        
    user_info = update.message.from_user
    
    message_body = (f"🔔 *طلب شراء جديد (بصامة)* 🔔\n\nالمنتج: {product_data['label']}\nالأسماء: *{names_text}*\nالتاريخ: *{date_text}*\nالكود: {product_data['callback']}")
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(chat_id=update.message.chat_id, text=f"شكراً لك! تفاصيل الطلب:\n\n✋ البصامة: {product_data['label']}\n✍️ الأسماء: {names_text}\n📅 التاريخ: {date_text}\n\nلإتمام الطلب، اضغط على الزر التالي:", reply_markup=reply_markup)
    context.user_data.clear()
    return ConversationHandler.END


# --- [دوال محادثات مناديل كتب الكتاب (التي طلبها المستخدم)] ---

def get_tissue_items():
    return wedding_tissues_submenu

def start_tissue_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data  
    product_callback = data.replace("buy_", "")
    
    # 1. Get product data
    items_list = get_tissue_items() 
    selected_product = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END
        
    context.user_data['tissue_product'] = selected_product
    context.user_data['state'] = GET_TISSUE_NAMES
    
    # 2. Prepare keyboard (Back button to wedding_tissues menu)
    # ملاحظة: تم تعديل الـ Callback هنا للرجوع للقائمة الرئيسية للمناديل
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
        
    # رجوع لصفحة منتجات المناديل
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
    
    # زر الرجوع هنا يعود للخطوة السابقة (إدخال الأسماء)
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_tissue_names")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"تم حفظ الأسماء: **{names}**\n\nمن فضلك الآن **اكتب التاريخ** (مثال: 2024/1/1) او اضغط زر رجوع للعودة الي القائمة السابقة:",
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


# ------------------------------------
# الدالة الرئيسية لمعالجة ضغطات الأزرار (للملاحة فقط)
# ------------------------------------
def button(update, context):
    query = update.callback_query
    data = query.data
    query.answer() 

    # 1. حالة العودة للقائمة الرئيسية
    if data == "main_menu":
        start(update, context)
        return

    # 2. معالجة فتح قوائم المستوى الأول (Sawany, Taarat, Haram, Doro3, Mugat)
    if data in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus[data], clean_title, back_callback="main_menu") 
        return
        
    # 3. معالجة فتح قوائم المستوى الأول المباشرة (engraved_wallet, aqlam, bsamat, etc.)
    if data in ["engraved_wallet", "aqlam", "bsamat", "wedding_tissues", "abajorat", "katb_kitab_box"]:
        # Find the correct submenu list
        submenu_list = all_submenus.get(data)
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        
        # إذا كانت "بصمات" أو أي قائمة أخرى تحتاج عرض المنتجات أولاً
        if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box", "engraved_wallet", "aqlam"]:
             show_product_page(update, data, submenu_list, is_direct_list=True)
             return
        
        # عرض القائمة الفرعية (لن يتم الوصول إلى هنا في هذا الكود المعدل لكن للاحتياط)
        show_submenu(update, context, submenu_list, title.split()[-1], back_callback="main_menu") 
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
        products_list = [] # تهيئة قائمة المنتجات
        
        # ⚠️ (تم تعديل منطق البحث ليكون أكثر وضوحاً وتجنب أي دمج غير مقصود)
        # إذا كانت قائمة من المستوى الثاني
        found_item = None
        for parent_submenu in all_submenus.values():
            # البحث باستخدام دالة next داخل كل قائمة فرعية
            found_item = next((item for item in parent_submenu if item.get("callback") == data and 'items' in item), None)
            
            if found_item:
                products_list = found_item['items']
                break
        
        if products_list:
            show_product_page(update, data, products_list, is_direct_list=False)
            return

    # إذا لم يطابق أي من الحالات أعلاه (وهو زر غير معروف)، نعتبره خطأ في التنقل ونعود للقائمة الرئيسية
    context.bot.send_message(chat_id=update.effective_chat.id, text="عذراً، حدث خطأ عام في التنقل. الرجاء البدء مجدداً.", parse_mode="Markdown")
    start(update, context) # نعود للقائمة الرئيسية كإجراء وقائي
    return

# دالة لمعالجة أزرار الشراء العادية (التي لا تحتاج محادثة)
def handle_generic_buy(update, context):
    query = update.callback_query
    data = query.data
    product_key = data.replace("buy_", "")
    product_data = None
    
    # البحث عن بيانات المنتج باستخدام مفتاح المنتج
    for submenu in all_submenus.values():
        for item in submenu:
            if item.get("callback") == product_key and 'items' not in item:
                product_data = item
                break
            if 'items' in item:
                for sub_item in item['items']:
                    if sub_item.get("callback") == product_key:
                        product_data = sub_item
                        break
            if product_data:
                break
        if product_data:
            break
            
    if not product_data:
        query.answer(text="عذراً، لم يتم العثور على بيانات المنتج.", show_alert=True)
        return
        
    user_info = query.from_user
    message_body = (f"🔔 *طلب شراء جديد*\nالمنتج: {product_data['label']}\nالكود: {product_key}\nالعميل: {user_info.first_name}\n🔗 صورة: {product_data.get('image', 'لا يوجد')}")
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    query.answer(text="سيتم فتح واتساب...", show_alert=False)
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # محاولة حذف رسالة المنتج السابقة
    try:
        query.message.delete()
    except Exception:
        pass

    context.bot.send_message(chat_id=query.message.chat_id, text=f"شكراً لطلبك! اضغط أدناه للإرسال:", reply_markup=reply_markup)


# --------------------
# 5. إعداد البوت 
# --------------------

def main():
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN).")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # 1. محافظ (ConversationHandler)
    engraved_wallet_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prompt_for_name, pattern='^wallet_.*')],
        states={
            GET_WALLET_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_name_and_prepare_whatsapp)]
        },
        fallbacks=[
            CommandHandler('start', start), 
            # ⚠️ تم التعديل: لتغطية زر الرجوع الجديد
            CallbackQueryHandler(back_to_wallets_list, pattern='^back_to_wallets_list$'), 
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 2. اقلام (ConversationHandler)
    engraved_pen_handler = ConversationHandler(
        # تم تصحيح prompt_for_pen_name
        entry_points=[CallbackQueryHandler(prompt_for_pen_name, pattern='^aqlam_.*')],
        states={
            GET_PEN_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp)]
        },
        fallbacks=[
            CommandHandler('start', start), 
            CallbackQueryHandler(back_to_pen_types, pattern='^back_to_pen_types$'), 
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 3. بوكس كتب الكتاب (ConversationHandler)
    box_handler = ConversationHandler(
        # تم تصحيح start_box_purchase
        entry_points=[CallbackQueryHandler(start_box_purchase, pattern='^buy_box_.*')],
        states={
            GET_BOX_COLOR: [CallbackQueryHandler(save_box_color_ask_names, pattern='^color_.*|katb_kitab_box$')],
            GET_BOX_NAMES: [MessageHandler(Filters.text & ~Filters.command, receive_box_names_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start), 
            CallbackQueryHandler(back_to_box_color, pattern='^back_to_box_color$'), 
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 4. صواني شبكة اكليريك / خشب (ConversationHandler)
    # تم توحيد الـ Handler لنوعي الصواني باستخدام دوال موحدة
    tray_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tray_purchase, pattern=r'^buy_(akerik|khashab)_m\d+$')],
        states={
            GET_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^sawany_(akerik|khashab)$')
            ],
            GET_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_tray_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_tray_names, pattern='^back_to_tray_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 5. طارات اكليريك / خشب (ConversationHandler)
    # تم توحيد الـ Handler لنوعي الطارات باستخدام دوال موحدة
    taarat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_taarat_purchase, pattern=r'^buy_taarat_(akerik|khashab)_m\d+$')],
        states={
            GET_AKRILIK_TAARAT_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_taarat_names_ask_date),
                CallbackQueryHandler(button, pattern='^taarat_(akerik|khashab)$')
            ],
            GET_AKRILIK_TAARAT_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_taarat_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_taarat_names, pattern='^back_to_taarat_names$'),
            CallbackQueryHandler(cancel_and_end)
        ]
    )
    
    # 6. بصامات (ConversationHandler)
    bsamat_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_bsamat_purchase, pattern=r'^buy_bsamat_m\d+$')],
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

    # 🆕 7. مناديل كتب الكتاب (ConversationHandler) - كما طلب المستخدم
    tissue_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_tissue_purchase, pattern=r'^buy_tissue_m\d+$')],
        states={
            GET_TISSUE_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tissue_names_ask_date),
                CallbackQueryHandler(button, pattern='^wedding_tissues$') 
            ],
            GET_TISSUE_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_tissue_date_and_finish),
                # زر الرجوع من التاريخ يعود للخطوة السابقة (إدخال الأسماء)
                CallbackQueryHandler(back_to_tissue_names, pattern='^back_to_tissue_names$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 🛑 إضافة جميع ConversationHandler أولاً لضمان الأولوية
    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler)
    dp.add_handler(box_handler)
    dp.add_handler(tray_handler)
    dp.add_handler(taarat_handler) 
    dp.add_handler(bsamat_handler) 
    dp.add_handler(tissue_handler) 
    
    # 8. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 9. معالج أزرار الشراء العامة (للمنتجات التي لا تحتاج محادثة)
    dp.add_handler(CallbackQueryHandler(handle_generic_buy, pattern='^buy_.*')) 
    
    # 10. معالج الأزرار المتبقية (للملاحة بين القوائم)
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()