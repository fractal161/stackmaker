import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage

# Internally represents the given image as a QImage with a small color table, which is easy to modify on command
class PaletteItem(QGraphicsPixmapItem):
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

  def __init__(self, imageFile, palette=8):
    super().__init__()
    self.palette = palette
    self.image = QImage(imageFile).convertToFormat(QImage.Format_Indexed8, [0xFFFFFEFF, 0xFF000000, 0xFF4240FF, 0xFFB53120])

    self.updatePalette(palette)
    # self.setPixmap(QPixmap(self.image))

  def setOpacity(self, opacity):
    self.image.setColorTable([color & ((opacity << 24) | 0x00FFFFFF) for color in self.image.colorTable()])
    self.setPixmap(QPixmap(self.image))

  # def setState(self, state):
  #   self.state = state
  #   newCell = Cell.tiles[state].copy()
  #   newCell.setColor(2, Cell.colors[self.meta['level'] % 10][0])
  #   newCell.setColor(3, Cell.colors[self.meta['level'] % 10][1])
  #   self.setPixmap(QPixmap(newCell))

  def updatePalette(self, palette):
    self.palette = palette
    self.image.setColor(2, PaletteItem.colors[palette][0])
    self.image.setColor(3, PaletteItem.colors[palette][1])
    self.setPixmap(QPixmap(self.image))
