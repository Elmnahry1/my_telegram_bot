import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# تم استيراد Updater بدلاً من Application
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 

# ⚠️ إعدادات الواتساب ورقم فودافون كاش
WHATSAPP_NUMBER = "201288846355" 
VODAFONE_CASH_NUMBER = "01032328500" # 🔥 تم إضافة رقم المحفظة هنا
# --------------------
# 1. تعريف حالات المحادثة
# --------------------

GET_WALLET_NAME = 1 # حالة المحافظ
GET_PEN_NAME = 2    # حالة الأقلام 
GET_BOX_COLOR = 3   # حالة اختيار لون البوكس
GET_BOX_NAMES = 4   # حالة كتابة أسماء العرسان للبوكس
GET_TRAY_NAMES = 5  # حالة كتابة الأسماء للصينية الاكليريك
GET_TRAY_DATE = 6   # حالة كتابة التاريخ للصينية الاكليريك
GET_KHASHAB_TRAY_NAMES = 7 # حالة كتابة الأسماء لصينية الخشب
GET_KHASHAB_TRAY_DATE = 8  # حالة كتابة التاريخ لصينية الخشب
GET_AKRILIK_TAARAT_NAMES = 9 # حالة أسماء طارات اكليريك
GET_AKRILIK_TAARAT_DATE = 10 # حالة تاريخ طارات اكليريك
GET_KHASHAB_TAARAT_NAMES = 11 # حالة أسماء طارات خشب
GET_KHASHAB_TAARAT_DATE = 12 # حالة تاريخ طارات خشب
GET_BSAMAT_NAMES = 13 # حالة كتابة الأسماء للبصامات
GET_BSAMAT_DATE = 14 # حالة كتابة التاريخ للبصامات
GET_TISSUE_TYPE = 15 # حالة اختيار نوع علبة المناديل
GET_ENGRAVED_PEN_NAME = 16 # حالة كتابة الاسم للقلم المعدن
# 🔥 الحالة الجديدة لطلب إيصال الدفع
GET_PAYMENT_RECEIPT = 17 
# 🔥 الحالة الجديدة لطلب صور المج (إضافة جديدة)
GET_MUG_PHOTOS = 18 

# --------------------
# 2. تعريف القوائم ولوحات المفاتيح (بيانات افتراضية للتكامل)
# --------------------

# (⚠️ افتراض: هذه المتغيرات موجودة في الملف الأصلي.)
# بيانات المجّات (للتوضيح فقط لعمل الدوال الجديدة)
mugat_submenu = [
    {
        'label': 'مج ابيض عادي',
        'callback': 'mugat_white',
        'items': [
            {'label': 'مج ابيض (تصميم 1)', 'price': '100 ج.م', 'callback': 'mugat_white_m1', 'image': 'https://example.com/mug_white_img1.jpg'}
        ]
    },
    {
        'label': 'مج سحري',
        'callback': 'mugat_magic',
        'items': [
            {'label': 'مج سحري (تصميم 1)', 'price': '150 ج.م', 'callback': 'mugat_magic_m1', 'image': 'https://example.com/mug_magic_img1.jpg'}
        ]
    },
    {
        'label': 'مج ديجيتال', # هذا النوع لا يطلب صور وهو ضمن Direct Buy
        'callback': 'mugat_digital',
        'items': [
            {'label': 'مج ديجيتال (تصميم 1)', 'price': '200 ج.م', 'callback': 'mugat_digital_m1', 'image': 'https://example.com/mug_digital_img1.jpg'}
        ]
    }
]

# (⚠️ افتراض: المتغيرات الأخرى مثل main_menu_keyboard و menus و VODAFONE_CASH_NUMBER موجودة.)
main_menu_keyboard = [[InlineKeyboardButton("المنتجات", callback_data='products')]]
VODAFONE_CASH_ACCOUNT_NAME = "اسم حساب فودافون كاش" # (افتراضي)

# --------------------------------------------------------------------------------
# 3. الدوال الأساسية والمعدلة
# --------------------------------------------------------------------------------

def start(update, context):
    """يبدأ المحادثة ويرسل القائمة الرئيسية."""
    # (الكود الأصلي لـ start)
    if update.message:
        chat_id = update.message.chat_id
        text = "مرحباً بك في بوت الطلبات. يرجى اختيار القسم:"
        context.bot.send_message(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
    elif update.callback_query:
        # لو عودة من محادثة
        update.callback_query.answer()
        chat_id = update.callback_query.message.chat_id
        text = "مرحباً بك في بوت الطلبات. يرجى اختيار القسم:"
        update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
    return ConversationHandler.END


def button(update, context):
    """يعالج أزرار القائمة الرئيسية والقوائم الفرعية."""
    # (الكود الأصلي لـ button)
    query = update.callback_query
    query.answer()
    data = query.data
    
    # مثال على معالجة زر الرجوع إلى قائمة المجّات
    if data == 'mugat':
        # (افتراض: عرض قائمة المجّات الرئيسية)
        text = "اختر نوع المج:"
        mugat_keyboard = [
            [InlineKeyboardButton(item['label'], callback_data=item['callback'])]
            for item in mugat_submenu
        ]
        mugat_keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data='products')])
        reply_markup = InlineKeyboardMarkup(mugat_keyboard)
        query.edit_message_text(text=text, reply_markup=reply_markup)
        return ConversationHandler.END
    
    # ... (بقية معالجة الأزرار)
    
    # في حال لم يتم معالجة الأمر هنا
    return ConversationHandler.END

def cancel_and_end(update, context):
    """ينهي أي محادثة جارية."""
    # (الكود الأصلي لـ cancel_and_end)
    if update.callback_query:
        update.callback_query.answer("تم إلغاء العملية.")
        chat_id = update.callback_query.message.chat_id
        context.bot.send_message(chat_id=chat_id, text="تم إلغاء العملية، يمكنك البدء مجدداً من القائمة الرئيسية.", reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
    return ConversationHandler.END


# --------------------------------------------------------------------------------
# 🔥 الدوال الخاصة بمعالجة مج ابيض ومج سحري (طلب 3 صور) (إضافة جديدة)
# --------------------------------------------------------------------------------

def get_mug_items():
    """دالة مساعدة للحصول على قائمة المج الأبيض والسحري فقط."""
    # مج ابيض (mugat_white) هو العنصر الأول في قائمة المجّات
    white_mugs = mugat_submenu[0]['items']
    # مج سحري (mugat_magic) هو العنصر الثاني في قائمة المجّات
    magic_mugs = mugat_submenu[1]['items']
    # نجمعهم في قائمة واحدة لتسهيل البحث
    return white_mugs + magic_mugs

def get_file_link(context, file_id):
    """دالة مساعدة للحصول على رابط مباشر للملف (الصورة)."""
    try:
        # الحصول على كائن الملف من تليجرام
        file = context.bot.get_file(file_id)
        
        # بناء الرابط المباشر
        return f"https://api.telegram.org/file/bot{context.bot.token}/{file.file_path}"
        
    except Exception as e:
        print(f"Error getting file link: {e}")
        return "غير متوفر"


def start_mug_purchase(update, context):
    """تبدأ محادثة المج، وتطلب إرفاق 3 صور للطباعة."""
    query = update.callback_query
    query.answer()
    data = query.data # buy_mugat_white_m1 or buy_mugat_magic_m1

    product_callback = data.replace("buy_", "")
    
    # 1. جلب بيانات المنتج
    all_mug_items = get_mug_items() 
    selected_product = next((item for item in all_mug_items if item["callback"] == product_callback), None)
    
    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['mug_product'] = selected_product
    context.user_data['mug_photos_links'] = [] # تهيئة قائمة لتخزين روابط الصور
    context.user_data['state'] = GET_MUG_PHOTOS 
    
    # 2. إعداد لوحة المفاتيح (زر الرجوع)
    back_callback = "mugat" # العودة إلى قائمة تصنيفات المجّات
    back_keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=back_callback)]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    # 3. إرسال رسالة طلب الصور
    try:
        query.message.delete()
    except:
        pass

    caption_text = (
        f"✅ **{selected_product['label']}** (السعر: *{selected_product.get('price', 'غير متوفر')}*)\n\n"
        f"من فضلك، **يرجى إرسال 3 صور** في رسائل متتالية لطباعتهم على المج.\n"
        f"سيتم إرسال رابط الصور إلينا ضمن طلب الشراء.\n\n"
        f"أو اضغط زر رجوع للعودة الي القائمة السابقة."
    )
    
    try:
        # نستخدم send_photo لأننا حذفنا الرسالة الأصلية
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_product['image'],
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except telegram.error.BadRequest as e:
        # رسالة احتياطية في حال خطأ الصورة
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    return GET_MUG_PHOTOS


def receive_mug_photos_and_finish(update, context):
    """تستقبل الصور وتنتقل لمرحلة الدفع بعد استلام 3 صور."""
    # هذا المعالج يستقبل الصور فقط
    if not update.message.photo:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="❌ يجب إرسال **صورة**. يرجى إرفاق صورة للطباعة.",
            parse_mode="Markdown"
        )
        return GET_MUG_PHOTOS # البقاء في نفس الحالة
        
    # الحصول على ملف الصورة بأعلى دقة
    photo_file_id = update.message.photo[-1].file_id 
    
    # تحويل معرف الملف إلى رابط مباشر
    photo_link = get_file_link(context, photo_file_id)
        
    
    mug_photos_links = context.user_data.get('mug_photos_links', [])
    mug_photos_links.append(photo_link)
    context.user_data['mug_photos_links'] = mug_photos_links
    
    # التحقق من اكتمال 3 صور
    count = len(mug_photos_links)
    remaining = 3 - count
    
    if remaining > 0:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"تم استلام الصورة رقم {count} بنجاح. يرجى إرسال **{remaining} صور إضافية** لطباعتهم."
        )
        return GET_MUG_PHOTOS # البقاء في نفس الحالة
    else:
        # تم استلام جميع الصور، الانتقال إلى مرحلة الدفع
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="✅ تم استلام الثلاث صور بنجاح! سيتم الآن الانتقال لخطوة الدفع."
        )
        # الانتقال إلى مرحلة الدفع وتمرير نوع المنتج الجديد
        return prompt_for_payment_and_receipt(update, context, product_type="مج (طباعة 3 صور)")

# --------------------------------------------------------------------------------


def handle_payment_photo(update, context):
    """يعالج إيصال الدفع ويرسل طلب الشراء عبر الواتساب."""
    # (الكود الأصلي لـ handle_payment_photo)
    chat_id = update.message.chat_id
    
    if not update.message.photo:
        context.bot.send_message(chat_id=chat_id, text="يرجى إرسال صورة إيصال الدفع فقط.")
        return GET_PAYMENT_RECEIPT

    # الحصول على رابط الإيصال
    receipt_photo_id = update.message.photo[-1].file_id
    receipt_link = get_file_link(context, receipt_photo_id)

    # بناء رسالة الواتساب النهائية (نفس الكود من direct_buy_handler)
    product_data = context.user_data.get('product_data', {})
    names_details = context.user_data.get('names_details', 'غير متوفر')
    date_details = context.user_data.get('date_details', 'غير متوفر')
    
    product_name = product_data.get('label', 'منتج غير معروف')
    product_price = product_data.get('price', 'غير متوفر')
    
    whatsapp_message = (
        f"🔥 طلب شراء جديد 🔥\n\n"
        f"**المنتج**: {product_name}\n"
        f"**السعر**: {product_price}\n"
        f"**التفاصيل/الأسماء**: {names_details}\n"
        f"**التاريخ/التفاصيل الإضافية**: {date_details}\n\n"
        f"**رابط إيصال الدفع**: {receipt_link}\n\n"
        f"**معرّف المشتري**: @{update.message.from_user.username or update.message.chat_id}"
    )
    
    encoded_message = quote_plus(whatsapp_message)
    whatsapp_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"
    
    context.bot.send_message(
        chat_id=chat_id,
        text=(
            "✅ **تم استلام الإيصال!**\n\n"
            "الآن، **يرجى الضغط على زر إرسال الطلب** لإتمام عملية الشراء وتحويل جميع التفاصيل إلينا عبر الواتساب.\n"
            "سنقوم بالتأكد من الدفع والرد عليك في أقرب وقت لتأكيد الطلب."
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("إرسال الطلب عبر الواتساب 🚀", url=whatsapp_link)],
            [InlineKeyboardButton("إلغاء العملية والعودة", callback_data='cancel')]
        ]),
        parse_mode="Markdown"
    )

    # يمكن إنهاء المحادثة أو إبقائها
    return ConversationHandler.END


def handle_payment_buttons(update, context):
    """يعالج أزرار مرحلة الدفع (مثل الإلغاء)."""
    # (الكود الأصلي لـ handle_payment_buttons)
    query = update.callback_query
    query.answer()
    data = query.data
    
    if data == 'cancel':
        return cancel_and_end(update, context)

    return GET_PAYMENT_RECEIPT


def prompt_for_payment_and_receipt(update, context, product_type):
    """
    الدالة المعدلة: تطلب من المستخدم طريقة دفع وإيصال الدفع لجميع مسارات الشراء.
    تم تعديلها لإضافة حالة 'مج (طباعة 3 صور)'.
    """
    # ... (الكود الحالي)

    # 1. إعداد تفاصيل الطلب حسب نوع المنتج (الكود الأصلي مع إضافة حالة المج)
    product_data = None
    names_details = ""
    date_details = ""
    if product_type == "بصامة":
        # (باقي الحالات الحالية)
        pass 
    elif product_type == "مج (طباعة 3 صور)": # 🔥 الحالة الجديدة لطلب المج
        product_data = context.user_data.get('mug_product')
        mug_photos_links = context.user_data.get('mug_photos_links', [])
        # يتم تحويل روابط الصور إلى نص واحد وإدراجه في حقل الأسماء لإرساله عبر الواتساب
        names_details = "روابط صور الطباعة:\n" + "\n".join([f"🔗 صورة {i+1}: {link}" for i, link in enumerate(mug_photos_links)])
        date_details = 'غير مطلوب'
    else: # الحالة العامة للمنتجات ذات الشراء المباشر (Direct Buy)
        # (الكود الأصلي)
        product_data = context.user_data.get('product_data', {})
        names_details = 'غير مطلوب'
        date_details = 'غير مطلوب'
        
    # 2. حفظ البيانات للمرحلة التالية (handle_payment_photo)
    context.user_data['product_data'] = product_data
    context.user_data['names_details'] = names_details
    context.user_data['date_details'] = date_details
    
    # 3. إرسال رسالة الدفع (الكود الأصلي)
    product_name = product_data.get('label', 'المنتج')
    product_price = product_data.get('price', 'غير متوفر')
    
    payment_message = (
        f"✅ تم تأكيد طلبك لـ **{product_name}** بسعر *{product_price}*.\n\n"
        f"لإتمام عملية الشراء، يرجى تحويل المبلغ المطلوب إلى رقم فودافون كاش التالي:\n"
        f"💰 **{VODAFONE_CASH_NUMBER}** (باسم: {VODAFONE_CASH_ACCOUNT_NAME})\n\n"
        f"**الخطوة الأخيرة:** يرجى إرسال **صورة إيصال الدفع** الآن لتأكيد عملية التحويل.\n"
        f"أو اضغط زر إلغاء للرجوع."
    )
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("إلغاء العملية", callback_data='cancel')]
    ])

    # نستخدم update.effective_chat.id لضمان العمل من داخل المحادثات
    chat_id = update.effective_chat.id 
    
    # تعديل: إذا كانت المحادثة قادمة من callback_query (أزرار)، نقوم بحذف الرسالة القديمة أولاً
    if update.callback_query:
        try:
            update.callback_query.edit_message_text(text=payment_message, reply_markup=reply_markup, parse_mode="Markdown")
        except:
            # في حال لم يتمكن من التعديل، يقوم بإرسال رسالة جديدة
            context.bot.send_message(chat_id=chat_id, text=payment_message, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        context.bot.send_message(chat_id=chat_id, text=payment_message, reply_markup=reply_markup, parse_mode="Markdown")
        
    context.user_data['state'] = GET_PAYMENT_RECEIPT
    return GET_PAYMENT_RECEIPT


def prepare_whatsapp_link_for_direct_buy(update, context):
    """يعالج المنتجات ذات الشراء المباشر (مثل مج ديجيتال) وينتقل لمرحلة الدفع."""
    # (الكود الأصلي لـ prepare_whatsapp_link_for_direct_buy)
    query = update.callback_query
    query.answer()
    data = query.data # buy_mugat_digital_m1

    product_callback = data.replace("buy_", "")
    
    # افتراض: قائمة المنتجات الأخرى موجودة
    direct_buy_items = [] # (يجب جلب قائمة المنتجات)
    
    # جلب قائمة المنتجات المباشرة (نضيف المج الديجيتال هنا افتراضياً)
    all_products = (
        mugat_submenu[2]['items'] + # مج ديجيتال
        direct_buy_items
    )
    
    selected_product = next((item for item in all_products if item["callback"] == product_callback), None)

    if not selected_product:
        query.answer("خطأ في العثور على المنتج", show_alert=True)
        return ConversationHandler.END

    context.user_data['product_data'] = selected_product
    
    # الانتقال إلى مرحلة الدفع باستخدام اسم المنتج
    return prompt_for_payment_and_receipt(update, context, product_type=selected_product.get('label'))


# --------------------------------------------------------------------------------
# 5. دالة main() وتجهيز الموزع (Dispatcher)
# --------------------------------------------------------------------------------

def main():
    # ⚠️ تم استعادة استخدام متغير البيئة BOT_TOKEN كما طلبت
    TOKEN = os.environ.get('TOKEN') 
    if not TOKEN:
         # يفضل طباعة رسالة خطأ أو استخدام قيمة placeholder إذا لم يتم العثور على التوكن
         print("Error: BOT_TOKEN environment variable is not set. Please set it or hardcode the token.")
         return
         
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # 2. تعريف معالجات المحادثات الأخرى
    # (افتراض: تعريفات box_handler, tray_handler, ... إلخ موجودة هنا)
    
    # 3. محادثة شراء مباشرة للمنتجات الأخرى (أباجورات، دروع، أهرام، مج ديجتال، سبلميشن)
    # 🔥 التعديل: تم استثناء المج الأبيض والسحري (مما يعني استثناء نمط "mugat" العام)
    direct_buy_handler = ConversationHandler(
        # 🔥 النمط المعدل لاستثناء mugat_white و mugat_magic
        entry_points=[CallbackQueryHandler(prepare_whatsapp_link_for_direct_buy, pattern='^buy_(abajora|haram|doro3|subli|mugat_digital)_.*')], 
        states={
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$') 
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 10. محادثة المج الأبيض والسحري (طلب 3 صور) (إضافة جديدة)
    mug_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_mug_purchase, pattern='^buy_mugat_white_.*$'),
            CallbackQueryHandler(start_mug_purchase, pattern='^buy_mugat_magic_.*$')
        ],
        states={
            GET_MUG_PHOTOS: [
                # يستقبل رسائل الصور
                MessageHandler(Filters.photo & ~Filters.command, receive_mug_photos_and_finish),
                # زر الرجوع يعود إلى قائمة المجّات الرئيسية
                CallbackQueryHandler(button, pattern='^mugat$') 
            ],
            GET_PAYMENT_RECEIPT: [
                MessageHandler(Filters.photo, handle_payment_photo),
                CallbackQueryHandler(handle_payment_buttons, pattern='^cancel$')
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(cancel_and_end)
        ]
    )

    # 4. إضافة جميع ConversationHandler أولاً لضمان الأولوية (افتراض: إضافة المعالجات الأخرى)
    # dp.add_handler(box_handler)
    # ... (بقية المعالجات)
    # dp.add_handler(engraved_pen_handler) 
    dp.add_handler(mug_handler) # 🔥 إضافة المعالج الجديد
    dp.add_handler(direct_buy_handler) 

    
    # 5. أوامر /start
    dp.add_handler(CommandHandler("start", start))
    
    # 6. معالج أزرار القائمة العامة (يجب أن يكون في النهاية)
    dp.add_handler(CallbackQueryHandler(button))

    # 7. بدء البوت (افتراض)
    # updater.start_polling()
    # updater.idle() 
    print("Bot started...") # (رسالة افتراضية للتكامل)

if __name__ == '__main__':
    main()