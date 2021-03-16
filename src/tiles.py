from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage

class Cell(QGraphicsPixmapItem):
  tiles = []
  for i in range(4):
    tiles.append(QImage(f'./assets/tile{i}.png').convertToFormat(3, [0xFFFFFEFF, 0xFF000000, 0xFF4240FF, 0xFFB53120]))

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

  def __init__(self, x, y, level=8):
    super().__init__()
    self.state = 0
    self.x = x
    self.y = y
    self.level = level
    self.setState(self.state)
    self.setAcceptHoverEvents(True)
    # self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

  def setState(self, state):
    self.state = state
    newCell = Cell.tiles[state].copy()
    newCell.setColor(2, Cell.colors[self.level % 10][0])
    newCell.setColor(3, Cell.colors[self.level % 10][1])
    self.setPixmap(QPixmap(newCell))

  def setLevel(self, level):
    self.level = level
    setState(self.state)

  def toggleState(self):
    if self.state:
      self.setPixmap(QPixmap('./assets/tile0.png'))
      self.state = 0
    else:
      self.setPixmap(QPixmap('./assets/tile1.png'))
      self.state = 1

  # Need to figure out how to handle this
  def hoverEnterEvent(self, e):
    if not self.state:
      self.setPixmap(QPixmap('./assets/tile1.png'))

  def hoverLeaveEvent(self, e):
    if not self.state:
      self.setPixmap(QPixmap('./assets/tile0.png'))

class Digit(QGraphicsPixmapItem):
  numbers = []
  for i in range(10):
    num = QImage(f'./assets/{i}.png').convertToFormat(1)
    numbers.append(num)

  def __init__(self, state, color=0xFFFFFEFF):
    super().__init__()
    self.state = state
    self.color = color
    self.setState(self.state)
    self.setAcceptHoverEvents(True)

  def setState(self, state):
    self.state = state
    newDigit = Digit.numbers[state].copy()
    newDigit.setColor(0, self.color)
    self.setPixmap(QPixmap(newDigit))
