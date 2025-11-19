import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات الواتساب: استبدل بالرقم الخاص بك
WHATSAPP_NUMBER = "201288846355" 
# 💡 يمكن تعيين التوكن هنا مباشرة إذا لم يتم تعيينه كمتغير بيئة
# TOKEN = "YOUR_BOT_TOKEN_HERE" 

# --------------------
# 1. تعريف حالات المحادثة
# --------------------

WAITING_FOR_IMAGE = 1   # انتظار إرفاق الصورة
ASK_FOR_NAMES = 2       # انتظار كتابة اسم العريس والعروسة
ASK_FOR_DATE = 3        # انتظار كتابة التاريخ

# ------------------------------------
# 2. الدوال الرئيسية والمساعدة
# ------------------------------------

def get_back_keyboard(callback_data):
    """ينشئ لوحة مفاتيح بـ زر "رجوع" للقائمة المحددة."""
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data=callback_data)]])

def start(update, context):
    """
    يرسل رسالة الترحيب ويعرض زر "ارسال شكل مختلف".
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
    
    
    # بناء لوحة المفاتيح بزر واحد فقط
    keyboard = [[InlineKeyboardButton("ارسال شكل مختلف 🖼️", callback_data="send_custom_design")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.effective_chat.send_message(
        greeting_text, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

def handle_callback_query(update, context):
    """
    تستقبل ضغطات الأزرار (Callback Queries) غير المرتبطة بالمحادثة.
    """
    query = update.callback_query
    data = query.data
    query.answer()
    
    if data == "main_menu":
        # العودة إلى دالة start للبدء من جديد
        start(update, context) 
        return ConversationHandler.END
        
    elif data == "send_custom_design":
        # بدء محادثة طلب الصورة
        return prompt_for_image(update, context) 

    return ConversationHandler.END 

# ------------------------------------
# 3. دوال معالجة الشكل المختلف (Custom Design Handlers)
# ------------------------------------

# --- دوال العرض ---
def ask_for_names_prompt(update, context):
    """يعرض رسالة طلب الأسماء."""
    text = (
        "✅ تم استلام الصورة بنجاح!\n\n"
        "**الخطوة الثانية:**\n"
        "يرجى كتابة **اسم العريس والعروسة** *معاً في رسالة واحدة* للمتابعة إلى الخطوة التالية."
    )
    reply_markup = get_back_keyboard("back_to_image_prompt")
    
    # تحديد مصدر التحديث (رسالة نصية أو callback)
    if update.callback_query:
        update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")

def ask_for_date_prompt(update, context):
    """يعرض رسالة طلب التاريخ."""
    text = (
        "✅ تم استلام الأسماء بنجاح!\n\n"
        "**الخطوة الثالثة:**\n"
        "يرجى كتابة **التاريخ** المطلوب حفره على التصميم للمتابعة."
    )
    reply_markup = get_back_keyboard("back_to_names_prompt")
    
    # تحديد مصدر التحديث (رسالة نصية أو callback)
    if update.callback_query:
        update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")


# --- دوال الاستلام والتنقل ---
def prompt_for_image(update, context):
    """الخطوة 0: تبدأ المحادثة وتطلب الصورة."""
    query = update.callback_query
    query.answer()
    
    context.user_data.clear() # مسح البيانات عند البدء
    
    try:
        query.message.delete()
    except Exception:
        pass
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]]
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="**الخطوة الأولى:**\nمن فضلك، **أرفق الصورة أو التصميم** الذي تود تنفيذه الآن.",
        reply_markup=InlineKeyboardMarkup(back_keyboard),
        parse_mode="Markdown"
    )
    
    return WAITING_FOR_IMAGE

def receive_photo_and_ask_names(update, context):
    """الخطوة 1: تستقبل الصورة وتنتقل لطلب الأسماء."""
    photo = update.message.photo[-1]
    file = context.bot.get_file(photo.file_id)
    
    # تخزين رابط الصورة والوصف (Caption) مؤقتاً
    context.user_data['photo_url'] = file.file_path
    context.user_data['caption'] = update.message.caption if update.message.caption else "لا يوجد وصف مرفق."
    
    # الانتقال إلى حالة طلب الأسماء
    ask_for_names_prompt(update, context)
    return ASK_FOR_NAMES

def receive_names_and_ask_date(update, context):
    """الخطوة 2: تستقبل الأسماء وتنتقل لطلب التاريخ."""
    # تخزين الأسماء مؤقتاً
    context.user_data['names'] = update.message.text
    
    # الانتقال إلى حالة طلب التاريخ
    ask_for_date_prompt(update, context)
    return ASK_FOR_DATE

def receive_date_and_send_whatsapp(update, context):
    """الخطوة 3: تستقبل التاريخ وتجمع البيانات وتجهز رابط الواتساب النهائي."""
    # تخزين التاريخ مؤقتاً
    context.user_data['date'] = update.message.text
    
    # تجميع البيانات
    user_info = update.message.from_user
    photo_url = context.user_data.get('photo_url', 'غير متوفر')
    caption = context.user_data.get('caption', 'لا يوجد')
    names = context.user_data.get('names', 'غير متوفر')
    date = context.user_data.get('date', 'غير متوفر')

    message_body = (
        f"🔔 *طلب تصميم شكل مختلف (Custom Design)* 🔔\n\n"
        f"اسم العريس والعروسة: *{names}*\n"
        f"التاريخ المطلوب: *{date}*\n\n"
        f"ملاحظات العميل المرفقة مع الصورة: {caption}\n"
        f"🔗 رابط الصورة (مؤقت من تليجرام): {photo_url}\n"
        f"اسم العميل: {user_info.first_name}...\n"
    )
    
    # إنشاء رابط الواتساب النهائي
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال طلب التصميم على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 العودة والبدء من جديد", callback_data="main_menu")]) 
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text=f"**✅ تم تجميع بياناتك بنجاح!**\n\nلإرسال الطلب النهائي إلى فريقنا عبر واتساب، اضغط على الزر التالي:", 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    context.user_data.clear()
    return ConversationHandler.END


# --- دوال الرجوع (Back Navigation) ---
def back_to_image_prompt(update, context):
    """الرجوع من خطوة الأسماء إلى خطوة إرفاق الصورة."""
    query = update.callback_query
    query.answer()
    
    # إعادة عرض رسالة طلب الصورة
    query.edit_message_text(
        text="**الخطوة الأولى:**\nمن فضلك، **أعد إرفاق الصورة أو التصميم** الذي تود تنفيذه الآن.",
        reply_markup=get_back_keyboard("main_menu"),
        parse_mode="Markdown"
    )
    
    context.user_data.pop('photo_url', None) # مسح الصورة المخزنة
    return WAITING_FOR_IMAGE

def back_to_names_prompt(update, context):
    """الرجوع من خطوة التاريخ إلى خطوة طلب الأسماء."""
    query = update.callback_query
    query.answer()
    
    # إعادة عرض رسالة طلب الأسماء
    query.edit_message_text(
        text="**الخطوة الثانية:**\nيرجى كتابة **اسم العريس والعروسة** *معاً في رسالة واحدة* للمتابعة إلى الخطوة التالية.",
        reply_markup=get_back_keyboard("back_to_image_prompt"),
        parse_mode="Markdown"
    )
    return ASK_FOR_NAMES

# --------------------
# 4. إعداد البوت (Main)
# --------------------
def main():
    
    # 💡 محاولة الحصول على التوكن من متغير البيئة (أو تعيينه يدوياً)
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN). يرجى تعيينه أو كتابته مباشرة.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    
    # مُعالج المحادثة متعدد الخطوات
    custom_design_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(prompt_for_image, pattern='^send_custom_design$')
        ],
        states={
            WAITING_FOR_IMAGE: [
                MessageHandler(Filters.photo & ~Filters.command, receive_photo_and_ask_names),
                MessageHandler((Filters.text | Filters.document) & ~Filters.command, 
                               lambda update, context: update.message.reply_text("من فضلك، يجب إرفاق **صورة** التصميم المطلوب فقط للمتابعة.", parse_mode="Markdown")),
            ],
            
            ASK_FOR_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, receive_names_and_ask_date),
            ],
            
            ASK_FOR_DATE: [
                MessageHandler(Filters.text & ~Filters.command, receive_date_and_send_whatsapp),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(back_to_image_prompt, pattern='^back_to_image_prompt$'),
            CallbackQueryHandler(back_to_names_prompt, pattern='^back_to_names_prompt$'),
            CallbackQueryHandler(start, pattern='^main_menu$'),
            CommandHandler('start', start),
        ]
    )

    dp.add_handler(custom_design_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_callback_query))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()