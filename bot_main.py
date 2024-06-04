import logging
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
from llama3 import simple_diolog


# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Retrieve the Telegram Bot Token from environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

### ititializate_llama


# Function to handle dialogue and generate responses
def calculate_answer(message: str, user_id: int, update: Update = None) -> str:

    bot_answer = simple_diolog(user_message=message)
    print(f'BOT_MESSAGE: {bot_answer}')
    return bot_answer

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    response = 'stariting_message'
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        reply_markup=ReplyKeyboardRemove()  # Remove buttons
    )
    logging.info(f"Started dialogue with user {user_id}")

# Handler for text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_message = update.message.text
    response = calculate_answer(user_message, user_id, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        reply_markup=ReplyKeyboardRemove()  # Remove buttons here just in case
    )
    logging.info(f"User {user_id} said: {user_message}")

# New handler for audio messages
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I received your audio recording!",
        reply_markup=ReplyKeyboardRemove()  # Remove buttons if any
    )
    logging.info(f"User {user_id} sent an audio recording.")

# Handler for the /end command
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    response = 'ending_message'
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        reply_markup=ReplyKeyboardRemove()  # Remove buttons
    )
    logging.info(f"Ended dialogue with user {user_id}")

# Main function to set up and start the bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers for commands and messages
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("end", end))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # Start polling for updates
    app.run_polling()

# Entry point for the script
if __name__ == '__main__':
    main()