from flask import Flask,request
from credentials import bot_token,chat_id

import logging
import telegram
import requests
import json

logging.basicConfig(level=logging.DEBUG)

global bot, TOKEN
#global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
chat_id = chat_id

app = Flask(__name__)

@app.route('/' , methods=['POST'])
def alertProxmox():
    try:
      msg = ''
      message = request.get_json(force=True)
      state = str(message['state'])
      if state == 'alerting' :
        msg += (str(message['title']) + '\n' + str(message['message']) + '\n')
        result = message['evalMatches']
        for data in result :
          ruleName = str(message['ruleName'])
          value = float(data['value'])
          value = "{:.2f}".format(value)
          host = str(data['tags']['host'])
          msg += ('\n' + str(host) + '\n' + 'value : '+ str(value) + ' % ' + '\n')
      if state == 'ok' :
          msg += str(message['title'] + '\n' + str(message['message']) + '\n')

      bot.sendMessage(chat_id=chat_id, text=msg)
      return str("OK")
    except Exception as error:
      return error.message

@app.route('/server' , methods=['GET'])
def server():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True,threaded=True)
