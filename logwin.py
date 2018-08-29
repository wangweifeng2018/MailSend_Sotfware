#coding=utf8 
#!/usr/bin/python

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
import smtplib

class LogDialog(QtWidgets.QDialog):
    
    #定义登陆信息信号
    log_info_signal = pyqtSignal()
    usrName_signal = pyqtSignal(str)
    log_yesNo = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(LogDialog, self).__init__(parent)
        self.server = None 
        self.usrName = None
         
        ## 窗口风格设置
        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(1, 178, 170))
        #palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('./img/CLlogo.png')))
        self.setPalette(palette1)
        self.setAutoFillBackground(False)
        self.setGeometry(400, 350, 300, 130)
        self.setWindowIcon(QIcon('img/CLlogo.png')) 
        self.setWindowTitle("邮件登陆窗口") 
        
        self.log_info_signal.connect(self.logging) 
        self.log_yesNo.connect(self.Close)
        
        self.labelName = QtWidgets.QLabel('邮箱地址')
        self.textName = QtWidgets.QLineEdit(self)
        
        #密码行
        self.labelPass = QtWidgets.QLabel('密码')
        self.textPass = QtWidgets.QLineEdit(self)
        #self.textPass.installEventFileter(self)

        self.textPass.setContextMenuPolicy(Qt.NoContextMenu)#取消密码条右键 菜单
        self.textPass.setPlaceholderText("请输入邮箱密码")
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)#圆点掩盖字符
        
        #button  
        self.buttonLogin = QtWidgets.QPushButton('登陆', self)
        self.cancelButton = QtWidgets.QPushButton('取消', self)
        self.buttonLogin.clicked.connect(self.chkInfo)
        self.cancelButton.clicked.connect(self.close)
        
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.buttonLogin)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.cancelButton)
        
        
        mainlayout = QtWidgets.QVBoxLayout(self)
        layout = QtWidgets.QFormLayout()
        layout.addRow(self.labelName, self.textName)
        layout.addRow(self.labelPass, self.textPass)
        mainlayout.addLayout(layout)
        mainlayout.addLayout(buttonLayout)

    def chkInfo(self):
        usrName = self.textName.text()
        psWord = self.textPass.text()
        try:
            usrName = str(usrName)
        except:
            QtWidgets.QMessageBox.warning(
                self, '错误', '邮箱地址是纯数字，格式错误')
        if (usrName.find("@") == -1 or len(usrName) - usrName.find("@") < 6 ):
            QtWidgets.QMessageBox.warning(self, '错误', '邮箱地址信息格式错误')
        elif  len(psWord) < 1:
            QtWidgets.QMessageBox.warning(
                self, '错误', '请填写密码！')
        else:
            self.usrName = usrName
            self.psWord = psWord
            print("邮箱地址和密码格式正确，发送登陆信号！")
            self.usrName_signal.emit(usrName)
            self.log_info_signal.emit()
            print("邮箱地址：", usrName, type(usrName))
            print("密码：", psWord, type(psWord))
    
    def logging(self):
        
        self.server = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
        self.server.set_debuglevel(1)
        try:
            self.server.login(self.usrName, self.psWord)
            self.log_yesNo.emit(self.usrName)
            print("登陆成功！"+self.usrName)
        except:
            self.log_yesNo.emit("No")
            print("登陆失败！")    
    
    def Close(self, n):
        if n != "No":
            print("登陆成功，关闭信息对话框！")
            self.close()
        else:
            QtWidgets.QMessageBox.warning(
            self, '错误', '登陆失败，请重新输入用户名密码')
            print("登陆失败！对话框不关闭！")

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = LogDialog()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = Window()
