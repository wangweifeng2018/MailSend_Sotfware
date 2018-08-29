#!/usr/bin/env python
#encoding=utf-8
import pandas as pd
import sys

from PyQt5.QtWidgets import (QApplication,  QFormLayout, QTableView,QLineEdit, QLabel, QAbstractItemView, 
QPushButton,  QVBoxLayout,QHBoxLayout, QWidget, QTextEdit, QGroupBox, QProgressBar)

        
class TextEdit(QTextEdit):
    #重定义QTextEdit类
    def __init__(self,  parent=None):
        super(TextEdit, self).__init__(parent) 
        self.setAcceptDrops(True)
            
    def dropEvent(self,  event): 
        fname = event.mimeData().text()
        filename = fname.split("///")[1]
        if filename.endswith(".csv"):

            try:
                df = pd.read_csv(filename, header = None, encoding="utf-8")
            except:
                df = pd.read_csv(filename, header = None, encoding="gbk")
            self.setPlainText(df.to_string())
            self.dataframe = df
            print("##############Page1.dataframe:", self.dataframe)
            #print(df)
        else:
            self.setPlainText("无法识别文件类型")
 

class Page1Win(QWidget):
    def __init__(self, parent=None):
        super(Page1Win, self).__init__(parent)
        self.createBox1()
        self.createBox2()
        
        # Main Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.box1Group)
        mainLayout.addWidget(self.box2Group)
        self.setLayout(mainLayout)
        self.setWindowTitle("Page1-wf")
    
    def createBox1(self):
        #BOX1
        self.box1Group = QGroupBox("样品信息")
        #col1
        self.fileButton1 = QPushButton("选择文件夹")
        self.fileButton1.setStyleSheet("background-color:rgb(020,150,150);"
                                                 "font:bold 10pt Comic Sans MS")
        self.fileButton1.setToolTip("打开所有检测样品PDF报告所在的文件夹")
        self.fileButton2 = QPushButton("打开文件")
        self.fileButton2.setStyleSheet("background-color:rgb(020,150,150);"
                                                 "font:bold 10pt Comic Sans MS")
        self.fileButton2.setToolTip("点击此处选择包含客户信息的文件，文件格式需要为CSV")
        self.fileButton3 = QPushButton("统计pdf文件")
        self.fileButton3.setStyleSheet("background-color:rgb(020,150,150);"
                                                 "font:bold 10pt Comic Sans MS")
        self.fileButton3.setToolTip("点击此处检测统计客户信息及pdf报告文件")
        col1layout= QVBoxLayout()
        col1layout.addWidget(self.fileButton1)
        col1layout.addWidget(self.fileButton2)
        col1layout.addStretch(1)
        col1layout.addWidget(self.fileButton3)
        col1layout.addStretch(8) 
        #col2
        self.pdfText = QLineEdit()
        self.pdfText.selectAll()
        self.pdfText.setFocus()
        self.samplePdTv =  QTableView(self)
        col2layout = QVBoxLayout()
        col2layout.addWidget(self.pdfText)
        col2layout.addWidget(self.samplePdTv)
        
        box1Layout = QHBoxLayout()
        box1Layout.addLayout(col1layout)
        box1Layout.addLayout(col2layout)
        self.box1Group.setLayout(box1Layout)
    
    def createBox2(self):
        
        self.sendButton = QPushButton("发送")
        self.sendButton.setStyleSheet("background-color:rgb(020,150,150);"
                                                 "font:bold 10pt Comic Sans MS") 
        self.sendButton.setToolTip("批量发送邮件")
        self.progressBar = QProgressBar()
        self.progressBar.setFormat("%v")
        self.infoTv = QTableView(self)
        
        self.box2Group = QGroupBox("报告结果统计")
        self.box2Layout = QFormLayout()
        self.box2Layout.addRow(self.sendButton, self.progressBar)
        self.box2Layout.addRow(QLabel('发送失败邮件'), self.infoTv)
        self.box2Group.setLayout(self.box2Layout)

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Page1Win()
    win.show()
    sys.exit(app.exec_()) 
