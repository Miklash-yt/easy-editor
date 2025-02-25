from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QFileDialog
import os
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageEnhance

app = QApplication([])
workdir = ''
def select_workdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
def filter(files, extensions):
    result = list()
    for file_name in files:
        for extension in extensions:
            if file_name.endswith(extension):
                result.append(file_name)
    return result

main_win = QWidget()
main_win.resize(700, 500)
main_win.setWindowTitle('Easy Editor')


folder = QPushButton('Папка')
app_list = QListWidget() #список с выбором элементов
picture = QLabel('Картинка')
button_left = QPushButton('Лево')
button_right = QPushButton('Право')
mirror = QPushButton('Зеркало')
sharpness = QPushButton('Резкость')
black_and_white = QPushButton('Ч/б')

v_line = QVBoxLayout()
v2_line = QVBoxLayout()
h_line = QHBoxLayout()
h2_line = QHBoxLayout()
v_line.addWidget(folder)
v_line.addWidget(app_list)
v2_line.addWidget(picture)
h_line.addWidget(button_left)
h_line.addWidget(button_right)
h_line.addWidget(mirror)
h_line.addWidget(sharpness)
h_line.addWidget(black_and_white)
v2_line.addLayout(h_line)
h2_line.addLayout(v_line, 20)
h2_line.addLayout(v2_line, 80)
main_win.setLayout(h2_line)

def ShowFileNamesList():
    select_workdir()
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    filenames = filter(os.listdir(workdir), extensions) 
    app_list.clear()
    app_list.addItems(filenames)

class ImageProcessor():
    def __init__(self):
        self.picture = None
        self.filename = None
        self.subfolder_name = "Modified/"
    
    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.picture = Image.open(image_path)

    def showImage(self, path):
        picture.hide()
        pixmapimage = QPixmap(path)
        w, h = picture.width(), picture.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        picture.setPixmap(pixmapimage)
        picture.show()
    
    def do_bw(self):
        self.picture = self.picture.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.subfolder_name, self.filename)
        self.showImage(image_path)
    
    def saveImage(self):
        path = os.path.join(workdir, self.subfolder_name)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.picture.save(image_path)

    def do_flip(self):
        self.picture = self.picture.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.subfolder_name, self.filename)
        self.showImage(image_path)

    def image_left(self):
        self.picture = self.picture.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.subfolder_name, self.filename)
        self.showImage(image_path)

    def image_sharpness(self):
        self.picture = ImageEnhance.Contrast(self.picture)
        self.picture = self.picture.enhance(1.5)
        self.saveImage()
        image_path = os.path.join(workdir, self.subfolder_name, self.filename)
        self.showImage(image_path)
    
    def image_right(self):
        self.picture = self.picture.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.subfolder_name, self.filename)
        self.showImage(image_path)

image_processor = ImageProcessor()

def showChosenImage():
    if app_list.currentRow() >= 0:
        filename2 = app_list.currentItem().text()
        image_processor.loadImage(filename2)
        image_path = os.path.join(workdir, image_processor.filename)
        image_processor.showImage(image_path)



folder.clicked.connect(ShowFileNamesList)
app_list.currentRowChanged.connect(showChosenImage)
black_and_white.clicked.connect(image_processor.do_bw)
mirror.clicked.connect(image_processor.do_flip)
button_left.clicked.connect(image_processor.image_left)
button_right.clicked.connect(image_processor.image_right)
sharpness.clicked.connect(image_processor.image_sharpness)


main_win.show()
app.exec_()

