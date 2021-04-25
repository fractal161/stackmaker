from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItemGroup, QGraphicsItem
from PyQt5.QtGui import QPixmap, QImage, QTransform

from .tile import Cell, Digit

class Board():
  def __init__(self, scene, width, height, meta):
    self.width = width
    self.height = height
    self.meta = meta

    self.cells = [[Cell(meta) for j in range(self.width)] for i in range(self.height)]
    for i in range(self.height):
      for j in range(self.width):
        self.cells[i][j].setOffset(8 * j, 8 * i)
        scene.addItem(self.cells[i][j])

  def translate(self, x, y):
    for i in range(self.height):
      for j in range(self.width):
        self.cells[i][j].setTransform(QTransform().translate(x, y))

  def updatePalette(self):
    for i in range(self.height):
      for j in range(self.width):
        self.cells[i][j].updatePalette()

  # Accepts a string
  def setCells(self, newCells):
    for i in range(self.height):
      for j in range(self.width):
        newState = int(newCells[i * self.width + j])
        self.cells[i][j].setState(newState)

class Number():
  def __init__(self, scene, length, color=0xFFFFFEFF, value=0):
    self.length = length
    self.color = color

    self.digits = []
    for i in range(length):
      digit = Digit(value % 10, self.color)
      digit.setOffset((length - i - 1) * 8, 0)
      scene.addItem(digit)
      self.digits.insert(0, digit)

      value //= 10

  def translate(self, x, y):
    for i in range(self.length):
      self.digits[i].setTransform(QTransform().translate(x, y))

  def getValue(self):
    value = 0
    for i in range(self.length):
      value *= 10
      value += self.digits[i].state
    return value

  def setValue(self, value):
    for i in range(self.length):
      self.digits[self.length - i - 1].setState(value % 10)
      value //= 10
