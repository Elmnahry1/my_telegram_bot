import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات الواتساب: استبدل بالرقم الخاص بك (كود الدولة + الرقم بدون علامة +)
WHATSAPP_NUMBER = "201288846355" 

# --------------------
# 1. بيانات القوائم والمنتجات (تم تحديث جميع القوائم الفرعية)
# --------------------
sawany_submenu = [
    {
        "label": "صواني شبكة اكليريك", 
        "callback": "sawany_akerik", 
        "items": [ 
            {
                "label": "صينية اكليريك موديل 1", 
                "callback": "akerik_m1",
                "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", 
                "description": "صينية اكليريك: وصف المنتج الأول."
            },
            {
                "label": "صينية اكليريك موديل 2", 
                "callback": "akerik_m2",
                "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", 
                "description": "صينية اكليريك: وصف المنتج الثاني."
            }
        ]
    },
    # هذا المنتج بقي كما هو كمنتج واحد
    {"label": "صواني شبكة خشب", "callback": "sawany_khashab", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف صواني شبكة خشب"}
]

taarat_submenu = [
    {
        "label": "طارات اكليريك", 
        "callback": "taarat_akerik", 
        "items": [
            {"label": "طارة اكليريك موديل 1", "callback": "taarat_akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة اكليريك موديل 1"},
            {"label": "طارة اكليريك موديل 2", "callback": "taarat_akerik_m2", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "وصف طارة اكليريك موديل 2"}
        ]
    },
    {
        "label": "طارات خشب", 
        "callback": "taarat_khashab", 
        "items": [
            {"label": "طارة خشب موديل 1", "callback": "taarat_khashab_m1", "image": "path/to/taarat_khashab_m1.jpg", "description": "وصف طارة خشب موديل 1"},
            {"label": "طارة خشب موديل 2", "callback": "taarat_khashab_m2", "image": "path/to/taarat_khashab_m2.jpg", "description": "وصف طارة خشب موديل 2"}
        ]
    }
]

haram_submenu = [
    {
        "label": "هرم مكتب اكليريك", 
        "callback": "haram_akerik", 
        "items": [
            {"label": "هرم اكليريك موديل 1", "callback": "haram_akerik_m1", "image": "path/to/haram_akerik_m1.jpg", "description": "وصف هرم اكليريك موديل 1"},
            {"label": "هرم اكليريك موديل 2", "callback": "haram_akerik_m2", "image": "path/to/haram_akerik_m2.jpg", "description": "وصف هرم اكليريك موديل 2"}
        ]
    },
    {
        "label": "هرم مكتب معدن بديل", 
        "callback": "haram_metal", 
        "items": [
            {"label": "هرم معدن موديل 1", "callback": "haram_metal_m1", "image": "path/to/haram_metal_m1.jpg", "description": "وصف هرم معدن موديل 1"},
            {"label": "هرم معدن موديل 2", "callback": "haram_metal_m2", "image": "path/to/haram_metal_m2.jpg", "description": "وصف هرم معدن موديل 2"}
        ]
    },
    {
        "label": "هرم مكتب خشب", 
        "callback": "haram_khashab", 
        "items": [
            {"label": "هرم خشب موديل 1", "callback": "haram_khashab_m1", "image": "path/to/haram_khashab_m1.jpg", "description": "وصف هرم خشب موديل 1"},
            {"label": "هرم خشب موديل 2", "callback": "haram_khashab_m2", "image": "path/to/haram_khashab_m2.jpg", "description": "وصف هرم خشب موديل 2"}
        ]
    }
]

doro3_submenu = [
    {
        "label": "دروع اكليريك", 
        "callback": "doro3_akerik", 
        "items": [
            {"label": "درع اكليريك موديل 1", "callback": "doro3_akerik_m1", "image": "path/to/doro3_akerik_m1.jpg", "description": "وصف درع اكليريك موديل 1"},
            {"label": "درع اكليريك موديل 2", "callback": "doro3_akerik_m2", "image": "path/to/doro3_akerik_m2.jpg", "description": "وصف درع اكليريك موديل 2"}
        ]
    },
    {
        "label": "دروع معدن بديل", 
        "callback": "doro3_metal", 
        "items": [
            {"label": "درع معدن موديل 1", "callback": "doro3_metal_m1", "image": "path/to/doro3_metal_m1.jpg", "description": "وصف درع معدن موديل 1"},
            {"label": "درع معدن موديل 2", "callback": "doro3_metal_m2", "image": "path/to/doro3_metal_m2.jpg", "description": "وصف درع معدن موديل 2"}
        ]
    },
    {
        "label": "دروع قطيفة", 
        "callback": "doro3_qatifah", 
        "items": [
            {"label": "درع قطيفة موديل 1", "callback": "doro3_qatifah_m1", "image": "path/to/doro3_qatifah_m1.jpg", "description": "وصف درع قطيفة موديل 1"},
            {"label": "درع قطيفة موديل 2", "callback": "doro3_qatifah_m2", "image": "path/to/doro3_qatifah_m2.jpg", "description": "وصف درع قطيفة موديل 2"}
        ]
    },
    {
        "label": "دروع خشب", 
        "callback": "doro3_khashab", 
        "items": [
            {"label": "درع خشب موديل 1", "callback": "doro3_khashab_m1", "image": "path/to/doro3_khashab_m1.jpg", "description": "وصف درع خشب موديل 1"},
            {"label": "درع خشب موديل 2", "callback": "doro3_khashab_m2", "image": "path/to/doro3_khashab_m2.jpg", "description": "وصف درع خشب موديل 2"}
        ]
    }
]

aqlam_submenu = [
    {
        "label": "قلم تاتش معدن", 
        "callback": "aqlam_metal", 
        "items": [
            {"label": "قلم معدن موديل 1", "callback": "aqlam_metal_m1", "image": "path/to/aqlam_metal_m1.jpg", "description": "وصف قلم معدن موديل 1"},
            {"label": "قلم معدن موديل 2", "callback": "aqlam_metal_m2", "image": "path/to/aqlam_metal_m2.jpg", "description": "وصف قلم معدن موديل 2"}
        ]
    },
    {
        "label": "قلم تاتش مضئ", 
        "callback": "aqlam_luminous", 
        "items": [
            {"label": "قلم مضئ موديل 1", "callback": "aqlam_luminous_m1", "image": "path/to/aqlam_luminous_m1.jpg", "description": "وصف قلم مضئ موديل 1"},
            {"label": "قلم مضئ موديل 2", "callback": "aqlam_luminous_m2", "image": "path/to/aqlam_luminous_m2.jpg", "description": "وصف قلم مضئ موديل 2"}
        ]
    }
]

mugat_submenu = [
    {
        "label": "مج ابيض", 
        "callback": "mugat_white", 
        "items": [
            {"label": "مج ابيض موديل 1", "callback": "mugat_white_m1", "image": "path/to/mugat_white_m1.jpg", "description": "وصف مج ابيض موديل 1"},
            {"label": "مج ابيض موديل 2", "callback": "mugat_white_m2", "image": "path/to/mugat_white_m2.jpg", "description": "وصف مج ابيض موديل 2"}
        ]
    },
    {
        "label": "مج سحري", 
        "callback": "mugat_magic", 
        "items": [
            {"label": "مج سحري موديل 1", "callback": "mugat_magic_m1", "image": "path/to/mugat_magic_m1.jpg", "description": "وصف مج سحري موديل 1"},
            {"label": "مج سحري موديل 2", "callback": "mugat_magic_m2", "image": "path/to/mugat_magic_m2.jpg", "description": "وصف مج سحري موديل 2"}
        ]
    },
    {
        "label": "مج ديجتال", 
        "callback": "mugat_digital", 
        "items": [
            {"label": "مج ديجتال موديل 1", "callback": "mugat_digital_m1", "image": "path/to/mugat_digital_m1.jpg", "description": "وصف مج ديجتال موديل 1"},
            {"label": "مج ديجتال موديل 2", "callback": "mugat_digital_m2", "image": "path/to/mugat_digital_m2.jpg", "description": "وصف مج ديجتال موديل 2"}
        ]
    }
]

main_menu = [
    {"label": "💍💍 صواني شبكة", "callback": "sawany"},
    {"label": "💍 طارات خطوبة وكتب الكتاب", "callback": "taarat"},
    {"label": "✋ بصامات", "callback": "bsamat"},
    {"label": "📜 مناديل كتب الكتاب", "callback": "wedding_tissues"},
    {"label": "🗄️ هرم مكتب", "callback": "haram"},
    {"label": "🏆 دروع", "callback": "doro3"},
    {"label": "💡 اباجورات", "callback": "abajorat"},
    {"label": "✏️ اقلام", "callback": "aqlam"},
    {"label": "☕ مجات", "callback": "mugat"},
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"},
    {"label": "🖨️ مستلزمات سبلميشن", "callback": "sublimation"}
]

product_to_submenu_map = {}
all_submenus = {
    "sawany": sawany_submenu,
    "taarat": taarat_submenu,
    "haram": haram_submenu,
    "doro3": doro3_submenu,
    "aqlam": aqlam_submenu,
    "mugat": mugat_submenu
}
for menu_key, submenu_list in all_submenus.items():
    for item in submenu_list:
        product_to_submenu_map[item["callback"]] = menu_key
        # 💡 نضمن إضافة كل عنصر فرعي لضمان عمل زر الشراء بشكل سليم
        if 'items' in item:
            for sub_item in item['items']:
                product_to_submenu_map[sub_item["callback"]] = menu_key
# -----------------------------------------------------------


# --------------------
# 2. الدوال المساعدة 
# --------------------
def start(update, context):
    query = update.callback_query
    if query:
        query.answer()
    
    user_name = update.effective_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختر طلبك من القائمة:"
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in main_menu]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query:
        try:
            query.message.delete()
        except Exception:
            pass 
        
        update.effective_chat.send_message(greeting_text, reply_markup=reply_markup)
    else:
        update.effective_message.reply_text(greeting_text, reply_markup=reply_markup)

def show_submenu(update, context, submenu, title):
    query = update.callback_query
    
    if query:
        query.answer()
        
        try:
            query.message.delete()
        except Exception:
            pass 
        
    keyboard = [[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in submenu]
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # تم تعديل هذا السطر لعرض رسالة "حدد اختيارك"
    update.effective_chat.send_message("حدد اختيارك:", reply_markup=reply_markup)


def show_product_page(update, product_callback_data, product_data):
    query = update.callback_query
    if query:
        query.answer()

    # نحصل على مفتاح القائمة الفرعية الأم لزر الرجوع
    previous_submenu_key = product_to_submenu_map.get(product_callback_data, "main_menu")

    # تحديد المنتجات سواء كانت حزمة أو منتج واحد
    products_to_show = []
    if 'items' in product_data:
        # إذا كانت حزمة، نستخدم الـ items
        products_to_show = product_data['items']
        # نحذف رسالة القائمة السابقة
        if query and query.message:
            try:
                query.message.delete()
            except Exception:
                pass 
    else:
        # إذا كان منتج واحد، نستخدم بياناته
        products_to_show = [product_data]
        # نحذف رسالة القائمة السابقة
        if query and query.message:
            try:
                query.message.delete()
            except Exception:
                pass
    
    # 1. إرسال المنتجات كرسائل منفصلة (صورة + وصف + زر شراء)
    for i, item in enumerate(products_to_show):
        # بناء لوحة المفاتيح للمنتج الحالي (زر شراء فقط)
        item_keyboard = [[InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{item['callback']}")]]
        item_reply_markup = InlineKeyboardMarkup(item_keyboard)
        
        # إرسال صورة ووصف المنتج
        update.effective_message.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=item['image'],
            caption=f"**{item['label']}**\n\n{item['description']}",
            reply_markup=item_reply_markup,
            parse_mode="Markdown"
        )
    
    # 2. إرسال زر الرجوع في رسالة منفصلة أخيرة (في نهاية العرض)
    # نستخدم callback القائمة الأم للرجوع إلى القائمة الفرعية الصحيحة
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=previous_submenu_key)]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
            
    update.effective_message.bot.send_message(
        chat_id=update.effective_chat.id,
        text="اضغط للرجوع إلى القائمة الفرعية:",
        reply_markup=back_reply_markup
    )


def button(update, context):
    query = update.callback_query
    data = query.data

    # 1. حالة العودة للقائمة الرئيسية أو الفرعية
    if data == "main_menu":
        start(update, context)
        return
    if data in all_submenus:
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        clean_title = title.split()[-1] 
        show_submenu(update, context, all_submenus[data], clean_title)
        return

    # 2. إذا اختير منتج معين (سواء كان حزمة أو مفرد)
    for submenu_key, submenu in all_submenus.items():
        for item in submenu:
            if data == item["callback"]:
                # إرسال كائن المنتج كاملاً
                show_product_page(update, item["callback"], item)
                return
            # فحص إذا كان العنصر هو منتج فرعي داخل حزمة (لم يعد يحدث هذا بعد الهيكلة الجديدة)
            if 'items' in item:
                for sub_item in item['items']:
                    if data == sub_item["callback"]:
                        # إذا كان زر الشراء تم الضغط عليه من منتج داخل حزمة
                        # يجب أن نرجع مفتاح القائمة الأم (item["callback"])
                        # لكن هنا نعتبر أن الـ callback_data الذي ليس 'buy_' هو فقط للأزرار الرئيسية في القوائم الفرعية
                        # ولذلك نعتمد على الحالة أعلاه `if data == item["callback"]:`
                        pass
    
    # 3. حالة زر الشراء (رابط واتساب مع رابط الصورة)
    if data.startswith("buy_"):
        product_key = data.replace("buy_", "")
        
        # البحث عن بيانات المنتج سواء كان مفرداً أو داخل حزمة
        product_data = None
        for submenu in all_submenus.values():
            for item in submenu:
                # إذا كان منتجاً مفرداً
                if item.get("callback") == product_key:
                    product_data = item
                    break
                # إذا كان منتجاً داخل حزمة
                if 'items' in item:
                    for sub_item in item['items']:
                        if sub_item.get("callback") == product_key:
                            product_data = sub_item
                            break
            if product_data:
                break
        
        if not product_data:
            query.answer(text="عذراً، لم يتم العثور على بيانات المنتج.", show_alert=True)
            return
            
        user_info = query.from_user
        
        # تكوين نص الرسالة الذي سيُفتح في واتساب
        message_body = (
            f"🔔 *طلب شراء جديد من بوت تليجرام* 🔔\n"
            f"المنتج: {product_data['label']}\n"
            f"الكود: {product_key}\n"
            f"العميل: {user_info.first_name}\n"
            f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
            f"🔗 رابط صورة المنتج: {product_data['image']}\n" 
            f"رابط التواصل عبر تليجرام: tg://user?id={user_info.id}"
        )
        
        # ترميز النص للرابط (URL Encoding)
        encoded_text = quote_plus(message_body)
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
        
        query.answer(text="سيتم فتح تطبيق واتساب الآن لإرسال الطلب.", show_alert=False)

        # إرسال رسالة جديدة تحتوي على زر الواتساب
        keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # نحذف رسالة الصورة القديمة ونرسل رسالة نصية جديدة
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
# 3. إعداد البوت 
# --------------------
def main():
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN) في بيئة العمل. يرجى التأكد من تعيينه.")
        return
    
    if WHATSAPP_NUMBER == "201288846355":
        print("⚠️ يرجى استبدال WHATSAPP_NUMBER برقمك الحقيقي.")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()