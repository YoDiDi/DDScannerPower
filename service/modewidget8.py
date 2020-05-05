from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout, QLineEdit,
                             QTextEdit, QComboBox)

__author__ = 'yodidi'

from py.mw.common.config import get_resource_path, get_tool_name, get_logo_path

RESOURCEPATH = get_resource_path()
TOOLNAME = get_tool_name()
LOGOPATH = get_logo_path()


class ModeWidget8(QWidget):
    """
    功能弹出框
    """
    def __init__(self):
        super().__init__()
        self.resize(450, 400)
        self.center()
        self.setWindowTitle("漏洞检测")
        self.setWindowIcon(QIcon(RESOURCEPATH + LOGOPATH))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.edit1 = ""
        self.edit3 = ""
        self.button3 = None
        self.initUI()

    def initUI(self):
        label1 = QLabel("选择漏洞类型：")
        self.cb = QComboBox(self, minimumWidth=350)
        self.cb.addItem("bash注入")
        self.cb.addItem("ecology远程命令执行")
        self.cb.addItem("phpstudy后门远程命令执行")
        self.cb.setStyleSheet("height:30px;")
        label2 = QLabel("URL地址:")
        label2.setStyleSheet("min-width:84px;height:30px;")
        self.edit2 = QLineEdit()
        self.edit2.setStyleSheet("height:30px;")
        self.button3 = QPushButton("点击执行")
        self.button3.setStyleSheet('''
                        background-color: lightblue;
                        height:30px;
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: beige;
                        font: bold 14px;
                        min-width: 8em;
                        padding: 6px;
                ''')
        self.button3.clicked.connect(self.func)
        self.edit3 = QTextEdit()

        # 添加一个竖直盒子，两个水平盒子
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()

        # 把按钮放在盒子里
        hbox1.addWidget(label1)
        hbox1.addWidget(self.cb)
        hbox2.addWidget(label2)
        hbox2.addWidget(self.edit2)
        hbox3.addWidget(self.button3)
        hbox4.addWidget(self.edit3)

        # 把竖直盒子和水平盒子嵌套在水平盒子中
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)

    def center(self):
        """
        居中
        :return:
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def func(self):
        pass