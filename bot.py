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
bsamat_submenu = [
    {"label": "بصامة موديل 1", "callback": "bsamat_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 1."},
    {"label": "بصامة موديل 2", "callback": "bsamat_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 2."}
]
wedding_tissues_submenu = [
    {"label": "منديل موديل 1", "callback": "tissue_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 1."},
    {"label": "منديل موديل 2", "callback": "tissue_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 2."}
]

# 🆕 قائمة بوكسات كتب الكتاب
katb_ketab_boxes_submenu = [
    {
        "label": "بوكس كتب كتاب (الموديل الكلاسيكي)", 
        "callback": "box_classic", 
        "image": "https://e7.pngegg.com/pngimages/1000/393/png-clipart-box-wooden-box-thumbnail.png", 
        "description": "بوكس كتب كتاب بتصميم كلاسيكي، خشب عالي الجودة ومناسب للحفر بالليزر."
    },
    {
        "label": "بوكس كتب كتاب (موديل الأكريليك)", 
        "callback": "box_acrylic", 
        "image": "https://e7.pngegg.com/pngimages/585/744/png-clipart-red-gift-box-gift-box-square-box-thumbnail.png", 
        "description": "بوكس كتب كتاب عصري من الأكريليك الشفاف، تصميم فاخر."
    }
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
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/489809156_1164483322357054_6286791651911010777_n.jpg?stp=dst-jpg_s590x590_tt6&_nc_cat=107&ccb=1-7&_nc_sid=833d8c&_nc_ohc=ELb9pciSoD0Q7kNvwG_rdLE&_nc_oc=AdkDWLOZBcjZp9AbNO2Fs-zK-suPtGc1D-KC3JP77j7g&oh=00_Afg-wJrTmoGZo5m1kVVh2IU0227UQ7pUtKSjRx_YEFoGWg&oe=6923B3BA", 
        "description": "قلم تاتش مضئ بتقنية متطورة ومناسب للحفر بالليزر."
    }
]

# --- القوائم المتداخلة (sawany, taarat, haram, doro3, mugat) تبقى كما هي ---
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
# 🚨 هنا يتم تعريف زر "بوكس كتب الكتاب" لضمان ظهوره.
main_menu = [
    {"label": "💍💍 صواني شبكة", "callback": "sawany"},
    {"label": "💍 طارات خطوبة وكتب الكتاب", "callback": "taarat"},
    {"label": "✋ بصامات", "callback": "bsamat"}, 
    {"label": "📜 مناديل كتب الكتاب", "callback": "wedding_tissues"}, 
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
    "sawany": sawany_submenu,
    "taarat": taarat_submenu,
    "haram": haram_submenu,
    "doro3": doro3_submenu,
    "aqlam": aqlam_submenu,
    "mugat": mugat_submenu,
    "bsamat": bsamat_submenu, 
    "wedding_tissues": wedding_tissues_submenu, 
    "katb_ketab_boxes": katb_ketab_boxes_submenu, # 🚨 تأكيد وجود القائمة
    "abajorat": abajorat_submenu,
    "engraved_wallet": engraved_wallet_submenu
}

# بناء خريطة المنتجات (مفتاح المنتج > مفتاح القائمة الأم)
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_ketab_boxes"]: 
        for product in submenu_list:
            product_to_submenu_map[product["callback"]] = menu_key
    else:
        for item in submenu_list:
            product_to_submenu_map[item["callback"]] = menu_key 
            if 'items' in item:
                for sub_item in item['items']:
                    product_to_submenu_map[sub_item["callback"]] = item["callback"] 


# --------------------
# 3. الدوال الرئيسية والمساعدة
# --------------------

def start(update, context):
    # 💡 يتم التحقق من أن الكود وصل إلى هنا
    print(f"DEBUG: Start command received from user {update.effective_user.first_name}") 
    
    query = update.callback_query
    
    if context.user_data.get('state') in [GET_WALLET_NAME, GET_PEN_NAME]:
        context.user_data.clear()
        context.user_data['state'] = None
        
    if query:
        query.answer()
    
    user_name = update.effective_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختر طلبك من القائمة:"
    
    # 🚨 هنا يتم بناء لوحة المفاتيح
    try:
        keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in main_menu]
        reply_markup = InlineKeyboardMarkup(keyboard)
    except Exception as e:
        # إذا حدث خطأ أثناء بناء لوحة المفاتيح
        print(f"ERROR: Failed to build keyboard in start function: {e}")
        update.effective_message.reply_text("عذراً، حدث خطأ داخلي في عرض القائمة الرئيسية. يرجى المحاولة مرة أخرى لاحقاً.")
        return


    # منطق عرض القائمة الرئيسية (حذف الرسالة القديمة وإرسال رسالة جديدة)
    if query:
        try:
            query.message.delete()
        except Exception:
            pass 
        
        update.effective_chat.send_message(greeting_text, reply_markup=reply_markup)
    else:
        update.effective_message.reply_text(greeting_text, reply_markup=reply_markup)

# 💡 دالة عرض القائمة الفرعية (باقي الدوال كما هي)
def show_submenu(update, context, submenu_list, title, back_callback="main_menu"):
    # ... (الكود كما هو) ...
    pass
        
# 🚨 تم تأكيد معالجة الأخطاء هنا في حالة فشل الصور (مما كان يوقف الكود)
def show_product_page(update, product_callback_data, product_data, is_direct_list=False):
    query = update.callback_query
    if query:
        query.answer()

    products_to_show = []
    if is_direct_list:
        products_to_show = product_data
    elif 'items' in product_data:
        products_to_show = product_data['items']
    else:
        products_to_show = [product_data]

    # نحذف رسالة القائمة السابقة
    if query and query.message:
        try:
            query.message.delete()
        except Exception:
            pass
    
    # حلقة إرسال المنتجات
    for item in products_to_show:
        item_keyboard = [[InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{item['callback']}")]]
        item_reply_markup = InlineKeyboardMarkup(item_keyboard)
        
        caption_text = f"**{item['label']}**\n\n{item['description']}"
        
        # محاولة إرسال صورة
        try:
            update.effective_message.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=item['image'],
                caption=caption_text,
                reply_markup=item_reply_markup,
                parse_mode="Markdown"
            )
        except telegram.error.BadRequest as e:
            # إذا فشل إرسال الصورة (قد يكون بسبب رابط الصورة الافتراضي)، نرسل نص كبديل
            fallback_text = f"⚠️ *خطأ في تحميل الصورة للمنتج: {item['label']}*\n\n{caption_text}"
            update.effective_message.bot.send_message(
                chat_id=update.effective_chat.id,
                text=fallback_text,
                reply_markup=item_reply_markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            fallback_text = f"❌ *حدث خطأ غير متوقع للمنتج: {item['label']}*\n\n{caption_text}"
            update.effective_message.bot.send_message(
                chat_id=update.effective_chat.id,
                text=fallback_text,
                reply_markup=item_reply_markup,
                parse_mode="Markdown"
            )


    # تحديد زر الرجوع
    if product_callback_data in ["bsamat", "wedding_tissues", "abajorat", "katb_ketab_boxes"]:
        back_callback = "main_menu"
        back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
    # ... (باقي منطق زر الرجوع) ...
    else:
        back_callback = product_to_submenu_map.get(product_callback_data, "main_menu")
        
        if back_callback in ["sawany", "taarat", "haram", "doro3", "mugat"]:
             back_callback = back_callback
             back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
        elif back_callback in ["engraved_wallet", "aqlam"]:
             back_callback = back_callback
             back_text = "🔙 اضغط للرجوع إلى القائمة الرئيسية"
        else:
             back_callback = back_callback
             back_text = "🔙 اضغط للرجوع إلى القائمة الفرعية"


    back_keyboard = [[InlineKeyboardButton(back_text, callback_data=back_callback)]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # إرسال زر الرجوع
    update.effective_message.bot.send_message(
        chat_id=update.effective_chat.id,
        text="---", 
        reply_markup=back_reply_markup
    )


# ------------------------------------
# الدالة الرئيسية لمعالجة ضغطات الأزرار
# ------------------------------------
def button(update, context):
    query = update.callback_query
    data = query.data

    # 1. حالة العودة للقائمة الرئيسية
    if data == "main_menu":
        start(update, context)
        return

    # 6. معالجة القوائم الفرعية التي تعرض المنتجات مباشرة (بما في ذلك بوكس كتب الكتاب)
    if data in ["bsamat", "wedding_tissues", "abajorat", "katb_ketab_boxes"]:
        product_list = all_submenus[data]
        show_product_page(update, data, product_list, is_direct_list=True)
        return

    # ... (باقي منطق الدالة button كما هو) ...

    # 2. معالجة فتح قائمة المحافظ 
    if data == "engraved_wallet":
        show_submenu(update, context, engraved_wallet_submenu, "محافظ محفورة بالاسم", back_callback="main_menu")
        return 
        
    # 3. معالجة فتح قائمة الأقلام (محادثة)
    if data == "aqlam":
        show_submenu(update, context, aqlam_submenu, "اقلام محفورة بالاسم", back_callback="main_menu")
        return 
        
    # 4. معالجة اختيار المنتج (سواء محفظة أو قلم)
    if data in [item["callback"] for item in engraved_wallet_submenu]:
        return prompt_for_name(update, context) 
    
    # 🛑 معالجة اختيار نوع القلم (معدن أو مضئ)
    if data in [item["callback"] for item in aqlam_submenu]:
        return prompt_for_pen_name(update, context) 

    # 5. معالجة فتح القوائم الفرعية المتداخلة 
    if data in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1]
        show_submenu(update, context, all_submenus[data], clean_title, back_callback="main_menu") 
        return
        
    # 7. معالجة ضغط زر المنتج للذهاب لصفحة الشراء أو لفتح قائمة فرعية متداخلة 
    if data in product_to_submenu_map:
        product_data = None
        
        for submenu_key, submenu_list in all_submenus.items():
            for item in submenu_list:
                if data == item.get("callback") and 'items' in item:
                    product_data = item
                    break 
                if data == item.get("callback") and 'items' not in item:
                    product_data = item
                    break
                if 'items' in item:
                    sub_item = next((si for si in item['items'] if si.get("callback") == data), None)
                    if sub_item:
                         product_data = sub_item
                         break
            if product_data:
                break
        
        if product_data:
            show_product_page(update, data, product_data)
            return
        else:
            query.answer(text="عذراً، لم يتم العثور على بيانات المنتج.", show_alert=True)
            return

    # 8. حالة زر الشراء (المنتجات العادية غير المحفورة)
    if data.startswith("buy_"):
        product_key = data.replace("buy_", "")
        product_data = None
        
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
        
        message_body = (
            f"🔔 *طلب شراء جديد من بوت تليجرام* 🔔\n"
            f"المنتج: {product_data['label']}\n"
            f"الكود: {product_key}\n"
            f"العميل: {user_info.first_name}\n"
            f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
            f"🔗 رابط صورة المنتج: {product_data['image']}\n" 
            f"رابط التواصل عبر تليجرام: tg://user?id={user_info.id}"
        )
        
        encoded_text = quote_plus(message_body)
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
        
        query.answer(text="سيتم فتح تطبيق واتساب الآن لإرسال الطلب.", show_alert=False)

        keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            query.message.delete()
        except Exception:
            pass

        context.bot.send_message(
            chat_id=query.message.chat_id, 
            text=f"شكراً لطلبك! لإنهاء عملية الشراء، اضغط على الزر التالي لإرسال تفاصيل الطلب:", 
            reply_markup=reply_markup
        )
        
        return
        
# --------------------
# 4. إعداد البوت 
# --------------------
def main():
    # 💡 استبدل بتوكن البوت الخاص بك
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN) في بيئة العمل. يرجى التأكد من تعيينه.")
        return
    
    if WHATSAPP_NUMBER == "201288846355":
        print("⚠️ يرجى استبدال WHATSAPP_NUMBER برقمك الحقيقي.")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # مُعالجات المحادثة
    engraved_wallet_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(prompt_for_name, pattern='^(' + '|'.join([item['callback'] for item in engraved_wallet_submenu]) + ')$')
        ],
        states={GET_WALLET_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_name_and_prepare_whatsapp)]},
        fallbacks=[CommandHandler('start', start), CallbackQueryHandler(back_to_wallets_color, pattern='^back_to_wallets_color$'), CallbackQueryHandler(button) ]
    )

    engraved_pen_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(prompt_for_pen_name, pattern='^(' + '|'.join([item['callback'] for item in aqlam_submenu]) + ')$')
        ],
        states={GET_PEN_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_pen_name_and_prepare_whatsapp)]},
        fallbacks=[CommandHandler('start', start), CallbackQueryHandler(back_to_pen_types, pattern='^back_to_pen_types$'), CallbackQueryHandler(button) ]
    )

    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler) 
    
    # إضافة معالجات الأوامر والأزرار الأخرى
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    #os.environ["TOKEN"] = "YOUR_BOT_TOKEN_HERE" 
    main()