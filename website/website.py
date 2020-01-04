# from https://realpython.com/using-flask-login-for-user-management-with-flask/#the-flask-ecosystem
# and https://www.codementor.io/@abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft
from flask import Flask, send_file, render_template, send_from_directory, request, make_response
from flask_cors import CORS
# from flask_login import LoginManager, login_required, login_user
import os, sys, json, base64
from pprint import pprint
from datetime import datetime, timedelta

from repositories.Repository import Repository
from services.ImageService import ImageService


class User():  # for logging users in
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    name = "admin"  # name of user
    password = "admin"  # encrypted password from database
    authenticated = True  # check if password is correct

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


# Flask App
app = Flask(__name__)
CORS(app)

# Globals
app.config["UPLOAD_FOLDER"] = "files/"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=20)  # makes sessions last 20 minutes.
uploadfolder = app.config["UPLOAD_FOLDER"]
staticfolder = "/static/"
imageuploadfolder = uploadfolder + "images/"

# Repositories
image_repository = None
image_service = None


def get_image_repository():
    """1 repository instance"""
    global image_repository
    if image_repository:
        return image_repository
    else:
        image_repository = Repository('images')
        return image_repository


def get_image_service():
    """1 service instance"""
    global image_service
    if image_service:
        return image_service
    else:
        image_service = ImageService()
        return image_service

# Services
image_service = ImageService(app.root_path, staticfolder, imageuploadfolder)


##LOGIN##

# login = LoginManager()
# login.init_app(app)

# def check_login(formdata):
#    name = formdata.name

# @login.user_loader
# def user_loader(name):
#    return user

# @app.route("/login")
# def login():
# check_login
#    login_user(user)
#    person = user.name
#    return "You're now logged in, {}".format(person)

##END OF LOGIN##

@app.route("/")
def hello():
    return "Hello world!"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/files/images'), 'pikayou.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/api/images')
def get_image_list():
    lst = image_service.getimagedircontents()
    r = make_response(json.dumps(lst))
    r.mimetype = 'application/json'
    return r

@app.route('/api/operations')
def get_operation_names_list():
    lst = get_image_repository().get_all_operation_names()
    r = make_response(json.dumps(lst))
    r.mimetype = 'application/json'
    return r

@app.route('/api/operations/<operation_name>')
def get_operation_image_list(operation_name: str):
    response = get_image_repository().get_by_operation(operation_name)
    r = make_response(json.dumps(response))
    r.mimetype = 'application/json'
    return r


@app.route("/test")
def test():
    thin = staticfolder + imageuploadfolder
    return thin


@app.route("/images/<filename>")
# @cross_origin()
def get_image(filename):
    # filename = 'pikayou.png' # get filename by checking /image
    imagelink = staticfolder + imageuploadfolder + filename
    lst = image_service.getimagedircontents()
    if filename in lst:
        return render_template("displayimage.html", imagelink=imagelink)
    else:
        return "Not found."


@app.route("/api/images", methods=["POST"])
def upload_image():
    data = json.loads(request.data.decode())
    print('POST /api/images, body:')
    pprint(data)
    imgdict, b64img = get_image_service().get_info(data)
    result, filepath = get_image_service().save_file(b64img, imgdict["image_name"])
    # print(b64img)

    if result:
        # write imgdict to database
        # add filepath to dict
        imgdict['image_info']['path_to_file'] = filepath

        get_image_repository().insert(imgdict)

        print("saved image info")
        return json.dumps(imgdict)
    return str(result)


@app.route("/api/images/<filename>")
def get_raw_image(filename):
    imagefolder = app.root_path + staticfolder + imageuploadfolder
    lst = image_service.getimagedircontents()
    if filename in lst:
        return send_from_directory(imagefolder, filename)
    else:
        return send_from_directory(app.root_path + staticfolder, "error.png")

#region old functions
#
# def getimagedircontents():
#     targetdir = staticfolder + imageuploadfolder
#     lst = os.listdir(os.path.join(app.root_path, targetdir[1:]))
#     return json.dumps(lst)
#
#
# def save_file(imgstring, filename):
#     try:
#         imgdata = base64.b64decode(imgstring)
#         # print(type(imgdata))
#         filepath = app.root_path + staticfolder + imageuploadfolder
#         filename = filepath + filename
#         print("Trying to write to: {}".format(filename))
#         with open(filename, "wb") as f:
#             f.write(imgdata)
#             print("Writing to: {}".format(filename))
#         print("Finished writing to: {}".format(filename))
#         return True, filename
#     except Exception as e:
#         print("Couldn't save..")
#         print(str(e))
#         return str(e)
#
#
# def get_info(data):
#     print("**INSIDE GET_INFO**")
#     name, ext = data.get("image_name").split(".")
#     b64img = data["base_encoded_image"].split(",")[1]  # get actual base64 code
#     b64img += "===="  # add padding
#     operation = data.get("operation_name")
#     if not name:
#         name = operation
#     name = "{}.{}".format(name, ext)
#     comments = data.get("comments")
#     author = data.get("author")
#     imageInfo = data.get("image_info")
#     imgdict = {"image_name": name, "author": author, "operation_name": operation, "comments": comments,
#                "image_info": imageInfo}
#     return imgdict, b64img
#endregion

# region stand-alone startup
if __name__ == "__main__":
    app.run(host='0.0.0.0')
# endregion
