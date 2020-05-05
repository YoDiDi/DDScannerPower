# coding=utf-8
# author:DIDI
# https://www.cnblogs.com/Triomphe/p/12729644.html
from gevent import monkey

from py.mw.common.config import get_resource_path
#
monkey.patch_all()  # monkey补丁会将在它之后导入的模块的IO操作打包，使gevent认识他们
import gevent
'''
gevent是第三方库，通过greenlet实现协程，其基本思想是：
当一个greenlet遇到IO操作时，比如访问网络，就自动切换到其他的greenlet，等到IO操作完成，再在适当的时候切换回来继续执行。
由于IO操作非常耗时，经常使程序处于等待状态.
有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO。
由于切换是在IO操作时自动完成，所以gevent需要修改Python自带的一些标准库，这一过程在启动时通过monkey patch完成：
'''
# TODO 识别cms


import requests
import json,hashlib

from gevent.queue import Queue
import time
RESOURCEPATH = get_resource_path()


class gwhatweb(object):

    def __init__(self, url, json_path):
        self.tasks = Queue()
        self.url = url.rstrip("/")

        fp = open(json_path, 'rb')
        xiama = fp.read()
        webdata = json.loads(xiama)
        for i in webdata:
            self.tasks.put(i)
        fp.close()
        print("webdata total:%d" % len(webdata))

    def _GetMd5(self, body):
        m2 = hashlib.md5()
        m2.update(body.encode("utf8"))
        return m2.hexdigest()

    def _clearQueue(self):
        while not self.tasks.empty():
            self.tasks.get()

    def _worker(self, output):
        data = self.tasks.get()
        test_url = self.url + data["url"]
        try:
            print(test_url)
            r = requests.get(test_url, timeout=5)
            if r.status_code != 200:
                return
            rtext = r.text
            if rtext is None:
                return
        except:
            rtext = ''

        if data["re"]:
            if rtext.find(data["re"]) != -1:
                result = data["name"]
                output.append("CMS:%s Judge:%s re:%s" % (result, test_url, data["re"]))
                print("CMS:%s Judge:%s re:%s" % (result, test_url, data["re"]))
                self._clearQueue()
                return True
        else:
            md5 = self._GetMd5(rtext)
            if md5 == data["md5"]:
                result = data["name"]
                output.append("CMS:%s Judge:%s md5:%s" % (result, test_url, data["md5"]))
                print("CMS:%s Judge:%s md5:%s" % (result, test_url, data["md5"]))
                self._clearQueue()
                return True

    def _boss(self, result):
        while not self.tasks.empty():
            self._worker(result)

    def whatweb(self, result, maxsize=100):
        start = time.perf_counter()
        allr = [gevent.spawn(self._boss, result) for i in range(maxsize)]
        gevent.joinall(allr)
        end = time.perf_counter()
        print("cost: %f s" % (end - start))


if __name__ == '__main__':
    result = []
    url = "http://mmcxjz.com"
    g = gwhatweb(url, "D:\\WSpace\\DDScannerPower\\resources\dict\gwhatwebdata.json")
    g.whatweb(result, 1000)
    # print(result)

