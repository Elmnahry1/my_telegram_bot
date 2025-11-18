import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# رقم الواتساب اللي هيجيلك عليه الطلب
WHATSAPP_NUMBER = "201234567890"  # ضع رقمك هنا بدون +
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUMBER}?text="

# بيانات الأقسام والصور
sections = {
    "صواني شبكة": {
        "subsections": {
            "صواني شبكة اكليريك": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"},
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف2"}
            ],
            "صواني شبكة خشب": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف3"},
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف4"}
            ]
        }
    },
    "طارات خطوبة وكتب الكتاب": {
        "subsections": {
            "طارات خطوبة وكتب الكتاب اكليريك": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف5"}
            ],
            "طارات خطوبة وكتب الكتاب خشب": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف6"}
            ]
        }
    },
    "بصامات": {
        "subsections": {
            "مناديل كتب الكتاب": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف7"}
            ]
        }
    },
    "هرم مكتب": {
        "subsections": {
            "هرم مكتب اكليريك": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف8"}
            ],
            "هرم مكتب بديل المعدن": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف9"}
            ],
            "هرم مكتب خشب": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف10"}
            ]
        }
    },
    "دروع": {
        "subsections": {
            "دروع اكليريك": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف11"}
            ],
            "دروع بديل المعدن": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف12"}
            ],
            "دروع خشب": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف13"}
            ]
        }
    },
    "اقلام": {
        "subsections": {
            "قلم تاتش معدن": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف14"}
            ],
            "قلم تاتش مضئ": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف15"}
            ]
        }
    },
    "مجات": {
        "subsections": {
            "مج ابيض": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف16"}
            ],
            "مج سحري": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف17"}
            ],
            "مج ديجتال": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف18"}
            ],
            "محافظ محفورة بالاسم": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف19"}
            ]
        }
    }
}

# ---------------------------------------------------------
# القائمة الرئيسية
# ---------------------------------------------------------
def start(update: Update, context: CallbackContext):
    user_first_name = update.effective_user.first_name
    welcome_text = f"✅ مرحباً بك {user_first_name} في البوت الرسمي لمصنع المناهري للحفر بالليزر وجميع مستلزمات الزفاف والسبلميشن\n\nمن فضلك اختار طلبك من القائمة:"
    keyboard = []
    for section in sections:
        keyboard.append([InlineKeyboardButton(section, callback_data=f"section|{section}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(welcome_text, reply_markup=reply_markup)

# ---------------------------------------------------------
# عرض الصور ووصفها مع زر شراء وزر رجوع
# ---------------------------------------------------------
def show_images(update: Update, context: CallbackContext, items, parent_callback):
    query = update.callback_query
    media_group = []
    for item in items:
        media_group.append(InputMediaPhoto(media=item["photo"], caption=f"{item['description']}\n\nاضغط شراء لطلب هذا المنتج"))
    context.bot.send_media_group(chat_id=query.message.chat_id, media=media_group)
    
    # زر شراء + زر رجوع
    keyboard = []
    for idx, item in enumerate(items):
        keyboard.append([InlineKeyboardButton(f"شراء {idx+1}", callback_data=f"buy|{parent_callback}|{idx}")])
    keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة السابقة", callback_data=f"back|{parent_callback}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=query.message.chat_id, text="اختار:", reply_markup=reply_markup)
    query.answer()

# ---------------------------------------------------------
# التعامل مع الأزرار
# ---------------------------------------------------------
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data
    query.answer()
    
    if query_data.startswith("section|"):
        section_name = query_data.split("|")[1]
        subsections = sections[section_name]["subsections"]
        keyboard = []
        for subsec in subsections:
            keyboard.append([InlineKeyboardButton(subsec, callback_data=f"subsec|{section_name}|{subsec}")])
        keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"اختر القسم الفرعي من {section_name}:", reply_markup=reply_markup)
    
    elif query_data.startswith("subsec|"):
        _, section_name, subsec_name = query_data.split("|")
        items = sections[section_name]["subsections"][subsec_name]
        show_images(update, context, items, parent_callback=f"subsec|{section_name}")
    
    elif query_data.startswith("buy|"):
        _, parent_callback, idx = query_data.split("|")
        section_key, subsec_name = parent_callback.split("|")[1], parent_callback.split("|")[2]
        item = sections[section_key]["subsections"][subsec_name][int(idx)]
        text = f"طلب جديد: {item['description']}\nرابط المنتج: {item['photo']}"
        wa_link = WHATSAPP_URL + text.replace(" ", "%20")
        context.bot.send_message(chat_id=query.message.chat_id, text=f"اضغط هنا لإرسال الطلب على واتساب:\n{wa_link}")
    
    elif query_data.startswith("back|"):
        _, parent_callback = query_data.split("|")
        if parent_callback == "main":
            start(update, context)
        else:
            section_name = parent_callback.split("|")[1]
            subsections = sections[section_name]["subsections"]
            keyboard = []
            for subsec in subsections:
                keyboard.append([InlineKeyboardButton(subsec, callback_data=f"subsec|{section_name}|{subsec}")])
            keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(f"اختر القسم الفرعي من {section_name}:", reply_markup=reply_markup)
    
    elif query_data == "main":
        start(update, context)

# ---------------------------------------------------------
# تشغيل البوت
# ---------------------------------------------------------
def main():
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        print("Error: TOKEN environment variable is not set.")
        return
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
