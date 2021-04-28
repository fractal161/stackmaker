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

    self.ccwAct = QAction(QIcon(), '&Counterclockwise')
    self.ccwAct.setShortcut('Q')
    self.ccwAct.setStatusTip('Rotate counterclockwise')
    self.ccwAct.setEnabled(False)
    self.ccwAct.triggered.connect(self.scene.cursor.ccw)

    self.cwAct = QAction(QIcon(), '&Clockwise')
    self.cwAct.setShortcut('W')
    self.cwAct.setStatusTip('Rotate clockwise')
    self.cwAct.setEnabled(False)
    self.cwAct.triggered.connect(self.scene.cursor.cw)

    self.mainActs = QActionGroup(self)

    pieceNames = ['T','J','Z','O','S','L','I']
    self.pieceActs = []
    for i in range(7):
      pieceAct = QAction(QIcon(QPixmap(os.path.join(main_path, f'./assets/{pieceNames[i]}.png'))), pieceNames[i], self.mainActs)
      pieceAct.setShortcut(pieceNames[i])
      pieceAct.setStatusTip(f'Draw the {pieceNames[i]} piece')
      pieceAct.setCheckable(True)
      # Ugly solution but it works
      pieceAct.triggered.connect(lambda x=False,i=i: self.scene.cursor.setType([i, 0]))
      pieceAct.triggered.connect(lambda : self.ccwAct.setEnabled(True))
      pieceAct.triggered.connect(lambda : self.cwAct.setEnabled(True))
      self.pieceActs.append(pieceAct)

    self.cellActs = []

    self.eraseAct = QAction(QIcon(QPixmap(os.path.join(main_path, './assets/tile0.png')).scaled(16, 16)), '&Erase', self.mainActs)
    self.eraseAct.setShortcut('e')
    self.eraseAct.setStatusTip('Erase cell')
    self.eraseAct.setCheckable(True)
    self.eraseAct.triggered.connect(lambda : self.scene.setCellState(0))
    self.eraseAct.triggered.connect(lambda : self.ccwAct.setEnabled(False))
    self.eraseAct.triggered.connect(lambda : self.cwAct.setEnabled(False))
    self.cellActs.append(self.eraseAct)

    self.fillWhiteAct = QAction(QIcon(QPixmap(os.path.join(main_path, './assets/tile1.png')).scaled(16, 16)), '&White Cell', self.mainActs)
    self.fillWhiteAct.setShortcut('1')
    self.fillWhiteAct.setStatusTip('Paint the white cell')
    self.fillWhiteAct.setCheckable(True)
    self.fillWhiteAct.setChecked(True)
    self.fillWhiteAct.triggered.connect(lambda : self.scene.setCellState(1))
    self.fillWhiteAct.triggered.connect(lambda : self.ccwAct.setEnabled(False))
    self.fillWhiteAct.triggered.connect(lambda : self.cwAct.setEnabled(False))
    self.cellActs.append(self.fillWhiteAct)

    self.fillLightAct = QAction(QIcon(QPixmap(os.path.join(main_path, './assets/tile2.png')).scaled(16, 16)), '&Light Cell', self.mainActs)
    self.fillLightAct.setShortcut('2')
    self.fillLightAct.setStatusTip('Paint the light cell')
    self.fillLightAct.setCheckable(True)
    self.fillLightAct.triggered.connect(lambda : self.scene.setCellState(2))
    self.fillLightAct.triggered.connect(lambda : self.ccwAct.setEnabled(False))
    self.fillLightAct.triggered.connect(lambda : self.cwAct.setEnabled(False))
    self.cellActs.append(self.fillLightAct)

    self.fillDarkAct = QAction(QIcon(QPixmap(os.path.join(main_path, './assets/tile3.png')).scaled(16, 16)), '&Dark Cell', self.mainActs)
    self.fillDarkAct.setShortcut('3')
    self.fillDarkAct.setStatusTip('Paint the dark cell')
    self.fillDarkAct.setCheckable(True)
    self.fillDarkAct.triggered.connect(lambda : self.scene.setCellState(3))
    self.fillDarkAct.triggered.connect(lambda : self.ccwAct.setEnabled(False))
    self.fillDarkAct.triggered.connect(lambda : self.cwAct.setEnabled(False))
    self.cellActs.append(self.fillDarkAct)

    self.fillColAct = QAction(QIcon(QPixmap(os.path.join(main_path, './assets/tileStack.png'))), '&Fill Column', self.mainActs)
    self.fillColAct.setShortcut('C')
    self.fillColAct.setStatusTip('Fill basic stack.')
    self.fillColAct.setCheckable(True)
    self.fillColAct.triggered.connect(lambda : self.scene.setColCursor())
    self.fillColAct.triggered.connect(lambda : self.ccwAct.setEnabled(False))
    self.fillColAct.triggered.connect(lambda : self.cwAct.setEnabled(False))

    self.transparentAct = QAction(QIcon(), '&Transparent')
    self.transparentAct.setShortcut('Ctrl+V')
    self.transparentAct.setStatusTip('Draw with transparent cells')
    self.transparentAct.setCheckable(True)

    self.rgbAct = QAction(QIcon(), '&Option Colors')
    self.rgbAct.setShortcut('Ctrl+A')
    self.rgbAct.setStatusTip('Tint drawn objects with varying colors')
    self.rgbAct.setCheckable(True)

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

    drawMenu = menubar.addMenu('&Draw')
    for act in self.cellActs:
      drawMenu.addAction(act)
    drawMenu.addAction(self.fillColAct)
    # drawMenu.addSeparator()
    pieceMenu = drawMenu.addMenu('&Piece')
    for act in self.pieceActs:
      pieceMenu.addAction(act)
    pieceMenu.addSeparator()
    pieceMenu.addAction(self.ccwAct)
    pieceMenu.addAction(self.cwAct)

    viewMenu = menubar.addMenu('&View')
    viewMenu.addAction(self.transparentAct)
    viewMenu.addAction(self.rgbAct)

    connectMenu = menubar.addMenu('&Connect')
    connectMenu.addAction(self.connectStatusAct)
    connectMenu.addAction(self.toggleMirrorAct)

  def _createToolBar(self):
    self.toolbar = self.addToolBar('test')
    self.toolbar.setMovable(False)
    for act in self.cellActs:
      self.toolbar.addAction(act)
    self.toolbar.addAction(self.fillColAct)
    self.toolbar.addSeparator()
    for act in self.pieceActs:
      self.toolbar.addAction(act)

  def initUI(self):
    self.scene = Scene(10, 20)

    self._createActions()
    self._createMenuBar()
    self._createToolBar()

    statusbar = self.statusBar()
    statusbar.setStyleSheet('QStatusBar{border-top: 1px outset grey;}')

    self.resize(768, 720 + self.statusBar().sizeHint().height() + self.menuBar().sizeHint().height() + self.toolbar.height())
    self.center()
    self.setWindowTitle('Stackmaker')

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
  app.setWindowIcon(QIcon('./assets/tile3.png'))
  ex = StackMaker()
  sys.exit(app.exec_())


if __name__ == '__main__':
    main()
