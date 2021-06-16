#!/usr/bin/python3
import sys

from PyQt5.QtCore import Qt, QRect, QRectF, QPointF
from PyQt5.QtWidgets import (
QApplication, QAction, QActionGroup, qApp,
QDesktopWidget, QGraphicsView, QMainWindow, QRubberBand
)
from PyQt5.QtGui import QGuiApplication, QIcon, QPixmap, QImage, QPainter
from PyQt5.QtNetwork import QHostAddress

from src.scene import Scene
from src.util import resource_path

class View(QGraphicsView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.rubberBandActive = False
    self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
    self.baseRect = QRect()
    self.clearSelection()

  # Returns a QRect that covers the scene tile the coords are over
  def _getBox(self, pos):
    scenePos = self.mapToScene(pos)
    newX = scenePos.x() // 8
    newY = scenePos.y() // 8
    topLeft = QPointF(8*newX, 8*newY)
    bottomRight = topLeft+QPointF(8.0,8.0)
    return QRect(self.mapFromScene(topLeft), self.mapFromScene(bottomRight))

  def toggleBand(self):
    self.rubberBandActive = not self.rubberBandActive
    if self.rubberBandActive:
      self.scene().cursor.setVisible(False)
    else:
      self.clearSelection()

  def clearSelection(self):
    self.rubberBand.setGeometry(QRect())

  def selection(self):
    return self.rubberBand.geometry()

  def sceneSelection(self):
    topLeft = self.rubberBand.geometry().topLeft()
    topLeft = self.mapToScene(topLeft)
    bottomRight = self.rubberBand.geometry().bottomRight()
    bottomRight = self.mapToScene(bottomRight)
    return QRectF(topLeft, bottomRight)

  def mousePressEvent(self, e):
    if self.rubberBandActive:
      if e.button() == Qt.LeftButton:
        if self.rubberBand.geometry() == QRect():
          self.baseRect = self._getBox(e.pos())
          self.rubberBand.setGeometry(self.baseRect)
          self.rubberBand.show()
        else:
          self.clearSelection()
    else:
      super().mousePressEvent(e)
  def mouseMoveEvent(self, e):
    if self.rubberBandActive:
      if int(e.buttons()) & Qt.LeftButton and self.rubberBand.geometry() != QRect():
        newRect = self._getBox(e.pos())
        self.rubberBand.setGeometry(self.baseRect.united(newRect))
    else:
      super().mouseMoveEvent(e)


  def mouseReleaseEvent(self, e):
    super().mouseReleaseEvent(e)

  def mouseDoubleClickEvent(self, e):
    if not self.rubberBandActive:
      super().mouseDoubleClickEvent(e)
    # self.clearSelection()

class StackMaker(QMainWindow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.initUI()

  def _createActions(self):
    # https://realpython.com/python-menus-toolbars/ for menu stuff later
    self.exitAct = QAction(QIcon(resource_path('./assets/icons/exit.png')), '&Exit', self)
    self.exitAct.setShortcut('Ctrl+Q')
    self.exitAct.setStatusTip('Exit application')
    self.exitAct.triggered.connect(qApp.quit)

    self.copyAct = QAction(QIcon(resource_path('./assets/icons/copy.png')), '&Copy', self)
    self.copyAct.setShortcut('Ctrl+C')
    self.copyAct.setStatusTip('Copy entire board')
    self.copyAct.triggered.connect(self.copy)

    self.mainActs = QActionGroup(self)

    self.selectAct = QAction(QIcon(resource_path('./assets/icons/select.ico')), '&Select', self.mainActs)
    self.selectAct.setShortcut('Shift+S')
    self.selectAct.setStatusTip('Select board part for copying.')
    self.selectAct.setCheckable(True)
    self.selectAct.setEnabled(True)
    self.selectAct.toggled.connect(self.view.toggleBand)

    self.undoAct = QAction(QIcon(resource_path('./assets/icons/undo.ico')), '&Undo', self)
    self.undoAct.setShortcut('Ctrl+Z')
    self.undoAct.setStatusTip('Undo most recent action')
    self.undoAct.setEnabled(True)
    self.undoAct.triggered.connect(self.scene.undo)

    self.redoAct = QAction(QIcon(resource_path('./assets/icons/redo.ico')), '&Redo', self)
    self.redoAct.setShortcut('Ctrl+Y')
    self.redoAct.setStatusTip('Redo most recent action')
    self.redoAct.setEnabled(True)
    self.redoAct.triggered.connect(self.scene.redo)


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

    pieceNames = ['T','J','Z','O','S','L','I']
    self.pieceActs = []
    for i in range(7):
      pieceAct = QAction(QIcon(resource_path(f'./assets/icons/icon{pieceNames[i]}.ico')), pieceNames[i], self.mainActs)
      pieceAct.setShortcut(pieceNames[i])
      pieceAct.setStatusTip(f'Draw the {pieceNames[i]} piece')
      pieceAct.setCheckable(True)
      # Ugly solution but it works
      pieceAct.triggered.connect(lambda x=False,i=i: self.scene.cursor.setType([i, 0]))
      pieceAct.triggered.connect(lambda : self.ccwAct.setEnabled(True))
      pieceAct.triggered.connect(lambda : self.cwAct.setEnabled(True))
      self.pieceActs.append(pieceAct)

    self.cellActs = []
    icons = [
      QIcon(QPixmap(resource_path('./assets/tile0.png')).scaled(16, 16)),
      QIcon(resource_path('./assets/icons/whiteCell.ico')),
      QIcon(resource_path('./assets/icons/darkCell.ico')),
      QIcon(resource_path('./assets/icons/lightCell.ico')),
      QIcon(resource_path('./assets/icons/stack.ico'))
    ]
    names = ['&Erase', '&White Cell', '&Dark Cell', '&Light Cell', '&Stack Mode']
    shortcuts = ['E', '1', '2', '3', 'C']
    tips = ['Erase cell', 'Paint the white cell', 'Paint the dark cell', 'Paint the light cell', 'Fill basic stack']

    for i in range(5):
      cellAct = QAction(icons[i], names[i], self.mainActs)
      cellAct.setShortcut(shortcuts[i])
      cellAct.setStatusTip(tips[i])
      cellAct.setCheckable(True)
      if i == 4:
        cellAct.triggered.connect(lambda : self.scene.setColCursor())
      else:
        cellAct.triggered.connect(lambda x=False,i=i : self.scene.setCellState(i))
      cellAct.triggered.connect(lambda : self.ccwAct.setEnabled(False))
      cellAct.triggered.connect(lambda : self.cwAct.setEnabled(False))
      self.cellActs.append(cellAct)

    self.cellActs[1].setChecked(True)

    self.transparentAct = QAction(QIcon(), '&Transparent')
    self.transparentAct.setShortcut('Ctrl+V')
    self.transparentAct.setStatusTip('Draw with transparent cells')
    self.transparentAct.setCheckable(True)
    self.transparentAct.triggered.connect(lambda x : self.scene.setTransparentDraw(x))

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
    drawMenu.addAction(self.selectAct)
    drawMenu.addAction(self.undoAct)
    drawMenu.addAction(self.redoAct)
    for act in self.cellActs:
      drawMenu.addAction(act)
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
    self.toolbar.addAction(self.selectAct)
    self.toolbar.addAction(self.undoAct)
    self.toolbar.addAction(self.redoAct)
    self.toolbar.addSeparator()
    for act in self.cellActs:
      self.toolbar.addAction(act)
    self.toolbar.addSeparator()
    for act in self.pieceActs:
      self.toolbar.addAction(act)

  def initUI(self):
    self.scene = Scene(10, 20)

    self.view = View(self.scene)
    self.view.setCacheMode(QGraphicsView.CacheBackground)
    self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate);
    self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.setCentralWidget(self.view)

    self._createActions()
    self._createMenuBar()
    self._createToolBar()

    statusbar = self.statusBar()
    statusbar.setStyleSheet('QStatusBar{border-top: 1px outset grey;}')

    self.resize(768, 720 + self.statusBar().sizeHint().height() + self.menuBar().sizeHint().height() + self.toolbar.height())
    self.center()
    self.setWindowTitle('Stackmaker')

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
    rect = self.scene.sceneRect() if self.view.selection() == QRect() else self.view.sceneSelection()
    board = QImage(rect.size().toSize(), QImage.Format_ARGB32)
    board.fill(Qt.transparent)
    painter = QPainter(board)
    self.scene.render(painter, QRectF(), rect)
    board1 = board.scaled(board.width()*2, board.height()*2)

    clipboard.setImage(board1)
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
  app.setWindowIcon(QIcon(resource_path('./assets/mainIcon.png')))
  ex = StackMaker()
  sys.exit(app.exec_())


if __name__ == '__main__':
    main()
