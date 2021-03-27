import os

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap, QTransform

from .tile import Cell, Digit
from .tile_group import Board, Number
from .cursor_item import CursorItem
from .connect import OcrHandler


class Scene(QGraphicsScene):
  def __init__(self, width, height, *args, **kwargs):
    self.width = width
    self.height = height
    self.meta = {
      'level' : 18,
      'cellType' : 1
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

    self.cursor = CursorItem(0, self.meta)
    self.addItem(self.cursor)
    self.cursor.setVisible(False)
    self.drawMode = False

  def setCellType(self, type):
    self.meta['cellType'] = type

  def itemAtMouse(self, pos):
    itemList = self.items(pos)
    for item in itemList:
      if item != self.cursor:
        return item
    return None

  def mousePressEvent(self, e):
    # print(e.scenePos())
    # item = self.itemAt(e.scenePos(), QTransform())
    item = self.itemAtMouse(e.scenePos())
    if isinstance(item, Cell):
      self.drawMode = True
      item.setState(self.meta['cellType'])
    super().mousePressEvent(e)
    if item in self.level.digits:
      self.meta['level'] = self.level.getValue()
      self.board.updatePalette()

  def mouseDoubleClickEvent(self, e):
    self.mousePressEvent(e)

  def mouseReleaseEvent(self, e):
    self.drawMode = False
    super().mouseReleaseEvent(e)

  # Potentially inefficient, but seems fine for now
  def mouseMoveEvent(self, e):
    # print(e.scenePos())
    mouseX, mouseY = 8*(e.scenePos().x() // 8), 8*(e.scenePos().y() // 8)
    if mouseX in range(12*8,12*8+10*8,8) and mouseY in range(6*8,6*8+20*8,8):
      self.cursor.setVisible(True)
      self.cursor.updateOffset(mouseX, mouseY)
    else:
      self.cursor.setVisible(False)
    # This usually works
    # item = self.items(e.scenePos())[1]
    item = self.itemAtMouse(e.scenePos())
    # item = self.itemAt(e.scenePos(), QTransform())
    # if item is not None:
    #   print(item.boundingBox())
    if self.drawMode:
      # item = self.itemAtMouse(e.scenePos())
      if isinstance(item, Cell):
        item.setState(self.meta['cellType'])
    super().mouseMoveEvent(e)
