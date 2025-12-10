import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. الإعدادات الأساسية ---

# استبدل هذا التوكن بالتوكن الخاص ببوتك
def main():
    TOKEN = os.environ.get('TOKEN') 
    if not TOKEN:
         print("Error: BOT_TOKEN environment variable is not set. Please set it or hardcode the token.")
         return
         
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

# إعداد السجل (لتتبع الأخطاء والأحداث في الكونسول)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- 2. بناء الأزرار (Reply Keyboard) ---

def build_reply_keyboard():
    """ينشئ لوحة المفاتيح المخصصة التي تظهر أسفل المحادثة."""
    
    # تعريف الأزرار
    button_buy = "💳 Buy | VIP 🛒"
    button_account = "👤 My Account"
    button_stats = "📊 Stats"
    button_support = "✉️ Support"
    button_language = "🌍 Language"
    
    # ترتيب الأزرار في صفوف
    row1 = [button_buy, button_account, button_stats]
    row2 = [button_support, button_language]

    # بناء اللوحة
    keyboard = [row1, row2]
    
    return ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True,      # لتغيير حجم الأزرار حسب الشاشة
        one_time_keyboard=False    # لإبقاء اللوحة ظاهرة دائماً
    )

# --- 3. مُعالِجات الأوامر (Handlers) ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """الاستجابة لأمر /start وإرسال لوحة المفاتيح."""
    
    reply_markup = build_reply_keyboard()
    
    await update.message.reply_text(
        "👋 أهلاً بك! يرجى اختيار أحد الأزرار الرئيسية أدناه:",
        reply_markup=reply_markup
    )

async def handle_keyboard_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """تستجيب لضغطات الأزرار (وهي نصوص عادية في هذه الحالة)."""
    
    text = update.message.text
    
    if text == "👤 My Account":
        # هنا ستضع الكود لجلب وعرض حالة الاشتراك، تاريخ الانتهاء، إلخ.
        await update.message.reply_text(
            "👤 معلومات الحساب:\n"
            "الحالة: عضو مجاني (Free Tier)\n"
            "للاشتراك في VIP، اضغط على زر 'Buy | VIP'."
        )
    
    elif text == "📊 Stats":
        # هنا ستضع الكود لجلب وعرض الإحصائيات (مثل الرسالة التي ظهرت في الصورة).
        # يمكن جلبها من قاعدة بيانات أو ملف.
        await update.message.reply_text(
            "📊 إحصائيات الأداء (آخر 7 أيام):\n"
            "* نسبة الربح الإجمالية: 4825.06%\n"
            "* إجمالي الصفقات: 75\n"
            "* الصفقات الفاشلة: 10"
        )
        
    elif text == "💳 Buy | VIP 🛒":
        # هنا سترسل رسالة تحتوي على رابط للدفع (عادةً يتم استخدام InlineKeyboard هنا).
        await update.message.reply_text(
            "💰 للاشتراك في خدمة الـ VIP، يرجى زيارة الرابط التالي للدفع الآمن:\n"
            "https://yourpaymentlink.com/vip"
        )
        
    elif text == "✉️ Support":
        await update.message.reply_text(
            "💬 يمكنك التواصل مع فريق الدعم على الرابط التالي: @YourAdminUsername"
        )

    elif text == "🌍 Language":
        await update.message.reply_text(
            "🌍 يرجى اختيار اللغة المفضلة (هنا تحتاج لإضافة Inline Keyboard لخيارات اللغة):"
        )

    else:
        # التعامل مع أي نص آخر لم يطابق الأزرار
        await update.message.reply_text("👋 رسالة غير مفهومة. يرجى استخدام الأزرار في الأسفل.")

# --- 4. دالة التشغيل الرئيسية ---

def main() -> None:
    """الوظيفة الرئيسية لتشغيل البوت."""
    
    # إنشاء التطبيق باستخدام التوكن
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # ربط المعالجات بالأوامر
    application.add_handler(CommandHandler("start", start_command))
    
    # ربط المعالج بالنصوص التي ليست أوامر (وهنا ستُعالج ضغطات الأزرار)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyboard_text))

    # تشغيل البوت (Polling)
    logger.info("Bot started and running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()