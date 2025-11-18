import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# رقم واتسابك
WHATSAPP_NUMBER = "201288846355"  # ضع رقمك هنا بدون +
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUMBER}?text="

# بيانات الأقسام والقوائم الفرعية والمنتجات
sections = {
    "💍💍 صواني شبكة": {
        "subsections": {
            "صواني شبكة اكليريك": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف1"},
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف2"}
            ],
            "صواني شبكة خشب": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف3"}
            ]
        }
    },
    "💍 طارات خطوبة وكتب الكتاب": {
        "subsections": {
            "طارات خطوبة وكتب الكتاب اكليريك": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف4"}
            ],
            "طارات خطوبة وكتب الكتاب خشب": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف5"}
            ]
        }
    },
    "✋ بصامات": {
        "subsections": {
            "بصامات": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف6"}
            ],
            "مناديل كتب الكتاب": [
                {"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف7"}
            ]
        }
    },
    "🗄️ هرم مكتب": {
        "subsections": {
            "هرم مكتب اكليريك": [{"photo": "https://png.pngtree.com/png-vector/20230531/ourmid/pngtree-banana-coloring-page-vector-png-image_6787674.png", "description": "وصف8"}],
            "هرم مكتب بديل المعدن": [{"photo": "https://png.pngtree.com/png-vector/202]()
