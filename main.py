from flask import Flask,render_template,request,redirect
import sqlite3 as sql
from discord_webhook import DiscordWebhook
from datetime import datetime,timedelta

app = Flask(__name__)

conn = sql.connect("devops.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS discord(message VARCHAR(100))''')
conn.commit()
webhook_url = 'https://discord.com/api/webhooks/1293218016137314445/pboguFB-u44G0XchzTXpB9phZvkiu-9vX_bAxx37iPKtQ9FSKy5BvWzWjPfRowdzX4V6'

def connection():
    conn = sql.connect('devops.db')
    conn.row_factory = sql.Row
    return conn

@app.route('/get',methods=['POST'])
def get():
    message = request.form['message']
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO discord (message) VALUES (?)', (message,))
    conn.commit()
    conn.close()
    discord(message)
    return redirect('/')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/messages', methods=['GET'])
def get_messages():
    conn = connection()
    cursor = conn.cursor()
    thirty_minutes_ago = datetime.now() - timedelta(minutes=30)
    cursor.execute('SELECT message, timestamp FROM discord WHERE timestamp >= ?', (thirty_minutes_ago,))
    rows = cursor.fetchall()
    conn.close()
    return render_template('messages.html', messages=rows)


def discord(message):
   webhook = DiscordWebhook(url = webhook_url,content=message)
   res = webhook.execute()
   print(res)

if __name__ == "__main__":
    app.run()