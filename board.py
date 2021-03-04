#!/usr/bin/python3

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Cell(QGraphicsPixmapItem):
  def __init__(self, *args, **kwargs):
    self.on = False
    super().__init__(*args, **kwargs)

  def mousePressEvent(self, e):
    if self.on:
      self.setPixmap(QPixmap("./assets/tile0.png"))
      self.on = False
    else:
      self.setPixmap(QPixmap("./assets/tile1.png"))
      self.on = True

class Board(QGraphicsScene):
  def __init__(self, width, height, *args, **kwargs):
    self.width = width
    self.height = height
    super().__init__(*args, **kwargs)
    self.initBoard()

  def initBoard(self):
    # self.scene = QGraphicsScene()
    self.setSceneRect(0,0,256,240)
    bgImage = QPixmap("./assets/boardLayout.png")
    bgImage = bgImage.scaled(bgImage.width(), bgImage.height())
    image = self.addPixmap(bgImage)

    tile = QPixmap("./assets/tile0.png")
    for i in range(0,self.height):
      for j in range(0,self.width):
        cell = Cell(tile)
        cell.setOffset((12+j)*8, (6+i)*8)
        self.addItem(cell)
