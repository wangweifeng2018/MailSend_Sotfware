#encoding=utf-8

import sys, os
import pandas as pd
import datetime as dt
from PyQt5 import QtWidgets
from MainDialog import mainDialog
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import pyqtSignal, QEventLoop
from logwin import LogDialog
from help import helpDialog
from PandasModel import PandasModel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate
import base64


email_content_normal = """\
<html>
        <head><meta charset=UTF-8></head>
    <body style="font-family:楷体;font-size:24px">
        <p>尊敬的**小姐/先生：</br>
            &nbsp;&nbsp;&nbsp;&nbsp;您好！</br>
            &nbsp;&nbsp;&nbsp;&nbsp;感谢您的关注~</br></br>
            祝您生活愉快，谢谢！
        </p>
    </body>
</html>
"""

email_content_9800 = """
<html>
    <head></head>
    <body style="font-family:楷体;font-size:24px">
        <p>尊敬**小姐/先生：</br>
        &nbsp;&nbsp;&nbsp;&nbsp;您好！</br>
         &nbsp;&nbsp;&nbsp;&nbsp;感谢您的关注</br>
        </p>
    </body>
    </body>
</html>
"""


def Mailconfig(send_from, send_to, subject, message, files=[]):
    print("send_from:", send_from)
    print("send_to:", send_to)
    msg = MIMEMultipart('related')
    msg['From'] = send_from
    msg['To'] = send_to
    #msg['Co'] = [weifeng19901990@163.com, wangweifeng@cheerlandgroup.com'
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    msgText = MIMEText(message, 'html')
    msgAlternative.attach(msgText)
    
    #the image is in the ./img/ directory
    fp = open('img/mailLogo.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    
    #define the image's ID as referenced as in the html file
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)
    
    for path in files:
            #file = path.split("\\")[-1]
            att = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
            file = path.split("\\")[-1]
            att["Content-Type"] = 'application/octet-stream'
            
            name_base64 = base64.b64encode(file.encode('utf-8'))
            name_format = "=?UTF-8?B?"+name_base64.decode() + "?="
            att.add_header('Content-Disposition', 'attachment', filename=name_format)
            msg.attach(att)
    return (msg)

def chkEmailAddr(usrName):
    try:
        usrName = str(usrName)
    except:
        return False
    if (usrName.find("@") == -1 or len(usrName) - usrName.find("@") < 6):
        return False
    else:
        return True


def ReadHistoryFile():
    if os.path.isfile("hist/email_history.xls"):
        hist_df = pd.read_table("hist/email_history.xls", encoding='gbk', sep='\t')
    else:
        hist_df = pd.DataFrame(columns=['序号', '检测项目', '客户编码', '客户姓名', '邮箱', 'pdf报告', '邮件发送', '发送日期'])
    return hist_df
    
def SaveHistoryFile(df):
    hist_df = ReadHistoryFile()
    df = hist_df.append(df)
    print ("*************", df)
    df.to_csv("hist/email_history.xls", encoding='gbk', index=False, sep="\t")
    
def showHelp():
    helpWin = helpDialog()
    helpWin.show()
    qe = QEventLoop()
    qe.exec_()
    return

class MainRun(mainDialog):    
    log_yesNo = pyqtSignal(int)
    def __init__(self, parent=None):
        super(MainRun, self).__init__(parent)
        self._step = 0
        self.server = None
        self.usrName = None
        self.send_yesNo = []
        
        #menu bar trigger
        self.actionLog.triggered.connect(self.getLog)
        self.actionChangeUser.triggered.connect(self.getLog)
        self.actionOut.triggered.connect(self.logout)
        self.actionHelp.triggered.connect(showHelp)

       #sendButton
        self.page1.sendButton.clicked.connect(self.page1Run)
        self.closeButton.clicked.connect(self.logout)

    def page1Run(self):
        if self.page1._Folder  == False :
            QtWidgets.QMessageBox.warning(
                self, '错误', '请选择pdf报告所在文件夹')
            print ("请选择pdf报告所在文件夹")
            
        elif  self.page1._Info == False:
            QtWidgets.QMessageBox.warning(
                self, '错误', '请先选择样品信息文件')
            print ("请先选择样品信息文件")
        elif self.page1._pdfChk == False:
            print (self.page1._Folder)
            QtWidgets.QMessageBox.warning(
                self, '错误', '请统计Pdf报告是存在')
            print ("请先检测pdf报告")
        elif self.server == None:
            QtWidgets.QMessageBox.warning(
                self, '错误', '邮箱未登录,请登陆邮箱')
            self.getLog()
        else:
            print ("已上传样品信息文件和检测结果文件,并登陆邮箱")
            print("可以发送邮件")  
            self.send(self.page1.sampleDF)    
        
    def startLog(self):
        self.server = None
        win = LogDialog()
        #self.statusBar.showMessage('正在登陆')
        win.usrName_signal.connect(self.getUser)
        win.log_yesNo.connect(self.logStat)
        win.exec_()
        self.server = win.server
        self.usrName = win.usrName
        print("server:", self.server)
        print("邮箱准备就绪，可以发送邮件！")
    
    def getLog(self):
        if not self.server :
            self.startLog()
        else:
            reply= QMessageBox.information(self, '提示', '已有账号登陆，是否要更换登陆账号', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,QMessageBox.No )
            if reply == QMessageBox.Yes:
                self.server.close()
                self.statusBar.showMessage("邮箱已断开")
                self.startLog()
            elif reply == QMessageBox.No:#放弃更换账号
                pass
            else:
                pass#取消更换账号

    def logStat(self, n):
        if n != "No":
            self.statusBar.showMessage("已登陆账号 :\t"+self.user)
        else:
            self.statusBar.showMessage('登陆失败')
          
    def logout(self):
        if self.server:
            self.server.close()
            self.server = None
            self.user = None
            self.usrName = None
            self.statusBar.showMessage("邮箱未登录")
        else:
            QtWidgets.QMessageBox.warning(
                        self, '错误',"未有邮箱登陆")
            
            
    def getUser(self, user):
         self.user = user
         print(self.user)
    
    def send(self, df):
            me = self.usrName
            email_num = df.shape[0]
            self.page1.progressBar.setMinimum(0)
            self.page1.progressBar.setMaximum(email_num)
            #me = u'wangweifeng@cheerlandgroup.com'
            email_count = 0
            self.statusBar.showMessage('准备发送邮件')
            
            for Index, Row in df.iterrows():
                print(email_count)
                #msg = EmailMessage()
                #msg = MIMEMultipart()
                if not chkEmailAddr(Row['邮箱']):
                    QtWidgets.QMessageBox.warning(
                        self, '错误', str(Row["客户编码"])+"无邮箱信息")
                    self.send_yesNo.append("No")
                    continue
                if not Row['pdf报告']:
                    self.send_yesNo.append("No")
                    QtWidgets.QMessageBox.warning(
                        self, '错误', str(Row["客户编码"])+"无pdf报告")
                    continue
                
                if '常规项目' in str(Row["检测项目"]) :
                    message = email_content_normal
                elif str(9800) in str(Row["检测项目"]):
                    message = email_content_9800.replace('sample_id', Row['客户编码'])
                else:
                    QtWidgets.QMessageBox.warning(
                        self, '错误', str(Row["客户编码"])+"未知检测检测项目")
                    print(str(Row["客户编码"])+"未知检测检测项目")
                    self.send_yesNo.append("No")
                    continue
                    
                customer = Row["邮箱"]
                subject = u'您好，您的基因检测报告已出，请注意查收。'
                msg = Mailconfig(me,customer, subject, message, Row['pdf报告'])
                try:
                    self.server.send_message(msg)
                    self.send_yesNo.append("Yes")
                except Exception as e:
                    print("################")
                    print ("err:", e)
                    print("################")
                    QtWidgets.QMessageBox.warning(
                        self, '错误', str(Row["客户编码"])+"邮件发送失败！")
                    self.send_yesNo.append("No")
                    continue
                email_count += 1
                self.page1.progressBar.setValue(email_count)
            self.statusBar.showMessage('邮件发送结束')
            df['邮件发送'] = self.send_yesNo
            df["发送日期"] = [dt.datetime.now()]*len(self.send_yesNo)
            try:
                SaveHistoryFile(df)
            except Exception as e:
                print("Here1", e)
            try:
                model = PandasModel(df)
            except Exception as e:
                print("Here2", e)
            print("sample", df)
            self.page1.samplePdTv.setModel(model)
            err_df = df[df['邮件发送'] == "No"]
            print("err", err_df)
            if err_df.size != 0:
                try:
                    err_df = err_df.reset_index(drop=True)
                    err_model = PandasModel(err_df)
                    self.page1.infoTv.setModel(err_model)
                except Exception as e:
                    print("e", e)
            print (self.send_yesNo)
            print("邮件发送结束！")
            

if __name__ == "__main__":

    app = QApplication(sys.argv)
    dialog = MainRun()
    dialog.show()
    sys.exit(app.exec_())
    
