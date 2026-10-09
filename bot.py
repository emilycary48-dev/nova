import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler, CommandHandler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ================= CONFIGURATION =================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Reads token from Railway Variables

WELCOME_MESSAGE = """
👋 Hello! Thanks for requesting to join our private channel.

📢 **Channel:** GANESH TENNIS ANALYST
📝 **Status:** Your request is pending approval.

⚠️ **Important:** Please wait for the admin to accept your request.
Once accepted, you will receive all updates here.

🔗 **Website:** www.Dharma247.com
"""

BUTTON_TEXT = "🌐 Visit Website"
BUTTON_URL = "https://www.Dharma247.com"
# =================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is alive! Add me as an admin to your channel to see join requests.")

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggers when a user requests to join the channel."""
    join_request = update.chat_join_request
    user = join_request.from_user

    logging.info(f"New join request from {user.full_name} (ID: {user.id})")

    keyboard = [[InlineKeyboardButton(BUTTON_TEXT, url=BUTTON_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=WELCOME_MESSAGE,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        logging.info(f"Message sent successfully to {user.id}")
    except Exception as e:
        logging.error(f"Failed to send message to {user.id}: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(ChatJoinRequestHandler(handle_join_request))

    print("Bot is running...")
    application.run_polling()
