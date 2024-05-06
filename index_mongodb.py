from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, session,g,app
import psycopg2
import os
from datetime import datetime,timedelta

def connect_to_db():
    # Підключення до MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['']  # Назва бази даних
    return db

#час сесії
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)

#базова директорія
@app.route('/')
def home():
    db = connect_to_db()
    if 'username' in session:
        # Отримання даних користувача
        user_data = db['tbl_users'].find_one({'username': session['username']})
        if user_data:
            return render_template('home.html', 
                                   username=user_data.get('username', ''),
                                   email=user_data.get('email', ''),
                                   join_date=user_data.get('join_date', ''),
                                   address=user_data.get('address', ''),
                                   education=user_data.get('education', ''),
                                   country=user_data.get('country', ''),
                                   state=user_data.get('state', ''),
                                   phone=user_data.get('phone', ''),
                                   firstname=user_data.get('firstname', ''),
                                   lastname=user_data.get('lastname', ''))
    
    return render_template('home.html')

#директорія для логіну
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session:
        if request.method == 'POST':
            username = request.form['username']
            pwd = request.form['password']

            db = connect_to_db()
            user = db['tbl_users'].find_one({'username': username, 'is_deleted': {'$ne': 1}})

            if user and pwd == user.get('password'):
                session['username'] = user['username']
                session['id'] = str(user['_id'])  # Конвертуємо ObjectId в рядок для зберігання у сесії
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error='Invalid username or password')

        return render_template('login.html')
    else:
        return redirect(url_for('home'))