import base64
import os


class ImageService(object):
    def __init__(self, root_path, staticfolder, imageuploadfolder, image_repository):
        self.root_path = root_path
        self.staticfolder = staticfolder
        self.imageuploadfolder = imageuploadfolder
        self.image_repository = image_repository

    def getimagedircontents(self):
        targetdir = self.staticfolder + self.imageuploadfolder
        lst = os.listdir(os.path.join(self.root_path, targetdir[1:]))
        return lst

    def save_file(self, imgstring, imgdict):
        try:
            filename = imgdict["image_name"]
            imgdata = base64.b64decode(imgstring)
            relativefilepath = self.staticfolder + self.imageuploadfolder
            filepath = self.root_path + relativefilepath
            absolutefilename = filepath + filename
            print("Trying to write to: {}".format(filename))
            with open(absolutefilename, "wb") as f:
                f.write(imgdata)
                print("Writing to: {}".format(filename))
            print("Finished writing to: {}".format(filename))
            print("Trying to insert into database")
            imgdict['image_info']['path_to_file'] = relativefilepath
            self.image_repository.insert(imgdict)
            print("Inserted into the database")
            return True, imgdict
        except Exception as e:
            print("Couldn't save..")
            print(str(e))
            return False, str(e)


    def get_info(self, data):
        print("**INSIDE GET_INFO**")
        print(data.get("image_name"))
        name, ext = data.get("image_name").split(".")
        b64img = data["base_encoded_image"].split(",")[1] # get actual base64 code
        b64img = b64img + "===="  # add padding
        print(b64img)
        operation = data.get("operation_name")  # data["operation"]
        if not name:
            name = operation
        name = "{}.{}".format(name, ext)
        comments = data.get("comments")
        author = data.get("author")
        imageInfo = data.get("image_info")
        imgdict = {"image_name": name, "author":author, "operation_name": operation, "comments": comments, "image_info": imageInfo}
        return imgdict, b64img

