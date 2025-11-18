import os
import urllib.parse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# -------------------------
# مراحل المحادثة عند الشراء
# -------------------------
DETAILS = 1

# -------------------------
# الأقسام والصور
# -------------------------
sections = {
    "sawany": {"name": "صواني شبكة 💍", "images": ["https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"]},
    "taarat": {"name": "طارات خطوبة وكتب الكتاب 💍", "images": ["https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"]},
    "bsamat": {"name": "بصامات ✨", "images": ["https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"]},
    "menadeel": {"name": "مناديل كتب الكتاب ✨", "images": ["https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"]},
    "haram": {"name": "هرم مكتب 🏢", "images": ["https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"]},
    "doro3": {"name": "دروع 🏆", "images": ["https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"]},
    "abajorat": {"name": "اباجورات 💡", "images": ["https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"]},
    "aqlam": {"name": "اقلام ✏️", "images": ["https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"]},
    "mugat": {"name": "مجات ☕", "images": ["https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"]},
    "mahafez": {"name": "محافظ محفورة بالاسم ☕", "images": ["https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"]},
    "sublimation": {"name": "مستلزمات سبلميشن 🖼️", "images": ["https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png"]},
}

# -------------------------
# قائمة رئيسية
# -------------------------
def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    welcome_text = f"✅ مرحباً بك {user_name}!\nفي البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن.\n\nمن فضلك اختر طلبك من القائمة:"
    
    keyboard = []
    for key, val in sections.items():
        keyboard.append([InlineKeyboardButton(val["name"], callback_data=key)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup)
    else:
        update.message.reply_text(welcome_text, reply_markup=reply_markup)

# -------------------------
# إرسال الصور لكل قسم مع زر شراء وزر رجوع
# -------------------------
def send_section(update: Update, context: CallbackContext, section_key: str):
    query = update.callback_query
    query.answer()

    section = sections[section_key]

    # إرسال كل الصور كـ media group
    media = [InputMediaPhoto(url) for url in section["images"]]
    context.bot.send_media_group(chat_id=query.message.chat_id, media=media)

    # لكل قسم، أضف زر شراء + زر رجوع
    keyboard = [
        [InlineKeyboardButton("🛒 شراء", callback_data=f"buy_{section_key}")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=query.message.chat_id, text="اختر:", reply_markup=reply_markup)

# -------------------------
# التعامل مع الأزرار
# -------------------------
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    
    if data == "back":
        start(update, context)
        return

    if data.startswith("buy_"):
        section_key = data.replace("buy_", "")
        context.user_data['section'] = sections[section_key]["name"]
        query.message.reply_text(f"📝 من فضلك اكتب تفاصيل طلبك للـ {sections[section_key]['name']}: (كمية، ألوان، حجم ...)")
        return DETAILS
    
    if data in sections:
        send_section(update, context, data)

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

# -------------------------
# تشغيل البوت
# -------------------------
def main():
    TOKEN = os.getenv("TOKEN")  # تأكد أن المتغير موجود على Railway أو Render
    if not TOKEN:
        print("Error: TOKEN environment variable is not set.")
        return
    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={DETAILS: [MessageHandler(Filters.text & ~Filters.command, receive_details)]},
        fallbacks=[]
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
