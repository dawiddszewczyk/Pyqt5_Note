import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon,QFont,QPixmap,QImage, QPalette, QBrush,QPainter, QColor, QBrush,QFontDatabase
from PyQt5.QtCore import pyqtSlot,QSize,QRect
import mysql.connector
from functools import partial
from Note import login, insertdata, UserConfig,InfoWindow, ShowFullTask
class MainPanel(QWidget):
        def __init__(self,nick,UserID,Password):
            super(MainPanel, self).__init__()
            #<----- Set a global Valiabels from other class.
            self.user = nick
            self.uID = UserID
            self.sPassword = Password
            self.TaskLabel = []
            # <------- Set a font to datafontbase
            QFontDatabase.addApplicationFont("Fonts/DukeFill.ttf")
            QFontDatabase.addApplicationFont("Fonts/Focus-Medium.ttf")
            QFontDatabase.addApplicationFont("Fonts/Roboto-ThinItalic.ttf")
            # <--- END
            screen = QApplication.primaryScreen().grabWindow(0)
            self.size = screen.size()
            self.WindowWidth = self.size.width() * 50 / 100
            self.WindowHeight = self.size.height() * 50 / 100
            # Photo On the Background
            oImage = QImage("img/tlo.png")
            sImage = oImage.scaled(QSize(800, 500))
            palette = QPalette()
            palette.setBrush(10, QBrush(sImage))
            self.setPalette(palette)
            # <----END

            # Set Window Size ( x ,y ,width ,height )
            #               (420,0         , 262,5         , 840,0         , 525.0          )
            self.setGeometry(self.size.width() / 4, self.size.height() / 4,  self.WindowWidth, self.WindowHeight)
            # <----END
            # Set windows Without Frame
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            # <----END

            # Label which check if the Button will be press.
            exit = QLabel("           ", self)
            exit.move(self.WindowWidth * 94 / 100, self.WindowHeight * 1 / 100)
            exit.mousePressEvent = self.exit
            # <-- END

            self.initUI()

            # To show more info about errors !

        sys._excepthook = sys.excepthook

        def my_exception_hook(exctype, value, traceback):
            print(exctype, value, traceback)
            sys._excepthook(exctype, value, traceback)
            sys.exit(1)

        sys.excepthook = my_exception_hook

        # <----------END!!

        def initUI(self):

            self.ConsistWindow()
            self.printBeforeButton()
            self.printNextButton()
            self.show()

        # <-----Function to draw a reckt (baner,button,menu,line)
        def paintEvent(self, e):
            self.draw = QPainter()
            self.draw.begin(self)
            self.drawRectangles()
            self.draw.end()

        def drawRectangles(self):
            # <---------- draw.drawRect(x,y,width,height)

            col = QColor(28, 28, 31)
            self.draw.setPen(col)

            # Right menu
            self.draw.setBrush(QColor(28, 28, 31))
            self.draw.drawRect(self.WindowWidth * 83 / 100, self.WindowHeight * 5 / 100, self.WindowWidth * 15 / 100,
                               self.WindowHeight * 90 / 100)

            # Cointaner
            self.draw.setBrush(QColor(28, 28, 31))
            self.draw.drawRect(self.WindowWidth * 2 / 100, self.WindowHeight * 5 / 100, self.WindowWidth * 78 / 100,
                               self.WindowHeight * 90 / 100)

            # Exit
            self.draw.setBrush(QColor(220, 20, 60))
            self.draw.drawRect(self.WindowWidth * 94 / 100, self.WindowHeight * 1 / 100, 35, 15)

            # Green Line
            self.draw.setBrush(QColor(132, 189, 0))
            self.draw.drawRect(self.WindowWidth * 84 / 100, self.WindowHeight * 30 / 100, self.WindowWidth * 13 / 100,
                               2)

        # <----END

        # <-- To close window
        def exit(self, event):
            self.close()

        def ConsistWindow(self):
            logo = QLabel(self)
            pixmaplog = QPixmap('img/logo1.png')
            logo.setPixmap(pixmaplog)
            logo.move(self.WindowWidth*87/100, self.WindowHeight*10/100)

            connection = mysql.connector.connect(user='NoteUser', password='Note',host='192.168.1.45',database='NoteDB')
            DataBaseOperate = connection.cursor()

            query = "SELECT Date,Title,Contents,TaskState.State AS State, U1.Login AS Creator, U2.Login AS User, Tasks.ID " \
                   "FROM Tasks " \
                   "JOIN TaskState ON Tasks.StateID = TaskState.ID " \
                   "JOIN Users U1 ON Tasks.CreatorID = U1.ID " \
                   "JOIN Users U2 ON Tasks.UserID = U2.ID " \
                   "WHERE Tasks.UserID = {0}".format(self.uID)

            DataBaseOperate.execute(query)
            self.QueryResult = DataBaseOperate.fetchall()

            TempID = self.QueryResult[0][6] # First task ID

            self.TaskLabel = [] #Task date
            self.TitleLabel = [] #Task title
            self.TaskRect = [] #Rect task background
            self.TaskContent = [] #Task contents
            self.TaskReadMore = []
            self.TaskNumber = []
            self.UserTaskID = 0
            self.y = 1
            self.LabelCounter = 1 #Useless like Polish Educational System
            self.RowCounter = 0 #Count displayed objects (tasks)
            self.LastPrint = DataBaseOperate.rowcount%4 #Number of last object to print
            self.PrintAmount = DataBaseOperate.rowcount // 4 #Number of full 4-objects to print
            self.BeforeCounter = -1
            self.bPrintNext = True
            self.bPrintBefore = False
            self.btrue = True
            self.b3true = True
            self.i = 4
            self.BeforeLastPrint = False
            self.printNext(1)

            self.sLabelMainContainer = QLabel(self)
            self.sLabelMainContainer.move(200, 60)
            self.sLabelMainContainer.setStyleSheet(" QLabel {font-weight: bold;color: #84bd00;}")

            self.sUserName = QLabel(self)
            self.sUserName.setGeometry(self.WindowWidth*88/100, self.WindowHeight*30/100, self.WindowWidth * 15 / 100,
                               self.WindowHeight * 5 / 100)
            self.sUserName.setStyleSheet(" QLabel {font-weight: bold;color: #84bd00; text-align: center;}")
            self.sUserName.setText("Witaj {0}".format(self.user))

            textboxstyleSheet = """QLineEdit{border:1px solid  #383838; color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0);}"""

            self.InsertButton = QPushButton('Dodaj zdarzenie', self)
            self.InsertButton.setStyleSheet("QPushButton { color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0); text-align: center; }")
            self.InsertButton.setGeometry(self.WindowWidth * 83 / 100, self.WindowHeight * 35 / 100, self.WindowWidth * 15 / 100,
                               self.WindowHeight * 5 / 100)

            self.UserConfigButton = QPushButton("Ustawienia", self)
            self.UserConfigButton.setStyleSheet("QPushButton { color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0); text-align: center; }")
            self.UserConfigButton.setGeometry(self.WindowWidth * 83 / 100, self.WindowHeight * 39 / 100, self.WindowWidth * 15 / 100,
                               self.WindowHeight * 5 / 100)
            self.UserConfigButton.clicked.connect(self.on_clickUserConfig)

            self.InsertButton.setToolTip('Dodaj zdarzenie do Bazy')
            self.InsertButton.clicked.connect(self.on_clickInsert)

            self.button = QPushButton('Logout', self)
            self.button.setStyleSheet("QPushButton { color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0); text-align: center}")
            self.button.setGeometry(self.WindowWidth * 83 / 100, self.WindowHeight * 43 / 100, self.WindowWidth * 15 / 100,
                               self.WindowHeight * 5 / 100)

            self.button.setToolTip('Wyloguj sie z systemu')
            self.button.clicked.connect(self.on_click)
            for j in range(len(self.TaskReadMore)):
                self.TaskNumber[j] = self.UserTaskID
                self.TaskReadMore[j].clicked.connect(self.FullTask)
        def printBeforeButton(self):
            NextButton = QLabel(self)
            NextIMG = QPixmap('img/arrowUP.png')
            NextButton.setPixmap(NextIMG)
            NextButton.move(self.WindowWidth*89/100,self.WindowHeight*50/100)
            NextButton.mousePressEvent = self.printBefore

        def printNextButton(self):
            NextButton = QLabel(self)
            NextIMG = QPixmap('img/arrowDOWN.png')
            NextButton.setPixmap(NextIMG)
            NextButton.move(self.WindowWidth*89/100,self.WindowHeight*57/100)
            NextButton.mousePressEvent = self.printNext

        def printNext(self,event):
            if self.bPrintNext:
                if not self.PrintAmount:
                    print(len(self.TaskRect))
                    print("RowCounter -> ",self.RowCounter)
                    if self.RowCounter >= 4:
                        print("BOLEK: ",range(self.RowCounter-4, self.RowCounter))
                        for k in range(self.RowCounter-4, self.RowCounter):
                            print(k)
                            self.TaskRect[0].hide()
                            del (self.TaskRect[0])
                            self.TitleLabel[0].hide()
                            del (self.TitleLabel[0])
                            self.TaskLabel[0].hide()
                            del (self.TaskLabel[0])
                            self.TaskContent[0].hide()
                            del (self.TaskContent[0])
                            for n in range(len(self.TaskReadMore)):
                                self.TaskReadMore[n].hide()
                            self.y = 1
                    print("Print Next -> Printing {0} objects.".format(self.LastPrint))
                    print("Range printNext PA =1 -> ", range(self.RowCounter, self.LastPrint + self.RowCounter))
                    for n in range(self.RowCounter, self.LastPrint + self.RowCounter):
                        self.addLabel(self.QueryResult[n][0], self.QueryResult[n][1], self.QueryResult[n][2],self.QueryResult[n][6])
                        print(self.QueryResult[n][0], self.QueryResult[n][1], self.QueryResult[n][2])

                    self.RowCounter += self.LastPrint
                    self.bPrintNext = False
                    self.BeforeLastPrint = True
                else:
                    print("Task rect", len(self.TaskRect))
                    if self.RowCounter >= 4:
                        print("RowCOunter  TEMP -> ", self.RowCounter)
                        print("Range printNext PA =0 HOJDING -> ",range(self.RowCounter, self.RowCounter + 4))
                        for k in range(self.RowCounter-4, self.RowCounter):
                            self.TaskRect[0].hide()
                            del (self.TaskRect[0])
                            self.TitleLabel[0].hide()
                            del (self.TitleLabel[0])
                            self.TaskLabel[0].hide()
                            del (self.TaskLabel[0])
                            self.TaskContent[0].hide()
                            del (self.TaskContent[0])
                            for n in range(len(self.TaskReadMore)):
                                self.TaskReadMore[n].hide()
                            self.y = 1
                    print("Print Next -> Printing 4 objects.")
                    print("Range printNext PA =0 -> ", range(self.RowCounter, self.RowCounter +4))
                    for n in range(self.RowCounter, self.RowCounter + 4):
                        self.addLabel(self.QueryResult[n][0], self.QueryResult[n][1], self.QueryResult[n][2],self.QueryResult[n][6])
                        print(self.QueryResult[n][0], self.QueryResult[n][1], self.QueryResult[n][2])
                    self.RowCounter += 4
                    self.PrintAmount -= 1
                self.BeforeCounter += 1

#Do poprawy wyświetlanie elementów
        def printBefore(self,event):
            if self.BeforeCounter:
                if self.BeforeLastPrint:
                    print("Task rectlen -> ",len(self.TaskRect))
                    print("Range printBefore PA =1 -> ", range(self.RowCounter, self.RowCounter-self.LastPrint, -1))
                    print("RowCounter -> ", self.RowCounter)
                    print("LastPrint -> ", self.LastPrint)
                    for k in range(self.RowCounter-1, self.RowCounter-1-self.LastPrint, -1):
                        self.TaskRect[0].hide()
                        del (self.TaskRect[0])
                        self.TitleLabel[0].hide()
                        del (self.TitleLabel[0])
                        self.TaskLabel[0].hide()
                        del (self.TaskLabel[0])
                        self.TaskContent[0].hide()
                        del (self.TaskContent[0])
                        for n in range(len(self.TaskReadMore)):
                            self.TaskReadMore[n].hide()
                        self.y = 1
                    self.RowCounter -= self.LastPrint
                    self.BeforeLastPrint = False
                else:
                    for k in range(self.RowCounter-4,self.RowCounter):
                        self.TaskRect[0].hide()
                        del (self.TaskRect[0])
                        self.TitleLabel[0].hide()
                        del (self.TitleLabel[0])
                        self.TaskLabel[0].hide()
                        del (self.TaskLabel[0])
                        self.TaskContent[0].hide()
                        del (self.TaskContent[0])
                        for n in range(len(self.TaskReadMore)):
                            self.TaskReadMore[n].hide()
                        self.y = 1
                    self.RowCounter -= 4
                    self.PrintAmount += 1
                print("Print Before -> Printing 4 objects.")
                print("Range printBefore PA =0 -> ",range(self.RowCounter - 4, self.RowCounter) )
                for n in range(self.RowCounter - 4, self.RowCounter):
                    self.addLabel(self.QueryResult[n][0], self.QueryResult[n][1], self.QueryResult[n][2], self.QueryResult[n][6])
                    print(self.QueryResult[n][0], self.QueryResult[n][1], self.QueryResult[n][2])
                self.BeforeCounter -= 1
                self.bPrintNext = True


        def addLabel(self, date, Title, contain, TaskID):
            rect = QLabel(self)
            rect.resize(self.WindowWidth*74/100, self.WindowHeight*20/100)
            rect.move(self.WindowWidth*4/100, 1 + self.y * self.WindowHeight*7.3/100)
            rect.setStyleSheet("QLabel {background-color: black;}")
            self.TaskRect.append(rect)

            date = QLabel("{0} \n ".format(date), self)
            date.setStyleSheet(" QLabel {font-weight: bold;color: #84bd00;}")
            date.move(self.WindowWidth*65/100, 11 + self.y * self.WindowHeight*7.3/100)

            title = QLabel("{0} \n ".format(Title), self)
            title.setStyleSheet(" QLabel {color: #84bd00;}")
            title.move(self.WindowWidth*6/100, 11 + self.y * self.WindowHeight*7.3/100)
            self.TitleLabel.append(title)
            self.TaskLabel.append(date)

            content = QLabel("{0} \n ".format(contain), self)
            content.setStyleSheet(" QLabel {color: #84bd00;}")
            content.move(self.WindowWidth*6/100, 41 + self.y * self.WindowHeight*7.3/100)
            content.setGeometry(QRect(content.x(), content.y(), 450, content.height()))

            if len(content.text()) > 80:
                self.TaskNumber.append(TaskID)
                readmore = QPushButton("Czytaj dalej ", self)
                readmore.setStyleSheet("QPushButton { color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0); }")
                readmore.move(self.WindowWidth*65/100, 61 + self.y * self.WindowHeight*7.3/100)
                self.TaskReadMore.append(readmore)
            self.TaskContent.append(content)

            self.y += 3
            rect.show()
            date.show()
            title.show()
            content.show()
            if len(content.text()) > 80:
                readmore.show()

        def ShowStatusWindow(self, message):
            self.StatusWindow = InfoWindow.StateWindow(message)
            self.StatusWindow.show()

        @pyqtSlot()
        def on_click(self):
            self.SWA = login.SecondWindow()
            self.SWA.show()
            self.ShowStatusWindow("Wylogowano")
            self.destroy()

        @pyqtSlot()
        def on_clickInsert(self):
            self.k = insertdata.Insert(self.uID)
            self.k.show()

        def on_clickUserConfig(self):
            self.ucWindow = UserConfig.UserConfigWindow(self.uID,self.user,self.sPassword)
            self.ucWindow.show()

        @pyqtSlot()
        def FullTask(self):
            self.a = ShowFullTask.ShowFullTask(self.UserTaskID)
            self.a.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainPanel()
    sys.exit(app.exec_())