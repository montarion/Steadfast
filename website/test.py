# from https://realpython.com/using-flask-login-for-user-management-with-flask/#the-flask-ecosystem
from flask import Flask
from flask_login import LoginManager, login_required, UserMixin, login_user
from forms import ContactForm

class User():
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    name = "admin" # name of user
    password = "admin" # encrypted password from database
    authenticated = True # check if password is correct

    def is_active(self):
        """True, as all users are active."""
        return False

    def get_id(self):
        """Return the name to satisfy Flask-Login's requirements."""
        return self.name

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return False

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False



app = Flask(__name__)
user = User()


login = LoginManager()
login.init_app(app)

def check_login(formdata):
    name = formdata.name
@login.user_loader
def user_loader(name):
    return user

@app.route("/")
@login_required
def hello():
    person = user.name
    return "Hello {}!".format(person)

@app.route("/login")
def login():
    login_user(user)
    person = user.name
    return "You're now logged in, {}".format(person)


