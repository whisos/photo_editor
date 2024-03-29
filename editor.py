import os
from PyQt5.QtWidgets import(QApplication, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance

app = QApplication([])
win = QWidget()
win.resize(700, 400)
win.setWindowTitle("Editor")
lb_image = QLabel("Картинка")
btn_dir = QPushButton("Папка") 
file_list = QListWidget()

btn_left = QPushButton("Лево")
btn_right = QPushButton("Право")
btn_flip = QPushButton("Зеркало")
btn_sharp = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")

row = QHBoxLayout() #Основная линия

col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(file_list)

col2.addWidget(lb_image, 90)

row_tools = QHBoxLayout()

row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)

col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)

win.setLayout(row)

win.show()

workdir = ''

def filter(filenames, extensions):
    result = []
    for filename in filenames:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg','.jpeg','.png','.gif']
    chooseWorkDir()
    filenames = filter(os.listdir(workdir), extensions)
    file_list.clear()
    for filename in filenames:
        file_list.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)





class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def make_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def turn_left(self):
         self.image = self.image.transpose(Image.ROTATE_90)
         self.saveImage()
         image_path = os.path.join(workdir, self.save_dir, self.filename)
         self.showImage(image_path)

    def turn_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def contrast(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def showImage(self, path):
        lb_image.hide()
        pixmapImage = QPixmap(path)
        w = lb_image.width()
        h = lb_image.height()
        pixmapImage = pixmapImage.scaled(w,h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapImage)
        lb_image.show()

def showChosenImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)    


workimage = ImageProcessor()

file_list.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.make_bw)
btn_sharp.clicked.connect(workimage.blur)
btn_flip.clicked.connect(workimage.do_flip)
app.exec()