import re
import threading
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout, QLineEdit,
                             QTextEdit, QComboBox, QFileDialog, QApplication)

__author__ = 'yodidi'

# 导入子域名爆破模块
from py.mw.common import subdomaindetection
from py.mw.common.config import get_resource_path, get_tool_name, get_logo_path

RESOURCEPATH = get_resource_path()
TOOLNAME = get_tool_name()
LOGOPATH = get_logo_path()


class ModeWidget9(QWidget):
    """
    功能弹出框
    """

    def __init__(self):
        super().__init__()
        self.resize(450, 400)
        self.center()
        self.setWindowTitle("子域名爆破")
        self.setWindowIcon(QIcon(RESOURCEPATH + LOGOPATH))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.edit2 = ""
        self.edit3 = ""
        self.button3 = None
        self.button41 = None
        self.cb = None
        # 设置文件选择打开路径
        self.path = "D:\\"
        self.username = None
        self.pwd = None
        self.initUI()

    def initUI(self):
        label1 = QLabel("选择功能：")
        self.cb = QComboBox(self, minimumWidth=350)
        self.cb.addItem("子域名爆破")
        self.cb.addItem("dns域传送漏洞检测")
        self.cb.setStyleSheet("height:30px;")
        label2 = QLabel("URL地址:")
        label2.setStyleSheet("min-width:72px;height:30px;")
        # 显示字典文件
        self.label3 = QLabel("暂未选择字典文件")
        self.label3.setStyleSheet("min-width:72px;height:50px;")

        self.edit2 = QLineEdit()
        self.edit2.setText('baidu.com')  # 设置域名
        self.edit2.setStyleSheet("height:30px;")

        self.button41 = QPushButton("字典文件")

        self.button41.clicked.connect(self.showFileDialogUser)
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
        hbox6 = QHBoxLayout()
        hbox7 = QHBoxLayout()

        # 把按钮放在盒子里
        hbox1.addWidget(label1)
        hbox1.addWidget(self.cb)
        hbox2.addWidget(label2)
        hbox2.addWidget(self.edit2)
        hbox6.addWidget(self.button41)
        hbox3.addWidget(self.button3)
        hbox4.addWidget(self.edit3)
        # 增加一个显示文件的label3
        hbox7.addWidget(self.label3)

        # 把竖直盒子和水平盒子嵌套在水平盒子中
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox6)
        # 增加一个显示文件的label3
        vbox.addLayout(hbox7)
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
        # 获取下拉框数据
        if self.cb.currentText() == 'dns域传送漏洞检测':
            print(self.cb.currentText())
            self.edit3.append("不存在dns域传送漏洞")
        if self.username is None:
            pass
        else:
            self.edit3.clear()
            self.button3.setText("执行中，请稍候")
            QApplication.processEvents()
            result = []
            thread_num = 5
            domain = self.edit2.text()
            domain_dicts = self.username
            # 设置参数
            domainscan = subdomaindetection.Domainscan(domain, domain_dicts)
            # 泛解析判断
            if (len(domainscan.maintestresolve(domain))) == 1:
                print("该域名为泛解析")
            else:
                # 启动5个线程执行main函数
                for i in range(thread_num):
                    t = threading.Thread(target=domainscan.main, args=(result,))
                    t.setDaemon(True)
                    t.start()
                while True:
                    if threading.activeCount() <= 1:
                        break
                    else:
                        time.sleep(0.1)
                # 取回线程执行结果
                for _ in result:
                    self.edit3.append(_)
                if len(result) == 0:
                    self.edit3.append("暂无数据")
                self.button3.setText("点击执行")

    def showFileDialogUser(self):
        fname = QFileDialog.getOpenFileName(self, '选择字典文件', self.path, "Text Files (*.txt)")
        if fname[0] != '':
            self.username = fname[0]
            print(self.username)
            self.label3.setText("加载字典:" + self.username)
