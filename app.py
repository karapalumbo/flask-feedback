from flask import Flask, render_template, redirect, session, flash
# from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

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

        user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username

        return redirect(f'/users/{user.username}')

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
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username and/or password.']
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)



@app.route('/users/<username>', methods=['GET', 'POST'])
def show_user(username):
    if "username" not in session:
        flash("You must be logged in.", "danger")
        return redirect('/')
    else:
        user = User.query.get(username)
        feedback = Feedback.query.all()
        return render_template('user.html', user=user, feedback=feedback)
    

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user():

    if "username" not in session:
        flash("You do not have permission to delete a user.", "danger")
        return redirect('/')

    else:
        db.session.delete(user)
        db.session.commit()
        session.pop("username")

        return redirect("/")


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):

    if "username" not in session:
        flash("Please login or register to add feedback.", "danger")
        return redirect('/')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data 
        content = form.content.data 

        feedback = Feedback(
            title=title, 
            content=content, 
            username=username
        )

        db.session.add(feedback)
        db.session.commit() 

        return redirect(f"/users/{username}")

    else:
        return render_template('feedback.html', form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=['GET', 'POST'])
def update_feedback(feedback_id):

    if "username" not in session:
        flash("Please login or register to update feedback.", "danger")
        return redirect('/')

    feedback = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data 
        feedback.content = form.content.data 

        db.session.commit()

        return redirect(f'/users/{feedback.username}')
    
    return render_template("edit.html", form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session:
        flash("Please login or register to delete feedback.", "danger")
        return redirect('/')

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")


@app.route('/logout')
def logout_user():
    session.pop('username')
    return redirect('/')

