#!/usr/bin/env python
 
import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import (QApplication, QHBoxLayout,QWidget,   QMenuBar, 
        QListView, QListWidget, QListWidgetItem, QPushButton, 
        QStackedWidget, QVBoxLayout,   QStatusBar)
from Call_page1 import CallPage1
#from Call_page2 import CallPage2
from Call_page3 import CallPage3

 
class mainDialog(QWidget):
    def __init__(self, parent=None):
        super(mainDialog, self).__init__(parent)
        
        #编辑菜单栏
        self.menubar =  QMenuBar()
        self.menubar.setStyleSheet("""QMenuBar{
                                                              background-color:rgb(000,178,180);
                                                              border:1px solid#188;
                                                              }
                                                """)
        #账户菜单
        self.usrMenu = self.menubar.addMenu('账户')
        self.actionLog = self.usrMenu.addAction( '登陆&L')
        self.actionChangeUser = self.usrMenu.addAction('更换账号&A')
        self.actionOut = self.usrMenu.addAction ('退出登陆&O')
        #编辑菜单
        self.revMenu = self.menubar.addMenu('编辑')
        self.helpMenu = self.menubar.addMenu('帮助')
        self.actionHelp = self.helpMenu.addAction('显示使用文档')
        self.actionAbout = self.helpMenu.addAction('？')
        self.menuLayout = QHBoxLayout()
        self.menuLayout.addWidget(self.menubar)
        self.menuLayout.addStretch(1)
        
        #状态栏 
        self.statusBar = QStatusBar()
        self.statusBar.showMessage(u'未登录') 
         
        #导航栏 
        self.contentsWidget = QListWidget()
        self.setStyleSheet("""QListWidget{
                                                     background-color:rgb(000,178,180);
                                                     border:0px;
                                                     }
                                    QListWidget::item:hover{
                                                     background:skyblue;padding-top:0px;padding-bottom:0px;
                                                     }
                                    QListWidget::item:selected{
                                                    background:lightgray;color:bule;
                                                    }
                                                     background-color:rgb(000,178,180);
                                                     }
                                                     """)
        self.contentsWidget.setViewMode(QListView.IconMode)
        self.contentsWidget.setIconSize(QSize(50, 50))
        self.contentsWidget.setMovement(QListView.Static)
        self.contentsWidget.setMaximumSize(60, 140)
        #self.contentsWidget.setMaxmumHeight(120)
        self.contentsWidget.setSpacing(0)
          
        #设置三个页面为StackedWidget
        self.page1 = CallPage1()
        self.page3 = CallPage3()
        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget(self.page1)
        self.pagesWidget.addWidget(self.page3)
        
        #设置导航栏默认选择邮件发送页面
        self.createNav()
        self.contentsWidget.setCurrentRow(0)
        
        #水平布局(包含导航栏和一个页面)
        horizontalLayout = QHBoxLayout()
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.contentsWidget)
        vlayout.addStretch(12)
        horizontalLayout.addLayout(vlayout)
        horizontalLayout.addWidget(self.pagesWidget)
        
        #最底层状态栏和关闭按钮
        self.closeButton = QPushButton("关闭程序")
        self.closeButton.clicked.connect(self.close)
        bottomLayout = QHBoxLayout()
        #bottomLayout.addStretch(1)
        bottomLayout.addWidget(self.statusBar)
        #bottomLayout.addStretch(10)
        bottomLayout.addWidget(self.closeButton)
        #bottomLayout.addStretch(1)
        
        #设置页面总体布局
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.menuLayout)
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(bottomLayout)
        self.setLayout(mainLayout)
 
        ## 窗口风格设置
        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(1, 178, 170))
        #palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('./img/CLlogo.png')))
        self.setPalette(palette1)
        self.setAutoFillBackground(False)
        self.setGeometry(300, 300, 300, 500)
        self.setWindowIcon(QIcon('img/title.png')) 
        self.setWindowTitle("Python实现图像界面-PyQt5")
    
    def changePage(self, current, previous) :
        if not current:
            current = previous
        self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))
 
    def createNav(self):
        page1Button = QListWidgetItem(self.contentsWidget)
        page1Button.setIcon(QIcon('img/send.png'))
        page1Button.setText("发送邮件")
        page1Button.setTextAlignment(Qt.AlignHCenter)
        page1Button.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
 
        page2Button = QListWidgetItem(self.contentsWidget)
        page2Button.setIcon(QIcon('img/find.png'))
        page2Button.setText("查看历史")
        page2Button.setTextAlignment(Qt.AlignHCenter)
        page2Button.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
 
        self.contentsWidget.currentItemChanged.connect(self.changePage)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = mainDialog()
    dialog.show()
    sys.exit(app.exec_()) 
