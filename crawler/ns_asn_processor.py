import socket

import dns.resolver
import time

import parser
import asn
import tcc_mysql

from multiprocessing.dummy import Pool as ThreadPool

from subprocess import Popen, PIPE

tasksDone = 0

def get_ns_ipv6(name):
    try:
        addrinfo = socket.getaddrinfo(name, None, socket.AF_INET6)
        if addrinfo is None:
            return None

        return addrinfo[0][4][0]
    except:
        return None


def process_list(ns_item):

        print "Updating {}...".format(ns_item[1])

        ns_asn = asn.get_asn_from_ip(ns_item[0])
        as_number = ns_asn[0] if (ns_asn[0] is not None) else None
        as_subnet = ns_asn[1] if (ns_asn[1] is not None) else None
        ipv6 = get_ns_ipv6(ns_item[1])
        tcc_mysql.update_ns_asn(ns_item[0], as_number, as_subnet, ipv6)

        global tasksDone
        tasksDone += 1


def process_domain_list(domain_list):

    pool = ThreadPool(150)
    result = pool.map_async(process_list, domain_list)

    while not result.ready():
        print "Domains processed: " + str(tasksDone)
        time.sleep(10)

    pool.close()
    pool.join()


if __name__ == '__main__':

    list = tcc_mysql.get_ns_without_asn(1000)
    process_domain_list(list)

    while len(list) > 0:
        list = tcc_mysql.get_ns_without_asn(10000)
        process_domain_list(list)
