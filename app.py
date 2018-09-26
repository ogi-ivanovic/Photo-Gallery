import os
import face_recognition
from flask import Flask, render_template, request

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
IMAGES_FOLDER = os.path.join('static', 'images')
baseDirectory = os.path.join(APP_ROOT, IMAGES_FOLDER)
selfiesDirectory = os.path.join(baseDirectory, 'selfies')
groupDirectory = os.path.join(baseDirectory, 'group')
noneDirectory = os.path.join(baseDirectory, 'none')

app.config['UPLOAD_FOLDER'] = IMAGES_FOLDER


class faces:
    pictures = {}

    def __init__(self):
        self.pictures = {'selfie' : [], 'group' : [], 'none' : []}


    def __numFaces(self, picDirectory):
        image = face_recognition.load_image_file(picDirectory)
        face_locations = face_recognition.face_locations(image)
        numFaces = len(face_locations)
        return numFaces


    def __makeFolders(self):
        try:
            if not os.path.exists(selfiesDirectory):
                os.makedirs(selfiesDirectory)
        except OSError:
            print('Error: Creating directory ') + selfiesDirectory

        try:
            if not os.path.exists(groupDirectory):
                os.makedirs(groupDirectory)
        except OSError:
            print('Error: Creating directory ') + groupDirectory

        try:
            if not os.path.exists(noneDirectory):
                os.makedirs(noneDirectory)
        except OSError:
            print('Error: Creating directory ') + noneDirectory


    def __movePictures(self):
        for pic in os.listdir(baseDirectory):
            if pic == 'group' or pic == 'none' or pic == 'selfies':
                continue
            picDirectory = os.path.join(baseDirectory, pic)
            numFaces = self.__numFaces(picDirectory)

            if numFaces == 0:
                folder = os.path.join(baseDirectory, 'none')
                newPicDirectory = os.path.join(folder, pic)
                try:
                    os.rename(picDirectory, newPicDirectory)
                except OSError:
                    print('Error: Moving file ' + pic)
            if numFaces == 1:
                folder = os.path.join(baseDirectory, 'selfies')
                newPicDirectory = os.path.join(folder, pic)
                try:
                    os.rename(picDirectory, newPicDirectory)
                except OSError:
                    print('Error: Moving file ' + pic)
            else:
                folder = os.path.join(baseDirectory, 'group')
                newPicDirectory = os.path.join(folder, pic)
                try:
                    os.rename(picDirectory, newPicDirectory)
                except OSError:
                    print('Error: Moving file ' + pic)


    def updatePictures(self):
        selfieList = os.listdir('static/images/selfies')
        selfieList = ['images/selfies/' + file for file in selfieList]

        groupList = os.listdir('static/images/group')
        groupList = ['images/group/' + file for file in groupList]

        noneList = os.listdir('static/images/none')
        noneList = ['images/none/' + file for file in noneList]

        self.pictures['selfie'] = selfieList
        self.pictures['group'] = groupList
        self.pictures['none'] = noneList


    def sort(self):
        self.__makeFolders()

        self.__movePictures()


@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/gallery/<gallery_number>')
def gallery(gallery_number):
    return render_template('gallery.html', gallery_number=gallery_number)

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'static/images/')

    if not os.path.isdir(target): # make a try statement
        os.mkdir(target)

    for file in request.files.getlist('file'):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)

    pics = faces()
    pics.sort()

    return render_template('options.html')

@app.route('/selfies')
def selfies():
    selfiesObj = faces()
    selfiesObj.updatePictures()
    slfs = selfiesObj.pictures['selfie']
    return render_template('gallery.html', hists=slfs, length=len(slfs))

@app.route('/group')
def group():
    groupObj = faces()
    groupObj.updatePictures()
    grp = groupObj.pictures['group']
    return render_template('gallery.html', hists=grp, length=len(grp))

@app.route('/none')
def none():
    noneObj = faces()
    noneObj.updatePictures()
    nn = noneObj.pictures['none']
    return render_template('gallery.html', hists=nn, length=len(nn))


if __name__ == '__main__':
    app.run(port=4555, debug=True)