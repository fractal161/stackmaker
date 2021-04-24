from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .tile import Cell

class Piece(QGraphicsItem):
  tileStates = [1, 2, 3, 1, 2, 3, 1]
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
  def __init__(self, type, orient, meta, opacity=127, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.meta = meta
    self.opacity = opacity
    self.setType(type, orient)

  def setType(self, type, orient=0):
    self.prepareGeometryChange()
    self.type = type
    self.orient = orient
    self.items = []
    state = Piece.tileStates[type]
    for coord in Piece.coords[type][orient]:
      item = Cell(0, 0, self.meta)
      item.setState(state)
      item.setOffset(8 * coord[0], 8 * coord[1])
      item.setOpacity(self.opacity)
      self.items.append(item)

  def cw(self):
    self.setType([self.type[0], (self.type[1]+1)%len(CursorItem.coords[self.type[0]])])

  def ccw(self):
    self.setType([self.type[0], (self.type[1]-1)%len(CursorItem.coords[self.type[0]])])


  def updatePalette(self):
    for item in self.items:
      item.updatePalette()
      item.setOpacity(self.opacity)
    self.update()

  def updateOffset(self, x, y):
    # self.prepareGeometryChange()
    self.setTransform(QTransform().translate(x, y))

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
