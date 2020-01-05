import sys, os
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon,QFont,QPixmap,QImage, QPalette, QBrush,QPainter, QColor, QBrush,QFontDatabase,QSessionManager
from PyQt5.QtCore import pyqtSlot,QSize,QRect
from Note import mainprograme, InfoWindow

class UserConfigWindow(QWidget):

    def __init__(self, ID, Login, Password):
        super().__init__()

        #Setting Fonts
        QFontDatabase.addApplicationFont("Fonts/DukeFill.ttf")
        QFontDatabase.addApplicationFont("Fonts/Focus-Medium.ttf")
        QFontDatabase.addApplicationFont("Fonts/Roboto-ThinItalic.ttf")
        #Setting styles
        self.QLabelStyle = """QLabel{color: #99cc00;font-family:DukeFill;font-size:19px; }"""
        self.QLineEditStyle = """QLineEdit{color: #99cc00;font-family:DukeFill;font-size:19px; 
                                            background-color: rgba(0,0,0,0); border: 1px solid #383838;}"""
        self.QPushButtonStyle = """QPushButton { color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0); font-size:19px; }"""
        #Setting size variable
        screen = QApplication.primaryScreen().grabWindow(0)
        self.size = screen.size()
        self.WindowWidth = self.size.width() * 30 / 100
        self.WindowHeight = self.size.height() * 38 / 100
        #Setting global variables
        self.sID = ID
        self.sLogin = Login
        self.sPassword = Password
        #Title for windows
        self.title = "Settings"
        #Setting photo on background
        Background= QLabel(self)
        BackgroundIMG = QPixmap("img/tlo.png")
        Background.setPixmap(BackgroundIMG)
        self.initUI()

    def initUI(self):
        #Setting title
        self.setWindowTitle(self.title)
        #Drawing window
        self.setGeometry(self.size.width() / 4, self.size.height() / 4, self.WindowWidth, self.WindowHeight)
        #Drawing without frames
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        #Drawing exit button
        self.ExitLabel()
        #Drwaing photo label
        self.UserPhotoLabel()
        #Drawing login label
        self.LoginLabel()
        #Drwaing password label
        self.PasswordLabel()
        #Showind window
        self.show()

    def ExitLabel(self):
        self.ExitButton = QLabel(self)
        ExitIMG = QPixmap("img/close.png")
        self.ExitButton.setPixmap(ExitIMG)
        self.ExitButton.move(self.WindowWidth*92/100,self.WindowHeight*3/100)
        self.ExitButton.mousePressEvent = self.exit

    def UserPhotoLabel(self):
        self.PhotoL = QLabel(self)
        self.DefaultPhotoIMG =  QPixmap("img/user.png")
        self.PhotoL.setPixmap(self.DefaultPhotoIMG)
        self.PhotoL.move(self.WindowWidth*5/100,self.WindowHeight*3/100)
        self.PhotoL.mousePressEvent = self.ChangePhoto

    #Do zmiany, prawa autorskie ;)
    def ChangePhoto(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","PNG Files (*.png);;JPG Files (*.jpg)", options=options)
        if fileName:
            self.DefaultPhotoIMG = QPixmap(fileName)
            self.PhotoL.setPixmap(self.DefaultPhotoIMG)
            self.ShowStatusWindow("Zmieniono awatar!")

    def LoginLabel(self):
        self.LogLabel = QLabel("Login:",self)
        self.LogLabel.move(self.WindowWidth*5/100,self.WindowHeight*40/100)
        self.LogLabel.setStyleSheet(self.QLabelStyle)
        self.LogLabelEdit = QLineEdit(self)
        self.LogLabelEdit.setText(self.sLogin)
        self.LogLabelEdit.move(self.WindowWidth*15/100,self.WindowHeight*40/100)
        self.LogLabelEdit.setStyleSheet(self.QLineEditStyle)
        self.ChangeLoginButton = QPushButton("Zmień login", self)
        self.ChangeLoginButton.move(self.WindowWidth*45/100,self.WindowHeight*39/100)
        self.ChangeLoginButton.setStyleSheet(self.QPushButtonStyle)
        self.ChangeLoginButton.clicked.connect(self.on_clickLoginChange)

    def PasswordLabel(self):
        self.PasswordButton = QPushButton("Zmień hasło", self)
        self.PasswordButton.move(self.WindowWidth*4/100,self.WindowHeight*48/100)
        self.PasswordButton.setStyleSheet(self.QPushButtonStyle)
        self.PasswordButton.clicked.connect(self.on_clickPasswordChangeShow)

    def PasswordInput(self):
        self.OldPassLabel = QLabel("Wprowadź stare hasło: ",self)
        self.OldPassLabel.move(self.WindowWidth*5/100,self.WindowHeight*52/100)
        self.OldPassLabel.setStyleSheet(self.QLabelStyle)
        self.OldPassLabel.show()
        #--------------------------------------------------------
        self.OldPassword = QLineEdit(self)
        self.OldPassword.move(self.OldPassLabel.width()+30,self.WindowHeight*52/100)
        self.OldPassword.setStyleSheet(self.QLineEditStyle)
        self.OldPassword.show()

        self.NewPassLabel = QLabel("Wprowadź nowe hasło: ", self)
        self.NewPassLabel.move(self.WindowWidth*5/100,self.WindowHeight*60/100)
        self.NewPassLabel.setStyleSheet(self.QLabelStyle)
        self.NewPassLabel.show()
        # --------------------------------------------------------
        self.NewPassword = QLineEdit(self)
        self.NewPassword.move(self.NewPassLabel.width()+30,self.WindowHeight*60/100)
        self.NewPassword.setStyleSheet(self.QLineEditStyle)
        self.NewPassword.show()

        self.RepeatNewPassLabel = QLabel("Wprowadź ponownie nowe hasło: ", self)
        self.RepeatNewPassLabel.move(self.WindowWidth*5/100,self.WindowHeight*68/100)
        self.RepeatNewPassLabel.setStyleSheet(self.QLabelStyle)
        self.RepeatNewPassLabel.show()
        # --------------------------------------------------------
        self.RepeatNewPassword = QLineEdit(self)
        self.RepeatNewPassword.move(self.RepeatNewPassLabel.width()+30,self.WindowHeight*68/100)
        self.RepeatNewPassword.setStyleSheet(self.QLineEditStyle)
        self.RepeatNewPassword.show()

        self.ChangePasswordButton = QPushButton("Zmień hasło", self)
        self.ChangePasswordButton.move(self.WindowWidth*4/100,self.WindowHeight*76/100)
        self.ChangePasswordButton.setStyleSheet(self.QPushButtonStyle)
        self.ChangePasswordButton.show()
        self.ChangePasswordButton.clicked.connect(self.on_clickPasswordChange)

    def on_clickLoginChange(self):
        if self.LogLabelEdit.text() != self.sLogin:
            connection = mysql.connector.connect(user='NoteUser', password='Note',host='192.168.1.45',database='NoteDB')
            DataBaseOperate = connection.cursor()

            query = "UPDATE Users SET Login='{0}' WHERE ID={1};".format(self.LogLabelEdit.text(), self.sID)
            DataBaseOperate.execute(query)
            connection.commit()
            connection.close()
            self.ShowStatusWindow("Zmieniono login!")
        else:
            self.ShowStatusWindow("Proszę wpisać nowy login, różny\nod poprzedniego!")

    def on_clickPasswordChangeShow(self):
        self.PasswordButton.hide()
        self.PasswordInput()

    def on_clickPasswordChange(self):
        OldPass = self.OldPassword.text()
        NewPass = self.NewPassword.text()
        RepeatPass = self.RepeatNewPassword.text()

        if OldPass==self.sPassword and NewPass == RepeatPass:
            connection = mysql.connector.connect(user='NoteUser', password='Note',host='192.168.1.45',database='NoteDB')
            DatabaseOperate = connection.cursor()

            query = "UPDATE Users SET Password='{0}' WHERE ID={1}".format(NewPass, self.sID)
            DatabaseOperate.execute(query)
            connection.commit()
            connection.close()

            self.OldPassLabel.hide()
            self.OldPassword.hide()
            self.NewPassLabel.hide()
            self.NewPassword.hide()
            self.RepeatNewPassLabel.hide()
            self.RepeatNewPassword.hide()
            self.ChangePasswordButton.hide()
            self.PasswordButton.show()

            self.ShowStatusWindow("Hasło zmieniono pomyślnie!")

        else:
            self.ShowStatusWindow("Błąd! Sprawdź poprawność haseł!")

    def ShowStatusWindow(self, message):
        self.StatusWindow = InfoWindow.StateWindow(message)
        self.StatusWindow.show()

    def exit(self, event):
        self.close()


if __name__ ==  '__main__':
    app = QApplication(sys.argv)
    ex = UserConfigWindow()
    sys.exit(app.exec_())