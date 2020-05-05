# author:DIDI
import threading
import time
from queue import Queue
import requests
import re

from py.mw.common.config import get_resource_path
from py.mw.common.urlcheck import url_check


def check_404(text):
    pattern = re.compile(r'404')  # 设置pattern
    m = pattern.match(text)
    if m is None:
        return True
    else:
        return False


class Dirscan(object):
    def __init__(self, scanSite, scanDict, threadNum):
        self.scanSite = scanSite if scanSite.find('://') != -1 else 'http://%s' % scanSite
        self.scanDict = scanDict
        self.threadNum = threadNum
        self._loadHeaders()
        self._loadDict(self.scanDict)

    def _loadDict(self, dict_list):
        self.q = Queue()
        with open(dict_list, encoding='utf-8') as f:
            for line in f:
                if line[0:1] != '#':
                    self.q.put(line.strip())

    def _loadHeaders(self):
        self.headers = {
            'Accept': '*/*',
            'Referer': 'http://www.baidu.com',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
            'Cache-Control': 'no-cache',
        }

    def _scan(self, url, result):
        html_result = 0
        try:
            html_result = requests.get(url, headers=self.headers, allow_redirects=False, timeout=2)
        except requests.exceptions.ConnectionError:
            pass
        finally:
            if html_result != 0:
                if html_result.status_code == 200 and check_404(html_result.text):
                    result.append('[%i]%s' % (html_result.status_code, html_result.url))
                    print('[%i]%s' % (html_result.status_code, html_result.url))

    def run(self, result):
        while not self.q.empty():
            url = self.scanSite + self.q.get()
            print(url)
            self._scan(url, result)


if __name__ == '__main__':
    RESOURCEPATH = get_resource_path()
    result = []
    thread_num = 5
    url = "www.baidu.com"
    if url_check(url):
        scan = Dirscan(url, RESOURCEPATH + "dict/" + "webdirscandict.txt", thread_num)
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
            print(_)
        if len(result) == 0:
            print("暂无数据")
