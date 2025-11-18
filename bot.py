import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# ---------------------------------------------------------
# القائمة الرئيسية
# ---------------------------------------------------------
def start(update, context):
    user_name = update.message.from_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختار طلبك من القائمة:"
    keyboard = [
        [InlineKeyboardButton("💍💍 صواني شبكة", callback_data='sawany')],
        [InlineKeyboardButton("💍 طارات خطوبة وكتب الكتاب", callback_data='taarat')],
        [InlineKeyboardButton("✋ بصامات", callback_data='bsamat')],
        [InlineKeyboardButton("📜 مناديل كتب الكتاب", callback_data='wedding_tissues')],
        [InlineKeyboardButton("🗄️ هرم مكتب", callback_data='haram')],
        [InlineKeyboardButton("🏆 دروع", callback_data='doro3')],
        [InlineKeyboardButton("💡 اباجورات", callback_data='abajorat')],
        [InlineKeyboardButton("✏️ اقلام", callback_data='aqlam')],
        [InlineKeyboardButton("☕ مجات", callback_data='mugat')],
        [InlineKeyboardButton("👝 محافظ محفورة بالاسم", callback_data='engraved_wallet')],
        [InlineKeyboardButton("🖨️ مستلزمات سبلميشن", callback_data='sublimation')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(greeting_text, reply_markup=reply_markup)

# ---------------------------------------------------------
# دالة إرسال الصور + زر الرجوع
# ---------------------------------------------------------
def send_photos(update, context, photos):
    query = update.callback_query
    query.answer()

    media = [InputMediaPhoto(p) for p in photos]
    context.bot.send_media_group(chat_id=query.message.chat_id, media=media)

    back_keyboard = [[InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    context.bot.send_message(chat_id=query.message.chat_id, text="اختار:", reply_markup=reply_markup)

# ---------------------------------------------------------
# التحكم في الأزرار
# ---------------------------------------------------------
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    
    if data == "back":
        start(update, context)
        return

    # روابط تجريبية للصور (حط الروابط الحقيقية بعدين)
    image_url = "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"

    if data == "sawany":
        send_photos(update, context, [image_url, image_url])
    elif data == "taarat":
        send_photos(update, context, [image_url])
    elif data == "bsamat":
        send_photos(update, context, [image_url])
    elif data == "haram":
        send_photos(update, context, [image_url])
    elif data == "doro3":
        send_photos(update, context, [image_url])
    elif data == "abajorat":
        send_photos(update, context, [image_url])
    elif data == "aqlam":
        send_photos(update, context, [image_url])
    elif data == "mugat":
        send_photos(update, context, [image_url])
    elif data == "sublimation":
        send_photos(update, context, [image_url])

# ---------------------------------------------------------
# التحكم في الأزرار
# ---------------------------------------------------------
def button_handler(update, context):
    query = update.callback_query
    data = query.data

    # رجوع للقائمة الرئيسية
    if data == "back":
        start(update, context)
        return

    if data.startswith("buy_"):
        section_key = data.replace("buy_", "")
        context.user_data['section'] = sections[section_key]["name"]
        query.message.reply_text(f"📝 من فضلك اكتب تفاصيل طلبك للـ {sections[section_key]['name']}: (كمية، ألوان، حجم ...)")
        return DETAILS
    
    if data in sections:
        send_photos(update, context, data)

    # معالجة الأقسام الرئيسية
    sections = {
        "sawany": ["صواني اكليريك", "صواني خشب"],
        "taarat": ["taarat_acrylic", "taarat_wood"],
        "bsamat": ["bsamat"],
        "wedding_tissues": ["wedding_tissues"],
        "haram": ["haram_acrylic", "haram_metal", "haram_wood"],
        "doro3": ["doro3_acrylic", "doro3_metal", "doro3_wood"],
        "abajorat": ["abajorat"],
        "aqlam": ["aqlam_touch_metal", "aqlam_touch_light"],
        "mugat": ["mugat_white", "mugat_magic", "mugat_digital"],
        "engraved_wallet": ["engraved_wallet"],
        "sublimation": ["sublimation"]
    }

    # إذا كان القسم يحتوي على أقسام فرعية
    if data in sections:
        subs = sections[data]
        keyboard = [[InlineKeyboardButton(sub.replace("_", " ").title(), callback_data=sub)] for sub in subs]
        keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"اختر القسم الفرعي:", reply_markup=reply_markup)
        return

    # إذا كان القسم فرعي أو منتجات مباشرة
    if data in products:
        send_product_photos(update, context, data)
        return

    # إذا كان الضغط على زر شراء
    if data.startswith("buy_"):
        parts = data.split("_")
        key = "_".join(parts[1:-1])
        idx = int(parts[-1])
        item = products[key][idx]
        phone_number = "201288846355"  # ضع رقم واتساب هنا مع كود الدولة بدون +
        text = f"طلب منتج من البوت:\nالمنتج: {key}\nالوصف: {item['description']}"
        wa_link = f"https://wa.me/{phone_number}?text={text}"
        query.answer(text="يتم فتح واتساب لإرسال الطلب", show_alert=True)
        query.bot.send_message(chat_id=query.message.chat_id, text=f"اضغط هنا لإرسال الطلب على واتساب:\n{wa_link}")

# -------------------------
# استقبال تفاصيل الطلب
# -------------------------
def receive_details(update: Update, context: CallbackContext):
    user_input = update.message.text
    section_name = context.user_data.get('section', 'عام')

    user_name = update.effective_user.first_name
    user_id = update.effective_user.id

    # رقم واتسابك بصيغة دولية
    YOUR_WHATSAPP_NUMBER = "201288846355"

    message_text = f"📌 طلب جديد من القسم {section_name}:\nاسم العميل: {user_name}\nرقم تيليجرام: {user_id}\nتفاصيل الطلب: {user_input}"
    encoded_message = urllib.parse.quote(message_text)
    whatsapp_link = f"https://wa.me/{YOUR_WHATSAPP_NUMBER}?text={encoded_message}"

    update.message.reply_text(f"✅ تم تجهيز طلبك!\nاضغط هنا لإرساله على واتساب:\n{whatsapp_link}")
    return ConversationHandler.END

# ---------------------------------------------------------
# تشغيل البوت
# ---------------------------------------------------------
def main():
    TOKEN = os.getenv("TOKEN")  # يجب أن يكون موجود كـ Environment Variable على Railway

    if not TOKEN:
        print("Error: TOKEN environment variable is not set.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
