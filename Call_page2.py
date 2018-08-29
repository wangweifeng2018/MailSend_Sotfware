#!/usr/bin/env python
#encoding=utf-8
 
import sys
from PyQt5.QtGui import  QColor, QBrush, QFont
from PyQt5.QtWidgets import (QApplication, QComboBox, QTableWidgetItem)
from Page2 import Page2Win



class CallPage2(Page2Win):
     def __init__(self):
        super(CallPage2, self).__init__() 
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CallPage2()
    win.show()
    sys.exit(app.exec_()) 
