from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_ID

# एडमिन की ऑनलाइन स्थिति को ट्रैक करने के लिए एक सरल तरीका
admin_online = False 

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start कमांड पर यूजर को जवाब देता है, परिचय और एडमिन की स्थिति बताता है।"""
    user_name = update.message.from_user.first_name
    
    # --- नया परिचय मैसेज ---
    intro_message = '🤝 **यह बॉट आपको सीधे एडमिन से संपर्क करने में मदद करता है।**\n\n'
    # -----------------------

    if admin_online:
        # अगर एडमिन ऑनलाइन है
        status_message = (
            f'नमस्ते {user_name}! 😊\n'
            'एडमिन अभी **ऑनलाइन** हैं। आप अपना मैसेज भेज सकते हैं, वह जल्द ही जवाब देंगे।'
        )
    else:
        # अगर एडमिन ऑनलाइन नहीं है
        status_message = (
            f'नमस्ते {user_name}! 🥺\n'
            '**क्षमा करें, एडमिन अभी ऑनलाइन नहीं हैं।** '
            'ऑनलाइन आते ही वह आपको **जल्द ही मैसेज** करेंगे।\n\n'
            'आप चाहें तो अपनी बात यहाँ छोड़ सकते हैं, वह बाद में देखेंगे।'
        )
        
    await update.message.reply_text(
        intro_message + status_message,
        parse_mode='Markdown' # बोल्ड टेक्स्ट के लिए Markdown का उपयोग करें
    )


async def message_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    एडमिन की ऑनलाइन स्थिति को बदलने के लिए एक डेवलपर कमांड। 
    इसे केवल एडमिन ही इस्तेमाल कर सकते हैं।
    """
    global admin_online
    
    # यह चेक करता है कि कमांड चलाने वाला व्यक्ति एडमिन है या नहीं।
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("माफ करें, आप यह कमांड इस्तेमाल नहीं कर सकते।")
        return
    
    # कमांड के बाद का तर्क (argument) लेता है, जैसे /message_admin online
    if not context.args or context.args[0].lower() not in ['online', 'offline']:
        await update.message.reply_text("कृपया सही स्थिति बताएं: /message_admin online या /message_admin offline")
        return

    new_status = context.args[0].lower()
    
    if new_status == 'online' and not admin_online:
        admin_online = True
        await update.message.reply_text("✅ एडमिन अब **ऑनलाइन** हैं! सभी यूजर्स को सूचित किया जा रहा है।")
        
    elif new_status == 'offline' and admin_online:
        admin_online = False
        await update.message.reply_text("❌ एडमिन अब **ऑफलाइन** हैं।")

    elif new_status == 'online' and admin_online:
        await update.message.reply_text("एडमिन पहले से ही ऑनलाइन हैं।")

    elif new_status == 'offline' and not admin_online:
        await update.message.reply_text("एडमिन पहले से ही ऑफलाइन हैं।")


def main() -> None:
    """बॉट्स को शुरू करने का मुख्य फंक्शन।"""
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # कमांड हैंडलर्स जोड़ें
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("message_admin", message_admin_command))

    # बॉट को पोलिंग मोड में शुरू करें
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
  
