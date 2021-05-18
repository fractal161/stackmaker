import os

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QTransform

from .tile import Cell, Digit
from .tile_group import Board, Number
from .cursor_item import CursorItem
from .palette_item import PaletteItem
from .piece import Piece
from .connect import OcrHandler
from .undo import *


class Scene(QGraphicsScene):
  def __init__(self, width, height, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.width = width
    self.height = height
    self.initScene()
    # Gonna be weird for a bit
    self.ocrHandler = OcrHandler(self)

  def initScene(self):
    main_path = os.path.dirname(__file__)
    self.setSceneRect(0,0,256,240)
    bgImage = QPixmap(os.path.join(os.path.dirname(__file__), '../assets/boardLayout.png'))
    self.image = self.addPixmap(bgImage)

    self.board = Board(self, 10, 20)
    self.board.translate(12 * 8, 6 * 8)

    self.top = Number(self, 6)
    self.top.translate(24 * 8, 5 * 8)

    self.score = Number(self, 6)
    self.score.translate(24 * 8, 8 * 8)

    self.lines = Number(self, 3)
    self.lines.translate(19 * 8, 3 * 8)

    self.level = Number(self, 2, value=18)
    self.level.translate(26 * 8, 21 * 8)

    self.stats = []
    for i in range(7):
      statNum = Number(self, 3, 0xFFB53120)
      statNum.translate(6 * 8, (12 + 2 * i) * 8)
      self.stats.append(statNum)

    main_path = os.path.dirname(__file__)
    self.statsPieces = PaletteItem(QPixmap(os.path.join(main_path, f'../assets/pieceStats.png')))
    self.statsPieces.setTransform(QTransform.fromTranslate(24, 88))
    self.addItem(self.statsPieces)


    self.previewCoords = [(204,119), (204,119), (204,119), (208,119), (204,119), (204,119), (208,123)]
    self.previewType = 0
    self.preview = Piece(self.previewType, 0, 255)
    self.addItem(self.preview)
    self.preview.updateOffset(*self.previewCoords[self.previewType])

    self.cursor = CursorItem(1)
    self.addItem(self.cursor)
    self.cursor.setVisible(False)

    self.cellState = 1
    self.transparentDraw = False
    self.drawMode = False
    self.lastMousePos = None

    self.actionBuffer = ActionBuffer()
    self.actionGroup = []

  def setCellState(self, state):
    self.cellState = state
    self.cursor.setType(state)

  def setColCursor(self):
    # Figure out height using current mouse position
    if self.lastMousePos is None:
      self.cursor.setType([-1, 0])
      return
    mouseY = self.lastMousePos.y() // 8
    height = int(max(0, 26 - mouseY))
    self.cursor.setType([-1, height])

  def drawCell(self, cell, state=None,buffer=True):
    x,y=int((cell.scenePos().x() - 96) // 8), int((cell.scenePos().y() - 48) // 8)
    oldData = CellData(x, y, cell.state, cell.opacity == 127)

    if state is None:
      cell.setState(self.cursor.getState())
    else:
      cell.setState(state)
    if self.transparentDraw:
      cell.setOpacity(127)
    if buffer and (oldData.state != cell.state or (oldData.transparency != (cell.opacity == 127))):
      newData = CellData(x, y, cell.state, cell.opacity == 127)
      self.actionBuffer.removeForward()
      self.actionGroup.append(CellAction(oldData, newData))


  def drawCol(self):
    boardX, boardY = int((self.lastMousePos.x() // 8)-12), int((self.lastMousePos.y() // 8)-6)
    if boardX < 0 or boardX > 9:
      return
    boardY = max(0, boardY)
    self.maxColHeight = min(self.maxColHeight, boardY)
    i = self.maxColHeight
    while i < boardY and i < 20:
      self.drawCell(self.board.cells[i][boardX], 0)
      i += 1
    while i < 20:
      self.drawCell(self.board.cells[i][boardX], 1)
      i += 1
    self.appendToBuffer()

  def setTransparentDraw(self, state):
    self.transparentDraw = state

  def updatePalette(self):
    level = self.level.getValue() % 10
    self.board.updatePalette(level)
    self.cursor.updatePalette(level)
    self.preview.updatePalette(level)
    self.statsPieces.updatePalette(level)

  def setPreview(self, type):
    self.previewType = type
    if type == 7:
      self.preview.setVisible(False)
    else:
      self.preview.setVisible(True)
      self.preview.setType(type)
      self.preview.updateOffset(*self.previewCoords[type])

  def appendToBuffer(self):
    if len(self.actionGroup) > 0:
      self.actionBuffer.append(self.actionGroup[:])
      self.actionGroup = []

  def undo(self):
    actions = self.actionBuffer.undo()
    if isinstance(actions, list) and isinstance(actions[0], CellAction):
      tmp = self.transparentDraw
      for act in actions:
        x,y = act.old.x, act.old.y
        self.transparentDraw = act.old.transparency
        self.drawCell(self.board.cells[y][x], act.old.state,False)
      self.transparentDraw = tmp

  def redo(self):
    actions = self.actionBuffer.redo()
    if isinstance(actions, list) and isinstance(actions[0], CellAction):
      tmp = self.transparentDraw
      for act in actions:
        x,y = act.new.x, act.new.y
        self.transparentDraw = act.new.transparency
        self.drawCell(self.board.cells[y][x], act.new.state,False)
      self.transparentDraw = tmp

  def itemAtMouse(self, pos):
    itemList = self.items(pos)
    for item in itemList:
      if item != self.cursor:
        return item
    return None

  def mousePressEvent(self, e):
    item = self.itemAtMouse(e.scenePos())
    # Checks if mouse is inside next box
    if QRectF(192, 112, 32, 24).contains(e.scenePos()):
      if e.button() == Qt.LeftButton:
        self.previewType += 1
      else:
        self.previewType -= 1
      self.previewType %= 8
      if self.previewType == 7:
        self.preview.setVisible(False)
      else:
        self.preview.setVisible(True)
        self.preview.setType(self.previewType)
        self.preview.updateOffset(*self.previewCoords[self.previewType])

    if isinstance(item, Cell):
      # Drawing a single tile
      if isinstance(self.cursor.type, int):
        self.drawMode = True
        self.drawCell(item)
        self.appendToBuffer()
      # Drawing a column
      elif self.cursor.type[0] == -1:
        self.drawMode = True
        self.maxColHeight = 19
        self.drawCol()
      #Drawing a piece, so need to drag stuff
      else:
        mouseX, mouseY = int((e.scenePos().x() // 8)-12), int((e.scenePos().y() // 8)-6)
        for coord in self.cursor.getCoords():
          tmpX = mouseX + coord[0]
          tmpY = mouseY + coord[1]
          if tmpY in range(20) and tmpX in range(10):
            self.drawCell(self.board.cells[tmpY][tmpX])
        self.appendToBuffer()

    super().mousePressEvent(e)
    if item in self.level.digits:
      self.updatePalette()

  def mouseDoubleClickEvent(self, e):
    self.mousePressEvent(e)

  def mouseReleaseEvent(self, e):
    self.drawMode = False
    super().mouseReleaseEvent(e)

  # Potentially inefficient, but seems fine for now
  def mouseMoveEvent(self, e):
    mouseX, mouseY = 8*(e.scenePos().x() // 8), 8*(e.scenePos().y() // 8)
    if mouseX in range(12*8,12*8+10*8,8) and mouseY in range(6*8,6*8+20*8,8):
      self.cursor.setVisible(True)
      self.cursor.updateOffset(mouseX, mouseY)
      # Update column height if necessary
      if isinstance(self.cursor.type, list) and self.cursor.type[0] == -1:
        self.setColCursor()
    else:
      self.cursor.setVisible(False)

    item = self.itemAtMouse(e.scenePos())
    if self.drawMode:
      if isinstance(self.cursor.type, list):
        self.drawCol()
      elif isinstance(item, Cell):
        self.drawCell(item)
        self.appendToBuffer()
    self.lastMousePos = e.scenePos()
    super().mouseMoveEvent(e)
