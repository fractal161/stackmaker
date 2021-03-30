from PyQt5.QtNetwork import QTcpServer, QHostAddress

import struct
import json
from random import randint
import src.debug

class OcrHandler(QTcpServer):
  def __init__(self, scene, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.scene = scene
    self.HOST = 'localhost'
    self.PORT = 3338
    self.dataBuffer = b''
    self.connected = False
    self.newConnection.connect(self.onConnected)
    self.lastField = ''

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

  def parse(self):
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
      self.updateScene(json.loads(str(msg, 'utf-8')))

  # Process data
  def updateScene(self, game):
    if self.lastField != game['field']:
      self.scene.level.setValue(int(game['level']))
      self.scene.meta['level'] = int(game['level'])
      self.scene.score.setValue(int(game['score']))
      self.scene.lines.setValue(int(game['lines']))
      self.scene.board.setCells(game['field'])
    self.lastField = game['field']
