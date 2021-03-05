#!/usr/bin/python3

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

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
    self.setPixmap(QPixmap(f"./assets/tile{state}.png"))

  def toggleState(self):
    if self.state:
      self.setPixmap(QPixmap("./assets/tile0.png"))
      self.state = 0
    else:
      self.setPixmap(QPixmap("./assets/tile1.png"))
      self.state = 1

  # def mousePressEvent(self, e):
  #   self.toggleState()

  def hoverEnterEvent(self, e):
    if not self.state:
      self.setPixmap(QPixmap("./assets/tile1.png"))

  def hoverLeaveEvent(self, e):
    if not self.state:
      self.setPixmap(QPixmap("./assets/tile0.png"))

'''
Game plan for proper drag-and-draw:
Use mousePressEvent and mouseReleaseEvent to initiate/terminate "draw move"
work with mouseMoveEvent and use itemAt/e.mousePos or whatever the method is to see what item needs to be updated.
Maybe keep a boolean array of which cells have been updated to reduce total painting.

'''

class Board(QGraphicsScene):
  def __init__(self, width, height, *args, **kwargs):
    self.width = width
    self.height = height
    super().__init__(*args, **kwargs)
    self.initBoard()

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

  def mousePressEvent(self, e):
    item = self.itemAt(e.scenePos(), QTransform())
    if item is not None and item is not self.image:
      self.drawMode = True
      item.setState(1)
    super().mousePressEvent(e)

  def mouseReleaseEvent(self, e):
    self.drawMode = False
    super().mouseReleaseEvent(e)

  # Potentially inefficient, but seems fine for now
  def mouseMoveEvent(self, e):
    if self.drawMode:
      item = self.itemAt(e.scenePos(), QTransform())
      if item is not None and item is not self.image:
        item.setState(1)

    super().mouseMoveEvent(e)
