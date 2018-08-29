#!/usr/bin/env python 
import sys
from PyQt5.QtWidgets import (QApplication,QHeaderView, QAbstractItemView, QTableView,
         QGroupBox, QHBoxLayout, QVBoxLayout, QWidget,  QTableWidget)
        
        
class Page2Win(QWidget):
    def __init__(self, parent=None):
        #BOX
        mainLayout = QVBoxLayout()
        boxGroup = QGroupBox("发送历史信息")
        super(Page2Win, self).__init__(parent)
        self.historyTv =  QTableView(self)
        layout = QHBoxLayout()
        layout.addWidget(self.historyTv)
        boxGroup.setLayout(layout)
        mainLayout.addWidget(boxGroup)
        self.setLayout(mainLayout)
                                                           

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Page2Win()
    win.show()
    sys.exit(app.exec_()) 
