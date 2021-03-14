from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap, QTransform

from .tiles import Cell, Digit
from .connect import OcrHandler


class Board(QGraphicsScene):
  def __init__(self, width, height, *args, **kwargs):
    self.width = width
    self.height = height
    super().__init__(*args, **kwargs)
    self.initBoard()
    self.ocrHandler = OcrHandler(self.cells)

  def initBoard(self):
    self.setSceneRect(0,0,256,240)
    bgImage = QPixmap("./assets/boardLayout.png")
    bgImage = bgImage.scaled(bgImage.width(), bgImage.height())
    self.image = self.addPixmap(bgImage)
    tile = QPixmap("./assets/tile0.png")
    self.cells = [[Cell(j, i, tile) for j in range(self.width)] for i in range(self.height)]

    for i in range(0,self.height):
      for j in range(0,self.width):
        self.cells[i][j].setOffset((12+j)*8, (6+i)*8)
        self.addItem(self.cells[i][j])

    self.drawMode = False
    self.cellType = 1

  def setCellType(self, type):
    self.cellType = type

  def setCell(self, y, x, type=None):
    if type is None:
      type = self.cellType
    self.cells[y][x].setState(type)

  def mousePressEvent(self, e):
    item = self.itemAt(e.scenePos(), QTransform())
    if item is not None and item is not self.image:
      self.drawMode = True
      item.setState(self.cellType)
    super().mousePressEvent(e)

  def mouseReleaseEvent(self, e):
    self.drawMode = False
    super().mouseReleaseEvent(e)

  # Potentially inefficient, but seems fine for now
  def mouseMoveEvent(self, e):
    if self.drawMode:
      item = self.itemAt(e.scenePos(), QTransform())
      if item is not None and item is not self.image:
        item.setState(self.cellType)

    super().mouseMoveEvent(e)
