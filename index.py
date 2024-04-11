from flask import Flask, render_template, request, redirect, url_for, session,g,app
import psycopg2
import os
from datetime import datetime,timedelta

app = Flask(__name__,static_url_path="/static")

#значення використовується для захисту від зміни даних сесії користувача з боку клієнта
app.secret_key = os.urandom(24) 

#час сесії
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)

#Конект до бази та використання flask об'єкта G. він викор. для зберігання глоб. змінних протягом одного запиту. + безпека
def connect_to_db():
    if 'db_connection' not in g:
        g.db_connection = psycopg2.connect(
            dbname="",
            user="",
            password="",
            host="",
            port=""
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
            cur.execute("UPDATE tbl_users SET lastname = %s, firstname = %s, phone = %s, address = %s, education = %s, country = %s, state = %s WHERE id = %s",
                    (lastname, firstname, phone, address, education, country, state, user_id))
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

#Отримання нотаток
def get_notes():
    conn = connect_to_db()  # Підключення до БД
    cur = conn.cursor()
    user_id = session['id']
    cur.execute("SELECT id,title,description FROM tbl_notes WHERE user_id= %s", (user_id,))
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return notes
#Вивід нотаток на сторінку notes
@app.route('/notes',methods=['GET','POST'])
def notes():
    username = session.get('username')
    if 'username' not in session:
        
        return redirect(url_for('login'))  # Перенаправлення на сторінку входу, якщо користувач не увійшов у систему
    else:
        notes = get_notes()  # Виклик функції для отримання нотаток з БД
        return render_template('notes.html', notes=notes, username=username)
# Маршрут для видалення нотатки
@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    print("Deleting note with ID:", note_id)
    # Отримати ідентифікатор нотатки, яку потрібно видалити
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tbl_notes WHERE id = %s", (note_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    # Після видалення перенаправити користувача на сторінку з нотатками
    return redirect(url_for('notes'))

# Маршрут для додавання нотатки
@app.route('/add_note', methods=['POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))  # Перенаправлення на сторінку входу, якщо користувач не увійшов у систему
    user_id = session['id']
    note_text = request.form['note_text']  # Отримання тексту нотатки з форми
    note_title = request.form['note_title']# Отримання тексту нотатки з форми

    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tbl_notes (user_id,title,description) VALUES (%s, %s, %s)", (user_id,note_text,note_title))
    conn.commit()
    cur.close()
    conn.close()
    
    # Після додавання перенаправити користувача на сторінку з нотатками
    return redirect(url_for('notes'))

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))