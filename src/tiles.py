from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap

class Cell(QGraphicsPixmapItem):
  def __init__(self, x, y, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.state = 0
    self.x = x
    self.y = y
    self.setAcceptHoverEvents(True)
    # self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

  def setState(self, state):
    self.state = state
    self.setPixmap(QPixmap(f'./assets/tile{state}.png'))

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
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.state = 0
    self.setAcceptHoverEvents(True)
    # self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

  def setState(self, state):
    self.state = state
    self.setPixmap(QPixmap(f'./assets/{state}.png'))

  # Need to figure out how to handle this
  # def hoverEnterEvent(self, e):
  #   if not self.state:
  #     self.setPixmap(QPixmap('./assets/tile1.png'))
  #
  # def hoverLeaveEvent(self, e):
  #   if not self.state:
  #     self.setPixmap(QPixmap('./assets/tile0.png'))
