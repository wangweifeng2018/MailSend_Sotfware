#!/usr/bin/env python
 
import sys
from PyQt5.QtCore import QDate

from PyQt5.QtWidgets import (QApplication, QCheckBox,  QDateTimeEdit,
         QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,QHeaderView, 
        QVBoxLayout, QWidget, QTableWidget, QAbstractItemView)
        

class Page3Win(QWidget):
    def __init__(self, parent=None):
        super(Page3Win, self).__init__(parent)
        self.conditionBox()
        self.resultTable()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.setConditGroup)
        mainLayout.addWidget(self.table)
        mainLayout.addSpacing(12)
        mainLayout.addStretch(1)
 
        self.setLayout(mainLayout)
        
    def conditionBox(self):
        
        self.typeChkBoxGroup()
        
        ##查找条件设定Box
        self.setConditGroup = QGroupBox("查找条件")
        grid = QGridLayout()
        
        #COL1
        nameLabel = QLabel("样品姓名:")
        idLabel = QLabel("样品ID")
        companyLabel = QLabel("来源公司")
        typeLabel = QLabel("产品类型")
        time1Label = QLabel("起始时间")
        time2Label = QLabel("结束时间")
        
        #COL2
        nameEdit = QLineEdit()
        idEdit = QLineEdit()
        companyEdit = QLineEdit()
        
        self.dateEdit1 = QDateTimeEdit(QDate.currentDate())
        self.dateEdit1.setCalendarPopup(True)

        self.dateEdit2 = QDateTimeEdit(QDate.currentDate())
        self.dateEdit2.setCalendarPopup(True)
        self.dateEdit2.setMaximumDate(QDate.currentDate().addDays(200))

        
        #COL3
        nameNote = QLabel("支持输入多姓名查找，姓名之间使用','或'/'间隔")
        idNote = QLabel("支持输入多id查找，id之间使用','或'/'间隔")
        companyNote = QLabel("请输入样品来源公司的中文名称，支持模糊匹配")
        
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(idLabel, 1, 0)
        grid.addWidget(companyLabel, 2, 0)
        grid.addWidget(typeLabel, 3, 0)
        grid.addWidget(time1Label, 4, 0)
        grid.addWidget(time2Label, 5, 0)
        grid.addWidget(nameEdit, 0, 1)
        grid.addWidget(idEdit, 1, 1)
        grid.addWidget(companyEdit, 2, 1)
        grid.addWidget(self.typeGroupBox, 3, 1)
        grid.addWidget(self.dateEdit1, 4, 1)
        grid.addWidget(self.dateEdit2, 5, 1)
        grid.addWidget(nameNote, 0, 2)
        grid.addWidget(idNote, 1, 2)
        grid.addWidget(companyNote, 2, 2)
         
        self.setConditGroup.setLayout(grid)
    
    
    
    def resultTable(self):
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setRowCount(2)
        self.table.setVerticalHeaderLabels(["报告数", "样品ID"])
        self.table.setHorizontalHeaderLabels(["常规项目","9800" ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.table.setSelectionBehavior(QAbstractItemView.SelectColumns)
        
    def typeChkBoxGroup(self):
        ##用于产品类型的ChkBox
        self.typeGroupBox = QGroupBox()
        self.typeGroupBox.setMaximumSize(500, 40)
        layout = QHBoxLayout()
        
        CheckBox_cg = QCheckBox("常规项目")
        CheckBox_9800 = QCheckBox("9800项目")

        layout.addWidget(CheckBox_cg)
        layout.addWidget(CheckBox_9800)
        
        self.typeGroupBox.setLayout(layout)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Page3Win()
    win.show()
    sys.exit(app.exec_()) 
