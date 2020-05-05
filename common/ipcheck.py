from IPy import IP

__author__ = 'Raiynin'


def verify_ip(ip):
    if len(ip.split('.')) != 4:
        return False
    try:
        ip = IP(ip)
        return True
    except:
        return False