import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات الواتساب: استبدل بالرقم الخاص بك
WHATSAPP_NUMBER = "201288846355" 

# --------------------
# 1. تعريف حالات المحادثة
# --------------------

WAITING_FOR_IMAGE = 1 # الحالة الوحيدة: انتظار الصورة

# ------------------------------------
# 2. الدوال الرئيسية
# ------------------------------------

def start(update, context):
    """
    يرسل رسالة الترحيب ويعرض زر "ارسال شكل مختلف".
    هذه هي نقطة الدخول للبوت.
    """
    query = update.callback_query
    
    # إنهاء أي محادثة سابقة وضبط الحالة
    context.user_data.clear()
        
    if query:
        query.answer()
        try:
            query.message.delete()
        except Exception:
            pass 
        
    user_name = update.effective_user.first_name if update.effective_user else "عميل"
    
    greeting_text = (
        f"✅ مرحباً بك {user_name} في خدمة طلبات التصميم الخاصة بنا.\n\n"
        "من فضلك، اضغط على الزر أدناه لبدء إرسال الصورة أو التصميم الذي تود تنفيذه."
    )
    
    # 💡 بناء لوحة المفاتيح بزر واحد فقط
    keyboard = [[InlineKeyboardButton("ارسال شكل مختلف 🖼️", callback_data="send_custom_design")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.effective_chat.send_message(
        greeting_text, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    # ننهي أي محادثة جارية عند /start
    return ConversationHandler.END


def prompt_for_image(update, context):
    """
    يبدأ المحادثة، يحذف الرسالة السابقة، ويطلب من العميل إرفاق الصورة.
    """
    query = update.callback_query
    query.answer()

    # حذف الرسالة السابقة
    try:
        query.message.delete()
    except Exception:
        pass
        
    # 💡 زر الرجوع
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="من فضلك، **أرفق الصورة أو التصميم** الذي تود تنفيذه الآن.\n\n"
             "سيتم إرسال رابط الصورة مباشرةً إلينا على الواتساب.",
        reply_markup=back_reply_markup,
        parse_mode="Markdown"
    )
    
    # الدخول إلى حالة انتظار الصورة
    return WAITING_FOR_IMAGE

def receive_photo_and_prepare_whatsapp(update, context):
    """
    تستقبل الصورة، تحصل على رابطها، وتجهز رسالة واتساب للعميل.
    """
    user_info = update.message.from_user
    
    # الحصول على أكبر نسخة من الصورة المرفقة
    photo = update.message.photo[-1]
    
    # الحصول على رابط الصورة المؤقت من تليجرام
    file = context.bot.get_file(photo.file_id)
    photo_url = file.file_path
    
    caption = update.message.caption if update.message.caption else "لا يوجد وصف مرفق بالصورة."

    message_body = (
        f"🔔 *طلب تصميم شكل مختلف (Custom Design)* 🔔\n\n"
        f"مرفق صورة للتصميم المطلوب.\n"
        f"التعليق المرفق: *{caption}*\n\n"
        f"🔗 رابط الصورة (مؤقت من تليجرام): {photo_url}\n"
        f"اسم العميل: {user_info.first_name} {user_info.last_name if user_info.last_name else ''}\n"
    )
    
    # تشفير الرسالة لواتساب
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    # 💡 لوحة المفاتيح لإتمام الطلب
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال طلب التصميم على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 العودة والبدء من جديد", callback_data="main_menu")]) 
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text=f"شكراً لك! تم استلام الصورة بنجاح.\n\nلإرسالها إلى فريقنا وتأكيد الطلب، اضغط على الزر التالي:", 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    context.user_data.clear()
    return ConversationHandler.END


def handle_callback_query(update, context):
    """
    تستقبل جميع ضغطات الأزرار (Callback Queries) وتوجهها.
    """
    query = update.callback_query
    data = query.data
    query.answer()
    
    if data == "main_menu":
        # العودة إلى دالة start للبدء من جديد
        return start(update, context) 
        
    elif data == "send_custom_design":
        # بدء محادثة طلب الصورة
        return prompt_for_image(update, context)


# --------------------
# 3. إعداد البوت
# --------------------
def main():
    # 💡 استبدل بتوكن البوت الخاص بك
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN). يرجى تعيينه أو كتابته مباشرة.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    
    # 1. مُعالج محادثة "ارسال شكل مختلف" (هو المعالج الوحيد الآن)
    custom_design_handler = ConversationHandler(
        entry_points=[
            # نقطة الدخول للمحادثة هي زر "send_custom_design"
            CallbackQueryHandler(prompt_for_image, pattern='^send_custom_design$')
        ],
        states={
            WAITING_FOR_IMAGE: [
                # يستقبل فقط الرسائل التي تحتوي على صور
                MessageHandler(Filters.photo & ~Filters.command, receive_photo_and_prepare_whatsapp),
                # إذا أرسل العميل نصاً أو أي شيء آخر، نطالبه بالصورة
                MessageHandler(Filters.all & ~Filters.command, lambda update, context: update.message.reply_text("من فضلك، يجب إرفاق **صورة** التصميم المطلوب فقط للمتابعة.", parse_mode="Markdown")),
            ],
        },
        fallbacks=[
            # يسمح بالعودة للقائمة الرئيسية في أي وقت أثناء انتظار الصورة
            CallbackQueryHandler(start, pattern='^main_menu$'),
            CommandHandler('start', start),
        ]
    )

    # 🛑 إضافة مُعالج المحادثة
    dp.add_handler(custom_design_handler)
    
    # 🛑 إضافة معالجات الأوامر والأزرار العامة
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_callback_query))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()