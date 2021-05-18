# Extremely crude type that has metadata for a cell before/after
# x, y, type, transparency (not undoing level, so no need to do that)
from collections import namedtuple

CellData = namedtuple('CellData', ['x', 'y', 'state', 'transparency'])
CellAction = namedtuple('CellAction', ['old', 'new'])

class ActionBuffer():
  def __init__(self):
    self.buffer = []
    self.pointer = -1

  def append(self, actions):
    self.pointer += 1
    self.buffer.append(actions)

  def undo(self):
    if self.pointer == -1:
      return None
    self.pointer -= 1
    return self.buffer[self.pointer + 1]

  def redo(self):
    if self.pointer == len(self.buffer) - 1:
      return None
    self.pointer += 1
    return self.buffer[self.pointer]

  def removeForward(self):
    self.buffer = self.buffer[:self.pointer+1]
