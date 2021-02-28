#!/usr/bin/python3

"""
ZetCode PyQt5 tutorial

This program creates a menubar. The
menubar has one menu with an exit action.

Author: Jan Bodnar
Website: zetcode.com
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap


class StackMaker(QMainWindow):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    exitAct = QAction(QIcon('exit.png'), '&Exit', self)
    exitAct.setShortcut('Ctrl+Q')
    exitAct.setStatusTip('Exit application')
    exitAct.triggered.connect(qApp.quit)

    self.statusBar()

    menubar = self.menuBar()
    fileMenu = menubar.addMenu('&File')
    fileMenu.addAction(exitAct)

    # Put better math later
    self.resize(768, 746)
    self.center()
    self.setWindowTitle('Stackmaker')

    # Possibly better background methods
    # https://stackoverflow.com/questions/19939938/how-do-i-add-a-background-image-to-the-qmainwindow
    # https://stackoverflow.com/questions/19939938/how-do-i-add-a-background-image-to-the-qmainwindow
    self.bg = QPixmap("./assets/boardLayout.png")
    self.label = QLabel()
    self.label.setPixmap(self.bg.scaled(3*self.bg.width(), 3*self.bg.height()))
    self.setCentralWidget(self.label)

    self.show()

  def center(self):
    """centers the window on the screen"""

    screen = QDesktopWidget().screenGeometry()
    size = self.geometry()
    self.move(int((screen.width() - size.width()) / 2),
              int((screen.height() - size.height()) / 2))


def main():
  app = QApplication(sys.argv)
  ex = StackMaker()
  sys.exit(app.exec_())


if __name__ == '__main__':
    main()
