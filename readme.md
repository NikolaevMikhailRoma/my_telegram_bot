# Telegram Bot with Watchdog and Llama3 Model

This repository contains code for a Telegram bot that interacts with users via text and voice messages. The bot is built with `python-telegram-bot` library and uses a Llama3 model for generating responses. Additionally, a `watchdog` script is included to monitor changes in the code and automatically restart the bot.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)
  - [watchdog_script.py](#watchdog_scriptpy)
  - [bot_main.py](#bot_mainpy)
  - [llama3.py](#llama3py)

## Installation

To run this project, ensure you have Python 3.11+ and pip installed. Clone the repository and navigate to the project directory. Then, install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. **Environment Variables:**
   Create a `.env` file in the root of your project and add your Telegram bot token:
   ```sh
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

2. **Running the Watchdog Script:**
   To start the `watchdog_script.py`, which will monitor your bot code for changes and restart it upon modification, run:
   ```bash
   python watchdog_script.py
   ```

3. **Running the Bot:**
   Alternatively, you can run the bot directly without the watchdog script:
   ```bash
   python bot_main.py
   ```

## Files

### requirements.txt

This file should contain the required dependencies for running the project. You need to add these dependencies manually as it was not provided in the snippets:
```text
python-telegram-bot
python-dotenv
watchdog
torch
```

### watchdog_script.py

This script uses the `watchdog` library to monitor file changes in the specified directory. If any Python files are modified, it automatically restarts the bot.

```python
import subprocess
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
        self.restart_bot()

    def restart_bot(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(['python', self.script_name])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f'{event.src_path} has been modified, restarting bot...')
            self.restart_bot()

if __name__ == "__main__":
    path = "."
    script_name = "bot_main.py"
    event_handler = ChangeHandler(script_name)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f'Started watching for changes in {path}')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```


### bot_main.py

The main bot script. It handles different types of events and messaging using `python-telegram-bot` library.

```python
import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
from llama3 import simple_diolog

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def calculate_answer(message: str, user_id: int, update: Update = None) -> str:
    bot_answer = simple_diolog(user_message=message)
    print(f'BOT_MESSAGE: {bot_answer}')
    return bot_answer

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    response = 'starting_message'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=ReplyKeyboardRemove())
    logging.info(f"Started dialogue with user {user_id}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_message = update.message.text
    response = calculate_answer(user_message, user_id, update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=ReplyKeyboardRemove())
    logging.info(f"User {user_id} said: {user_message}")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I received your audio recording!", reply_markup=ReplyKeyboardRemove())
    logging.info(f"User {user_id} sent an audio recording.")

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    response = 'ending_message'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=ReplyKeyboardRemove())
    logging.info(f"Ended dialogue with user {user_id}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("end", end))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.run_polling()

if __name__ == '__main__':
    main()
```

### llama3.py

This script handles the Llama3 model, loading it either from a local directory or downloading it if it’s not available locally.

```python
import os
import pickle
from mlx_lm import load, generate

models_dir = './models'
llama3_model_name = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"
local_llama3_model_path = os.path.join(models_dir, llama3_model_name)

def save_object(obj, path):
    with open(path, 'wb') as file:
        pickle.dump(obj, file)

def load_object(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

llama3_model_file = os.path.join(local_llama3_model_path, 'llama3_model.pkl')
llama3_tokenizer_file = os.path.join(local_llama3_model_path, 'llama3_tokenizer.pkl')

if os.path.exists(llama3_model_file) and os.path.exists(llama3_tokenizer_file):
    llama3_model = load_object(llama3_model_file)
    _, llama3_tokenizer = load(llama3_model_name)
    print(f"llama3_model and tokenizer loaded from local directory: {local_llama3_model_path}")
else:
    llama3_model, llama3_tokenizer = load(llama3_model_name)
    print(f"llama3_model downloaded: {llama3_model_name}")
    os.makedirs(local_llama3_model_path, exist_ok=True)
    save_object(llama3_model, llama3_model_file)
    save_object(llama3_tokenizer, llama3_tokenizer_file)
    print(f"llama3_model and tokenizer saved locally to: {local_llama3_model_path}")

def simple_diolog(model=llama3_model, tokenizer=llama3_tokenizer, chatbot_role="You are a test_machine", user_message='Say something'):
    messages = [
        {"role": "system", "content": chatbot_role},
        {"role": "user", "content": user_message}
    ]
    input_ids = llama3_tokenizer.apply_chat_template(messages, add_generation_prompt=True)
    prompt = tokenizer.decode(input_ids)
    response = generate(model, tokenizer, max_tokens=1024, prompt=prompt)
    return response

def main():
    chatbot_role = "You are a test_machine"
    question = "Say something"
    messages = [
        {"role": "system", "content": chatbot_role},
        {"role": "user", "content": question}
    ]
    input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
    prompt = tokenizer.decode(input_ids)
    response = generate(llama3_model, tokenizer, max_tokens=1024, prompt=prompt)
    print(response)

if __name__ == '__main__':
    print(simple_diolog())
```

## Contributing

Feel free to open issues or submit pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
