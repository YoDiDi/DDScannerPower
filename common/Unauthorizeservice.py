# -*- coding:utf-8 -*-
# author:DIDI
import requests
import redis
import pymongo


class Services:
    def __init__(self, types, ip, port):
        self.types = types
        self.ip = ip
        self.port = port
        self.result = []

    def elasticsearch(self):
        url = self.ip.strip()
        url = url + "/_plugin/head/"
        try:
            requests.packages.urllib3.disable_warnings()
            a = requests.get(url, timeout=3)
            if a.status_code == 200:
                print("存在elasticsearch未授权访问")
        except:
            pass

    def MongoDB(self):
        # 未授权访问漏洞成因：
        # Mongodb 在启动的时候提供了很多参数，如日志记录到哪个文件夹，是否开启认证等。
        # 造成未授权访问的根本原因就在于启动 Mongodb 的时候未设置 --auth
        # 也很少会有人会给数据库添加上账号密码（默认空口令），
        # 使用默认空口令这将导致恶意攻击者无需进行账号认证就可以登陆到数据服务器。
        url = self.ip
        try:
            client = pymongo.MongoClient("mongodb://" + url, 27017)  # 运行 mongod 实例创建一个MongoClient,明确连接指定主机和端口
            mydb = client['local']  # 获取数据库对象
            sevenday = mydb['startup_log']  # 获取集合对象
            doc = sevenday.find()
            for d in doc:
                if d:
                    print(d + "存在未授权")
                    break
                else:
                    print("wrong")
        except pymongo.errors.OperationFailure:
            print("ooo")
        except pymongo.errors.ServerSelectionTimeoutError:
            print("oo")
        except pymongo.errors.ConfigurationError:
            print("o")
        except pymongo.errors.NetworkTimeout:
            print("o")

    def Redis(self):
        url = self.ip.strip()
        try:
            r = redis.Redis(host=url, port=int(self.port), db=0)
            rs = r.info()
            if rs:
                print('[+] Vuln Found:' + url + "存在redis未授权访问")
                return ["[+] Vuln Found:" + url +":"+str(self.port)+ "存在redis未授权访问 \n[+]INFO:\n" + str(rs)]
            else:
                pass
        except:
            pass

    def run(self):
        if self.types == 'Redis':
            self.result = self.Redis()
        if self.types == 'elasticsearch':
            pass
            # self.result = self.elasticsearch()
        if self.types == 'MongoDB':
            pass
            # self.result = self.MongoDB()
        if self.result is not None:
            return self.result
        else:
            return '[*] 不存在%s未授权访问' % self.types
if __name__ == '__main__':
    init_s = Services(types="Redis", ip="192.168.111.130", port=6379)
    result = init_s.run()
    print(result)
