# from https://realpython.com/using-flask-login-for-user-management-with-flask/#the-flask-ecosystem
# and https://www.codementor.io/@abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft
from flask import Flask, send_file, render_template, send_from_directory, request
from flask_cors import CORS
#from flask_login import LoginManager, login_required, login_user
import os, sys, json, base64
from datetime import datetime, timedelta
class User(): # for logging users in
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
CORS(app)
app.config["UPLOAD_FOLDER"] = "files/"

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=20) # makes sessions last 20 minutes.
uploadfolder = app.config["UPLOAD_FOLDER"]
staticfolder = "/static/"
imageuploadfolder =  uploadfolder + "images/"
##LOGIN##

#login = LoginManager()
#login.init_app(app)

#def check_login(formdata):
#    name = formdata.name
    
#@login.user_loader
#def user_loader(name):
#    return user

#@app.route("/login")
#def login():
    #check_login
#    login_user(user)
#    person = user.name
#    return "You're now logged in, {}".format(person)

##END OF LOGIN##

@app.route("/")
def hello():
    return "Hello world!"

@app.route('/api/images')
def get_image_list():
    lst = getimagedircontents()
    return str(lst)


@app.route("/test")
def test():
    thin = staticfolder + imageuploadfolder
    return thin

@app.route("/images/<filename>")
#@cross_origin()
def get_image(filename):
    #filename = 'pikayou.png' # get filename by checking /image
    imagelink = staticfolder + imageuploadfolder + filename
    lst = getimagedircontents()
    if filename in lst:
        return render_template("displayimage.html", imagelink=imagelink)
    else:
        return "Not found."

@app.route("/api/images", methods=["POST"])
def upload_image():
    data = json.loads(request.data.decode())

    b64img = data["base-encoded-image"]
    imgdict = get_info(data)
    print(imgdict["image_name"])
    result = save_file(b64img, imgdict["image_name"])
    if result == True:
        # write imgdict to database
        print("saved image.")
        return json.dumps(imgdict)
    return str(result)

@app.route("/api/images/<filename>")
def get_raw_image(filename):
    imagefolder =  app.root_path + staticfolder + imageuploadfolder
    lst = getimagedircontents()
    if filename in lst:
        return send_from_directory(imagefolder, filename)
    else:
        return send_from_directory(app.root_path + staticfolder, "error.png")

def getimagedircontents():
    targetdir = staticfolder + imageuploadfolder
    lst = os.listdir(os.path.join(app.root_path, targetdir[1:]))
    return json.dumps(lst)

def save_file(imgstring, filename):
    try:
        imgdata = base64.b64decode(imgstring)
        filepath = app.root_path + staticfolder + imageuploadfolder
        filename = filepath + filename
        print("Trying to write to: {}".format(filename))
        with open(filename, "wb") as f:
            f.write(imgdata)
            print("Writing to: {}".format(filename))
        print("Finished writing to: {}".format(filename))
        return True
    except Exception as e:
        print(str(e))
        return str(e)

def get_info(data):
    name, ext = data.get("image-name").split(".")
    b64img = data["base-encoded-image"]
    operation = data.get("operation") #data["operation"]
    if not name:
        name = operation
    name = "{}.{}".format(name, ext)
    comments = data.get("comments")
    author = data.get("author")
    imageInfo = data.get("info")
    imgdict = {"image_name": name, "author":author, "operation_name":operation, "comments":comments, "image_info":imageInfo}
    return imgdict
