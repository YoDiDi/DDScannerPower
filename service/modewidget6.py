import threading, time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout, QLineEdit,
                             QTextEdit, QComboBox, QApplication)

__author__ = 'Yodidi'

from py.mw.common.config import get_resource_path, get_tool_name, get_logo_path
from py.mw.common.grafana import weak
from py.mw.common.dolog import log

RESOURCEPATH = get_resource_path()
TOOLNAME = get_tool_name()
LOGOPATH = get_logo_path()


class ModeWidget6(QWidget):
    """
    功能弹出框
    """

    def __init__(self):
        super().__init__()
        self.resize(650, 400)
        self.center()
        self.setWindowTitle("弱口令服务")
        self.setWindowIcon(QIcon(RESOURCEPATH + LOGOPATH))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.edit2 = ""
        self.edit3 = ""
        # self.edit5 = ""
        self.button3 = None
        self.initUI()

    def initUI(self):
        label1 = QLabel("服务类型：")
        self.cb = QComboBox(self, minimumWidth=538)
        self.cb.addItem("Grafana")
        self.cb.setStyleSheet("height:30px;")
        label2 = QLabel("URL地址:")
        label2.setStyleSheet("min-width:84px;height:30px;")
        self.edit2 = QLineEdit()
        self.edit2.setStyleSheet("height:30px;")
        self.edit2.setText("http://192.168.111.130:3000")
        # label5 = QLabel("端口号:")
        # label5.setStyleSheet("min-width:84px;height:30px;")

        # self.edit5 = QLineEdit()
        # 整形 范围：[1, 65535]
        pPortValidator = QIntValidator(self)
        pPortValidator.setRange(1, 65535)
        # self.edit5.setPlaceholderText("请输入1-65535")
        # self.edit5.setValidator(pPortValidator)
        # self.edit5.setStyleSheet("height:30px;")
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
        # hbox5 = QHBoxLayout()

        # 把按钮放在盒子里
        hbox1.addWidget(label1)
        hbox1.addWidget(self.cb)
        hbox2.addWidget(label2)
        hbox2.addWidget(self.edit2)
        # hbox5.addWidget(label5)
        # hbox5.addWidget(self.edit5)
        hbox3.addWidget(self.button3)
        hbox4.addWidget(self.edit3)

        # 把竖直盒子和水平盒子嵌套在水平盒子中
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        # vbox.addLayout(hbox5)
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
        bug = ''
        url = ''
        result = []
        try:
            self.edit3.clear()
            self.button3.setText("执行中，请稍候")
            QApplication.processEvents()
            url = self.edit2.text()
            t = threading.Thread(target=weak, args=(url, result))
            t.setDaemon(True)
            t.start()

            # 等待线程完成
            # t.join()

            # 检测线程是否存活,不使用t.join() 避免gui假死
            while True:
                if threading.activeCount() <= 1:
                    break
                else:
                    time.sleep(0.1)

            if len(result) != 0:
                print(result)
                self.button3.setText("点击执行")
                self.edit3.append(result[0])
            else:
                self.button3.setText("暂无数据")

        except BaseException as e:
            bug = str(e)
        log('弱口令服务', url, '-', result, bug)
