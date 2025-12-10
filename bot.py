import logging
from telegram import ReplyKeyboardMarkup, Update
# لاحظ استخدام Updater بدلاً من Application، و Filters بحرف كبير
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# --- 1. الإعدادات الأساسية ---

TELEGRAM_BOT_TOKEN = "TOKEN"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- 2. بناء الأزرار (Reply Keyboard) ---

def build_reply_keyboard():
    """ينشئ لوحة المفاتيح المخصصة."""
    button_buy = "💳 Buy | VIP 🛒"
    button_account = "👤 My Account"
    button_stats = "📊 Stats"
    button_support = "✉️ Support"
    button_language = "🌍 Language"
    
    row1 = [button_buy, button_account, button_stats]
    row2 = [button_support, button_language]

    keyboard = [row1, row2]
    
    return ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True, 
        one_time_keyboard=False
    )

# --- 3. مُعالِجات الأوامر (Handlers) ---
# ملاحظة: تم إزالة async و await واستخدام CallbackContext

def start_command(update: Update, context: CallbackContext) -> None:
    """الاستجابة لأمر /start."""
    reply_markup = build_reply_keyboard()
    
    # تم إزالة await
    update.message.reply_text(
        "👋 أهلاً بك! يرجى اختيار أحد الأزرار الرئيسية أدناه:",
        reply_markup=reply_markup
    )

def handle_keyboard_text(update: Update, context: CallbackContext) -> None:
    """تستجيب لضغطات الأزرار."""
    text = update.message.text
    
    if text == "👤 My Account":
        update.message.reply_text(
            "👤 معلومات الحساب:\n"
            "الحالة: عضو مجاني (Free Tier)\n"
            "للاشتراك في VIP، اضغط على زر 'Buy | VIP'."
        )
    
    elif text == "📊 Stats":
        update.message.reply_text(
            "📊 إحصائيات الأداء (آخر 7 أيام):\n"
            "* نسبة الربح الإجمالية: 4825.06%\n"
            "* إجمالي الصفقات: 75\n"
            "* الصفقات الفاشلة: 10"
        )
        
    elif text == "💳 Buy | VIP 🛒":
        update.message.reply_text(
            "💰 للاشتراك في خدمة الـ VIP، يرجى زيارة الرابط التالي للدفع الآمن:\n"
            "https://yourpaymentlink.com/vip"
        )
        
    elif text == "✉️ Support":
        update.message.reply_text(
            "💬 يمكنك التواصل مع فريق الدعم على الرابط التالي: @YourAdminUsername"
        )

    elif text == "🌍 Language":
        update.message.reply_text(
            "🌍 يرجى اختيار اللغة المفضلة:"
        )

    else:
        update.message.reply_text("👋 رسالة غير مفهومة. يرجى استخدام الأزرار في الأسفل.")

# --- 4. دالة التشغيل الرئيسية ---

def main() -> None:
    """الوظيفة الرئيسية لتشغيل البوت."""
    
    # إعداد Updater بدلاً من Application
    # use_context=True هو الافتراضي في الإصدار 13 ولكن يفضل كتابته للتأكيد
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    # الحصول على الـ dispatcher لتسجيل المعالجات
    dispatcher = updater.dispatcher

    # ربط المعالجات بالأوامر
    dispatcher.add_handler(CommandHandler("start", start_command))
    
    # ربط المعالج بالنصوص (لاحظ Filters بحرف كبير)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_keyboard_text))

    # تشغيل البوت
    logger.info("Bot started and running (v13 mode)...")
    updater.start_polling()
    
    # هذا الأمر يبقي البوت يعمل حتى يتم إيقافه يدوياً (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()