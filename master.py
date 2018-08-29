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
        <p>尊敬的客户：</br>
            &nbsp;&nbsp;&nbsp;&nbsp;您好！</br>
            &nbsp;&nbsp;&nbsp;&nbsp;感谢您选择乐土基因，附件为您的电子版报告，请及时下载查阅~</br>
            如有疑问欢迎致电客服热线：400-6698-988，我们将为您提供进一步的咨询服务。</br>
            温馨提示：报告是PDF格式文件，建议您先下载PDF阅读软件再进行阅读。</br>
            '一次相遇，终生相伴'，再次感谢您选择乐土基因！</br>
            祝您生活愉快，谢谢！
        </p>
        <hr style="align:center;opacity:0.7;height:5px;border:white;border-top:1px solid black;"/>
        <img src="cid:image1"/>
        </br></br>
        <p style="font-weight:600"  width="128" height="80" >乐土精准医疗科技有限公司（客服中心）</p>
        <span style="font-size:20;font-weight:600">Tel：</span><span style="font-size:20">400-6698-988</span>
        </br>
		<p style="font-size:20;font-weight:600"  width="128" height="80" >深圳总部：</p>
        <span style="font-size:20;font-weight:600">Email：</span><span style="font-size:20">cl-healthcare@cheerlandgroup.com</span></br>
        <span style="font-size:20;font-weight:600">Add：</span><span style="font-size:20">深圳市南山区桃源街道南方科技大学创园8栋</span>
		<p style="font-size:20;font-weight:600"  width="128" height="80" >北京公司：</p>
		<span style="font-size:20;font-weight:600">Email：</span><span style="font-size:20">CL-BJKF@cheerlandgroup.com</span></br>
		<span style="font-size:20;font-weight:600">Add：</span><span style="font-size:20">北京市昌平区回龙观镇中关村生命科学园生命路8号院一区15号楼</span>	
    </body>
</html>
"""

email_content_9800 = """
<html>
    <head></head>
    <body style="font-family:楷体;font-size:24px">
        <p>尊敬的客户：</br>
        &nbsp;&nbsp;&nbsp;&nbsp;您好！</br>
         &nbsp;&nbsp;&nbsp;&nbsp;感谢您选择乐土基因，附件为您的电子版报告，有效期为30天，请您及时下载查阅~</br>
        电子版报告查询方式有两种：</br>
        &nbsp;&nbsp;（一）您可以直接下载附件查看；</br>
        温馨提示：报告是PDF格式文件，建议您先下载PDF阅读软件再进行阅读。</br>
        &nbsp;&nbsp;（二）您可以通过在线形式查看，在线查看操作流程如下：</br>
        &nbsp;&nbsp;&nbsp;&nbsp;1. 首先打开查询地址:http://sys.clgene.com/login </br>
        &nbsp;&nbsp;&nbsp;&nbsp;2. 在网页界面通过样本编号进行注册，填写个人注册信息，为了双重保障您的个人信息，</br>
        获取手机验证码，注册成功后即可登陆个人报告查询界面。</br>
        您的样本编号为：<span>sample_id</span></br>
        "温馨提示：如有疑问欢迎致电客服热线：400-6698-988，我们将为您提供进一步的咨询服务。</br>
        （报告解读预约热线：010-80766700，我们的解读人员将为您提供专业的解读服务）</br>
        </p>
        <hr style="align:center;opacity:0.7;height:5px;border:white;border-top:1px solid black;"/>
        <img src="cid:image1" />
        </br></br>
        <p style="font-weight:600">乐土精准医疗科技有限公司（客服中心）</p>
        <span style="font-size:20;font-weight:600">Tel：</span><span style="font-size:20">400-6698-988</span>
        </br>
		<p style="font-size:20;font-weight:600">深圳总部：</p>
        <span style="font-size:20;font-weight:600">Email：</span><span style="font-size:20">cl-healthcare@cheerlandgroup.com</span></br>
        <span style="font-size:20;font-weight:600">Add：</span><span style="font-size:20">深圳市南山区桃源街道南方科技大学创园8栋</span>
        </br>
        <p style="font-size:20;font-weight:600">北京公司：</p>
        <span style="font-size:20;font-weight:600">Email：</span><span style="font-size:20">CL-BJKF@cheerlandgroup.com</span></br>
        <span style="font-size:20;font-weight:600">Add：</span><span style="font-size:20">北京市昌平区回龙观镇中关村生命科学园生命路8号院一区15号楼</span>
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
    
