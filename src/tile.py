import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage



class Cell(QGraphicsPixmapItem):
  tiles = []
  for i in range(4):
    main_path = os.path.dirname(__file__)
    tiles.append(QImage(os.path.join(main_path, f'../assets/tile{i}.png')).convertToFormat(3, [0xFFFFFEFF, 0xFF000000, 0xFF4240FF, 0xFFB53120]))

  colors = [
    [0xFF4240FF, 0xFF64B0FF],
    [0xFF0C9300, 0xFF88D800],
    [0xFFA01ACC, 0xFFF36AFF],
    [0xFF4240FF, 0xFF5CE430],
    [0xFFB71E7B, 0xFF45E082],
    [0xFF45E082, 0xFF9290FF],
    [0xFFB53210, 0xFF666666],
    [0xFF7527FE, 0xFF6E0040],
    [0xFF4240FF, 0xFFB53120],
    [0xFFB53120, 0xFFEA9E22]
  ]

  def __init__(self, x, y, meta):
    super().__init__()
    self.state = 0
    self.oldstate = 0
    self.x = x
    self.y = y
    self.meta = meta
    self.setState(self.state)
    self.setAcceptHoverEvents(True)
    # self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

  def setOpacity(self, opacity):
    newCell = Cell.tiles[self.state].copy()
    newCell.setColor(2, Cell.colors[self.meta['level'] % 10][0])
    newCell.setColor(3, Cell.colors[self.meta['level'] % 10][1])
    newCell.setColorTable([color & ((opacity << 24) | 0x00FFFFFF) for color in newCell.colorTable()])
    self.setPixmap(QPixmap(newCell))

  def setState(self, state, backup=True):
    if backup:
      self.oldstate = self.state
    self.state = state
    newCell = Cell.tiles[state].copy()
    newCell.setColor(2, Cell.colors[self.meta['level'] % 10][0])
    newCell.setColor(3, Cell.colors[self.meta['level'] % 10][1])
    self.setPixmap(QPixmap(newCell))

  def updatePalette(self):
    self.setState(self.state, False)

  def restoreState(self):
    self.setState(self.oldstate)

class Digit(QGraphicsPixmapItem):
  numbers = []
  for i in range(10):
    main_path = os.path.dirname(__file__)
    num = QImage(os.path.join(main_path, f'../assets/{i}.png')).convertToFormat(1)
    numbers.append(num)

  def __init__(self, state, color=0xFFFFFEFF):
    super().__init__()
    self.state = state
    self.color = color
    self.setState(self.state)

  def setState(self, state):
    self.state = state
    newDigit = Digit.numbers[state].copy()
    newDigit.setColor(0, self.color)
    self.setPixmap(QPixmap(newDigit))

  def mousePressEvent(self, e):
    if e.button() == Qt.LeftButton and self.state < 9:
      self.state += 1
      self.setState(self.state)
    if e.button() == Qt.RightButton and self.state > 0:
      self.state -= 1
      self.setState(self.state)
