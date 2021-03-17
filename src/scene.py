from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap, QTransform

from .tile import Cell, Digit
from .tile_group import Board, Number
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
    self.ocrHandler = OcrHandler(self.board)

  def initScene(self):
    self.setSceneRect(0,0,256,240)
    bgImage = QPixmap('./assets/boardLayout.png')
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

    self.drawMode = False

  def setCellType(self, type):
    self.meta['cellType'] = type

  def mousePressEvent(self, e):
    item = self.itemAt(e.scenePos(), QTransform())
    if isinstance(item, Cell):
      self.drawMode = True
      item.setState(self.meta['cellType'])
    super().mousePressEvent(e)

  def mouseReleaseEvent(self, e):
    self.drawMode = False
    super().mouseReleaseEvent(e)

  # Potentially inefficient, but seems fine for now
  def mouseMoveEvent(self, e):
    if self.drawMode:
      item = self.itemAt(e.scenePos(), QTransform())
      if isinstance(item, Cell):
        item.setState(self.meta['cellType'])
    super().mouseMoveEvent(e)
