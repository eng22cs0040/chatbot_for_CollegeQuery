# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request, session, Response
from supportFile import *
import os
import json
import pandas as pd
from datetime import datetime
from autocorrect import Speller
import sqlite3

# 🌍 MULTILINGUAL IMPORTS
from googletrans import Translator
from langdetect import detect

translator = Translator()

# ✅ ALLOWED LANGUAGES
ALLOWED_LANGS = ["en", "hi", "kn"]


# 🌍 Language Functions
def detect_language(text):
    try:
        lang = detect(text)
        if lang not in ALLOWED_LANGS:
            return "en"
        return lang
    except:
        return "en"


def translate_to_english(text):
    try:
        return translator.translate(text, dest='en').text
    except:
        return text


def translate_from_english(text, lang):
    try:
        if lang not in ALLOWED_LANGS:
            lang = "en"
        return translator.translate(text, dest=lang).text
    except:
        return text


# ✅ Default fallback (ONLY 3 LANGUAGES)
def default_response(lang):
    if lang == "hi":
        return "माफ कीजिए! मैं आपका सवाल समझ नहीं पाया। कृपया कोर्स, प्रवेश या फीस के बारे में पूछें।"
    elif lang == "kn":
        return "ಕ್ಷಮಿಸಿ! ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ನಾನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಕೋರ್ಸ್, ಪ್ರವೇಶ ಅಥವಾ ಶುಲ್ಕ ಬಗ್ಗೆ ಕೇಳಿ."
    else:
        return "Sorry! I didn’t understand your question. Please ask about courses, admission, or fees."


name = ''
num = ''

spell = Speller(lang='en')

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('home.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/bot', methods=['GET', 'POST'])
def bot():
    state = 0
    global name
    global num
    
    if request.method == 'POST':
        if request.form['sub'] == 'Submit':
            state = 1
            name = request.form['name']
            num = request.form['num']
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            con = sqlite3.connect('mydatabase.db')
            cursorObj = con.cursor()
            cursorObj.execute("CREATE TABLE IF NOT EXISTS Users (Date text,Name text,Contact text)")
            cursorObj.execute("INSERT INTO Users VALUES(?,?,?)", (dt_string, name, num))
            con.commit()

        if request.form['sub'] == 'Rate':
            rating = request.form['rate']
            suggestion = request.form['suggestions']
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            con = sqlite3.connect('mydatabase.db')
            cursorObj = con.cursor()
            cursorObj.execute("CREATE TABLE IF NOT EXISTS Feedback (Date text,Name text,Contact text,Ratings text,Feedback text)")
            cursorObj.execute("INSERT INTO Feedback VALUES(?,?,?,?,?)", (dt_string, name, num, rating, suggestion))
            con.commit()
            return redirect(url_for('home'))

    return render_template('bot.html', state=json.dumps(state))


# 🌍 MAIN CHATBOT ROUTE (FIXED)
@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg')

    # 1️⃣ Detect language (restricted)
    lang = detect_language(user_input)

    # 2️⃣ Convert to English
    user_response = translate_to_english(user_input)

    # 3️⃣ Spell correction
    user_response = spell(user_response)
    user_response = user_response.lower()

    botResponse = ''

    if 'bye' not in user_response:
        if ('thank you' in user_response or 
            'thanks' in user_response or 
            'thanx' in user_response or 
            'ty' in user_response):
            
            botResponse = "You are welcome."
        
        else:
            if greeting(user_response) is not None:
                botResponse = greeting(user_response)
            else:
                botResponse = response(user_response)

                # ✅ If no proper answer → fallback
                if not botResponse or "sorry" in botResponse.lower():
                    return default_response(lang)

                if user_response in sent_tokens:
                    sent_tokens.remove(user_response)
    else:
        botResponse = "Bye! Take care."

    # 4️⃣ Translate back ONLY allowed language
    final_response = translate_from_english(botResponse, lang)

    return final_response


@app.route('/unanswered', methods=['GET', 'POST'])
def unanswered():
    df = pd.read_csv('unanswered.txt', delimiter="\n")
    return render_template('unanswered.html',
                           tables=[df.to_html(classes='w3-table-all w3-hoverable')],
                           titles=df.columns.values)


@app.route('/user', methods=['GET', 'POST'])
def user():
    conn = sqlite3.connect('mydatabase.db', isolation_level=None,
                           detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql_query("SELECT * FROM Users", conn)
    return render_template('user.html',
                           tables=[db_df.to_html(classes='w3-table-all w3-hoverable w3-padding')],
                           titles=db_df.columns.values)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    global name
    global num
    if request.method == 'POST':
        rating = request.form['rate']
        suggestion = request.form['suggestions']
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute("CREATE TABLE IF NOT EXISTS Feedback (Date text,Name text,Contact text,Ratings text,Feedback text)")
        cursorObj.execute("INSERT INTO Feedback VALUES(?,?,?,?,?)", (dt_string, name, num, rating, suggestion))
        con.commit()
        return redirect(url_for('home'))

    return render_template('feedback.html')


@app.route('/view_feedback', methods=['GET', 'POST'])
def view_feedback():
    conn = sqlite3.connect('mydatabase.db', isolation_level=None,
                           detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql_query("SELECT * FROM Feedback", conn)
    return render_template('view_feedback.html',
                           tables=[db_df.to_html(classes='w3-table-all w3-hoverable w3-padding')],
                           titles=db_df.columns.values)


# ❌ Disable cache
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)