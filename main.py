#!/usr/bin/python3

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from src.board import Board
import src.debug

class StackMaker(QMainWindow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.initUI()

  def _createActions(self):
    # https://realpython.com/python-menus-toolbars/ for menu stuff later
    self.exitAct = QAction(QIcon('./assets/icons/exit.png'), '&Exit', self)
    self.exitAct.setShortcut('Ctrl+Q')
    self.exitAct.setStatusTip('Exit application')
    self.exitAct.triggered.connect(qApp.quit)

    self.copyAct = QAction(QIcon('./assets/icons/copy.png'), '&Copy', self)
    self.copyAct.setShortcut('Ctrl+C')
    self.copyAct.setStatusTip('Copy entire board')
    self.copyAct.triggered.connect(self.copy)

    self.eraseAct = QAction(QIcon(QPixmap('./assets/tile0.png').scaled(16, 16)), '&Erase', self)
    self.eraseAct.setShortcut('e')
    self.eraseAct.setStatusTip('Erase cell')
    self.eraseAct.triggered.connect(lambda : self.scene.setCellType(0))

    self.fillWhiteAct = QAction(QIcon(QPixmap('./assets/tile1.png').scaled(16, 16)), '&White Cell', self)
    self.fillWhiteAct.setShortcut('1')
    self.fillWhiteAct.setStatusTip('Paint the white cell')
    self.fillWhiteAct.triggered.connect(lambda : self.scene.setCellType(1))

    self.fillLightAct = QAction(QIcon(QPixmap('./assets/tile2.png').scaled(16, 16)), '&Light Cell', self)
    self.fillLightAct.setShortcut('2')
    self.fillLightAct.setStatusTip('Paint the light cell')
    self.fillLightAct.triggered.connect(lambda : self.scene.setCellType(2))

    self.fillDarkAct = QAction(QIcon(QPixmap('./assets/tile3.png').scaled(16, 16)), '&Dark Cell', self)
    self.fillDarkAct.setShortcut('3')
    self.fillDarkAct.setStatusTip('Paint the dark cell')
    self.fillDarkAct.triggered.connect(lambda : self.scene.setCellType(3))

  def _createMenuBar(self):
    menubar = self.menuBar()
    fileMenu = menubar.addMenu('&File')
    fileMenu.addAction(self.exitAct)
    fileMenu.addAction(self.copyAct)

    editMenu = menubar.addMenu('&Edit')
    editMenu.addAction(self.eraseAct)
    editMenu.addAction(self.fillWhiteAct)
    editMenu.addAction(self.fillLightAct)
    editMenu.addAction(self.fillDarkAct)

  def _createToolBar(self):
    self.toolbar = self.addToolBar("test")
    self.toolbar.setMovable(False)
    self.toolbar.addAction(self.eraseAct)
    self.toolbar.addAction(self.fillWhiteAct)
    self.toolbar.addAction(self.fillLightAct)
    self.toolbar.addAction(self.fillDarkAct)

  def initUI(self):
    self._createActions()
    self._createMenuBar()
    self._createToolBar()

    statusbar = self.statusBar()
    statusbar.setStyleSheet("QStatusBar{border-top: 1px outset grey;}")

    self.resize(768, 720 + self.statusBar().sizeHint().height() + self.menuBar().sizeHint().height() + self.toolbar.height())
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
    self.view.viewport().resize(self.width(), self.height() - self.statusBar().sizeHint().height()-self.menuBar().sizeHint().height()-self.toolbar.height())
    self.view.fitInView(self.view.sceneRect(), Qt.KeepAspectRatio)

  def copy(self):
    clipboard = QGuiApplication.clipboard()

    board = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
    board.fill(Qt.transparent)
    painter = QPainter(board)
    self.scene.render(painter)

    clipboard.setImage(board)
    painter.end()
    self.statusBar().showMessage("Copied!", 500)

  def doStuff(self):
    type = (1 + self.scene.cells[0][0].state) % 4
    for i in range(0, 20):
      for j in range(0, 10):
        self.scene.setCell(i,j,type)

def main():
  app = QApplication(sys.argv)
  ex = StackMaker()
  sys.exit(app.exec_())


if __name__ == '__main__':
    main()
