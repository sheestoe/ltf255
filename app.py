from flask import Flask, request
import telegram
import telegram.ext as ext
import os
from telebot.mastermind import get_response

global bot
global TOKEN
TOKEN = os.environ['BOT_TOKEN']
URL = os.environ['URL']
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    # get the chat_id to be able to respond to the same user
    chat_id = update.message.chat.id
    # get the message id to be able to reply to this specific message
    msg_id = update.message.message_id
    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
    # here we call our super AI
    response = get_response(text)
    # now just send the message back
    # notice how we specify the chat and the msg we reply to
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
    main()
    return 'ok'


async def start(update: telegram.Update, context: ext.ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            telegram.InlineKeyboardButton("Option 1", callback_data="1"),
            telegram.InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [telegram.InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: telegram.Update, context: ext.ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")


async def help_command(update: telegram.Update, context: ext.ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = ext.Application.builder().token("TOKEN").build()

    application.add_handler(ext.CommandHandler("start", start))
    application.add_handler(ext.CallbackQueryHandler(button))
    application.add_handler(ext.CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    print('testing webhook')
    print('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    print('after webhook')
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
   app.run(threaded=True)