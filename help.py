#coding=utf8 
#!/usr/bin/python

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
import smtplib


instr = """
        ------请按照以下依次操作--------
        
        
        1. --邮箱登陆--
            账户 -> 登陆 -> 邮箱地址 -> 密码  -> 登陆
            邮箱登陆须在发送报告之前执行，
            登陆成功后，页面左下角会显示登陆的邮箱账户。
   
         
        2. --选择pdf报告所在文件夹--
            选择文件夹 -> 确定

        
        3. --打开用户信息文件--
            操作顺序： 打开文件 -> 确定
            此步骤为打开包含客户信息的excel表格，文件格式固定。
            每列顺序由左至右依次为：
            序号 -> 项目类型 -> 样品编号 -> 客户姓名 -> 邮箱地址
            注意， 以上顺序不可调换。
    
         
        4. --检测pdf 文件文件存在与否（不可省略）--
             点击 “统计pdf 文件” 按钮，此步骤目的在于统计每份样品的pdf情况。
             如样品在指定目录下有pdf检测报告，则该样品对应的所有pdf 报告显示在统计列，
             如无pdf 报告，则统计情况为 "[] "，该客户邮件不发送。
     
             
        5. --发送邮件--
            点击 “发送” 按钮，等待邮件逐一发送。
            发送成功的邮件在页面相应信息框中的相应样品行显示为Yes,
            反之，发送失败的显示为No。
            伴随邮件发送，进度条会显示发送邮件份数。发送失败的邮件会显示在右下方的显示栏中。
            
        
"""


class helpDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=None):
        super(helpDialog, self).__init__(parent)
        self.server = None 
        self.usrName = None
         
        ## 窗口风格设置
        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(1, 178, 170))
        #palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('./img/CLlogo.png')))
        self.setPalette(palette1)
        self.setAutoFillBackground(False)
        self.setGeometry(200, 200, 600, 600)
        self.setWindowIcon(QIcon('img/CLlogo.png')) 
        self.setWindowTitle("邮件定制发送使用说明") 
        
        
        text = QtWidgets.QTextEdit()
        text.setText(instr)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)
        self.setModal(False)

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = helpDialog()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = Window()
