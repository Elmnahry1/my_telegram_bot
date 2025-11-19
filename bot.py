# 1. مُعالج محادثة "ارسال شكل مختلف" (هو المعالج الوحيد الآن)
    custom_design_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(prompt_for_image, pattern='^send_custom_design$')
        ],
        states={
            WAITING_FOR_IMAGE: [
                # المعالج الأول: يستقبل الصورة ويمضي قدماً
                MessageHandler(Filters.photo & ~Filters.command, receive_photo_and_prepare_whatsapp),
                
                # المعالج الثاني: يرفض الرسائل النصية أو المستندات، ويطالب العميل بإرسال صورة
                MessageHandler((Filters.text | Filters.document) & ~Filters.command, 
                               lambda update, context: update.message.reply_text("من فضلك، يجب إرفاق **صورة** التصميم المطلوب فقط للمتابعة.", parse_mode="Markdown")),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(start, pattern='^main_menu$'),
            CommandHandler('start', start),
        ]
    )