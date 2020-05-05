# -*- coding:utf-8 -*-
# author:DIDI
import requests


def weak(url, result):
    data_json = {"user": "admin", "email": "", "password": "admin"}
    url = url.strip()
    url = url + "/login"
    print(url)
    try:
        requests.packages.urllib3.disable_warnings()
        seesion = requests.session()
        seesion.get(url)
    except requests.exceptions.ConnectTimeout:
        # NETWORK_STATUS = False
        pass

    except requests.exceptions.Timeout:
        # REQUEST_TIMEOUT = True
        pass

    except requests.exceptions.ConnectionError:
        pass
    try:
        requests.packages.urllib3.disable_warnings()
        b = requests.session()

        b1 = b.post(url, data_json)
        if b1.status_code == 200:
            print("[+] %s 存在grafana服务弱口令,帐号 %s 密码 %s" %(url,data_json['user'],data_json['password']))
            result.append("[+] %s 存在grafana服务弱口令,帐号 %s 密码 %s" %(url,data_json['user'],data_json['password']))

    except requests.exceptions.ConnectTimeout as e:
        # NETWORK_STATUS = False
        result.append(str(e))
        pass
    except requests.exceptions.Timeout:
        # REQUEST_TIMEOUT = True
        result.append(str(e))
        pass
    except requests.exceptions.ConnectionError:
        result.append(str(e))
        pass


if __name__ == '__main__':
    pass
    # weak("http://192.168.111.130:3000",[])
