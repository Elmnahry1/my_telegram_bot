import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات الواتساب: استبدل بالرقم الخاص بك (كود الدولة + الرقم بدون علامة +)
WHATSAPP_NUMBER = "201288846355" 

# --------------------
# 1. بيانات القوائم والمنتجات
# --------------------

# --- تعريف حالات المحادثة للمنتجات المخصصة ---
GET_NAME = 1 

# تعريف القوائم الفرعية (لضمان عمل الكود)
bsamat_submenu = [
    {"label": "بصامة موديل 1", "callback": "bsamat_m1", "image": "https://example.com/bsamat1.png", "description": "وصف البصامة موديل 1."},
    {"label": "بصامة موديل 2", "callback": "bsamat_m2", "image": "https://example.com/bsamat2.png", "description": "وصف البصامة موديل 2."}
]
wedding_tissues_submenu = [
    {"label": "منديل موديل 1", "callback": "tissue_m1", "image": "https://example.com/tissue1.png", "description": "وصف منديل كتب الكتاب موديل 1."},
    {"label": "منديل موديل 2", "callback": "tissue_m2", "image": "https://example.com/tissue2.png", "description": "وصف منديل كتب الكتاب موديل 2."}
]
abajorat_submenu = [
    {"label": "أباجورة موديل 1", "callback": "abajora_m1", "image": "https://example.com/abajora1.png", "description": "وصف الأباجورة موديل 1."},
    {"label": "أباجورة موديل 2", "callback": "abajora_m2", "image": "https://example.com/abajora2.png", "description": "وصف الأباجورة موديل 2."}
]

# قائمة المحافظ (مهمة لتحديد اللون)
engraved_wallet_submenu = [
    {"label": "محفظة لون بيج (هافان)", "callback": "wallet_bege", "image": "https://example.com/wallet_bege.png", "description": "محفظة جلد رجالي، لون بيج (هافان)."},
    {"label": "محفظة لون بني", "callback": "wallet_brown", "image": "https://example.com/wallet_brown.png", "description": "محفظة جلد رجالي، لون بني."},
    {"label": "محفظة لون اسود", "callback": "wallet_black", "image": "https://example.com/wallet_black.png", "description": "محفظة جلد رجالي، لون أسود."}
]

# تم اختصار باقي القوائم مثل sawany_submenu, taarat_submenu, ... إلخ
# يجب أن تكون موجودة في الكود الفعلي. سنستخدم قائمة واحدة تمثيلية للمنتجات المعقدة
sawany_submenu = [
    {
        "label": "صواني شبكة اكليريك", 
        "callback": "sawany_akerik", 
        "items": [ 
            {"label": "صينية اكليريك موديل 1", "callback": "akerik_m1", "image": "https://example.com/sawany1.png", "description": "صينية اكليريك: وصف المنتج الأول."},
            {"label": "صينية اكليريك موديل 2", "callback": "akerik_m2", "image": "https://example.com/sawany2.png", "description": "صينية اكليريك: وصف المنتج الثاني."}
        ]
    }
]

main_menu = [
    {"label": "💍💍 صواني شبكة", "callback": "sawany"},
    {"label": "👝 محافظ محفورة بالاسم", "callback": "engraved_wallet"},
    {"label": "✋ بصامات", "callback": "bsamat"}, 
    {"label": "💡 اباجورات", "callback": "abajorat"}, 
    {"label": "📜 مناديل كتب الكتاب", "callback": "wedding_tissues"}, 
    # ... (باقي القائمة الرئيسية)
]

all_submenus = {
    "sawany": sawany_submenu,
    "bsamat": bsamat_submenu, 
    "wedding_tissues": wedding_tissues_submenu, 
    "abajorat": abajorat_submenu,
    "engraved_wallet": engraved_wallet_submenu,
    # ... (باقي القوائم)
}

# بناء خريطة المنتجات
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet"]:
        for product in submenu_list:
            product_to_submenu_map[product["callback"]] = menu_key
    else:
        for item in submenu_list:
            product_to_submenu_map[item["callback"]] = menu_key
            if 'items' in item:
                for sub_item in item['items']:
                    product_to_submenu_map[sub_item["callback"]] = menu_key


# --------------------
# 2. الدوال المساعدة 
# --------------------

# دالة start ودالة show_submenu ودالة show_product_page
# تظل كما هي (لم يتم تضمينها للاختصار)

def start(update, context):
    if update.callback_query and context.user_data.get('state') == GET_NAME:
        context.user_data.clear()
        context.user_data['state'] = None

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
    
    return ConversationHandler.END


# 💡 دالة معالجة اختيار اللون (تبدأ المحادثة)
def prompt_for_name(update, context):
    query = update.callback_query
    data = query.data
    query.answer()
    
    selected_wallet_data = next((item for item in engraved_wallet_submenu if item["callback"] == data), None)
    context.user_data['wallet_data'] = selected_wallet_data
    context.user_data['state'] = GET_NAME

    try:
        query.message.delete()
    except Exception:
        pass

    update.effective_chat.send_message(
        text=f"اختيارك: **{selected_wallet_data['label']}**.\n\nمن فضلك، **اكتب الاسم الذي تريد حفره** على المحفظة الآن:",
        parse_mode="Markdown"
    )
    
    return GET_NAME 

# 🛑 الدالة المُعدَّلة: لمعالجة رسالة الاسم المُدخل وإرسال الطلب (للمحافظ المحفورة)
def receive_name_and_prepare_whatsapp(update, context):
    engraving_name = update.message.text
    product_data = context.user_data.get('wallet_data')
    
    if not product_data:
        update.effective_chat.send_message("عفواً، حدث خطأ في استرجاع بيانات المنتج. يرجى البدء من القائمة الرئيسية.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]))
        context.user_data.clear()
        return ConversationHandler.END

    # استرجاع بيانات العميل
    user_info = update.message.from_user
    
    # محاولة استخلاص اللون من اسم المنتج
    product_label = product_data['label']
    try:
        # إذا كان الليبل "محفظة لون بيج (هافان)"، نستخلص "بيج (هافان)"
        color = product_label.split(' ', 2)[2].strip() 
        wallet_type = "محفظة جلد رجالي" # نوع المنتج الأساسي
    except IndexError:
        color = product_label
        wallet_type = product_label

    # 💡 تكوين نص الرسالة الذي سيُفتح في واتساب - (للمحافظ المحفورة)
    message_body = (
        f"🔔 *طلب شراء جديد (محافظ محفورة بالاسم)* 🔔\n\n"
        f"المنتج: {wallet_type}\n"
        f"اللون: {color}\n" # حقل اللون
        f" الاسم المطلوب حفره: *{engraving_name}*\n" # حقل الحفر
        f"الكود: {product_data['callback']}\n\n"

        f"اسم العميل: {user_info.first_name} {user_info.last_name if user_info.last_name else ''}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط صورة المنتج: {product_data['image']}\n"
        f"رابط التواصل عبر التليجرام: tg://user?id={user_info.id}"
    )
    
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]) 
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text=f"شكراً لك! سيتم حفر اسم **{engraving_name}** على محفظة **{product_data['label']}**.\n\nلإتمام الطلب، اضغط على الزر التالي:", 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    context.user_data.clear()
    return ConversationHandler.END

# 🛑 الدالة المُعدَّلة: لمعالجة جميع ضغطات الأزرار
def button(update, context):
    query = update.callback_query
    data = query.data

    if data == "main_menu":
        start(update, context)
        return ConversationHandler.END

    if data == "engraved_wallet":
        show_submenu(update, context, engraved_wallet_submenu, "محافظ محفورة بالاسم")
        return ConversationHandler.END 
    
    if data in [item["callback"] for item in engraved_wallet_submenu]:
        return # سيتم معالجتها بواسطة ConversationHandler

    # (منطق عرض القوائم الفرعية والمنتجات كما هو)
    # ...
    
    # 🛑 حالة زر الشراء (المنتجات العادية - تم التأكيد على بيانات العميل)
    if data.startswith("buy_"):
        product_key = data.replace("buy_", "")
        product_data = None
        
        # منطق البحث عن بيانات المنتج 
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
        
        if not product_data:
            query.answer(text="عذراً، لم يتم العثور على بيانات المنتج.", show_alert=True)
            return ConversationHandler.END
            
        # استرجاع بيانات العميل
        user_info = query.from_user
        
        # 💡 تكوين نص الرسالة الذي سيُفتح في واتساب - (المنتجات العادية)
        message_body = (
            f"🔔 *طلب شراء جديد* 🔔\n\n"
            f"المنتج: {product_data['label']}\n"
            f"الكود: {product_key}\n\n"

            f"اسم العميل: {user_info.first_name} {user_info.last_name if user_info.last_name else ''}\n"
            f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
            f"🔗 رابط صورة المنتج: {product_data['image']}\n" 
            f"رابط التواصل عبر التليجرام: tg://user?id={user_info.id}"
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
        
        return ConversationHandler.END

    return ConversationHandler.END

# --------------------
# 3. إعداد البوت 
# --------------------
def main():
    # يجب تعيين التوكن في بيئة التشغيل
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN) في بيئة العمل. يرجى التأكد من تعيينه.")
        return
    
    if WHATSAPP_NUMBER == "201288846355":
        print("⚠️ يرجى استبدال WHATSAPP_NUMBER برقمك الحقيقي.")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # تعريف مُعالج المحادثة لـ "محافظ محفورة بالاسم"
    engraved_wallet_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                prompt_for_name, 
                pattern='^(' + '|'.join([item['callback'] for item in engraved_wallet_submenu]) + ')$'
            )
        ],
        states={
            GET_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_name_and_prepare_whatsapp)],
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(button) 
        ]
    )

    # إضافة مُعالج المحادثة أولاً
    dp.add_handler(engraved_wallet_handler)
    
    # إضافة معالجات الأوامر والأزرار الأخرى
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button)) 

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()