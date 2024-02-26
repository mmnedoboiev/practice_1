from flask import Flask, render_template, request, redirect, url_for, session,g
import psycopg2
import os
from datetime import datetime

app = Flask(__name__,static_url_path="/static")

#значення використовується для захисту від зміни даних сесії користувача з боку клієнта
app.secret_key = os.urandom(24) 

#Конект до бази та використання flask об'єкта G. він викор. для зберігання глоб. змінних протягом одного запиту. + безпека
def connect_to_db():
    if 'db_connection' not in g:
        g.db_connection = psycopg2.connect(
            dbname="db",
            user="root",
            password="root",
            host="192.168.0.165",
            port="5435"
        )
    return g.db_connection

#декоратор, який викликається в кінці щоб завершити з'єднання з базою
@app.teardown_appcontext
def close_db_connection(exception=None):
    db_connection = g.pop('db_connection', None)
    if db_connection is not None:
        db_connection.close()

#базова директорія
@app.route('/')
def home():
    conn = connect_to_db()
    if 'username' in session:
        cur = conn.cursor()
        cur.execute("SELECT username, email, join_date,address,education,country,state,phone,firstname,lastname FROM tbl_users WHERE username = %s", (session['username'],))
        user_data = cur.fetchone()  # Отримуємо дані користувача
        cur.close()
        return render_template('home.html', username=user_data[0], email=user_data[1],join_date=user_data[2],address=user_data[3],
                               education=user_data[4],country=user_data[5],state=user_data[6],phone=user_data[7],lastname=user_data[8],firstname=user_data[9])   # Передаємо дані користувача у шаблон
    return render_template('home.html')

#Оновлення інформації на формі користувача
@app.route('/update',methods=['GET', 'POST'])
def updateInfo():
    if 'username' in session:
        if request.method == 'POST':
            conn = connect_to_db()
            cur = conn.cursor()
            user_id = session['id']
            # Отримання даних з форми
            lastname = request.form['lastname']
            firstname = request.form['firstname']
            phone = request.form['phone']
            address = request.form['address']
            education = request.form['education']
            country = request.form['country']
            state = request.form['state']
        # Виконуємо запит UPDATE для оновлення інформації користувача
            if lastname is not None and firstname is not None:
                cur.execute("UPDATE tbl_users SET lastname = %s, firstname = %s WHERE id = %s",
                    (lastname, firstname,user_id))
                
            if phone is not None:
                cur.execute("UPDATE tbl_users SET phone = %s WHERE id = %s",
                    (phone, user_id))   

            if address is not None:
                cur.execute("UPDATE tbl_users SET address = %s WHERE id = %s",
                    (address, user_id)) 

            if education is not None:
                cur.execute("UPDATE tbl_users SET education  = %s WHERE id = %s",
                    (education, user_id)) 
                
            if country is not None and state is not None:
                cur.execute("UPDATE tbl_users SET country  = %s, state = %s WHERE id = %s",
                    (country,state, user_id)) 
                
                conn.commit()
                cur.close()
                conn.close()              
            return redirect(url_for('home'))
    return render_template('login.html', error='You must be logged in to update your information.')


@app.route('/delete', methods=['GET', 'POST'])
def deleteInfo():
    if 'username' in session:
        conn = connect_to_db()
        cur = conn.cursor()
        user_id = session['id']
        # Виконуємо запит DELETE для видалення інформації користувача
        cur.execute("UPDATE tbl_users SET is_deleted = 1 WHERE id = %s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('logout'))
    else:
        return render_template('login.html', error='You must be logged in to delete your information.')


#директорія для логіну
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session:
        if request.method == 'POST':
            username = request.form['username']
            pwd = request.form['password']

            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("SELECT id, username, password FROM tbl_users WHERE username = %s and is_deleted != 1", (username,))
            user = cur.fetchone()
            cur.close()

            if user and pwd == user[2]:
                session['username'] = user[1]
                session['id'] = user[0]
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error='Invalid username or password')
        return render_template('login.html')
    else:
        return redirect(url_for('home'))
    
#директорія для реєстрації
@app.route('/register',methods=['GET', 'POST'])
def register():
    conn = connect_to_db()
    # Отримання поточної дати
    current_date = datetime.today().strftime('%Y-%m-%d')

    if 'username' not in session:
        if request.method == 'POST':
            username = request.form['username']
            pwd = request.form['password']

            cur = conn.cursor()
            #Перевірка на існування логіна в БД
            cur.execute("SELECT username FROM tbl_users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()
            if user is None:
                cur = conn.cursor()
                cur.execute(f"INSERT INTO tbl_users (username, password, join_date,is_deleted) VALUES ('{username}', '{pwd}', '{current_date}',0)")
                conn.commit()
                cur.close()
            else:
                return render_template('register.html', error='User exist')
            return redirect(url_for('login'))
        return render_template('register.html')
    else:
        return render_template('home.html')


# @app.route('/restore', methods=['GET', 'POST'])
# def restoreAccount():
#     if 'username' not in session:
#         if request.method == 'POST':
#             username = request.form['username']
#             pwd = request.form['password']
#             conn = connect_to_db()
#             cur = conn.cursor()

#             cur.execute("UPDATE tbl_users SET is_deleted = 0 WHERE username = %s and password = %s", (username, pwd))
#             conn.commit()

#             if cur.rowcount > 0:
#                 return redirect(url_for('login'))
#             else:
#                 return render_template('restore.html', error='Failed to restore account.')
#             cur.close()
#             conn.close()
#         return redirect(url_for('logout'))  # Перенаправлення на сторінку виходу
#     else:
#         return render_template('login.html', error='You must be logged in to restore your account.')




#завершення сесії
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))





if __name__ == '__main__':
    app.run(debug=True)