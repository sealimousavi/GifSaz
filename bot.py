import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Get environment variables from Doprax
TOKEN = os.getenv("Y7606766248:AAF7vMiguoJhAyrVp2JvIhOrxX68IVHe-Uo")  # Your Telegram Bot Token
PORT = int(os.environ.get("PORT", 5000))  # Default Flask port

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram bot application
application = Application.builder().token(TOKEN).build()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me two images, and I'll create a fading GIF for you! 😊")

# Handle messages (you can add your image processing logic here)
async def handle_message(update: Update, context: CallbackContext):
    await update.message.reply_text("I received your message! 🚀")

# Flask route to handle Telegram webhooks
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Handle incoming Telegram updates via webhook."""
    update = Update.de_json(request.get_json(), application.bot)
    application.process_update(update)
    return "OK", 200

def main():
    """Start the bot using webhooks."""
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, handle_message))

    # Set webhook
    webhook_url = f"https://{os.getenv('HEROKU_APP_NAME', 'your-doprax-app')}.doprax.com/{TOKEN}"
    application.bot.setWebhook(webhook_url)

    # Start Flask server
    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
