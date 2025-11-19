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

GET_WALLET_NAME = 1 
GET_PEN_NAME = 2    
WAITING_FOR_IMAGE = 3 # 💡 حالة جديدة لانتظار الصورة

# --------------------
# 2. بيانات القوائم (نحتفظ بها كما هي للرجوع إليها)
# --------------------

# (جميع القوائم مثل bsamat_submenu, aqlam_submenu, main_menu إلخ... تبقى كما هي)
# ...

# --------------------
# 3. الدوال الرئيسية والمساعدة
# --------------------

def start(update, context):
    query = update.callback_query
    # إنهاء أي محادثة جارية عند استخدام /start 
    if context.user_data.get('state') in [GET_WALLET_NAME, GET_PEN_NAME, WAITING_FOR_IMAGE]:
        context.user_data.clear()
        context.user_data['state'] = None
        
    if query:
        query.answer()
        try:
            query.message.delete()
        except Exception:
            pass 
    
    user_name = update.effective_user.first_name
    greeting_text = f"✅ مرحباً بك {user_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر...\n\nمن فضلك اختر طلبك من القائمة:"
    
    # 💡 إضافة زر "ارسال شكل مختلف"
    keyboard = [[InlineKeyboardButton("ارسال شكل مختلف 🖼️", callback_data="send_custom_design")]]
    keyboard.extend([[InlineKeyboardButton(item["label"], callback_data=item["callback"])] for item in main_menu])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.effective_chat.send_message(greeting_text, reply_markup=reply_markup)
    
    # يجب أن تكون هذه الدالة غير منتهية إذا كانت ستُستخدم كـ fallback في ConversationHandler
    return ConversationHandler.END


# ------------------------------------
# دوال معالجة الشكل المختلف (Custom Design Handlers)
# ------------------------------------

def prompt_for_image(update, context):
    query = update.callback_query
    query.answer()

    # حذف الرسالة السابقة وعرض رسالة طلب الصورة
    try:
        query.message.delete()
    except Exception:
        pass
        
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="من فضلك، **أرفق الصورة أو التصميم** الذي تود تنفيذه الآن.\n\n"
             "سيتم إرسال الصورة مباشرةً إلينا على الواتساب.",
        reply_markup=back_reply_markup,
        parse_mode="Markdown"
    )
    
    # الدخول إلى حالة انتظار الصورة
    return WAITING_FOR_IMAGE

def receive_photo_and_prepare_whatsapp(update, context):
    # 💡 هذه الدالة تستقبل أي رسالة تحتوي على صورة (Photo)
    
    user_info = update.message.from_user
    
    # نحصل على أكبر نسخة من الصورة المرفقة
    photo = update.message.photo[-1]
    
    # نطلب من تليجرام رابط مباشر لتحميل الصورة
    file = context.bot.get_file(photo.file_id)
    photo_url = file.file_path
    
    # نحصل على أي كابشن (وصف) كتبه العميل مع الصورة
    caption = update.message.caption if update.message.caption else "لا يوجد وصف مرفق بالصورة."

    message_body = (
        f"🔔 *طلب تصميم شكل مختلف (Custom Design)* 🔔\n\n"
        f"مرفق صورة للتصميم المطلوب:\n"
        f"التعليق المرفق مع الصورة: *{caption}*\n\n"
        f"اسم العميل: {user_info.first_name} {user_info.last_name if user_info.last_name else ''}\n"
        f"اليوزر: @{user_info.username if user_info.username else 'غير متوفر'}\n"
        f"🔗 رابط الصورة (مؤقت من تليجرام): {photo_url}\n"
        f"رابط التواصل عبر التليجرام: tg://user?id={user_info.id}"
    )
    
    # تشفير الرسالة لواتساب
    encoded_text = quote_plus(message_body)
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
    
    keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال طلب التصميم على واتساب", url=wa_link)]]
    keyboard.append([InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]) 
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text=f"شكراً لك! تم استلام الصورة.\n\nلإرسالها وتأكيد الطلب عبر واتساب، اضغط على الزر التالي:", 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    context.user_data.clear()
    return ConversationHandler.END

def cancel_image_upload(update, context):
    # وظيفة الرجوع من حالة انتظار الصورة
    query = update.callback_query
    query.answer()
    
    try:
        query.message.delete()
    except Exception:
        pass 

    context.user_data.clear()
    return start(update, context) # العودة للقائمة الرئيسية

# ------------------------------------
# الدالة الرئيسية لمعالجة ضغطات الأزرار
# ------------------------------------
def button(update, context):
    # ... (باقي منطق دالة button لمعالجة الأزرار الأخرى) ...
    # ...
    
    query = update.callback_query
    data = query.data

    # 1. حالة العودة للقائمة الرئيسية
    if data == "main_menu":
        start(update, context)
        return ConversationHandler.END # إنهاء أي محادثة جارية

    # 💡 2. معالجة زر "ارسال شكل مختلف"
    if data == "send_custom_design":
        return prompt_for_image(update, context)
        
    # ... (باقي منطق معالجة الأزرار الأخرى مثل المحافظ والأقلام والمنتجات العادية)
    
    # إذا لم يكن الزر هو "send_custom_design"، أكمل معالجة باقي الأزرار 
    # (يجب أن يتم وضع هذا المنطق في مكانه الصحيح بالملف الكامل)
    
    # مثال بسيط لمنع الكود من الانهيار إذا لم يكن هناك منطق آخر
    query.answer(text="تم الضغط على زر آخر.", show_alert=False) 
    return ConversationHandler.END


# --------------------
# 4. إعداد البوت 
# --------------------
def main():
    # 💡 افترض أن لديك توكن معرف في البيئة أو متغير
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN).")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    
    # 1. مُعالج المحادثة لـ "إرسال شكل مختلف"
    custom_design_handler = ConversationHandler(
        entry_points=[
            # يتم بدء المحادثة عن طريق زر "ارسال شكل مختلف"
            CallbackQueryHandler(prompt_for_image, pattern='^send_custom_design$')
        ],
        states={
            WAITING_FOR_IMAGE: [
                # يستقبل أي رسالة تحتوي على صورة
                MessageHandler(Filters.photo & ~Filters.command, receive_photo_and_prepare_whatsapp),
                # يتجاهل الرسائل النصية ويطالب العميل بإرسال صورة
                MessageHandler(Filters.text & ~Filters.command, lambda update, context: update.message.reply_text("من فضلك، أرفق الصورة المطلوبة (ملف صورة).")),
            ],
        },
        fallbacks=[
            # معالجة زر الرجوع للقائمة الرئيسية
            CallbackQueryHandler(cancel_image_upload, pattern='^main_menu$'),
            CommandHandler('start', start),
        ]
    )

    # إضافة مُعالج إرسال الصورة
    dp.add_handler(custom_design_handler)
    
    # إضافة معالجات الأوامر والأزرار الأخرى (يجب دمجها مع handlers الأقلام والمحافظ)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    #os.environ["TOKEN"] = "YOUR_BOT_TOKEN_HERE" 
    main()