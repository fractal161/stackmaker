#!/usr/bin/python3

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from board import Board

class StackMaker(QMainWindow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.initUI()

  def initUI(self):
    # https://realpython.com/python-menus-toolbars/ for menu stuff later
    exitAct = QAction(QIcon('exit.png'), '&Exit', self)
    exitAct.setShortcut('Ctrl+Q')
    exitAct.setStatusTip('Exit application')
    exitAct.triggered.connect(qApp.quit)

    copyAct = QAction(QIcon('copy.png'), '&Copy', self)
    copyAct.setShortcut('Ctrl+C')
    copyAct.setStatusTip('Copy entire board')
    copyAct.triggered.connect(self.copy)

    statusbar = self.statusBar()
    statusbar.setStyleSheet("QStatusBar{border-top: 1px outset grey;}")

    menubar = self.menuBar()
    fileMenu = menubar.addMenu('&File')
    fileMenu.addAction(exitAct)
    fileMenu.addAction(copyAct)

    self.resize(768, 720 + self.statusBar().sizeHint().height()+ menubar.sizeHint().height())
    self.center()
    self.setWindowTitle('Stackmaker')


    self.scene = Board(10, 20)

    self.view = QGraphicsView(self.scene)
    self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.setCentralWidget(self.view)
    self.show()


  def center(self):
    """centers the window on the screen"""

    screen = QDesktopWidget().screenGeometry()
    size = self.geometry()
    self.move(int((screen.width() - size.width()) // 2),
              int((screen.height() - size.height()) // 2))

  # Resizing the viewport is necessary for some reason. Should check why this needs to be used
  def resizeEvent(self, e):
    self.view.viewport().resize(self.width(), self.height() - self.statusBar().sizeHint().height()-self.menuBar().sizeHint().height())
    self.view.fitInView(self.view.sceneRect(), Qt.KeepAspectRatio)

  def copy(self):
    clipboard = QGuiApplication.clipboard()

    board = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
    board.fill(Qt.transparent)
    painter = QPainter(board)
    self.scene.render(painter)

    clipboard.setImage(board)
    painter.end()
    self.statusBar().showMessage("Copied!", 1000)

def main():
  app = QApplication(sys.argv)
  ex = StackMaker()
  sys.exit(app.exec_())


if __name__ == '__main__':
    main()
