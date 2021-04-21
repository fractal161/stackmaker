from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .tile import Cell
from .piece import Piece

class CursorItem(QGraphicsItem):
  pieceStates = [1, 2, 3, 1, 2, 3, 1]
  coords = [
    [
      [[0, 1], [0, 0], [1, 0], [-1, 0]],
      [[0, 1], [0, 0], [1, 0], [0, -1]],
      [[-1, 0], [0, 0], [1, 0], [0, -1]],
      [[0, 1], [0, 0], [0, -1], [-1, 0]]
    ],
    [
      [[-1, 0], [0, 0], [1, 0], [1, 1]],
      [[0, -1], [1, -1], [0, 0], [0, 1]],
      [[-1, -1], [-1, 0], [0, 0], [1, 0]],
      [[0, -1], [0, 0], [-1, 1], [0, 1]]
    ],
    [
      [[-1, 0], [0, 0], [0, 1], [1, 1]],
      [[1, -1], [0, 0], [1, 0], [0, 1]]
    ],
    [
      [[-1, 0], [0, 0], [-1, 1], [0, 1]]
    ],
    [
      [[0, 0], [1, 0], [-1, 1], [0, 1]],
      [[0, -1], [0, 0], [1, 0], [1, 1]]
    ],
    [
    [
      [-1, 0], [0, 0], [1, 0], [-1, 1]],
      [[0, -1], [0, 0], [0, 1], [1, 1]],
      [[1, -1], [-1, 0], [0, 0], [1, 0]],
      [[-1, -1], [0, -1], [0, 0], [0, 1]]
    ],
    [
      [[-2, 0], [-1, 0], [0, 0], [1, 0]],
      [[0, -2], [0, -1], [0, 0], [0, 1]]
    ]
  ]

  def __init__(self, type, meta, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.type = type
    self.meta = meta
    self.setType(self.type)
    self.boundingRect()

  # For now, the int type represents a single cell, and a list represents a piece/orientation
  def setType(self, type):
    self.prepareGeometryChange()
    self.type = type
    self.items = []
    if isinstance(type, int):
      item = Cell(0, 0, self.meta)
      item.setState(type)
      item.setOpacity(127)
      self.items.append(item)
    else:
      state = CursorItem.pieceStates[type[0]]
      for coord in CursorItem.coords[type[0]][type[1]]:
        item = Cell(0, 0, self.meta)
        item.setState(state)
        item.setOffset(8 * coord[0], 8 * coord[1])
        item.setOpacity(127)
        self.items.append(item)
    self.update()

  def getCoords(self):
    if isinstance(self.type, int):
      return None
    return CursorItem.coords[self.type[0]][self.type[1]]

  def getState(self):
    if isinstance(self.type, int):
      return self.type
    return CursorItem.pieceStates[self.type[0]]

  def cw(self):
    self.setType([self.type[0], (self.type[1]+1)%len(CursorItem.coords[self.type[0]])])

  def ccw(self):
    self.setType([self.type[0], (self.type[1]-1)%len(CursorItem.coords[self.type[0]])])

  def updatePalette(self):
    for item in self.items:
      item.updatePalette()
      item.setOpacity(127)

  def updateOffset(self, x, y):
    # self.prepareGeometryChange()
    self.setTransform(QTransform().translate(x, y))

  # Make cursor item visible with respect to a certain rectangle
  def setVisible(self, visible, *args):
    super().setVisible(visible)

  '''
  This will probably be a massive headache, so let's not worry abt it now
  def setVisible(self, visible, rect=QRectF()):
    if not visible:
      for item in self.items:
        item.setVisible(False)
      self.update()
      return
    for item in self.items:
      # print(rect)
      # print(item.boundingRect())
      if rect.isNull() or rect.contains(item.sceneBoundingRect()):
        item.setVisible(True)
  '''

  def paint(self, painter, option, widget):
    for tile in self.items:
      tile.paint(painter, option, widget)
    # self.bound.paint(painter, option, widget)

  def boundingRect(self):
    if len(self.items) == 0:
      self.bound = QGraphicsRectItem(QRectF())
      self.bound.setPen(QPen(Qt.red, 1))
      return QRectF()
    # All items contain the center tile, so this is probably alright
    minx,miny,maxx,maxy=0,0,8,8
    for tile in self.items:
      minx = min(minx, tile.boundingRect().x())
      miny = min(miny, tile.boundingRect().y())
      maxx = max(maxx, tile.boundingRect().x()+tile.boundingRect().width())
      maxy = max(maxy, tile.boundingRect().y()+tile.boundingRect().height())
    self.bound = QGraphicsRectItem(QRectF(QPointF(minx, miny), QPointF(maxx, maxy)))
    self.bound.setPen(QPen(Qt.red, 1))
    # print(QRectF(QPointF(minx, miny), QPointF(maxx, maxy)))
    return QRectF(QPointF(minx, miny), QPointF(maxx, maxy))
