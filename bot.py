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

# --------------------
# 2. بيانات القوائم والمنتجات
# --------------------

# --- قوائم فرعية مباشرة (تعرض منتجاتها مباشرة) ---
# ... (bsamat_submenu, wedding_tissues_submenu, abajorat_submenu, engraved_wallet_submenu) ...

# 🆕 الإضافة المطلوبة: قائمة بوكسات كتب الكتاب (تمت الإضافة هنا)
katb_ketab_boxes_submenu = [
    {
        "label": "بوكس كتب كتاب (الموديل الكلاسيكي)", 
        "callback": "box_classic", 
        "image": "https://e7.pngegg.com/pngimages/1000/393/png-clipart-box-wooden-box-thumbnail.png", # صورة افتراضية للمنتج الأول
        "description": "بوكس كتب كتاب بتصميم كلاسيكي، خشب عالي الجودة ومناسب للحفر بالليزر."
    },
    {
        "label": "بوكس كتب كتاب (موديل الأكريليك)", 
        "callback": "box_acrylic", 
        "image": "https://e7.pngegg.com/pngimages/585/744/png-clipart-red-gift-box-gift-box-square-box-thumbnail.png", # صورة افتراضية للمنتج الثاني
        "description": "بوكس كتب كتاب عصري من الأكريليك الشفاف، تصميم فاخر."
    }
]

# ... (aqlam_submenu والقوائم المتداخلة) ...


# --- القائمة الرئيسية ---
# 🚨 تم تعديل هذه القائمة لإضافة الزر في الترتيب الصحيح
main_menu = [
    {"label": "💍💍 صواني شبكة", "callback": "sawany"},
    {"label": "💍 طارات خطوبة وكتب الكتاب", "callback": "taarat"},
    {"label": "✋ بصامات", "callback": "bsamat"}, 
    {"label": "📜 مناديل كتب الكتاب", "callback": "wedding_tissues"}, 
    # 🆕 الإضافة المطلوبة: زر بوكس كتب الكتاب أسفل مناديل كتب الكتاب
    {"label": "🎁 بوكس كتب الكتاب", "callback": "katb_ketab_boxes"}, 
    {"label": "🗄️ هرم مكتب", "callback": "haram"},
    {"label": "🏆 دروع", "callback": "doro3"},
    {"label": "💡 اباجورات", "callback": "abajorat"}, 
    {"label": "✏️ اقلام", "callback": "aqlam"}, 
    {"label": "☕ مجات", "callback": "mugat"},
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"},
    {"label": "🖨️ مستلزمات سبلميشن", "callback": "sublimation"}
]


all_submenus = {
    # ... (باقي القوائم) ...
    "wedding_tissues": wedding_tissues_submenu, 
    # 🆕 الإضافة المطلوبة: إضافة القائمة الجديدة إلى الخريطة
    "katb_ketab_boxes": katb_ketab_boxes_submenu,
    "abajorat": abajorat_submenu,
    "engraved_wallet": engraved_wallet_submenu
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    # 🚨 تم تعديل القائمة المباشرة لتشمل 'katb_ketab_boxes'
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_ketab_boxes"]: 
        # للقوائم المباشرة، نضيف كل منتج مباشرة
        for product in submenu_list:
            product_to_submenu_map[product["callback"]] = menu_key
    # ... (باقي المنطق) ...


# --------------------
# 3. الدوال الرئيسية والمساعدة
# --------------------

# ... (دوال start و show_submenu و show_product_page) ...

# ------------------------------------
# الدالة الرئيسية لمعالجة ضغطات الأزرار
# ------------------------------------
def button(update, context):
    query = update.callback_query
    data = query.data

    # ... (باقي منطق الدالة) ...

    # 6. معالجة القوائم الفرعية التي تعرض المنتجات مباشرة
    # 🚨 هذا هو الجزء المسؤول عن فتح صفحة البوكسات
    if data in ["bsamat", "wedding_tissues", "abajorat", "katb_ketab_boxes"]:
        product_list = all_submenus[data]
        show_product_page(update, data, product_list, is_direct_list=True)
        return
        
    # ... (باقي منطق الدالة) ...
    
    # 8. حالة زر الشراء (المنتجات العادية غير المحفورة)
    if data.startswith("buy_"):
        # ... (منطق البحث عن بيانات المنتج الذي تم ضغط زر الشراء له - يشمل البوكسات) ...
        # ...
        
        # ... (باقي منطق الشراء عبر واتساب) ...
        
        return


# --------------------
# 4. إعداد البوت 
# --------------------
# ... (دالة main) ...