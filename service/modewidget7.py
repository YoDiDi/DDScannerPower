import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout, QLineEdit,
                             QTextEdit, QComboBox, QApplication)

__author__ = 'Y(didi)'

from py.mw.common.config import get_resource_path, get_tool_name, get_logo_path
from py.mw.common import m7_cmsexp

RESOURCEPATH = get_resource_path()
TOOLNAME = get_tool_name()
LOGOPATH = get_logo_path()


class ModeWidget7(QWidget):
    """
    功能弹出框
    """

    def __init__(self):
        super().__init__()
        self.resize(650, 400)
        self.center()
        self.setWindowTitle("漏洞利用")
        self.setWindowIcon(QIcon(RESOURCEPATH + LOGOPATH))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.edit1 = ""
        self.edit3 = ""
        self.button3 = None
        self.cb = ''
        self.results = []

        # 相关信息
        self.cms = [
            '请选择漏洞利用',
            'PHPCMS v9.6.0 任意文件上传',
            'PHPCMS v9.6.0 sql注入',
            'dedecms',
        ]
        # cms对应的exp函数
        self.cms_exp = [
            '',
            'phpcmsv9_upload',
            'phpcmsv9_sqlinject',
            'dedecms exp',
        ]
        # 对应的info信息
        self.exp_info = [
            '',
            '影响版本:phpcms v9.6.0\n漏洞详情:用户注册处、无需登录，需要远程php shell地址\n参考链接:https://xz.aliyun.com/t/5730',
            '影响版本:phpcms v9.6.0\n漏洞详情:漏洞文件phpcms/modules/content/down.php\n参考链接:https://xz.aliyun.com/t/5730',
            '',
        ]
        # 统一的label样式
        self.labelcalss = 'min-width:84px;height:30px;'

        # 下拉框的次序
        self.index = 0

        # 额外参数定义
        self.edit_setargs = ''
        self.initUI()

    # 下拉框选择事件
    def onActivated(self, text):
        # 选中序列
        self.index = self.cb.currentIndex()
        # print(self.index)
        # 选中的文本
        # print(text)
        # 设置显示
        try:
            # 没有选择的时候
            if self.index == 0:
                self.button3.hide()
                self.label_args.hide()
                self.edit_setargs.hide()
                self.edit3.setText("请选择漏洞哦")
            # 没有详情的时候
            elif self.cms_exp[self.index] == '' and self.exp_info[self.index] == '':
                self.button3.show()
                self.edit3.setText("暂无漏洞详情")
            # 有详情 且次数不为0
            else:
                # 显示执行按钮
                self.button3.show()
                # 额外参数显示
                if self.index == 1:
                    # self.label_phpcmsv9_setargs.setVisible(True)
                    self.label_args.show()
                    # self.phpcmsv9_setargs.setVisible(True)
                    # 信息提示
                    self.edit_setargs.setPlaceholderText("请输入远程shell地址 e.g:http://xxx.com/xxx.txt")
                    self.edit_setargs.setText("http://192.168.8.106:81/shell.txt")
                    self.edit_setargs.show()

                # 其他exp设置
                else:
                    self.edit_setargs.setText('')
                    self.label_args.hide()
                    self.edit_setargs.hide()

                # 显示详情
                self.edit3.setText(self.cms_exp[self.index])
                self.edit3.append(self.exp_info[self.index])

        except IndexError:
            print('error')
            self.edit3.setText("暂无漏洞详情")

    # 加载UI
    def initUI(self):
        label1 = QLabel("选择漏洞:")
        label1.setStyleSheet(self.labelcalss)
        # 设置下拉框
        self.cb = QComboBox(self, minimumWidth=550)
        for i in self.cms:
            self.cb.addItem(i)
        self.cb.setStyleSheet("height:30px;")
        # 下路框选择事件
        self.cb.activated[str].connect(self.onActivated)
        label2 = QLabel("URL地址 :")
        label2.setStyleSheet(self.labelcalss)
        self.edit2 = QLineEdit()
        self.edit2.setStyleSheet("height:30px;min-width:548px;")
        self.edit2.setText("http://192.168.111.130")
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
        self.button3.clicked.connect(self.UIfuc)
        self.button3.hide()
        self.edit3 = QTextEdit()

        # 设置exp需要的参数 先设置隐藏属性,下拉后显示参数设置框
        self.label_args = QLabel("参数设置:")
        self.label_args.setStyleSheet(self.labelcalss)
        # self.label_phpcmsv9_setargs.setVisible(False)
        self.label_args.hide()
        self.edit_setargs = QLineEdit()
        self.edit_setargs.setStyleSheet("height:30px;min-width:348px;")
        # self.edit_setargs.setText("http://192.168.8.106:81/shell.txt")
        # self.phpcmsv9_setargs.setVisible(False)
        self.edit_setargs.hide()

        # 添加一个竖直盒子，两个水平盒子
        vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()

        hbox5 = QHBoxLayout()

        # 把按钮放在盒子里
        hbox2.addWidget(label2)
        hbox2.addWidget(self.edit2)
        hbox1.addWidget(label1)
        hbox1.addWidget(self.cb)
        hbox3.addWidget(self.button3)
        hbox4.addWidget(self.edit3)

        # 显示一个输入框填写参数
        hbox5.addWidget(self.label_args)
        hbox5.addWidget(self.edit_setargs)

        # 把竖直盒子和水平盒子嵌套在水平盒子中
        # 输入url的盒子
        vbox.addLayout(hbox2)
        # 下拉框的盒子
        vbox.addLayout(hbox1)
        # 显示一个输入框填写参数
        vbox.addLayout(hbox5)
        # 点击执行按钮的盒子
        vbox.addLayout(hbox3)
        # 显示框的盒子
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

    def UIfuc(self):
        # 使用QThread,重写run函数，开启子线程执行,通过构造函数__init___传递参数，这里直接把本类对象传递进去了 创建信号和槽函数的绑定
        self.thread = RunThread(self)
        self.thread.list1.connect(self.showEdit3)
        self.thread.start()

        # 设置执行中的状态
        self.edit3.clear()
        self.button3.setText("执行中，请稍候")
        # 禁用按钮
        self.button3.setEnabled(False)
        QApplication.processEvents()

    def showEdit3(self, list1):
        self.button3.setEnabled(True)
        # 取回线程执行结果
        print("显示线程执行结果")
        print(list1)
        for _ in list1:
            self.edit3.setText(str(_))
        if len(list1) == 0:
            self.edit3.setText("暂无数据")
        self.button3.setText("点击执行")


# todo 代码压缩 import常见模块写到一个包里 然后开放api调用

# todo QThread 的使用

# from PyQt5.QtCore import Qt, QThread, pyqtSignal https://www.cnblogs.com/XJT2018/p/10222981.html PyQt 5信号与槽的几种高级玩法
# https://www.jianshu.com/p/ed47a8959854 https://www.jianshu.com/p/ed47a8959854
# https://blog.csdn.net/zulien/article/details/84990708 PyQt5 界面显示无响应 http://www.cocoachina.com/articles/69346 python
# – PyQt正确使用emit()和pyqtSignal() https://blog.csdn.net/broadview2006/article/details/80132757 PyQt 5信号与槽的几种高级玩法
# https://blog.csdn.net/broadview2006/article/details/80132757
# https://www.jb51.net/article/154465.htm python之线程通过信号pyqtSignal刷新ui的方法
# http://www.broadview.com.cn/article/824 PyQt 5信号与槽的几种高级玩法

class RunThread(QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    # _signal = pyqtSignal(str)

    # 定义一个列表类型的信号
    list1 = pyqtSignal(list)

    # 声明带一个列表类型参数的信号
    list4 = pyqtSignal(list)

    def __init__(self, parent=None):
        # 父类
        print(parent)

        self.url = parent.edit2.text().strip()
        self.func = parent.cms_exp[parent.index]
        self.data = parent.edit_setargs.text()

        print(self.url, self.func, self.data)

        #  Python3.x 和 Python2.x 的一个区别是: Python 3 可以使用直接使用 super().xxx 代替 super(Class, self).xxx :
        # https://www.runoob.com/python/python-func-super.html
        # py2.x
        # super(Thread, self).__init__()  # 继承QThread
        # py3.x
        super().__init__(parent)  # 继承QThread

        # 定义线程工作状态
        self.working = True

    def __del__(self):
        self.wait()

    def run(self):
        # import time
        # time.sleep(50)
        # for i in range(1, 8):
        #     ss = []
        #     ss.append(i)
        #     time.sleep(1)
        #     self.list1.emit(ss)

        # 子线程的变量传递，可以通过在子线程对该变量操作实现信息传递，大量线程时需要考虑线程锁，此处没有用到子线程，是在一个线程里跑的
        # 因为该类本身就是一个子线程 ==
        result = []
        print(self.working)
        while self.working:
            try:
                # 下拉总数
                # print(self.cb.count())
                # 获取要执行的函数
                # print(self.cms_exp[self.index])
                # 获取额外的参数
                # print(self.edit_setargs.text())

                # 先实例化这个类
                cms_exp = m7_cmsexp.Cmsexp(self.url, self.func, self.data)
                # 执行完成后result参数已经改变了
                cms_exp.start(result)
                # 取回线程执行结果
                # shift + table 向左缩进
                print(result)

            except BaseException as e:
                # self.edit3.setText(str(e))
                result.append(str(e))
            # emit可以重新实现以将特定信号值发送到槽功能.，发送的类型需要与定义的一致，此处返回列表
            self.list1.emit(result)

            # 设置线程停止
            self.working = False
