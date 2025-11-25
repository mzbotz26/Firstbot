# bot.py

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# config.py से BOT_TOKEN इंपोर्ट करें
from config import BOT_TOKEN

# लॉगिंग सेट करें ताकि आप देख सकें कि क्या हो रहा है
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Handlers ---

# /start कमांड के लिए फ़ंक्शन
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start कमांड मिलने पर एक वेलकम मैसेज भेजता है।"""
    await update.message.reply_text('नमस्ते! मैं आपका Echo Bot हूँ। मुझे कोई मैसेज भेजकर देखें।')

# मुख्य फ़ंक्शन जो आपके लॉजिक को हैंडल करता है
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    यूजर द्वारा भेजे गए टेक्स्ट मैसेज को प्रोसेस करता है।
    
    यदि मैसेज का टेक्स्ट बॉट का username है, तो 'Hello' रिप्लाई करता है।
    अन्यथा, मैसेज को इको (दोहराता) करता है।
    """
    
    # बॉट का username प्राप्त करें (उदाहरण: MyTestBot)
    bot_username = context.bot.username
    user_text = update.message.text
    
    # चेक करें कि क्या यूजर का टेक्स्ट बॉट के username से मेल खाता है (केस-इन-सेंसिटिव)
    if user_text and bot_username and user_text.strip().lower() == '@' + bot_username.lower():
        # यदि यूजर ने बॉट को ही टैग किया है (या सिर्फ username भेजा है)
        await update.message.reply_text('Hello')
    else:
        # किसी अन्य मैसेज के लिए, बस मैसेज को दोहरा दें (Echo)
        logger.info(f"Received message: {user_text}")
        await update.message.reply_text(user_text)

# --- Main Function ---

def main() -> None:
    """बॉट को शुरू करें।"""
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ कृपया config.py में BOT_TOKEN को अपने असली टोकन से बदलें।")
        return

    # बॉट एप्लीकेशन बनाएं
    application = Application.builder().token(BOT_TOKEN).build()

    # कमांड हैंडलर जोड़ें
    application.add_handler(CommandHandler("start", start_command))

    # मैसेज हैंडलर जोड़ें - यह केवल टेक्स्ट मैसेज को प्रोसेस करेगा
    # और उन्हें handle_message फ़ंक्शन पर भेजेगा।
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # बॉट को पोलिंग मोड में शुरू करें (यह लगातार नए मैसेज के लिए चेक करेगा)
    logger.info("🤖 बॉट शुरू हो रहा है...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
