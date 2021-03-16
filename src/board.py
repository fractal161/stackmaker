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
    bgImage = QPixmap('./assets/boardLayout.png')
    bgImage = bgImage.scaled(bgImage.width(), bgImage.height())
    self.image = self.addPixmap(bgImage)
    tile = QPixmap('./assets/tile0.png')
    self.cells = [[Cell(j, i) for j in range(self.width)] for i in range(self.height)]
    for i in range(self.height):
      for j in range(self.width):
        self.cells[i][j].setOffset((12+j)*8, (6+i)*8)
        self.addItem(self.cells[i][j])

    self.cellType = 1
    self.drawMode = False

    self.top = [Digit(0) for i in range(6)]
    self.score = [Digit(0) for i in range(6)]
    for i in range(6):
      self.top[i].setOffset((24+i)*8, 5*8)
      self.addItem(self.top[i])

      self.score[i].setOffset((24+i)*8, 8*8)
      self.addItem(self.score[i])

    self.lines = [Digit(0) for i in range(3)]
    for i in range(3):
      self.lines[i].setOffset((19+i)*8, 3*8)
      self.addItem(self.lines[i])

    self.level = [Digit(0) for i in range(2)]
    for i in range(2):
      self.level[i].setOffset((26+i)*8, 21*8)
      self.addItem(self.level[i])

    self.stats = Digit(1, 0xFFB53120)
    self.stats.setOffset((8)*8, 18*8)
    self.addItem(self.stats)

  def setCellType(self, type):
    self.cellType = type

  def setCell(self, y, x, type=None):
    if type is None:
      type = self.cellType
    self.cells[y][x].setState(type)

  def mousePressEvent(self, e):
    item = self.itemAt(e.scenePos(), QTransform())
    if isinstance(item, Cell):
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
      if isinstance(item, Cell):
        item.setState(self.cellType)

    super().mouseMoveEvent(e)
