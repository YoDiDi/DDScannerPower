import sys

from gevent import monkey
monkey.patch_all()  # monkey补丁会将在它之后导入的模块的IO操作打包，使gevent认识他们
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont
from PyQt5.QtWidgets import (QWidget, QApplication, QAction, QMenu, QVBoxLayout, QSystemTrayIcon,
                             QMessageBox, QDesktopWidget, QMainWindow, QPushButton, QHBoxLayout)

__author__ = 'didi'
print(__file__)




from py.mw.common.config import get_resource_path, get_tool_name, get_logo_path
from py.mw.service.modewidget1 import ModeWidget1
from py.mw.service.modewidget2 import ModeWidget2
from py.mw.service.modewidget3 import ModeWidget3
from py.mw.service.modewidget4 import ModeWidget4
from py.mw.service.modewidget5 import ModeWidget5
from py.mw.service.modewidget6 import ModeWidget6
from py.mw.service.modewidget7 import ModeWidget7
from py.mw.service.modewidget8 import ModeWidget8
from py.mw.service.modewidget9 import ModeWidget9

RESOURCEPATH = get_resource_path()
TOOLNAME = get_tool_name()
LOGOPATH = get_logo_path()


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tray = None
        self.trayMenu = None
        self.exp = None
        self.timer = None
        self.process = QtCore.QProcess()
        print(RESOURCEPATH)
        self.initUI()

        # 全局样式
        app.setStyleSheet('''
                    QPushButton#mode{
                        background-color: lightblue ;
                        height:30px;
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: beige;
                        font: bold 14px;
                        min-width: 8em;
                        padding: 6px;
                    }
                ''')

    def initUI(self):
        # 设置窗口属性
        self.resize(450, 300)
        # 窗体居中
        self.center()
        self.setFixedSize(self.width(), self.height())  # 设置窗口不可被拉伸
        self.setWindowTitle(TOOLNAME)
        self.setWindowIcon(QIcon(RESOURCEPATH + LOGOPATH))
        self.setWindowFlags(Qt.WindowCloseButtonHint)   # 设置右上角可执行操作

        menubar = self.menuBar()
        menu = menubar.addMenu('关于')
        express = QAction('说明', self)
        express.triggered.connect(self.showExp)
        menu.addAction(express)

        send_widget = QSendWidget()
        self.setCentralWidget(send_widget)

        self.statusBar().showMessage('欢迎使用'+TOOLNAME)

        # 定时器的定义
        self.timer = QBasicTimer()
        self.timer.start(1000, self)

        # 显示托盘
        self.showTray()
        # 显示窗体
        self.show()

    def center(self):
        """
        居中
        :return:
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showTray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(RESOURCEPATH+LOGOPATH))

        restore_action = QAction("显示", self, triggered=self.showNormal)
        minimize_action = QAction("最小化", self, triggered=self.hide)
        quit_action = QAction("退出", self, triggered=self.closeTrayEvent)

        self.trayMenu = QMenu(self)
        self.trayMenu.addAction(restore_action)
        self.trayMenu.addAction(minimize_action)
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(quit_action)
        self.tray.setContextMenu(self.trayMenu)
        self.tray.show()
        self.tray.activated[QSystemTrayIcon.ActivationReason].connect(self.iconActivated)
        self.show()

    def iconActivated(self, reason):
        """
        托盘双击事件
        :param reason:
        :return:
        """
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isHidden():
                self.show()
            else:
                self.hide()

    def closeTrayEvent(self, event):
        self.show()
        reply = QtWidgets.QMessageBox.question(self, TOOLNAME, "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.tray.hide()
            event.accept()
        else:
            event.ignore()

    def showExp(self):
        self.exp = Express("工具介绍")
        self.exp.show()

    def closeEvent(self, event):
        message = QtWidgets.QMessageBox()   # 关闭按钮的对话框
        message.setWindowTitle("关闭按钮")
        message.setWindowFlag(Qt.WindowStaysOnTopHint)
        message.setIcon(QMessageBox.Question)   # 图标
        message.setText("退出程序?")
        message.addButton("退出", QMessageBox.AcceptRole)
        msg_no = message.addButton("最小化", QMessageBox.NoRole)
        message.setWindowIcon(QIcon(RESOURCEPATH + LOGOPATH))
        message.setDefaultButton(msg_no)

        reply = message.exec_()
        if reply == 0:
            event.accept()
            self.tray.hide()
        elif reply == 1:
            event.ignore()
            self.hide()  # 隐藏窗体

    def enterEvent(self, event):
        self.statusBar().showMessage("请选择功能")

    def leaveEvent(self, event):
        self.statusBar().showMessage('欢迎使用' + TOOLNAME)


class QSendWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.modeWidget1 = None
        self.modeWidget2 = None
        self.modeWidget3 = None
        self.modeWidget4 = None
        self.modeWidget5 = None
        self.modeWidget6 = None
        self.modeWidget7 = None
        self.modeWidget8 = None
        self.modeWidget9 = None
        self.initUI()

    def initUI(self):
        Button1 = self.ModeButton("地址解析")
        Button1.clicked.connect(self.showMode1)
        Button2 = self.ModeButton("扫描目录")
        Button2.clicked.connect(self.showMode2)
        Button3 = self.ModeButton("识别cms")
        Button3.clicked.connect(self.showMode3)
        Button4 = self.ModeButton("爆破服务")
        Button4.clicked.connect(self.showMode4)
        Button5 = self.ModeButton("未授权服务")
        Button5.clicked.connect(self.showMode5)
        Button6 = self.ModeButton("弱口令服务")
        Button6.clicked.connect(self.showMode6)
        Button7 = self.ModeButton("漏洞利用")
        Button7.clicked.connect(self.showMode7)
        Button8 = self.ModeButton("漏洞检测")
        Button8.clicked.connect(self.showMode8)
        Button9 = self.ModeButton("子域名爆破")
        Button9.clicked.connect(self.showMode9)

        # 添加一个竖直盒子，两个水平盒子
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()

        # 把按钮放在盒子里
        hbox1.addWidget(Button1)
        hbox1.addWidget(Button2)
        hbox1.addWidget(Button3)
        hbox2.addWidget(Button4)
        hbox2.addWidget(Button5)
        hbox2.addWidget(Button6)
        hbox3.addWidget(Button7)
        hbox3.addWidget(Button8)
        hbox3.addWidget(Button9)

        # 把竖直盒子和水平盒子嵌套在水平盒子中
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)

    def ModeButton(self, msg):
        """
        定义功能按钮 方便样式设计
        :param msg:
        :return:
        """
        mode_button = QPushButton(msg)
        mode_button.setObjectName('mode')
        return mode_button

    def showMode1(self):
        self.modeWidget1 = ModeWidget1()
        self.modeWidget1.show()

    def showMode2(self):
        self.modeWidget2 = ModeWidget2()
        self.modeWidget2.show()

    def showMode3(self):
        self.modeWidget3 = ModeWidget3()
        self.modeWidget3.show()

    def showMode4(self):
        self.modeWidget4 = ModeWidget4()
        self.modeWidget4.show()

    def showMode5(self):
        self.modeWidget5 = ModeWidget5()
        self.modeWidget5.show()

    def showMode6(self):
        self.modeWidget6 = ModeWidget6()
        self.modeWidget6.show()

    def showMode7(self):
        self.modeWidget7 = ModeWidget7()
        self.modeWidget7.show()

    def showMode8(self):
        self.modeWidget8 = ModeWidget8()
        self.modeWidget8.show()

    def showMode9(self):
        self.modeWidget9 = ModeWidget9()
        self.modeWidget9.show()


class Express(QWidget):
    """
    Exp设计
    """
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.initUI()

    def initUI(self):
        self.resize(260, 200)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('说明')
        self.setWindowIcon(QIcon(RESOURCEPATH + LOGOPATH))

    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QColor(255, 192, 203))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
