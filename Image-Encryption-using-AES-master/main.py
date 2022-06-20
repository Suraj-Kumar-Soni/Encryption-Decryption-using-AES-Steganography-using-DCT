from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog,QLabel,QAction,QMainWindow,QApplication
from PyQt5.uic import loadUiType
from Encrypter import Encrypter
from Decrypter import Decrypter
from watermarking import DCT
from PIL import Image as Img
from PIL import ImageTk as ImgTk  
#from tkinter import *
import base64
from Crypto.Cipher import AES
import os
import shutil
import sys
import cv2

Qt = QtCore.Qt




ui, _ = loadUiType('Image-Encryption-using-AES-master/ui.ui')
def start():
    global m
    m = Main_Window()
    m.show()
    
class encrypt_page():
    def __init__(self):
        self.file={}
        self.file1={}
        self.stri=""
        self.Handel_Buttons()
        self.pushButton_3.clicked.connect(self.chooseFile)
        self.pushButton_cover.clicked.connect(self.chooseFile1)
        self.pushButton_4.clicked.connect(self.onClickEncrypt)
    def Handel_Buttons(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
    def chooseFile(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open File')
        pixmap = QtGui.QPixmap(self.file[0])
        self.lbl.setPixmap(pixmap.scaledToHeight(201))
        if self.file != None:
            ba = QtCore.QByteArray()
            buff = QtCore.QBuffer(ba)
            buff.open(QtCore.QIODevice.WriteOnly) 
            ok = pixmap.save(buff, "PNG")
            assert ok
            pixmap_bytes = ba.data()
            #print(type(pixmap_bytes))
            #data = self.file[0]
            self.stri = base64.b64encode(pixmap_bytes)

    def chooseFile1(self):
        self.file1 = QFileDialog.getOpenFileName(self, 'Open File')
        pixmap = QtGui.QPixmap(self.file1[0])
        self.lbl_cover.setPixmap(pixmap.scaledToHeight(201))
        # if self.file1 != None:
        #     ba = QtCore.QByteArray()
        #     buff = QtCore.QBuffer(ba)
        #     buff.open(QtCore.QIODevice.WriteOnly) 
        #     ok = pixmap.save(buff, "PNG")
        #     assert ok
            # pixmap_bytes = ba.data()
            # #print(type(pixmap_bytes))
            # #data = self.file[0]
            # self.stri = base64.b64encode(pixmap_bytes)


    def onClickEncrypt(self):
        if os.path.exists("Encoded_image/"):
            shutil.rmtree("Encoded_image/")
        os.makedirs("Encoded_image/")
        myKey=self.lineEdit.text()
        # print(type(myKey))
        # print(myKey)

        x = Encrypter(self.stri, myKey)
        cipher = x.encrypt_image()
        # print(type(cipher))
        # name = QFileDialog.getSaveFileName(self, 'Save File')
        # file = open(name,'w')
        # text = cipher
        # file.write(text)
        # file.close()
        #fh.write(base64_decoded.decode('base64'))
        os.chdir("Encoded_image/")
        fh = open("cipher.txt", "wb")
        fh.write(cipher)
        fh.close()
        
        f = open("cipher.txt","r")
        secret_msg = f.read()
        print("The message length is: ",len(secret_msg))
        dct_img = cv2.imread(self.file1[0], cv2.IMREAD_UNCHANGED)
        dct_img_encoded = DCT().encode_image(dct_img, secret_msg)      
        dct_encoded_image_file = "dct_" + os.path.split(self.file1[0])[1]
        cv2.imwrite(dct_encoded_image_file,dct_img_encoded)  
        pixmap = QtGui.QPixmap(dct_encoded_image_file)       
        self.lbl_stego.setPixmap(pixmap.scaledToHeight(201))
        os.chdir("..")
        print("Encoded images were saved!")
        
        
class decrypt_page():
    def __init__(self):
        self.cipher={}
        self.Handel_Buttons()
        self.pushButton_5.clicked.connect(self.chooseFile2)
        self.pushButton_6.clicked.connect(self.onClickDecrypt)
    def Handel_Buttons(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
    def chooseFile2(self):
        self.cipher = QFileDialog.getOpenFileName(self, 'Open File')
        # self.file1 = QFileDialog.getOpenFileName(self, 'Open File')
        pixmap = QtGui.QPixmap(self.cipher[0])
        self.lbl_cover_2.setPixmap(pixmap.scaledToHeight(201))
        # print(text.encode('utf-8'))
    def onClickDecrypt(self):
        if os.path.exists("Decoded_output/"):
            shutil.rmtree("Decoded_output/")
        os.makedirs("Decoded_output/")
        myKey=self.lineEdit_2.text()
        dct_img = cv2.imread(self.cipher[0], cv2.IMREAD_UNCHANGED)
        os.chdir("Decoded_output/")
        dct_hidden_text = DCT().decode_image(dct_img)
        
        x = Decrypter(dct_hidden_text)
        image=x.decrypt_image(myKey)
        
        ba = QtCore.QByteArray(image)
        pixmap = QtGui.QPixmap()
        ok = pixmap.loadFromData(ba, "PNG")
        assert ok        
        self.lbl_2.setPixmap(pixmap.scaledToHeight(201))
        print("Image is decoded and decrypted successfully!!")
        # if image!=None:
        #     ba = QtCore.QByteArray()
        #     buff = QtCore.QBuffer(ba)
        #     buff.open(QtCore.QIODevice.WriteOnly) 
        #     ok = pixmap.save(buff, "PNG")
        #     assert ok
        #     pixmap_bytes = ba.data()
        #     #print(type(pixmap_bytes))
        #     #data = self.file[0]
        #     self.stri = base64.b64encode(pixmap_bytes)            
        
class Main_Window(QMainWindow, QWidget, ui,encrypt_page,decrypt_page):
    def __init__(self):
        QMainWindow.__init__(self)
        QWidget.__init__(self)
        self.setupUi(self)
        encrypt_page.__init__(self)
        decrypt_page.__init__(self)

        self.Handel_Buttons() 
        self.stackedWidget.setCurrentIndex(0)
    def Handel_Buttons(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_8.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
                
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    #connect()
    window = start()
    app.exec_()