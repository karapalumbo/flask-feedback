from flask import Flask, render_template, redirect, session, flash
# from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import UserForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "seecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

# toolbar = DebugToolbarExtension(app)


@app.route('/')
def homepage():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data 
        email = form.email.data 
        first_name = form.first_name.data 
        last_name = form.last_name.data

        user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        return redirect('/secret')

    else:
        return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect('/secret')
        else:
            form.username.errors = ['Invalid username and/or password.']

    return render_template('login.html', form=form)


@app.route('/secret')
def secret():
    return render_template('secret.html')
    

# @app.route('/logout')
# def logout_user():
#     session.pop('user_id')
#     flash("Goodbye!", "info")
#     return redirect('/')

