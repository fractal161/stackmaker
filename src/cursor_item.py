from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .tile import Cell
from .piece import Piece

class CursorItem(QGraphicsItem):
  def __init__(self, type, meta, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.type = type
    self.items = [Cell(0, 0, meta)]
    self.items[0].setState(1)
    # self.items[1].setState(1)
    # self.items[1].setOffset(8,0)
    # self.items[2].setState(1)
    # self.items[2].setOffset(-8,0)
    # self.items[3].setState(1)
    # self.items[3].setOffset(0,8)

    # print(self.items[0].boundingRect())
    # print(self.items[1].boundingRect())
    self.boundingRect()
    self.meta = meta

  def updateOffset(self, x, y):
    # self.prepareGeometryChange()
    self.setTransform(QTransform().translate(x, y))

  def updateItemType(self, type):
    # self.prepareGeometryChange()
    pass

  def paint(self, painter, option, widget):
    for tile in self.items:
      tile.paint(painter, option, widget)
    # self.bound.paint(painter, option, widget)

  def boundingRect(self):
    if len(self.items) == 0:
      self.bound = QGraphicsRectItem(QRectF(0,0,0,0))
      self.bound.setPen(QPen(Qt.red, 1))
      return QRectF(0,0,0,0)
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
