# --- Full Telegram Bot Code with "بوكس كتب الكتاب" Feature ---
# NOTE: Replace YOUR_BOT_TOKEN and whatsapp_number before running.

from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler
)

# States
ENTER_NAMES = range(1)

############################################################
#                     MAIN MENU                            #
############################################################

def main_menu(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("محافظ")],
        [KeyboardButton("أقلام")],
        [KeyboardButton("ميداليات")],
        [KeyboardButton("علب هدايا")],
        [KeyboardButton("مناديل كتب الكتاب")],
        [KeyboardButton("بوكس كتب الكتاب")],  # NEW BUTTON
        [KeyboardButton("فوانيس رمضان")],
        [KeyboardButton("رجوع")]
    ]

    update.message.reply_text(
        "اختار القسم:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

############################################################
#                 BOOK BOX MAIN MENU                       #
############################################################

def book_box_menu(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    keyboard = [
        [InlineKeyboardButton("بوكس فضي", callback_data="box_silver")],
        [InlineKeyboardButton("بوكس ذهبي", callback_data="box_gold")],
        [InlineKeyboardButton("رجوع", callback_data="back_to_main")]
    ]

    context.bot.send_message(
        chat_id,
        "اختر شكل بوكس كتب الكتاب:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

############################################################
#                    SHOW PRODUCTS                         #
############################################################

def show_box_silver(update, context):
    query = update.callback_query
    query.answer()

    context.user_data['selected_product'] = "بوكس كتب الكتاب – فضي"

    photo = "https://via.placeholder.com/500x500?text=بوكس+فضي"

    caption = (
        "📦 *بوكس كتب الكتاب – فضي*\n"
        "• شكل مميز\n"
        "• خامات ممتازة\n"
        "السعر: 250 جنيه\n"
    )

    keyboard = [
        [InlineKeyboardButton("إدخال اسم العروسة والعريس", callback_data="enter_names")],
        [InlineKeyboardButton("رجوع", callback_data="back_book_box_menu")]
    ]

    query.message.reply_photo(
        photo=photo,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


def show_box_gold(update, context):
    query = update.callback_query
    query.answer()

    context.user_data['selected_product'] = "بوكس كتب الكتاب – ذهبي"

    photo = "https://via.placeholder.com/500x500?text=بوكس+ذهبي"

    caption = (
        "📦 *بوكس كتب الكتاب – ذهبي*\n"
        "• شكل فاخر\n"
        "• خامات عالية الجودة\n"
        "السعر: 300 جنيه\n"
    )

    keyboard = [
        [InlineKeyboardButton("إدخال اسم العروسة والعريس", callback_data="enter_names")],
        [InlineKeyboardButton("رجوع", callback_data="back_book_box_menu")]
    ]

    query.message.reply_photo(
        photo=photo,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

############################################################
#                   ENTER NAMES STEP                       #
############################################################

def enter_names_screen(update, context):
    query = update.callback_query
    query.answer()

    query.message.reply_text(
        "يرجى إدخال اسم العروسة والعريس في رسالة واحدة:\n\nمثال: أحمد و سلمى",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="back_book_box_menu")]
        ])
    )

    return ENTER_NAMES


def save_names(update: Update, context: CallbackContext):
    names = update.message.text
    context.user_data['couple_names'] = names

    whatsapp_number = "201000000000"  # ← ضع رقمك

    product = context.user_data.get('selected_product', 'غير محدد')

    message = f"طلب جديد:\nالمنتج: {product}\nالعروسة والعريس: {names}"

    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message}"

    keyboard = [
        [InlineKeyboardButton("إرسال الطلب على واتساب", url=whatsapp_url)],
        [InlineKeyboardButton("رجوع", callback_data="back_book_box_menu")]
    ]

    update.message.reply_text(
        "اضغط لإرسال الطلب:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return ConversationHandler.END

############################################################
#                      HANDLERS                            #
############################################################

def callback_handler(update, context):
    data = update.callback_query.data

    if data == "box_silver":
        return show_box_silver(update, context)

    if data == "box_gold":
        return show_box_gold(update, context)

    if data == "enter_names":
        return enter_names_screen(update, context)

    if data == "back_book_box_menu":
        return book_box_menu(update.callback_query, context)

    if data == "back_to_main":
        update.callback_query.answer()
        update.callback_query.message.reply_text("رجعناك للقائمة الرئيسية ✔️")
        return main_menu(update.callback_query, context)

############################################################
#                    MAIN STARTUP                          #
############################################################

def start(update: Update, context: CallbackContext):
    main_menu(update, context)


def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    # Conversation for entering names
    conv_handler = ConversationHandler(
        entry_points=[],

        states={
            ENTER_NAMES: [MessageHandler(Filters.text & ~Filters.command, save_names)],
        },

        fallbacks=[],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex("^بوكس كتب الكتاب$"), book_box_menu))
    dp.add_handler(CallbackQueryHandler(callback_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()