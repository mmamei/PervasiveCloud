# pip install python-telegram-bot  v13
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from secret import bot_token
import matplotlib.pyplot as plt

data = {}

def welcome(update, context):
    msg = '''Welcome in <b>My Es2 Bot</b>
    Manda il messaggio:
    <b>newdata [city] [valore]</b>, es. newdata reggioemilia 34
    per memorizzare nuovi dati.
    manda il messaggio:
    <b>getdata [city]</b>, es. newdata reggioemilia
    per visualizzare i dati salvati'''
    update.message.reply_text(msg, parse_mode='HTML')

def process_chat(update, context):
    print(context)
    msg = update.message.text.lower()
    if msg.startswith('newdata'):
        cmd,city,valore = msg.split(' ')
        if city in data:
            data[city].append(float(valore))
        else:
            data[city] = [float(valore)]
        update.message.reply_text('dati ricevuti', parse_mode='HTML')
    elif msg.startswith('getdata'):
        cmd, city = msg.split(' ')
        plt.bar(range(len(data[city])), data[city])
        plt.savefig(city + '.png')
        chat_id = update.message.chat.id
        context.bot.send_document(chat_id=chat_id, document=open(city + '.png', 'rb'))
        #update.message.reply_text(str(data[city]), parse_mode='HTML')
    else:
        welcome(update, context)


def main():
   print('bot started')
   upd= Updater(bot_token, use_context=True)
   disp=upd.dispatcher

   disp.add_handler(CommandHandler("start", welcome))
   disp.add_handler(MessageHandler(Filters.regex('^.*$'), process_chat))

   upd.start_polling()
   upd.idle()



if __name__=='__main__':
   main()