from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from werkzeug.utils import secure_filename
import os
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'xlsx', 'pptx'}


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="college_notices"
)
cursor = conn.cursor(dictionary=True)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        admin = cursor.fetchone()
        if admin:
            user = User(admin['id'])
            login_user(user)
            return redirect(url_for('admin_panel'))
        else:
            flash("Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin_panel():
    search_query = request.args.get('search', '')

    if search_query:
        query = """
            SELECT * FROM notices
            WHERE title LIKE %s OR content LIKE %s
            ORDER BY created_at DESC
        """
        like_pattern = f"%{search_query}%"
        cursor.execute(query, (like_pattern, like_pattern))
    else:
        cursor.execute("SELECT * FROM notices ORDER BY created_at DESC")

    notices = cursor.fetchall()
    return render_template('admin_panel.html', notices=notices, search=search_query)



@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_notice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files['file']
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        cursor.execute("INSERT INTO notices (title, content, filename) VALUES (%s, %s, %s)", (title, content, filename))
        conn.commit()
        return redirect(url_for('admin_panel'))
    return render_template('add_notice.html')

@app.route('/delete/<int:notice_id>')
@login_required
def delete_notice(notice_id):
    cursor.execute("DELETE FROM notices WHERE id = %s", (notice_id,))
    conn.commit()
    return redirect(url_for('admin_panel'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/edit/<int:notice_id>', methods=['GET', 'POST'])
@login_required
def edit_notice(notice_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE notices SET title=%s, content=%s WHERE id=%s", (title, content, notice_id))
        conn.commit()
        return redirect(url_for('admin_panel'))

    cursor.execute("SELECT * FROM notices WHERE id = %s", (notice_id,))
    notice = cursor.fetchone()
    return render_template('edit_notice.html', notice=notice)


if __name__ == '__main__':
    app.run(port=5002, debug=True)
