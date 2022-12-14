from flask import Flask, request
import telegram
import os
from telebot.mastermind import get_response
from telebot.inline_keyboard import main

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

    # keyboard = [
    # [
    #     telegram.InlineKeyboardButton("" + str(x), callback_data="{}".format(x)) for x in range(1,6)  
    # ],
    # [
    #     telegram.InlineKeyboardButton("" + str(x), callback_data="{}".format(x)) for x in range(6,11)
    # ],
    # [
    #     telegram.InlineKeyboardButton("" + str(x), callback_data="{}".format(x)) for x in range(11,16)
    # ],
    # [
    #     telegram.InlineKeyboardButton("" + str(x), callback_data="{}".format(x)) for x in range(16,21)
    # ],
    # [
    #     telegram.InlineKeyboardButton("" + str(x), callback_data="{}".format(x)) for x in range(21,26)
    # ]]

    # reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    # update.message.reply_text("Please choose:", reply_markup=reply_markup)
    
    # # query = update.callback_query
    # # query.answer()
    # # query.edit_message_text(text=f"Selected option: {query.data}")

    # #bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
    main()
    print(response)
    return 'ok'

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
        return "webhook setup ok!"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
   app.run(threaded=True)