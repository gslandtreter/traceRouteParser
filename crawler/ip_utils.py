import socket
from urllib2 import urlopen


def get_public_ip_address():
    return urlopen('http://ip.42.pl/raw').read()


def get_host_by_ip_address(ip):
    return socket.gethostbyaddr(ip)


def get_host_by_name(hostname):
    return socket.gethostbyname(hostname.strip())
