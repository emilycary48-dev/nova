import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler, CommandHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ================= CONFIGURATION =================
# Replace this with your actual bot token
BOT_TOKEN = 8843049433:AAEtj09Opstf9V6OpGHf5yoI31VWPvY6gQ8

# The message you want to send to the user when they request to join
WELCOME_MESSAGE = """
👋 Hello! Thanks for requesting to join our private channel.

📢 **Channel:** GANESH TENNIS ANALYST
📝 **Status:** Your request is pending approval.

⚠️ **Important:** Please wait for the admin to accept your request. 
Once accepted, you will receive all updates here.

🔗 **Website:** www.Dharma247.com
"""

# Optional: Add a button to the message (e.g., Visit Website)
BUTTON_TEXT = "🌐 Visit Website"
BUTTON_URL = "https://www.Dharma247.com"
# =================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    await update.message.reply_text(
        "Hello! I am a bot that sends messages when users request to join private channels.\n"
        "Make sure I am an admin in your channel!"
    )

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function triggers automatically when a user requests to join a channel
    where the bot is an admin.
    """
    join_request = update.chat_join_request
    
    # Get user info
    user = join_request.from_user
    chat = join_request.chat
    
    logging.info(f"New join request from {user.full_name} (ID: {user.id}) for chat {chat.title}")

    # Create the inline button
    keyboard = [
        [InlineKeyboardButton(BUTTON_TEXT, url=BUTTON_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        # Send the private message to the user
        await context.bot.send_message(
            chat_id=user.id,
            text=WELCOME_MESSAGE,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        logging.info(f"Message sent successfully to {user.id}")
        
    except Exception as e:
        # If the user has blocked the bot or privacy settings prevent it, log the error
        logging.error(f"Failed to send message to {user.id}: {e}")

if __name__ == '__main__':
    # Create the Application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))
    
    # This handler listens for Chat Join Requests
    application.add_handler(ChatJoinRequestHandler(handle_join_request))

    # Run the bot
    print("Bot is running...")
    application.run_polling()
