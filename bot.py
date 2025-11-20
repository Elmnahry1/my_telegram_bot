import os
import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib.parse import quote_plus 
import re 

# ⚠️ إعدادات الواتساب: استبدل بالرقم الخاص بك
WHATSAPP_NUMBER = "201288846355" 

# --------------------
# 1. تعريف حالات المحادثة
# --------------------

GET_WALLET_NAME = 1 # حالة المحافظ
GET_PEN_NAME = 2    # حالة الأقلام 
GET_BOX_COLOR = 3   # حالة اختيار لون البوكس
GET_BOX_NAMES = 4   # حالة كتابة أسماء العرسان للبوكس
GET_TRAY_NAMES = 5  # حالة كتابة الأسماء (للصواني والطارات)
GET_TRAY_DATE = 6   # حالة كتابة التاريخ (للصواني والطارات)

# --------------------
# 2. بيانات القوائم والمنتجات
# --------------------

# --- قوائم فرعية مباشرة ---
bsamat_submenu = [
    {"label": "بصامة موديل 1", "callback": "bsamat_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 1."},
    {"label": "بصامة موديل 2", "callback": "bsamat_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف البصامة موديل 2."}
]
wedding_tissues_submenu = [
    {"label": "منديل موديل 1", "callback": "tissue_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 1."},
    {"label": "منديل موديل 2", "callback": "tissue_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف منديل كتب الكتاب موديل 2."}
]
katb_kitab_box_submenu = [
    {"label": "بوكس كتب كتاب موديل 1", "callback": "box_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف بوكس كتب الكتاب موديل 1، يحتوي على تصميم مميز."},
    {"label": "بوكس كتب كتاب موديل 2", "callback": "box_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف بوكس كتب الكتاب موديل 2، خامة عالية الجودة."}
]
abajorat_submenu = [
    {"label": "أباجورة موديل 1", "callback": "abajora_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف الأباجورة موديل 1."},
    {"label": "أباجورة موديل 2", "callback": "abajora_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف الأباجورة موديل 2."}
]
engraved_wallet_submenu = [
    {"label": "محفظة بيج (هافان)", "callback": "wallet_bege", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بيج (هافان)."},
    {"label": "محفظة بني", "callback": "wallet_brown", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون بني."},
    {"label": "محفظة سوداء", "callback": "wallet_black", "image": "https://m.media-amazon.com/images/I/41DrZIhSyiL._AC_SX300_SY300_QL70_ML2_.jpg", "description": "محفظة سافوكس الاصلية تقيلة، لون أسود."}
]
aqlam_submenu = [
    {
        "label": "قلم تاتش معدن", 
        "callback": "aqlam_metal", 
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/475773348_986832329974720_6197915277469223378_n.jpg?stp=dst-jpg_s720x720_tt6&_nc_cat=107&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=KrebndL4u2oQ7kNvwH3smA2&_nc_oc=AdkT6T_o5SpJKdr9FQ5OhX2vuI5Cp3WjQl0pV9vRotIn9csOIX1DX-I9dC3FpvlBLJM&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=JFYgN-MxG5oy8y3q9Os6Ew&oh=00_AfhJxajOEm9owiAqd00_zEZ4Hy4qzX7DYATV6p4tWdRxeA&oe=6923BE1B", 
        "description": "قلم تاتش معدن عالي الجودة ومناسب للحفر بالليزر."
    },
    {
        "label": "قلم تاتش مضئ", 
        "callback": "aqlam_luminous", 
        "image": "https://scontent.fcai24-1.fna.fbcdn.net/v/t39.30808-6/489809156_1164483322357054_6286791651911010777_n.jpg?stp=dst-jpg_s590x590_tt6&_nc_cat=107&ccb=1-7&_nc_sid=833d8c&_nc_ohc=ELb9pciSoD0Q7kNvwG_rdLE&_nc_oc=AdkDWLOZBcjZp9AbNO2Fs-zK-suPtGc1D-KC3JP7NlzhwgJB3WZeGQQfCQIsfxZgvrg&_nc_zt=23&_nc_ht=scontent.fcai24-1.fna&_nc_gid=U5_JMOw_cSsgrQQLv77j7g&oh=00_Afg-wJrTmoGZo5m1kVVh2IU0227UQ7pUtKSjRx_YEFoGWg&oe=6923B3BA", 
        "description": "قلم تاتش مضئ بتقنية متطورة ومناسب للحفر بالليزر."
    }
]

# --- القوائم المتداخلة ---
sawany_submenu = [
    {
        "label": "صواني شبكة اكليريك", "callback": "sawany_akerik", 
        "items": [ 
            {"label": "صينية اكليريك موديل 1", "callback": "akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "صينية اكليريك: وصف المنتج الأول."},
            {"label": "صينية اكليريك موديل 2", "callback": "akerik_m2", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "صينية اكليريك: وصف المنتج الثاني."}
        ]
    },
    {
        "label": "صواني شبكة خشب", "callback": "sawany_khashab", 
        "items": [ 
            {"label": "صينية خشب موديل 1", "callback": "khashab_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "صينية خشب: وصف المنتج الأول."},
            {"label": "صينية خشب موديل 2", "callback": "khashab_m2", "image": "https://e7.pngegg.com/pngimages/577/728/png-clipart-number-number-image-file-formats-orange-thumbnail.png", "description": "صينية خشب: وصف المنتج الثاني."}
        ]
    }
]
taarat_submenu = [
    {
        "label": "طارات اكليريك", "callback": "taarat_akerik", "items": [
             {"label": "طارة اكليريك موديل 1", "callback": "taarat_akerik_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة اكليريك موديل 1"},
             {"label": "طارة اكليريك موديل 2", "callback": "taarat_akerik_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة اكليريك موديل 2"}
        ]
    },
    {
        "label": "طارات خشب", "callback": "taarat_khashab", "items": [
            {"label": "طارة خشب موديل 1", "callback": "taarat_khashab_m1", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة خشب موديل 1"},
            {"label": "طارة خشب موديل 2", "callback": "taarat_khashab_m2", "image": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف طارة خشب موديل 2"}
        ]
    }
]
# ... بقية الكود كما هو ...

# بناء خريطة المنتجات
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


# قائمة مفاتيح منتجات الصواني والطارات التي تحتاج محادثة خاصة
TRAY_PRODUCT_KEYS = (
    [item["callback"] for item in sawany_submenu[0]['items']] + 
    [item["callback"] for item in sawany_submenu[1]['items']] + 
    [item["callback"] for item in taarat_submenu[0]['items']] + 
    [item["callback"] for item in taarat_submenu[1]['items']]
)

# ... دوال start, show_submenu, show_product_page, دوال المحافظ، الأقلام، بوكس كتب الكتاب، الصواني والطارات ... (كما في كودك الأصلي) ...

# ------------------------------------
# الدالة الرئيسية لمعالجة ضغطات الأزرار مع تعديل مهم هنا
# ------------------------------------
def button(update, context):
    query = update.callback_query
    data = query.data

    # ... باقي الحالات كما هي ...

    # حالة زر الشراء (المنتجات العادية)
    if data.startswith("buy_"):
        product_key = data.replace("buy_", "")
        
        # استثناء المنتجات التي لها محادثة خاصة (بوكس كتب الكتاب)
        if data.startswith("buy_box_"): 
            return # يتم معالجتها بواسطة box_handler

        # استثناء أزرار الشراء الخاصة بالصواني والطارات للسماح لـ tray_handler بمعالجتها
        if product_key in TRAY_PRODUCT_KEYS:
            return  # يتم معالجتها في tray_handler
        
        # متابعة معالجة المنتجات العادية
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
            query.answer(text="عذراً، لم يتم العثور على بيانات المنتج.", show_alert=True)
            return
            
        user_info = query.from_user
        message_body = (f"🔔 *طلب شراء جديد*\nالمنتج: {product_data['label']}\nالكود: {product_key}\nالعميل: {user_info.first_name}\n🔗 صورة: {product_data['image']}")
        encoded_text = quote_plus(message_body)
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_text}"
        
        query.answer(text="سيتم فتح واتساب...", show_alert=False)
        keyboard = [[InlineKeyboardButton("✅ اضغط هنا لإرسال الطلب على واتساب", url=wa_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            query.message.delete()
        except Exception:
            pass
        context.bot.send_message(chat_id=query.message.chat_id, text=f"شكراً لطلبك! اضغط أدناه للإرسال:", reply_markup=reply_markup)
        return

    # ... باقي الكود كما هو ...


# ------------------------------------
# إعداد البوت وإضافة المعالجات
# ------------------------------------
def main():
    TOKEN = os.getenv("TOKEN") 
    
    if not TOKEN:
        print("❌ لم يتم العثور على التوكن (TOKEN).")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # المحادثات handlers كما في كودك الأصلي (engraved_wallet_handler, engraved_pen_handler, box_handler, tray_handler)
    # مع tray_handler يستخدم النمط التالي لزر الشراء:
    tray_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_tray_purchase, pattern=r'^(buy_)(sawany|taarat)_(akerik|khashab)_(m1|m2)$')
        ],
        states={
            GET_TRAY_NAMES: [
                MessageHandler(Filters.text & ~Filters.command, save_tray_names_ask_date),
                CallbackQueryHandler(button, pattern='^(sawany_akerik|sawany_khashab|taarat_akerik|taarat_khashab)$')
            ],
            GET_TRAY_DATE: [MessageHandler(Filters.text & ~Filters.command, receive_tray_date_and_finish)]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(back_to_tray_names, pattern='^back_to_tray_names$'),
            CallbackQueryHandler(button)
        ]
    )

    # إضافة باقي handlers كما في كودك الأصلي
    dp.add_handler(engraved_wallet_handler)
    dp.add_handler(engraved_pen_handler)
    dp.add_handler(box_handler)
    dp.add_handler(tray_handler)
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    print("🤖 البوت يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()