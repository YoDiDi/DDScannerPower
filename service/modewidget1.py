import json
import re
import time

import requests
from bs4 import BeautifulSoup
from lxml import etree

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout, QLineEdit,
                             QTextEdit, QApplication)

__author__ = 'yodidi'

from py.mw.common.config import get_resource_path, get_tool_name, get_logo_path
from py.mw.common.ipcheck import verify_ip
from py.mw.common.urlcheck import url_check

RESOURCEPATH = get_resource_path()
TOOLNAME = get_tool_name()
LOGOPATH = get_logo_path()


class ModeWidget1(QWidget):
    """
    功能弹出框
    """
    def __init__(self):
        super().__init__()
        self.resize(450, 400)
        self.center()
        self.setWindowTitle("地址解析")
        self.setWindowIcon(QIcon(RESOURCEPATH + LOGOPATH))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.edit1 = ""
        self.edit3 = ""
        self.button3 = None
        self.initUI()

    def initUI(self):
        label1 = QLabel("输入URL或IP:")

        # QLineEdit 类  https://www.cnblogs.com/yinsedeyinse/p/10761861.html
        self.edit1 = QLineEdit()
        self.edit1.setPlaceholderText('输入URL或IP')  # 设置占位文本
        self.edit1.placeholderText()  # 获取占位文本

        self.edit1.setText('qq.com') #设置字符串
        #self.edit1.text() #获取字符串

        self.edit1.setStyleSheet("height:30px;")
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
        # 设置请求头，修复ip38不能请求的bug
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
        }

        self.edit3.clear()
        #设置按钮显示值
        self.button3.setText("执行中，请稍候")
        '''
        对于执行很耗时的程序来说，由于PyQt需要等待程序执行完毕才能进行下一步，
        这个过程表现在界面上就是卡顿，而如果需要执行这个耗时程序时不断的刷新界面。
        那么就可以使用QApplication.processEvents()，
        那么就可以一边执行耗时程序，一边刷新界面的功能，给人的感觉就是程序运行很流畅，
        因此QApplicationEvents（）的使用方法就是，在主函数执行耗时操作的地方，
        加入QApplication.processEvents()
        '''
        QApplication.processEvents()
        #获取输入的值
        text = self.edit1.text()
        try:
            print(verify_ip(text))
            print(url_check(text))
            if verify_ip(text):
                res = requests.get("http://site.ip138.com/" + text,headers=headers,timeout=5)
                res.encoding = 'utf-8'
                selector = etree.HTML(res.text)
                target = selector.xpath('//*[@id="list"]/li/a')  # 查多个url
                for ta in target:
                    a = ta.text
                    self.edit3.append(a)
                if len(target) == 0:
                    self.edit3.append("暂无数据")
            elif url_check(text):
                try:
                    url = re.sub('http://|https://', '', text)
                    res = requests.get("https://site.ip138.com/domain/read.do?domain=" + url + "&time=" + str(time.time_ns())[0:13],headers=headers,timeout=5)
                    res.encoding = 'utf-8'
                    result = json.loads(res.text)
                    status = result["status"]
                    print(status)
                    if not status:
                        again_res = requests.get("http://mip.chinaz.com/?query=" + url,headers=headers,timeout=5)
                        trs = BeautifulSoup(again_res.text, "html.parser").find("table", class_="table mb0").find_all("tr")
                        for tr in trs[1:]:
                            tds = tr.find_all("td")
                            if len(tds) != 1:
                                self.edit3.append(tds[1].text)
                            else:
                                self.edit3.append("暂无数据")
                    else:
                        #解析IP只有一个的情况
                        print(result["data"])
                        data = result["data"]
                        if len(data) == 0:
                            self.edit3.append("暂无数据")
                        else:
                            for one in data:
                                self.edit3.append(one["ip"])
                except BaseException as e:
                    self.edit3.append(str(e))
            else:
                self.edit3.append("输入有误")
            self.button3.setText("执行")
        except BaseException as e:
            print(e)
