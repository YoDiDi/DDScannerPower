from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout, QLineEdit,
                             QTextEdit, QComboBox, QFileDialog, QApplication)

__author__ = 'yodidi'

from py.mw.common.bruteservice import Brute
from py.mw.common.config import get_resource_path, get_tool_name, get_logo_path
from py.mw.common.ipcheck import verify_ip
from py.mw.common.dolog import log

RESOURCEPATH = get_resource_path()
TOOLNAME = get_tool_name()
LOGOPATH = get_logo_path()


class ModeWidget4(QWidget):
    """
    功能弹出框
    """
    def __init__(self):
        super().__init__()
        self.resize(650, 500)
        self.center()
        self.setWindowTitle("爆破服务")
        self.setWindowIcon(QIcon(RESOURCEPATH + LOGOPATH))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.edit1 = ""
        self.edit2 = ""
        self.edit3 = ""
        self.edit4 = ""
        self.edit5 = ""
        self.button3 = None
        self.button41 = None
        self.button42 = None
        self.cb = None
        self.path = "D:\\"
        self.username = None
        self.pwd = None
        self.initUI()

    def initUI(self):
        label1 = QLabel("选择协议：")
        self.cb = QComboBox(self, minimumWidth=549)
        self.cb.addItem("FTP")
        self.cb.addItem("SSH")
        self.cb.addItem("MYSQL")
        self.cb.setStyleSheet("height:30px;")
        label2 = QLabel("IP地址:")
        label2.setStyleSheet("min-width:72px;height:30px;")
        self.edit2 = QLineEdit()
        self.edit2.setStyleSheet("height:30px;")
        self.edit2.setText('192.168.111.130')
        label5 = QLabel("端口号:")
        label5.setStyleSheet("min-width:72px;height:30px;")

        self.edit5 = QLineEdit()
        # 整形 范围：[1, 65535]
        pPortValidator = QIntValidator(self)
        pPortValidator.setRange(1, 65535)
        self.edit5.setPlaceholderText("请输入1-65535")
        self.edit5.setText('22')

        self.edit5.setValidator(pPortValidator)
        self.edit5.setStyleSheet("height:30px;")

        label4 = QLabel("线程数:")
        label4.setStyleSheet("min-width:72px;height:30px;")
        self.edit4 = QLineEdit()
        # 整形 范围：[1, 10]
        pThreadValidator = QIntValidator(self)
        pThreadValidator.setRange(1, 10)
        self.edit4.setPlaceholderText("请输入1-10")
        self.edit4.setText('2')
        self.edit4.setValidator(pThreadValidator)
        self.edit4.setStyleSheet("height:30px;")
        self.button41 = QPushButton("用户名文件")
        self.button41.clicked.connect(self.showFileDialogUser)
        self.button42 = QPushButton("密码文件")
        self.button42.clicked.connect(self.showFileDialogPwd)
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
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()
        hbox7 = QHBoxLayout()

        # 把按钮放在盒子里
        hbox1.addWidget(label1)
        hbox1.addWidget(self.cb)
        hbox2.addWidget(label2)
        hbox2.addWidget(self.edit2)
        hbox7.addWidget(label5)
        hbox7.addWidget(self.edit5)
        hbox5.addWidget(label4)
        hbox5.addWidget(self.edit4)
        hbox6.addWidget(self.button41)
        hbox6.addWidget(self.button42)
        hbox3.addWidget(self.button3)
        hbox4.addWidget(self.edit3)

        # 把竖直盒子和水平盒子嵌套在水平盒子中
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
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
        success =[]
        self.edit3.clear()
        self.button3.setText("执行中，请稍候")
        QApplication.processEvents()
        protocol = self.cb.currentText()
        ip = self.edit2.text()
        port = self.edit5.text()
        thread_num = self.edit4.text()
        username_path = self.username
        pwd_path = self.pwd
        if ip == "":
            self.edit3.append("IP不允许为空")
        else:
            if not verify_ip(ip):
                self.edit3.append("IP输入错误")
            else:
                if username_path is None:
                    username_path = RESOURCEPATH + "dict/" + "userdict.txt"
                if pwd_path is None:
                    pwd_path = RESOURCEPATH + "dict/" + "pwddict.txt"
                if protocol == "FTP":
                    if port == "":
                        port = "21"
                elif protocol == "SSH":
                    if port == "":
                        port = "22"
                elif protocol == "MYSQL":
                    if port == "":
                        port = "3306"
                if thread_num == "":
                    thread_num = 5
                brute = Brute(protocol, ip, port, thread_num, username_path, pwd_path)
                result = brute.run()
                if len(result) == 0:
                    self.edit3.append("暂无数据")
                else:
                    for _ in result:
                        self.edit3.append(_)
                        if "成功" in _:
                            success.append(_)
        if len(success)>0:
            for s in success:
                print(s)
                self.edit3.append("\n")
                self.edit3.append("[+] 爆破成功!\n" + s)

        self.button3.setText("执行")
        bug=''
        log(protocol+'服务爆破', ip+port, ' ', result, bug)

    def showFileDialogUser(self):
        fname = QFileDialog.getOpenFileName(self, '选择用户名文件', self.path, "Text Files (*.txt)")
        if fname[0] != '':
            self.username = fname[0]
            self.button41.setText(self.username)

    def showFileDialogPwd(self):
        fname = QFileDialog.getOpenFileName(self, '选择密码文件', self.path, "Text Files (*.txt)")
        if fname[0] != '':
            self.pwd = fname[0]
            self.button42.setText(self.pwd)


