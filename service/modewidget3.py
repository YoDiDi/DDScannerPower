import json
import re
import time
import threading

import requests
from bs4 import BeautifulSoup
from lxml import etree

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout, QLineEdit,
                             QTextEdit, QApplication)

__author__ = 'Kgg&yodidi'

from py.mw.common import gwhatweb
from py.mw.common.config import get_resource_path, get_tool_name, get_logo_path
from py.mw.common.urlcheck import url_check
from py.mw.common.dolog import log

RESOURCEPATH = get_resource_path()
TOOLNAME = get_tool_name()
LOGOPATH = get_logo_path()


class ModeWidget3(QWidget):
    """
    功能弹出框
    """
    def __init__(self):
        super().__init__()
        self.resize(750, 400)
        self.center()
        self.setWindowTitle("识别cms")
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
        self.edit1.setText("http://192.168.111.130/index.php")
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
        bug =''
        try:
            self.edit3.clear()
            self.button3.setText("执行中，请稍候")
            QApplication.processEvents()
            result = []
            json_path = RESOURCEPATH + "dict/" + "gwhatwebdata.json"

            url = self.edit1.text()

            if url_check(url):
                g = gwhatweb.gwhatweb(url, json_path)
                g.whatweb(result, 1000)
                for _ in result:
                    self.edit3.append(_)
                if len(result) == 0:
                    self.edit3.append("暂无数据")
                    result = '暂无数据'
            else:
                self.edit3.append("输入有误")
            self.button3.setText("执行")
        except BaseException as e:
            self.edit3.append(str(e))
            bug = str(e)
        log('CMS识别', url, json_path,result,bug)

