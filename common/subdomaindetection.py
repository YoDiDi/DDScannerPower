# -*- coding:utf-8 -*-
# author:f0ngf0ng

from threading import Thread
import dns.resolver
from queue import Queue
import time


# z=['www','mail','info','wwww','home','music','map','news','open','like','org']
class Domainscan(object):
    def __init__(self, domain, dict):
        self.domain = domain
        self.dict = dict
        self._loadDict()
        self.domain_list = []

    def _loadDict(self):
        # 加载字典文件添加进线程队列
        self.q = Queue()
        with open(self.dict, encoding='utf-8') as f:
            for line in f:
                if line[0:1] != '#':
                    self.q.put(line.strip())
        # self.domain_list = [line.strip() for line in open(self.dict, 'r+',encoding='utf-8').readlines()]

    def main(self, result):
        # result 用来与父进程通信
        p = ""
        # 设置dns服务
        self_server = dns.resolver.Resolver()
        self_server.nameservers = ['8.8.8.8']  # 不用本机的DNS服务器,指定用这个

        # 如果队列不为空 则进行解析
        while not self.q.empty():
            # print(self.q.get())
            # 将子域名交给函数解析
            son_domian = self.q.get() + '.' + self.domain
            # print(son_domian)
            self.subdomain_scan(son_domian, result)

    def subdomain_scan(self, d, result):
        try:
            p = ""
            self_server = dns.resolver.Resolver()
            query = self_server.query(d)
            for i in query.response.answer:
                # print(45)
                # print(i)
                with open("output_" + self.domain + ".txt", "a+") as f:
                    f.write(d + "       ")
                with open("output_" + self.domain + ".txt", "a+") as f:
                    f.write("       ")
                if (len(i.items) == 1):
                    for x in i.items:
                        print(d + "." + self.domain + "       " + str(x))
                        result.append(d + "." + self.domain + "       " + str(x))
                        with open("output_" + self.domain + ".txt", "a+") as f:
                            # f.write(x.address + '\n')
                            f.write(str(x) + '\n')
                        # print(x.address)
                        # print(x)
                elif (len(i.items) > 1):
                    for x in i.items:
                        p = p + "," + x.address
                    with open("output_" + self.domain + ".txt", "a+") as f:
                        f.write(p.strip(',') + '\n')
                    print(p)
        except dns.resolver.NXDOMAIN as e:
            pass
            # print(e.args)

    # todo 测试泛解析
    def maintestresolve(self, y):
        zz = ['asdsfsadsfasd', 'asfdcxvqwe', '789454242', 'werqwqweweqweqwrwq', 'zxcsdfawegaareertwere',
              'qwdqdsdvdafwe']
        zz_sets = set()
        self_server = dns.resolver.Resolver()
        self_server.nameservers = ['8.8.8.8']  # 不用本机的DNS服务器,指定用这个
        try:
            for astr in zz:
                query = self_server.query(astr + "." + y)
                for i in query.response.answer:
                    with open("output" + y + ".txt", "a+") as f:
                        f.write(astr + "." + y)
                    print(astr + "." + y)

                    for x in i.items:
                        with open("output" + y + ".txt", "a+") as f:
                            zz_sets.add(x.address)
                        print(x.address)
        except Exception as e:
            print(e)
        return zz_sets


if __name__ == '__main__':
    pass
