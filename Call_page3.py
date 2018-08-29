#!/usr/bin/env python
#encoding=utf-8
 
import sys
import pandas as pd
from PyQt5.QtCore import QDate

from PyQt5.QtWidgets import (QApplication)
from Page3 import Page3Win       



class CallPage3(Page3Win):
     def __init__(self):
        super(CallPage3, self).__init__() 
        self.dateChange()
        
     def dateChange(self):
        self.dateEdit1.dateTimeChanged.connect(self.getDate) 
        self.dateEdit2.dateTimeChanged.connect(self.getDate)
        
     def getDate(self):
         dateStart = self.dateEdit1.dateTime()
         dateEnd = self.dateEdit2.dateTime()
         print("页面三起始时间："+dateStart.toString("yyyy-MM-dd"), "终止时间："+dateEnd.toString("yyyy-MM-dd"))
         
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CallPage3()
    win.show()
    sys.exit(app.exec_()) 
