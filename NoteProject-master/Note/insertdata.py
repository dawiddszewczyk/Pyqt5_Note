import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon,QFont,QPixmap,QImage, QPalette, QBrush,QPainter, QColor, QBrush,QFontDatabase
from PyQt5.QtCore import pyqtSlot,QSize,QRect,QDate
import sqlite3
import mysql.connector
from functools import partial
from Note import mainprograme



class Insert(QWidget):
    def __init__(self, ID):
        super(Insert, self).__init__()
        self.uID = ID
        # <------- Set a font to datafontbase
        QFontDatabase.addApplicationFont("Fonts/DukeFill.ttf")
        QFontDatabase.addApplicationFont("Fonts/Focus-Medium.ttf")
        QFontDatabase.addApplicationFont("Fonts/Roboto-ThinItalic.ttf")
        # <--- END
        screen = QApplication.primaryScreen().grabWindow(0)
        self.size = screen.size()
        self.WindowWidth = self.size.width() * 25 / 100
        self.WindowHeight = self.size.height() * 25 / 100

        # Photo On the Background
        oImage = QImage("img/tlo.png")
        sImage = oImage.scaled(QSize(800, 500))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        # <----END

        # Set Window Size ( x ,y ,width ,height )
        #               (420,0         , 262,5         , 840,0         , 525.0          )
        self.setGeometry(self.size.width() / 3, self.size.height() / 3, self.WindowWidth,self.WindowHeight)
        # <----END
        # Set windows Without Frame
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # <----END

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

        self.draw.setBrush(QColor(28, 28, 31))
        self.draw.drawRect(self.WindowWidth*4/100, self.WindowWidth*4/100, self.WindowWidth*92/100, self.WindowHeight*87/100)

    # <----END



    def ConsistWindow(self):
        textboxstyleSheet = """QPlainTextEdit{border:1px solid  #383838; color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0);}"""
        textboxstyleSheet1= """QLineEdit{border:1px solid  #383838; color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0);}"""
        textboxstyleSheet3 = """QLabel{color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0);}"""
        calendar="""QAbstractItemView:enabled  {background-color: rgba(28, 28, 31);color:rgb(132,189,0); }
                    QToolButton {background-color: rgba(28, 28, 31);color:rgb(132,189,0);}
                    QSpinBox    {background-color: rgba(28, 28, 31);color:rgb(132,189,0);}
                    QMenu   {background-color: rgba(28, 28, 31);color:rgb(132,189,0);}
                    QWidget{background-color: rgba(28, 28, 31);color:rgb(132,189,0);}
                    QAbstractItemView:disabled  {background-color: rgba(28, 28, 31);color:rgb(132,189,0);
                    QWidget#qt_calendar_navigationbar {background-color: rgba(28, 28, 31);color:rgb(132,189,0);}
        }"""
        #Insert label
        self.textBox = QPlainTextEdit(self)
        self.textBox.move(self.WindowWidth*7/100, self.WindowHeight*37/100)
        self.textBox.resize(self.WindowWidth*86/100,self.WindowHeight*48/100)
        self.textBox.setStyleSheet(textboxstyleSheet)

        #Calendar
        self.calendar = QPushButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap("img/calendar.png"))
        self.calendar.setIcon(icon)
        self.calendar.move(self.WindowWidth*40/100, self.WindowHeight*17/100)
        self.calendar.setStyleSheet("QPushButton { color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0); }")

        #Theme label
        self.TopicTheme = QLabel("Temat:",self)
        self.TopicTheme.setStyleSheet(textboxstyleSheet3)
        self.TopicTheme.move(self.WindowWidth*7/100,self.WindowHeight*10/100)

        #Content label
        self.TopicTheme = QLabel("Treść:", self)
        self.TopicTheme.setStyleSheet(textboxstyleSheet3)
        self.TopicTheme.move(self.WindowWidth*7/100, self.WindowHeight*30/100)

        #Topic input
        self.Topic_articule = QLineEdit(self)
        self.Topic_articule.move(self.WindowWidth*7/100, self.WindowHeight*18/100)
        self.Topic_articule.resize(self.WindowWidth*32/100, self.WindowHeight*8/100)
        self.Topic_articule.setStyleSheet(textboxstyleSheet1)

        self.AcceptButton = QPushButton('Zatwierdz', self)
        self.AcceptButton.setStyleSheet("QPushButton { color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0); }")
        self.AcceptButton.move(self.WindowWidth*45/100, self.WindowHeight*85/100)
        self.AcceptButton.clicked.connect(self.finish)

        self.CancelButton = QPushButton('Anuluj', self)
        self.CancelButton.setStyleSheet("QPushButton { color:rgb(132,189,0); background-color: rgba(0, 0, 0, 0); }")
        self.CancelButton.move(self.WindowWidth*35/100, self.WindowHeight*85/100)
        self.CancelButton.clicked.connect(self.cancel)

        self.lbl = QLabel(self)
        self.lbl.setStyleSheet(textboxstyleSheet3)
        self.lbl.move(self.WindowWidth*70/100, self.WindowHeight*18/100)
        self.cal = QCalendarWidget(self)

        self.cal.setStyleSheet(calendar)

        self.cal.hide()
        self.calendar.clicked.connect(self.calendar_app)




    def calendar_app(self):
        self.cal.show()
        self.cal.setGridVisible(True)
        self.cal.move(20, 20)
        self.cal.clicked[QDate].connect(self.showDate)

        self.date = self.cal.selectedDate()
        self.lbl.setGeometry(QRect(self.lbl.x(), self.lbl.y(), self.WindowWidth*20/100 ,self.lbl.height()))
        self.lbl.setText(self.date.toString())


    def showDate(self):
        self.lbl.setText(self.date.toString())
        self.cal.hide()
    def cancel(self):
        self.destroy()

    def finish(self):
        textboxValue = self.textBox.toPlainText()
        textboxValue2 = self.Topic_articule.text()
        datetext = self.date.toString()

        print("Tresc: {0} Temat: {1} Date: {2}".format(textboxValue,textboxValue2,datetext))

        connection = mysql.connector.connect(user='NoteUser', password='Note',host='192.168.1.45',database='NoteDB')
        DataBaseOperate = connection.cursor()

        query = "INSERT INTO Tasks VALUE(null,'{0}','{1}','{2}',2,{3},1)".format(datetext,textboxValue2,textboxValue,self.uID)
        try:
            DataBaseOperate.execute(query)
            connection.commit()
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
        connection.close()
        self.destroy()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Insert()
    sys.exit(app.exec_())