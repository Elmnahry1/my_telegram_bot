import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler

# إعدادات الواتساب
WHATSAPP_NUMBER = "201288846355"

# حالات المحادثة
GET_WALLET_NAME = 1
GET_PEN_NAME = 2
GET_BOX_COLOR = 3
GET_BOX_NAMES = 4
GET_TRAY_NAMES = 5
GET_TRAY_DATE = 6

# البيانات والقوائم (أولاً، أدرج البيانات التي أرسلتها مسبقًا هنا)

# مثال على البيانات
# جميع القوائم والبيانات التي أرسلتها يجب أن تكون هنا

# لنفترض أن لديك جميع البيانات مثل:
# all_submenus, sawany_submenu, taarat_submenu، وغيرها

# مثال بسيط لتوضيح
all_submenus = {
    "bsamat": [
        {"label": "بسمات", "callback": "bsamat", "image": "https://example.com/image.jpg"},
    ],
    "wedding_tissues": [
        {"label": "مجات الزفاف", "callback": "wedding_tissues", "image": "https://example.com/image2.jpg"},
    ],
    # أضف باقي القوائم هنا
}

sawany_submenu = [
    {
        "items": [
            {"label": "صواني أكرليك م1", "callback": "sawany_akerik_m1", "image": "https://example.com/sawany_akerik_m1.jpg"},
            {"label": "صواني خشب م2", "callback": "sawany_khashab_m2", "image": "https://example.com/sawany_khashab_m2.jpg"},
        ]
    }
]

taarat_submenu = [
    {
        "items": [
            {"label": "طارات أكرليك م1", "callback": "taarat_akerik_m1", "image": "https://example.com/taarat_akerik_m1.jpg"},
            {"label": "طارات خشب م2", "callback": "taarat_khashab_m2", "image": "https://example.com/taarat_khashab_m2.jpg"},
        ]
    }
]

# دوال البداية والمساعدة
def start(update, context):
    # هنا تضع الكود الخاص بالبدء
    pass

def show_submenu(update, context, submenu_list, title, back_callback="main_menu"):
    # هنا تضع الكود الخاص بعرض القوائم
    pass

def show_product_page(update, product_callback_data, product_list, is_direct_list=False):
    # هنا تضع الكود الخاص بعرض صفحة المنتج
    pass

# دالة المعالجة للأزرار
def button(update, context):
    query = update.callback_query
    data = query.data

    # معالجة زر العودة
    if data == "main_menu":
        start(update, context)
        return

    # معالجة صفحات القوائم
    if data in all_submenus:
        show_submenu(update, context, all_submenus[data], data)
        return

    # صفحات المنتجات المباشرة
    if data in ["bsamat", "wedding_tissues", "abajorat", "katb_kitab_box"]:
        show_product_page(update, data, all_submenus[data], True)
        return

    # صفحات منتجات الصواني والطارات
    if data == "sawany_akerik" or data == "sawany_khashab" or data == "taarat_akerik" or data == "taarat_khashab":
        if data == "sawany_akerik":
            show_product_page(update, data, sawany_submenu[0]['items'], True)
        elif data == "sawany_khashab":
            show_product_page(update, data, sawany_submenu[1]['items'], True)
        elif data == "taarat_akerik":
            show_product_page(update, data, taarat_submenu[0]['items'], True)
        elif data == "taarat_khashab":
            show_product_page(update, data, taarat_submenu[1]['items'], True)
        return

    # معالجة زر الشراء للمنتجات
    if data.startswith("buy_"):
        # هنا نحدد نوع المنتج بناءً على الكود
        if data.startswith("buy_sawany_") or data.startswith("buy_taarat_"):
            # عرض المنتج من جديد بناءً على النمط
            if data.startswith("buy_sawany_"):
                if "akerik" in data:
                    show_product_page(update, data, sawany_submenu[0]['items'], True)
                elif "khashab" in data:
                    show_product_page(update, data, sawany_submenu[1]['items'], True)
            elif data.startswith("buy_taarat_"):
                if "akerik" in data:
                    show_product_page(update, data, taarat_submenu[0]['items'], True)
                elif "khashab" in data:
                    show_product_page(update, data, taarat_submenu[1]['items'], True)
            return

        # معالجة المنتجات العادية
        product_key = data.replace("buy_", "")
        # ابحث عن المنتج في جميع القوائم
        product_data = None
        for submenu in all_submenus.values():
            for item in submenu:
                if item.get("callback") == product_key:
                    product_data = item
                    break
                if "items" in item:
                    for sub_item in item["items"]:
                        if sub_item.get("callback") == product_key:
                            product_data = sub_item
                            break
                if product_data:
                    break
            if product_data:
                break

        if not product_data:
            query.answer("لم يتم العثور على المنتج", show_alert=True)
            return

        # الآن نرسل الطلب عبر واتساب
        user_info = query.from_user
        message_body = f"🔔 *طلب شراء*\nالمنتج: {product_data['label']}\nالكود: {product_data['callback']}\nالعميل: {user_info.first_name}\n🔗 صورة: {product_data['image']}"
        from urllib.parse import quote_plus
        encoded_text = quote_plus(message_body)
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"

        # نرسل الرابط
        query.answer("سيتم فتح واتساب...", show_alert=False)
        keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            query.message.delete()
        except:
            pass
        context.bot.send_message(chat_id=query.message.chat_id, text="شكراً لطلبك! اضغط أدناه لإرسال الطلب:", reply_markup=reply_markup)
        return

    # زر الشراء لمنتجات الصواني والطارات
    if data.startswith("buy_sawany_") or data.startswith("buy_taarat_"):
        # عرض المنتجات من جديد بناءً على النمط
        if data.startswith("buy_sawany_"):
            if "akerik" in data:
                show_product_page(update, data, sawany_submenu[0]['items'], True)
            elif "khashab" in data:
                show_product_page(update, data, sawany_submenu[1]['items'], True)
        elif data.startswith("buy_taarat_"):
            if "akerik" in data:
                show_product_page(update, data, taarat_submenu[0]['items'], True)
            elif "khashab" in data:
                show_product_page(update, data, taarat_submenu[1]['items'], True)
        return

    # زر الرجوع
    if data == "back_to_tray_names":
        # وظيفة للرجوع لصفحة إدخال الأسماء
        pass

    # غير معروف
    query.answer("زر غير معروف أو غير مخصص", show_alert=True)

# إعداد البوت
def main():
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # أضف هنا كل المعالجات
    # ...
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    # ابدأ تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()