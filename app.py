from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app =Flask(__name__)

# config MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '3094'
app.config['MYSQL_DB'] = 'blogapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init mysql
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blogs')
def blogs():

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM blogs")

    blogs = cur.fetchall()

    if result > 0:
        return render_template('/blogs.html',blogs=blogs)

    else:
        msg = 'No blogs found'
        return render_template('/blogs.html', msg=msg)


    cur.close()
    return render_template('blogs.html', blogs = Blogs)

@app.route('/blog/<string:id>/')
def blog(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM blogs WHERE id=%s", [id])

    blog = cur.fetchone()
    return render_template('blog.html', id= id , blog=blog)

class RegisterForm(Form):
    name = StringField('Name',[validators.Length (min =1, max =50)])
    username = StringField('Username', [validators.Length(min = 4, max = 25)])
    email = StringField('Email', [validators.Length(min = 6, max = 50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message= 'passwords do not match')
    ])
    confirm = PasswordField('confirm password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method== 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, username, password) VALUES (%s, %s, %s, %s)",(name, email, username, password))

       # commit to DB
        mysql.connection.commit()

       # close connection

        cur.close()

        flash('You are now registered','success')



        return redirect(url_for('login'))
    return  render_template('register.html', form= form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method== 'POST':

        # Get form fields
        username = request.form['username']
        password_candidate = request.form['password']


        #create cursor
        cur = mysql.connection.cursor()

        #username
        result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
        
        if result > 0:

            data = cur.fetchone()
            password = data['password']

            #compare passwords
            if sha256_crypt.verify(password_candidate, password):

                #passed
                session['logged_in']= True
                session['username'] = username

                flash('You are now logged in','Success')
                
                return redirect(url_for('dashboard'))


            else:
                error = 'invalid login'
                return render_template('login.html', error=error)

            cur.close()

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

            

    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('unauthorized please login','danger')
            return redirect(url_for('login'))
    return wrap

@app.route ('/logout')
@is_logged_in
def logout():
    session.clear
    flash("you are now logged out","success")
    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM blogs")

    blogs = cur.fetchall()

    if result > 0:
        return render_template('/dashboard.html',blogs=blogs)

    else:
        msg = 'No blogs found'
        return render_template('/dashboard.html', msg=msg)


    cur.close()


class BlogForm(Form):
    title = StringField('Title',[validators.Length (min =1, max =200)])
    body = TextAreaField('Body', [validators.Length(min = 4)])

@app.route('/add_blog', methods=['GET', 'POST'])

@is_logged_in
def add_blog():
    form = BlogForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        cur = mysql.connection.cursor()

        cur.execute('INSERT INTO blogs(title, body, author) VALUES(%s, %s, %s)', (title, body, session['username']))

        mysql.connection.commit()

        cur.close()

        flash('Blog created','success')

        return redirect(url_for('dashboard'))

    return render_template('add_blog.html', form=form)

@app.route('/delete_blog/<string:id>')
@is_logged_in
def delete_blog(id):
    cur = mysql.connection.cursor()

    cur.execute('DELETE FROM blogs WHERE id =%s', [id])

    mysql.connection.commit()

    cur.close()


    flash('Blog Deleted','success')

    return redirect(url_for('dashboard'))





@app.route('/edit_blog/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_blog(id):
    #create cursor
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM blogs WHERE id = %s", [id])

    blog = cur.fetchone()


    form = BlogForm(request.form)

    form.title.data = blog['title']
    form.title.data = blog['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        cur = mysql.connection.cursor()

        cur.execute("UPDATE blogs SET title=%s, body=%s WHERE id = %s", (title, body, id))

        mysql.connection.commit()

        cur.close()

        flash('Blog Updated','success')

        return redirect(url_for('dashboard'))

    return render_template('edit_blog.html', form=form)

if __name__ == '__main__':
    app.secret_key='1234'
    app.run(debug = True)