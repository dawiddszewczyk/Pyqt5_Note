import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase, QImage, QPalette, QBrush, QColor, QPainter
from PyQt5.QtCore import QSize
from PyQt5 import QtCore
from Note import *

class ShowFullTask(QWidget):
        def __init__(self,ID):
            super(ShowFullTask, self).__init__()
            # <------- Set a font to datafontbase
            QFontDatabase.addApplicationFont("Fonts/DukeFill.ttf")
            QFontDatabase.addApplicationFont("Fonts/Focus-Medium.ttf")
            QFontDatabase.addApplicationFont("Fonts/Roboto-ThinItalic.ttf")
            print(ID)
            # <--- END
            self.preview_screen = QApplication.primaryScreen().grabWindow(0)
            self.size = self.preview_screen.size()

            # Photo On the Background
            oImage = QImage("img/tlo.png")
            sImage = oImage.scaled(QSize(800, 500))
            palette = QPalette()
            palette.setBrush(10, QBrush(sImage))
            self.setPalette(palette)
            # <----END

            # Set Window Size ( x ,y ,width ,height )
            #               (420,0         , 262,5         , 840,0         , 525.0          )
            self.setGeometry(self.size.width() / 3, self.size.height() / 3, self.size.width() / 3,self.size.height() / 3)
            print(self.size.width() / 3, self.size.height() / 3, self.size.width() / 2,self.size.height() / 2)
            # <----END
            # Set windows Without Frame
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

            exit = QLabel("           ", self)
            exit.move(500, 0)
            exit.mousePressEvent = self.exit

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

            # Exit
            self.draw.setBrush(QColor(220, 20, 60))
            self.draw.drawRect(500, 0, 35, 15)

            # <----END

        def exit(self, event):
            self.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShowFullTask()
    sys.exit(app.exec_())