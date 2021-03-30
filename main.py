#!/usr/bin/python3
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

from src.scene import Scene

class StackMaker(QMainWindow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.initUI()

  def _createActions(self):
    main_path = os.path.dirname(__file__)

    # https://realpython.com/python-menus-toolbars/ for menu stuff later
    self.exitAct = QAction(QIcon(os.path.join(main_path, './assets/icons/exit.png')), '&Exit', self)
    self.exitAct.setShortcut('Ctrl+Q')
    self.exitAct.setStatusTip('Exit application')
    self.exitAct.triggered.connect(qApp.quit)

    self.copyAct = QAction(QIcon(os.path.join(main_path, './assets/icons/copy.png')), '&Copy', self)
    self.copyAct.setShortcut('Ctrl+C')
    self.copyAct.setStatusTip('Copy entire board')
    self.copyAct.triggered.connect(self.copy)

    self.eraseAct = QAction(QIcon(QPixmap(os.path.join(main_path, './assets/tile0.png')).scaled(16, 16)), '&Erase', self)
    self.eraseAct.setShortcut('e')
    self.eraseAct.setStatusTip('Erase cell')
    self.eraseAct.triggered.connect(lambda : self.scene.setCellState(0))

    self.fillWhiteAct = QAction(QIcon(QPixmap(os.path.join(main_path, './assets/tile1.png')).scaled(16, 16)), '&White Cell', self)
    self.fillWhiteAct.setShortcut('1')
    self.fillWhiteAct.setStatusTip('Paint the white cell')
    self.fillWhiteAct.triggered.connect(lambda : self.scene.setCellState(1))

    self.fillLightAct = QAction(QIcon(QPixmap(os.path.join(main_path, './assets/tile2.png')).scaled(16, 16)), '&Light Cell', self)
    self.fillLightAct.setShortcut('2')
    self.fillLightAct.setStatusTip('Paint the light cell')
    self.fillLightAct.triggered.connect(lambda : self.scene.setCellState(2))

    self.fillDarkAct = QAction(QIcon(QPixmap(os.path.join(main_path, './assets/tile3.png')).scaled(16, 16)), '&Dark Cell', self)
    self.fillDarkAct.setShortcut('3')
    self.fillDarkAct.setStatusTip('Paint the dark cell')
    self.fillDarkAct.triggered.connect(lambda : self.scene.setCellState(3))

    pieceNames = ['T','J','Z','O','S','L','I']
    self.pieceActs = []
    for i in range(7):
      pieceAct = QAction(QIcon(QPixmap(os.path.join(main_path, f'./assets/{pieceNames[i]}.png')).scaled(16, 16)), pieceNames[i], self)
      pieceAct.setShortcut(pieceNames[i])
      pieceAct.setStatusTip(f'Draw the {pieceNames[i]} piece')
      # Ugly solution but it works
      # pieceAct.triggered.connect(lambda x=False,i=i: print(f'Selected {pieceNames[i]}'))
      pieceAct.triggered.connect(lambda x=False,i=i: self.scene.cursor.setType((i, 0)))
      # pieceAct.triggered.connect(lambda *args: print(args))
      self.pieceActs.append(pieceAct)

    self.connectStatusAct = QAction(QIcon(), '&Enable/Disable', self)
    self.connectStatusAct.triggered.connect(self.enableTracking)

    self.toggleMirrorAct = QAction(QIcon(), '&Toggle Mirror', self)
    self.toggleMirrorAct.setShortcut('Ctrl+M')
    self.toggleMirrorAct.setEnabled(False)
    self.toggleMirrorAct.triggered.connect(self.toggleMirror)

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
    for i in range(7):
      editMenu.addAction(self.pieceActs[i])

    connectMenu = menubar.addMenu('&Connect')
    connectMenu.addAction(self.connectStatusAct)
    connectMenu.addAction(self.toggleMirrorAct)

  def _createToolBar(self):
    self.toolbar = self.addToolBar('test')
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
    statusbar.setStyleSheet('QStatusBar{border-top: 1px outset grey;}')

    self.resize(768, 720 + self.statusBar().sizeHint().height() + self.menuBar().sizeHint().height() + self.toolbar.height())
    self.center()
    self.setWindowTitle('Stackmaker')

    self.scene = Scene(10, 20)

    self.view = QGraphicsView(self.scene)
    self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.setCentralWidget(self.view)
    self.show()

  def center(self):
    '''centers the window on the screen'''

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
    self.statusBar().showMessage('Copied!', 500)

  def toggleMirror(self):
    self.scene.ocrHandler.socket.blockSignals(not self.scene.ocrHandler.socket.signalsBlocked())

  def enableTracking(self):
    if not self.scene.ocrHandler.connected:
      print('Awaiting connection...')
      self.scene.ocrHandler.listen(QHostAddress.LocalHost, 3338)
      self.toggleMirrorAct.setEnabled(True)
    else:
      print('Disconnecting')
      self.scene.ocrHandler.exit()
      self.toggleMirrorAct.setEnabled(False)

def main():
  app = QApplication(sys.argv)
  ex = StackMaker()
  sys.exit(app.exec_())


if __name__ == '__main__':
    main()
