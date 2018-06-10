from flask import Flask, request
import json
import requests
import mongoengine
from models.users import User
from bot import Bot

# ตรง YOURSECRETKEY ต้องนำมาใส่เองครับจะกล่าวถึงในขั้นตอนต่อๆ ไป
global LINE_API_KEY, MONGODB_URL

LINE_API_KEY = "Bearer YOURSECRETKEY"

MONGODB_URL = "mongodb://pongpisit:a1s2d3@ds253960.mlab.com:53960/doctora2zdev"
mongoengine.connect(db='doctorAZdev', host=MONGODB_URL, connectTimeoutMS=30000, socketTimeoutMS=None ,socketKeepAlive=True)


app = Flask(__name__)
bot_client = Bot()


@app.route('/')
def index():
    return 'This is chatbot server.'


@app.route('/bot', methods=['POST'])
def bot():
    # ข้อความที่ต้องการส่งกลับ
    replyStack = list()
       
    # ข้อความที่ได้รับมา
    msg_in_json = request.get_json()
    msg_in_string = json.dumps(msg_in_json)
    
    # Token สำหรับตอบกลับ (จำเป็นต้องใช้ในการตอบกลับ)
    replyToken = msg_in_json["events"][0]['replyToken']
    userId = msg_in_json["events"][0]["source"]["userId"]
    message = msg_in_json["events"][0]["message"]

    response_msg = bot_client.response(userId, message)

    # ทดลอง Echo ข้อความกลับไปในรูปแบบที่ส่งไป-มา (แบบ json)
    reply(replyToken, response_msg)
    
    return('OK',200)


def reply(replyToken, textList):
    # Method สำหรับตอบกลับข้อความประเภท text กลับครับ เขียนแบบนี้เลยก็ได้ครับ
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': LINE_API_KEY
    }
    msgs = []
    for text in textList:
        msgs.append({
            "type":"text",
            "text":text
        })
    data = json.dumps({
        "replyToken":replyToken,
        "messages":msgs
    })
    requests.post(LINE_API, headers=headers, data=data)
    return

if __name__ == '__main__':
    app.run()
