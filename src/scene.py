import os

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QTransform

from .tile import Cell, Digit
from .tile_group import Board, Number
from .cursor_item import CursorItem
from .palette_item import PaletteItem
from .piece import Piece
from .connect import OcrHandler


class Scene(QGraphicsScene):
  def __init__(self, width, height, *args, **kwargs):
    self.width = width
    self.height = height
    self.meta = {
      'level' : 18,
      'cellState' : 1
    }
    super().__init__(*args, **kwargs)
    self.initScene()
    # Gonna be weird for a bit
    self.ocrHandler = OcrHandler(self)

  def initScene(self):
    main_path = os.path.dirname(__file__)
    self.setSceneRect(0,0,256,240)
    bgImage = QPixmap(os.path.join(os.path.dirname(__file__), '../assets/boardLayout.png'))
    self.image = self.addPixmap(bgImage)

    self.board = Board(self, 10, 20, self.meta)
    self.board.translate(12 * 8, 6 * 8)

    self.top = Number(self, 6)
    self.top.translate(24 * 8, 5 * 8)

    self.score = Number(self, 6)
    self.score.translate(24 * 8, 8 * 8)

    self.lines = Number(self, 3)
    self.lines.translate(19 * 8, 3 * 8)

    self.level = Number(self, 2, value=self.meta['level'])
    self.level.translate(26 * 8, 21 * 8)

    self.stats = []
    for i in range(7):
      statNum = Number(self, 3, 0xFFB53120)
      statNum.translate(6 * 8, (12 + 2 * i) * 8)
      self.stats.append(statNum)

    main_path = os.path.dirname(__file__)
    self.statsPieces = PaletteItem(QPixmap(os.path.join(main_path, f'../assets/pieceStats.png')))
    self.statsPieces.setOffset(24, 88)
    self.addItem(self.statsPieces)


    self.previewCoords = [(204,119), (204,119), (204,119), (208,119), (204,119), (204,119), (208,123)]
    self.previewType = 0
    self.preview = Piece(self.previewType, 0, self.meta, 255)
    self.addItem(self.preview)
    self.preview.updateOffset(*self.previewCoords[self.previewType])

    self.cursor = CursorItem(1, self.meta)
    self.addItem(self.cursor)
    self.cursor.setVisible(False)
    self.drawMode = False

  def setCellState(self, state):
    self.meta['cellState'] = state
    self.cursor.setType(state)

  def itemAtMouse(self, pos):
    itemList = self.items(pos)
    for item in itemList:
      if item != self.cursor:
        return item
    return None

  def mousePressEvent(self, e):
    item = self.itemAtMouse(e.scenePos())
    # Checks if mouse is inside next box
    if QRectF(192, 112, 32, 24).contains(e.scenePos()):
      if e.button() == Qt.LeftButton:
        self.previewType += 1
      else:
        self.previewType -= 1
      self.previewType %= 8
      if self.previewType == 7:
        self.preview.setVisible(False)
      else:
        self.preview.setVisible(True)
        self.preview.setType(self.previewType)
        self.preview.updateOffset(*self.previewCoords[self.previewType])
    if isinstance(item, Cell):
      # Drawing a single tile
      if isinstance(self.cursor.type, int):
        self.drawMode = True
        item.setState(self.meta['cellState'])
      #Drawing a piece, so need to drag stuff
      else:
        mouseX, mouseY = int((e.scenePos().x() // 8)-12), int((e.scenePos().y() // 8)-6)
        for coord in self.cursor.getCoords():
          tmpX = mouseX + coord[0]
          tmpY = mouseY + coord[1]
          if tmpY in range(20) and tmpX in range(10):
            self.board.cells[tmpY][tmpX].setState(self.cursor.getState())

    super().mousePressEvent(e)
    if item in self.level.digits:
      self.meta['level'] = self.level.getValue()
      self.board.updatePalette()
      self.cursor.updatePalette()
      self.preview.updatePalette()
      self.statsPieces.updatePalette(self.level.getValue() % 10)

  def mouseDoubleClickEvent(self, e):
    self.mousePressEvent(e)

  def mouseReleaseEvent(self, e):
    self.drawMode = False
    super().mouseReleaseEvent(e)

  # Potentially inefficient, but seems fine for now
  def mouseMoveEvent(self, e):
    mouseX, mouseY = 8*(e.scenePos().x() // 8), 8*(e.scenePos().y() // 8)
    if mouseX in range(12*8,12*8+10*8,8) and mouseY in range(6*8,6*8+20*8,8):
      self.cursor.setVisible(True)
      self.cursor.updateOffset(mouseX, mouseY)
    else:
      self.cursor.setVisible(False)

    item = self.itemAtMouse(e.scenePos())
    if self.drawMode:
      if isinstance(item, Cell):
        item.setState(self.meta['cellState'])
    super().mouseMoveEvent(e)
