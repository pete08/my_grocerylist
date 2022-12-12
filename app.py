import sqlite3
from markupsafe import escape
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from email.mime.text import MIMEText
import smtplib
from email.message import EmailMessage



def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'XspB3z/Nyj4VG1g'

@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route("/create", methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash("Title is missing!")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         'WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


@app.route("/sendemail/", methods=['POST'])
def sendemail():
    if request.method == "POST":
        name = request.form['name']
        subject = request.form['Subject']
        email = request.form['_replyto']
        message = request.form['message']
        # Set your credentials
        yourEmail = "skr@gmail.com"
        yourPassword = "$$$$$$"

        # Logging in to our gmail account server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(yourEmail, yourPassword)

        # Sender's and Receiver's email address
        msg = EmailMessage()
        msg.set_content("First Name : "+str(name)
                        +"\nEmail : "+str(email)
                        +"\nSubject : "+str(subject)
                        +"\nMessage : "+str(message))
        msg['To'] = email
        msg['From'] = yourEmail
        msg['Subject'] = subject
  
        # Send the message via our own SMTP server.
        try:
            # sending an email
            server.send_message(msg)
            print("Send")
        except:
            print("Fail to Send")
            pass
              
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)


# @app.route("/aboutme")
# def index():
#    return render_template("index.html")

# @app.route("/projects")
# def index():
#    return render_template("index.html")

# 2022-12-06
# 2. customize
# 3. Find way to add page
# 4. Link to page #2, #3
# 5. 