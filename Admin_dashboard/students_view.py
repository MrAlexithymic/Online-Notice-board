from flask import Flask, render_template, request, send_from_directory
import mysql.connector


app = Flask(__name__)

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="college_notices"
)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def index():
    keyword = request.args.get('search', '')
    if keyword:
        cursor.execute("SELECT * FROM notices WHERE title LIKE %s OR content LIKE %s ORDER BY created_at DESC",
                       (f"%{keyword}%", f"%{keyword}%"))
    else:
        cursor.execute("SELECT * FROM notices ORDER BY created_at DESC")
    notices = cursor.fetchall()

    return render_template('index.html', notices=notices)



UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
