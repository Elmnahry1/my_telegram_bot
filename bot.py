import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus

# إعدادات الواتساب
WHATSAPP_NUMBER = "201288846355"

# حالات المحادثة
GET_WALLET_NAME = 1
GET_PEN_NAME = 2
GET_BOX_COLOR = 3
GET_BOX_NAMES = 4
GET_TRAY_NAMES = 5
GET_TRAY_DATE = 6

# البيانات والقوائم
# (نفس البيانات والقوائم التي أرسلتها، أدرجها هنا كما هي)

# ... (نفس البيانات والقوائم التي أرسلتها مسبقًا)

# خريطة المنتجات
product_to_submenu_map = {}
for menu_key, submenu_list in all_submenus.items():
    if menu_key in ["bsamat", "wedding_tissues", "abajorat", "engraved_wallet", "aqlam", "katb_kitab_box"]:
        for product in submenu_list:
            product_to_submenu_map[product["callback"]] = menu_key
    else:
        for item in submenu_list:
            product_to_submenu_map[item["callback"]] = menu_key
            if 'items' in item:
                for sub_item in item['items']:
                    product_to_submenu_map[sub_item["callback"]] = item["callback"]

# قائمة أكواد المنتجات التي تحتاج محادثة
TRAY_PRODUCT_KEYS = (
    [item["callback"] for item in sawany_submenu[0]['items']] +
    [item["callback"] for item in sawany_submenu[1]['items']] +
    [item["callback"] for item in taarat_submenu[0]['items']] +
    [item["callback"] for item in taarat_submenu[1]['items']]
)

# -----------------------------------
# دوال البداية والمساعدة
# -----------------------------------

def start(update, context):
    # الكود كما هو
    # ...
    pass

def show_submenu(update, context, submenu_list, title, back_callback="main_menu"):
    # الكود كما هو
    # ...
    pass

def show_product_page(update, product_callback_data, product_data, is_direct_list=False):
    # الكود كما هو
    # ...
    pass

# -----------------------------------
# الدوال الخاصة بالمحفظة والأقلام
# -----------------------------------
# (نفس الدوال كما هو، بدون تغيير)

# -----------------------------------
# دوال بوكس كتب الكتاب
# -----------------------------------
# (نفس الدوال كما هو، بدون تغيير)

# -----------------------------------
# دوال الصواني والطارات (أكليريك وخشب)
# -----------------------------------

def start_tray_purchase(update, context):
    query = update.callback_query
    query.answer()
    data = query.data
    product_callback = data.replace("buy_", "")

    # تحديد المنتج بناءً على الكود
    if "akerik_m" in product_callback:
        items_list = taarat_submenu[0]['items'] if "taarat" in product_callback else sawany_submenu[0]['items']
        back_cb = "taarat_akerik" if "taarat" in product_callback else "sawany_akerik"
    elif "khashab_m" in product_callback:
        items_list = taarat_submenu[1]['items'] if "taarat" in product_callback else sawany_submenu[1]['items']
        back_cb = "taarat_khashab" if "taarat" in product_callback else "sawany_khashab"
    else:
        # خطأ
        query.answer("خطأ في تحديد المنتج", show_alert=True)
        return

    selected_tray = next((item for item in items_list if item["callback"] == product_callback), None)
    if not selected_tray:
        query.answer("بيانات المنتج غير موجودة", show_alert=True)
        return

    # حفظ البيانات
    context.user_data['tray_product'] = selected_tray
    context.user_data['tray_back_callback'] = back_cb
    context.user_data['state'] = GET_TRAY_NAMES

    # عرض الصورة وخطوة الإدخال
    try:
        query.message.delete()
    except:
        pass

    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=selected_tray['image'],
        caption=f"✅ **{selected_tray['label']}**\n\n من فضلك **اكتب اسم العريس والعروسة** في رسالة نصية بالأسفل او اضغط زر رجوع للعودة الي القائمة السابقة:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data=back_cb)]]),
        parse_mode="Markdown"
    )
    return GET_TRAY_NAMES

# ... (وظائف الرجوع وتسجيل الأسماء والتاريخ كما هي)

# -----------------------------------
# معالجة زر الشراء الخاص بالمنتجات (مهم جدًا)
# -----------------------------------

def button(update, context):
    query = update.callback_query
    data = query.data

    # العودة للقائمة الرئيسية
    if data == "main_menu":
        start(update, context)
        return

    # المحافظ والأقلام
    if data == "engraved_wallet":
        show_submenu(update, context, engraved_wallet_submenu, "محافظ محفورة بالاسم", back_callback="main_menu")
        return
    if data == "aqlam":
        show_submenu(update, context, aqlam_submenu, "اقلام محفورة بالاسم", back_callback="main_menu")
        return

    # القوائم المتداخلة
    if data in ["sawany", "taarat", "haram", "doro3", "mugat"]:
        # عرض القائمة
        title = next((item["label"] for item in main_menu if item["callback"] == data), "القائمة")
        show_submenu(update, context, all_submenus[data], title, back_callback="main_menu")
        return

    # صفحات المنتجات المباشرة
    if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box"]:
        show_product_page(update, data, all_submenus[data], is_direct_list=True)
        return

    # صفحات المنتجات المتداخلة (الصواني والطارات)
    if data == "sawany_akerik":
        show_product_page(update, "sawany_akerik", sawany_submenu[0]['items'], is_direct_list=True)
        return
    if data == "sawany_khashab":
        show_product_page(update, "sawany_khashab", sawany_submenu[1]['items'], is_direct_list=True)
        return
    if data == "taarat_akerik":
        show_product_page(update, "taarat_akerik", taarat_submenu[0]['items'], is_direct_list=True)
        return
    if data == "taarat_khashab":
        show_product_page(update, "taarat_khashab", taarat_submenu[1]['items'], is_direct_list=True)
        return

    # زر الشراء لمنتجات عادية
    if data.startswith("buy_"):
        # هنا نضيف معالجة خاصة لمنتجات الصواني والطارات
        if data.startswith("buy_sawany_") or data.startswith("buy_taarat_"):
            # عرض المنتجات
            if data.startswith("buy_sawany_"):
                if "akerik" in data:
                    show_product_page(update, data, sawany_submenu[0]['items'], is_direct_list=True)
                elif "khashab" in data:
                    show_product_page(update, data, sawany_submenu[1]['items'], is_direct_list=True)
            elif data.startswith("buy_taarat_"):
                if "akerik" in data:
                    show_product_page(update, data, taarat_submenu[0]['items'], is_direct_list=True)
                elif "khashab" in data:
                    show_product_page(update, data, taarat_submenu[1]['items'], is_direct_list=True)
            return

        # باقي المنتجات
        product_key = data.replace("buy_", "")
        # استخرج بيانات المنتج
        product_data = None
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
            if product_data:
                break

        if not product_data:
            query.answer("لم يتم العثور على المنتج.", show_alert=True)
            return

        # الآن أرسل الطلب عبر واتساب
        user_info = query.from_user
        message_body = (f"🔔 *طلب شراء جديد*\nالمنتج: {product_data['label']}\nالكود: {product_data['callback']}\nالعميل: {user_info.first_name}\n🔗 صورة: {product_data['image']}")
        encoded_text = quote_plus(message_body)
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"

        # إرسال الرابط
        query.answer("سيتم فتح واتساب...", show_alert=False)
        keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            query.message.delete()
        except:
            pass
        context.bot.send_message(chat_id=query.message.chat_id, text=f"شكراً لطلبك! اضغط أدناه للإرسال:", reply_markup=reply_markup)
        return

    # زر الشراء الخاص بمنتجات الصواني والطارات
    if data.startswith("buy_sawany_") or data.startswith("buy_taarat_"):
        # عرض المنتجات من جديد
        if data.startswith("buy_sawany_"):
            if "akerik" in data:
                show_product_page(update, data, sawany_submenu[0]['items'], is_direct_list=True)
            elif "khashab" in data:
                show_product_page(update, data, sawany_submenu[1]['items'], is_direct_list=True)
        elif data.startswith("buy_taarat_"):
            if "akerik" in data:
                show_product_page(update, data, taarat_submenu[0]['items'], is_direct_list=True)
            elif "khashab" in data:
                show_product_page(update, data, taarat_submenu[1]['items'], is_direct_list=True)
        return

    # زر الرجوع
    if data == "back_to_tray_names":
        back_to_tray_names(update, context)
        return

    # غير معروف
    query.answer("زر غير معروف أو غير مخصص.", show_alert=True)

# -----------------------------------
# النهاية، إعداد البوت
# -----------------------------------

def main():
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        print("توكن غير موجود")
        return
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # المعالجات
    # (نفس إعدادات المحادثات كما هي)
    # ...
    # أضف هنا المعالجات
    # ...

    # معالج زر الأزرار
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("start", start))
    print("البوت يعمل")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()