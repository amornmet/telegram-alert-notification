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
        result = message['evalMatches']
        for data in result :
          ruleName = str(message['ruleName'])
          value = float(data['value'])
          value = "{:.2f}".format(value)
          host = str(data['tags']['host'])
          msg += ('\n[ ALERTING ] '+  str(ruleName) + '\n' + 'msg : '+ str(message['message']) + '\n' + 'host : '+ str(host) + '\n' + 'value : '+ str(value) + ' % ' + '\n')
      if state == 'ok' :
          msg += ('[ OK ] '+ str(message['ruleName']) + '\n' + 'msg : ' + str(message['message']) + '\n')

      bot.sendMessage(chat_id=chat_id, text=msg)
      return str("OK")
    except Exception as error:
      return error.message

@app.route('/server' , methods=['GET'])
def server():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True,threaded=True)

#@app.route('/alertOpenstack' , methods=['POST'])
#def index():
#    try:
#      msg = ''
#      message = request.get_json()
#      result = message['alerts']
#      for data in result :
#          status = str(data['status'])
#          zone = "domz1" #str(data['labels']['zone'])
#          severity = str(data['labels']['severity'])
#          alertname = str(data['labels']['alertname'])

#          data_labels = data['labels']
#          if 'instanecs' in data_labels.keys() :
#              instances = str(data['labels']['instanecs'])
#          else:
#              instances = "none"

#          if status == 'resolved' :
#              msg += ('\xF0\x9F\x92\x9A [ OK ] '  + str(zone) +'\n' + 'Alert : '+ str(alertname) + '\n' + 'State : ' +  str(status) + '\n'+ 'Severity : ' + str(severity)  + '\n' + 'Host : ' + str(instances) +'\n\n')
#          else :
#              msg += ('\xF0\x9F\x98\xB1 [ ALERTING ] ' + str(zone) +'\n' + 'Alert : '+ str(alertname) + '\n' + 'State : ' +  str(status) + '\n'+ 'Severity : ' + str(severity) + '\n' + 'Host : ' + str(instances) +'\n\n')

#      bot.sendMessage(chat_id=chat_id, text=msg)#, reply_to_message_id=msg_id)
#      return str("OK")
#    except Exception as error:
#      return error.message

