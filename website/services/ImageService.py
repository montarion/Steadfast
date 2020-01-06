import base64
import os


class ImageService(object):
    def __init__(self, root_path, staticfolder, imageuploadfolder):
        self.root_path = root_path
        self.staticfolder = staticfolder
        self.imageuploadfolder = imageuploadfolder

    def getimagedircontents(self):
        targetdir = self.staticfolder + self.imageuploadfolder
        lst = os.listdir(os.path.join(self.root_path, targetdir[1:]))
        return lst

    def save_file_old(self, imgstring, filename):
        try:
            imgdata = base64.b64decode(imgstring)
            # print(type(imgdata))
            filepath = self.root_path + self.staticfolder + self.imageuploadfolder
            filename = filepath + filename
            print("Trying to write to: {}".format(filename))
            with open(filename, "wb") as f:
                f.write(imgdata)
                print("Writing to: {}".format(filename))
            print("Finished writing to: {}".format(filename))
            return True, filename
        except Exception as e:
            print("Couldn't save..")
            print(str(e))
            return str(e)


    def save_file(imgstring, filename):
        try:
            imgdata = base64.b64decode(imgstring)
            print(type(imgdata))
            filepath = app.root_path + staticfolder + imageuploadfolder
            filename = filepath + filename
            print("Trying to write to: {}".format(filename))
            with open(filename, "wb") as f:
                f.write(imgdata)
                print("Writing to: {}".format(filename))
            print("Finished writing to: {}".format(filename))
            return True, filename
        except Exception as e:
            print("Couldn't save..")
            print(str(e))
            return str(e)


    def get_info(self, data):
        print("**INSIDE GET_INFO**")
        name, ext = data.get("image-name").split(".")
        b64img = data["base-encoded-image"].split(",")[1] # get actual base64 code
        b64img = b64img + "====" # add padding
        print(b64img)
        operation = data.get("operation") #data["operation"]
        if not name:
            name = operation
        name = "{}.{}".format(name, ext)
        comments = data.get("comments")
        author = data.get("author")
        imageInfo = data.get("info")
        imgdict = {"image_name": name, "author":author, "operation_name": operation, "comments": comments, "image_info": imageInfo}
        return imgdict, b64img

