import re
import threading
import time


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout, QLineEdit,
                             QTextEdit, QApplication)

__author__ = 'yodidi'

from py.mw.common import webdirscan
from py.mw.common.config import get_resource_path, get_tool_name, get_logo_path
from py.mw.common.urlcheck import url_check

RESOURCEPATH = get_resource_path()
LOGOPATH = get_logo_path()


class ModeWidget2(QWidget):
    """
    功能弹出框
    """
    def __init__(self):
        super().__init__()
        self.resize(450, 400)
        self.center()
        self.setWindowTitle("扫描目录")
        self.setWindowIcon(QIcon(RESOURCEPATH + LOGOPATH))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.edit1 = ""
        self.edit3 = ""
        self.button3 = None
        self.initUI()

    def initUI(self):
        label1 = QLabel("输入URL:")
        self.edit1 = QLineEdit()
        self.edit1.setStyleSheet("height:30px;")
        self.edit1.setText('www.baidu.com')  # 设置字符串
        label2 = QLabel()
        label2.setStyleSheet("height:30px;")
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
        hbox1.addWidget(self.edit1)
        hbox2.addWidget(label2)
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
        self.edit3.clear()
        self.button3.setText("执行中，请稍候")
        QApplication.processEvents()
        result = []
        thread_num = 5
        url = self.edit1.text()
        if url_check(url):
            url = re.sub('http://|https://', '', url)
            #print(RESOURCEPATH + "dict/" + "webdirscandict.txt")
            scan = webdirscan.Dirscan(url, RESOURCEPATH + "dict/" + "webdirscandict.txt", thread_num)
            for i in range(thread_num):
                t = threading.Thread(target=scan.run, args=(result,))
                t.setDaemon(True)
                t.start()
            while True:
                if threading.activeCount() <= 1:
                    break
                else:
                    time.sleep(0.1)
            for _ in result:
                self.edit3.append(_)
            if len(result) == 0:
                self.edit3.append("暂无数据")
        else:
            self.edit3.append("输入有误")
        self.button3.setText("执行")

