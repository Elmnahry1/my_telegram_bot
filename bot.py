import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
from urllib.parse import quote_plus # 💡 تم إضافة هذه المكتبة

# ⚠️ إعدادات الواتساب: استبدل بالرقم الخاص بك (كود الدولة + الرقم بدون علامة +)
WHATSAPP_NUMBER = "201288846355" 

# --------------------
# 1. بيانات القوائم والمنتجات (لا تغيير)
# --------------------
sawany_submenu = [
    {"label": "صواني شبكة اكليريك", "callback": "sawany_akerik", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف صواني شبكة اكليريك"},
    {"label": "صواني شبكة خشب", "callback": "sawany_khashab", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف صواني شبكة خشب"}
]

taarat_submenu = [
    {"label": "طارات اكليريك", "callback": "taarat_akerik", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارات اكليريك"},
    {"label": "طارات خشب", "callback": "taarat_khashab", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارات خشب"}
]

haram_submenu = [
    {"label": "هرم مكتب اكليريك", "callback": "haram_akerik", "image": "path/to/haram_akerik.jpg", "description": "وصف هرم مكتب اكليريك"},
    {"label": "هرم مكتب معدن بديل", "callback": "haram_metal", "image": "path/to/haram_metal.jpg", "description": "وصف هرم مكتب معدن بديل"},
    {"label": "هرم مكتب خشب", "callback": "haram_khashab", "image": "path/to/haram_khashab.jpg", "description": "وصف هرم مكتب خشب"}
]

doro3_submenu = [
    {"label": "دروع اكليريك", "callback": "doro3_akerik", "image": "path/to/doro3_akerik.jpg", "description": "وصف دروع اكليريك"},
    {"label": "دروع معدن بديل", "callback": "doro3_metal", "image": "path/to/doro3_metal.jpg", "description": "وصف دروع معدن بديل"},
    {"label": "دروع قطيفة", "callback": "doro3_qatifah", "image": "path/to/doro3_qatifah.jpg", "description": "وصف دروع قطيفة"},
    {"label": "دروع خشب", "callback": "doro3_khashab", "image": "path/to/doro3_khashab.jpg", "description": "وصف دروع خشب"}
]

aqlam_submenu = [
    {"label": "قلم تاتش معدن", "callback": "aqlam_metal", "image": "path/to/aqlam_metal.jpg", "description": "وصف قلم تاتش معدن"},
    {"label": "قلم تاتش مضئ", "callback": "aqlam_luminous", "image": "path/to/aqlam_luminous.jpg", "description": "وصف قلم تاتش مضئ"}
]

mugat_submenu = [
    {"label": "مج ابيض", "callback": "mugat_white", "image": "path/to/mugat_white.jpg", "description": "وصف مج ابيض"},
    {"label": "مج سحري", "callback": "mugat_magic", "image": "path/to/mugat_magic.jpg", "description": "وصف مج سحري"},
    {"label": "مج ديجتال", "callback": "mugat_digital", "image": "path/to/mugat_digital.jpg", "description": "وصف مج ديجتال"}
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

    update.effective_chat.send_message(f"اختر {title}:", reply_markup=reply_markup)


def show_product_page(update, product_callback_data, image_url, description):
    query = update.callback_query
    if query:
        query.answer()

    previous_submenu_key = product_to_submenu_map.get(product_callback_data, "main_menu")

    # زر الشراء أصبح Inline Button عادي
    keyboard = [
        [InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{product_callback_data}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=previous_submenu_key)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # نحذف الرسالة السابقة (القائمة الفرعية)
    if query and query.message:
        try:
            query.message.delete()
        except Exception:
            pass
        
    update.effective_message.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_url,
        caption=f"**{product_callback_data.replace('_', ' ').title()}**\n\n{description}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
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

    # 2. إذا اختير منتج معين
    for submenu_key, submenu in all_submenus.items():
        for item in submenu:
            if data == item["callback"]:
                show_product_page(update, item["callback"], item["image"], item["description"])
                return
    
    # 3. حالة زر الشراء (الآلية الجديدة: رابط واتساب)
    if data.startswith("buy_"):
        product_key = data.replace("buy_", "")
        
        product_data = next((item for submenu in all_submenus.values() for item in submenu if item["callback"] == product_key), None)
        
        if not product_data:
            query.answer(text="عذراً، لم يتم العثور على بيانات المنتج.", show_alert=True)
            return
            
        user_info = query.from_user
        
        # 💡 تكوين نص الرسالة الذي سيُفتح في واتساب
        message_body = (
            f"🔔 *طلب شراء جديد من بوت تليجرام* 🔔\n"
            f"المنتج: {product_data['label']}\n"
            f"الكود: {product_key}\n"
            f"العميل: {user_info.first_name}\n"
            f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
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