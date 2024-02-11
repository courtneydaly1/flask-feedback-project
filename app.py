from flask import Flask, render_template, redirect, session
# from flask_debugtoolbar import DebugToolbarExtention
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User, Feedback
from forms import RegisterForm,LoginForm, FeedbackForm, DeleteForm

app= Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "sososoSecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar= DebugToolbarExtention(app)

connect_db(app)
app.app_context().push()

db.create_all()


@app.route('/')
def homepage():
    """Homepage. Redirects user to register if not signed in"""
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """register a new user. Show form and handle submissions"""
    if 'username' in session:
        return redirect(f"/users/{session['username']}")
    form= RegisterForm()
    
    if form.validate_on_submit():
        username= form.username.data
        password= form.password.data
        first_name= form.first_name.data
        last_name=form.last_name.data
        email=form.email.data
        
        user= User.register(username, password, first_name, last_name, email)
        
        db.session.commit()
        session['username']= user.username
        
        return redirect(f"/users/{user.username}")
    else:
        return render_templete('users/register.html', form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show login form and handle inputs"""
    
    if 'username' in sessions:
        return redirect(f"/users/{session['username']}")
    
    form =LoginForm()
    
    if form.validate_on_submit():
        username= form.username.data
        password= form. password.data
        
        user= User.authenticate(username, password)
        if user:
            session['username']= user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username/password. Check your spelling and try again.']
            return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Logs a user out. Redirects to login page"""
    
    session.pop('username')
    return redirect('/login')
    
    @app.route('/users/<username>')
    def show_user(username):
        """Page for logged in users"""
        
        if 'username' not in  session or username !=session['username']:
            raise Unauthorized()
        
        user= user.query.get(username)
        form= DeleteForm()
        
        return render_template('users/show.html', user=user, form=form)
    
    @app.route('/users/<username>/delete', methods= ["POST"])
    def delete_user(username):
        """deletes user and then redirects user to login"""
        
        if 'username' not in session or username != session['username']:
            raise Unauthorized()
        
        user= User.query.get(username)
        db.session.delet(username)
        db.session.commit()
        
        session.pop('username')
        
        return redirect('/login') 
    
     