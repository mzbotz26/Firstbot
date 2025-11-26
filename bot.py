# bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, BOT_INFO

# --- Command Handlers ---

async def start_command(update: Update, context):
    """Handles the /start command. Sends the BOT_INFO."""
    # update.effective_chat.id वह ID है जहाँ से मैसेज आया है
    await update.effective_chat.send_message(
        text=BOT_INFO,
        parse_mode='Markdown' # Markdown formatting के लिए
    )

# --- Message Handler ---

async def handle_message(update: Update, context):
    """Handles any non-command text message and replies 'Hello!'."""
    user_message = update.message.text
    
    # Check if the user's message is the bot's name (optional: to handle mentions)
    # या आप केवल 'if True:' का उपयोग करके हर संदेश पर हेलो भेज सकते हैं
    
    # Bot 'Hello!' reply logic
    await update.message.reply_text(
        text="Hello!",
        quote=True # Original message को कोट करते हुए रिप्लाई करें
    )

# --- Main Setup ---

def main():
    """Starts the bot."""
    # 1. Application Builder: BOT_TOKEN का उपयोग करके एप्लिकेशन सेट करें
    application = Application.builder().token(BOT_TOKEN).build()

    # 2. Register Handlers: कमांड्स और मैसेज के लिए फ़ंक्शन्स को रजिस्टर करें
    # /start कमांड के लिए
    application.add_handler(CommandHandler("start", start_command))
    
    # किसी भी टेक्स्ट मैसेज (जो कमांड नहीं है) के लिए
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # 3. Start Polling: बॉट को सक्रिय करें और मैसेज के लिए सुनना शुरू करें
    print("Bot is starting... Press Ctrl+C to stop.")
    application.run_polling(poll_interval=3) # हर 3 सेकंड में नए मैसेज के लिए चेक करें

if __name__ == '__main__':
    main()
