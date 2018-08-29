#!/usr/bin/env python
#encoding=utf-8 
import sys
import glob
import pandas as pd
from PandasModel import PandasModel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication,QFileDialog)
from Page1 import Page1Win


class CallPage1(Page1Win):
    def __init__(self):
        super(CallPage1, self).__init__()
        
        #初始化文件上传状态为False
        self._Folder = False
        self._Info = False
        self._pdfChk = False
        self.pdfFolder = ""
        self.sampleDF = pd.DataFrame()

        #样品上传状态
        self.fileButton1.clicked.connect(self.getFolderName)
        self.fileButton2.clicked.connect(self.openInfoFile)
        
        #统计Pdf文件
        self.fileButton3.clicked.connect(self.checkPdf)
         
    def openInfoFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, '样品信息文件', 'c:\\')
        if fname:
            self._Info = True
            print("#####Tip: 样品信息文件\n"+fname)
            if fname.endswith('.csv'):
                df = pd.read_csv(fname, header=None, skiprows=1, encoding='utf-8', names=['序号', '检测项目', '客户编码', '客户姓名', '邮箱'])
            elif fname.endswith('.xls') or  fname.endswith('.xlsx') :
                df = pd.read_excel(fname, header=None, skiprows=1, encoding='utf-8', names=['序号', '检测项目', '客户编码', '客户姓名', '邮箱'])
            else:
                sys.exit(1)
            model = PandasModel(df)
            self.samplePdTv.setModel(model)
            self.sampleDF = df
            return 
            
    def getFolderName(self):
        folderName= str(QFileDialog.getExistingDirectory(self, "选择文件夹"))
        if folderName:
            self._Folder = True
            print("Tip: PDF报告文件夹：\n"+folderName)
            self.pdfText.setText(folderName)
            self.pdfFolder = folderName
        return (folderName)
    
    def checkPdf(self):
        filepath = self.pdfFolder
        if not filepath:
            QtWidgets.QMessageBox.warning(
                self, '错误', '请选择pdf报告所在文件夹')
            print("请先选择包含PDF报告的文件夹！")
        if not self._Folder:
            QtWidgets.QMessageBox.warning(
                self, '错误', '请选择pdf报告所在文件夹')
            print("请先选择包含PDF报告的文件夹！")
        if not self._Info:
            QtWidgets.QMessageBox.warning(
            self, '错误', '请上传样品信息文件')
            print("请先上传样品信息文件！")
        else:
            self.sampleDF['报告位置'] = self.sampleDF['客户编码'].apply(lambda x: filepath+"/"+str(x)+".pdf")
            self.sampleDF['pdf报告'] = self.sampleDF['客户编码'].apply(lambda x: glob.glob(filepath+"/*"+str(x)+"*.pdf"))
            self.sampleDF = self.sampleDF.drop(['报告位置'], axis=1)
            self.samplePdTv.setModel(PandasModel(self.sampleDF))
            self._pdfChk = True
        return 
         
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CallPage1()
    win.show()
    sys.exit(app.exec_()) 
