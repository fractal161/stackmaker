#!/usr/bin/python3

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, qApp, QLabel, QDesktopWidget, QPushButton, QGridLayout, QWidget, QStackedWidget, QStatusBar, QMenuBar
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush

'''
Next order of business is to get basic cell toggling. Can use
layout.setContentsMargins(0,0,0,0)
layout.setSpacing(0)
with a QGridLayout to make things flush with each other.
Get solid blocks first, then add in images later.
For later: possibly stack possible tiles, or just redraw?
'''

class Cells(QWidget):
  def __init__(self, width, height, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.initUI()

  def initUI(self):
    pass

class StackMaker(QMainWindow):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    # https://realpython.com/python-menus-toolbars/ for menu stuff later
    exitAct = QAction(QIcon('exit.png'), '&Exit', self)
    exitAct.setShortcut('Ctrl+Q')
    exitAct.setStatusTip('Exit application')
    exitAct.triggered.connect(qApp.quit)

    statusbar = self.statusBar()
    statusbar.setStyleSheet("QStatusBar{border-top: 1px outset grey;}")

    menubar = self.menuBar()
    fileMenu = menubar.addMenu('&File')
    fileMenu.addAction(exitAct)

    self.resize(768, 720 + self.statusBar().sizeHint().height()+ menubar.sizeHint().height())
    self.center()
    self.setWindowTitle('Stackmaker')

    # Possibly better background methods
    # https://stackoverflow.com/questions/19939938/how-do-i-add-a-background-image-to-the-qmainwindow
    self.parent = QWidget()
    self.parent.setMinimumSize(256, 240)
    self.setCentralWidget(self.parent)

    bgImage = QPixmap("./assets/boardLayout.png")
    bgImage = bgImage.scaled(3*bgImage.width(), 3*bgImage.height())
    self.bgLabel = QLabel(self.parent)
    self.bgLabel.setPixmap(bgImage)
    self.bgLabel.resize(bgImage.size())
    self.bgLabel.setAlignment(Qt.AlignCenter)
    self.parent.resize(self.bgLabel.size())


    # BACKGROUND OPTION 2
    # palette = self.palette()
    # palette.setBrush(QPalette.Window, QBrush(bgImage));
    # self.setPalette(palette);

    # Use abstract button instead? https://doc.qt.io/qt-5/qabstractbutton.html#details
    self.cells = QWidget(self.parent)
    cellLayout = QGridLayout()
    for i in range(0,20):
      for j in range(0,10):
        cell = QPushButton()
        cell.clicked.connect(lambda x, i=i, j=j : print("clicked!",i,j))
        cell.setStyleSheet('''QPushButton{background-color: black;
        border-image: url(./assets/tile1.png);
        }''')
        cell.setFixedSize(24,24)
        cellLayout.addWidget(cell, i, j)
    cellLayout.setContentsMargins(0,0,0,0)
    cellLayout.setSpacing(0)
    self.cells.setLayout(cellLayout)
    #
    self.cells.resize(10*24,20*24)
    # This doesn't work, but resizing fixes it?
    self.cells.move((self.parent.width() - self.cells.width()) // 2, (self.parent.height() - self.cells.height()) // 2)

    self.show()

  def center(self):
    """centers the window on the screen"""

    screen = QDesktopWidget().screenGeometry()
    size = self.geometry()
    self.move(int((screen.width() - size.width()) / 2),
              int((screen.height() - size.height()) / 2))

  # Resizing should be more rigid.
  # It also causes flicker rn: https://doc.qt.io/archives/qq/qq06-flicker-free.html
  def resizeEvent(self, e):
    bgImage = QPixmap("./assets/boardLayout.png")
    bgImage = bgImage.scaled(self.width(), self.height() - (self.statusBar().sizeHint().height() + self.menuBar().sizeHint().height()), Qt.KeepAspectRatio)
    self.bgLabel.resize(bgImage.size())
    self.bgLabel.setPixmap(bgImage)
    self.bgLabel.move((self.parent.width() - self.bgLabel.width()) // 2, (self.parent.height() - self.bgLabel.height()) // 2)
    cellUnit = self.bgLabel.width() / 32
    self.cells.resize(int(10*cellUnit), int(20*cellUnit))
    self.cells.move((self.parent.width() - self.cells.width()) // 2+cellUnit, (self.parent.height() - self.cells.height()) // 2+cellUnit)


def main():
  app = QApplication(sys.argv)
  ex = StackMaker()
  sys.exit(app.exec_())


if __name__ == '__main__':
    main()
