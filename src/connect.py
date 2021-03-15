from PyQt5.QtNetwork import QTcpServer, QHostAddress

import struct
import json
from random import randint
import src.debug

class OcrHandler(QTcpServer):
  def __init__(self, cells, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.cells = cells
    self.HOST = 'localhost'
    self.PORT = 3338
    self.dataBuffer = b''
    self.connected = False
    self.newConnection.connect(self.onConnected)

  def onConnected(self):
    self.socket = self.nextPendingConnection()
    self.socket.readyRead.connect(self.parse)
    print('Connected!')
    self.connected = True
    self.close()

  def exit(self):
    self.connected = False
    self.socket.close()
    self.socket.readyRead.disconnect(self.parse)
    print('Disconnecting')

  # @src.debug.runtime
  def parse(self):
    # print('Connected by', addr)
    # print('test')
    # Get JSON data
    data = self.socket.readAll()
    # Parse size and board state
    self.dataBuffer += data
    # counter = 0
    msg = b''
    while len(self.dataBuffer) > 4:
      size = int(struct.unpack('<i', self.dataBuffer[0:4])[0])

      target_idx = size + 4
      if len(self.dataBuffer) < target_idx:
          break

      msg = self.dataBuffer[4:target_idx]

      self.dataBuffer = self.dataBuffer[target_idx:]
      # counter += 1
    # if debug:
    #   print(str(counter) + ' packets processed')
    if msg != b'':
      self.doStuff(json.loads(str(msg, 'utf-8')))

  # Process data
  def doStuff(self, game):
    field = game['field']
    for i in range(20):
      for j in range(10):
        type = int(field[i * 10 + j])
        self.cells[i][j].setState(type)
