
import ip_utils
import traceroute_helper
import socket

from crawlerDB.crawler_model import *


import dns.resolver

import parser
import asn
import tcc_mysql

from multiprocessing.dummy import Pool as ThreadPool
from scapy.all import *

from subprocess import Popen, PIPE


class Crawler:

    def __init__(self):
        self.my_ip = ip_utils.get_public_ip_address()
        self.new_version_info = VersionInfo.create(worker_ip=self.my_ip)

        self.new_version_info.save()
        self.tasks_done = 0
        self.domainList = []

    def get_domain_list(self, file_name):
        self.domainList = []
        with open(file_name) as fp:
            for line in fp:
                line_split = line.split(',')
                self.domainList.append({"position": int(line_split[0]), "name": line_split[1].rstrip()})

            return self.domainList

    def query_domain_nameservers(self, domain_name):
        return dns.resolver.query(domain_name, 'NS')

    def process_domain(self, domain):

        print "Querying Position {} [{}]".format(domain["position"], domain["name"])

        if tcc_mysql.get_if_domain_already_processed(domain["name"], self.new_version_info):
            print "Domain {} already processed. Skipping...".format(domain["name"]);
            return

        nameservers = None

        try:
            nameservers = self.query_domain_nameservers(domain["name"])
        except:
            # print u"{} has no DNS servers. Skipping...".format(domain["name"])
            self.tasks_done += 1
            return

        for rdata in nameservers:
            try:

                traceroute_dest_name = str(rdata.target)
                traceroute_dest_ip = ip_utils.get_host_by_name(traceroute_dest_name)

                hops_to_host = traceroute_helper.tracert(traceroute_dest_name)
                before_the_last_hop_ip = traceroute_helper.get_hop_before_the_last(hops_to_host)

                if before_the_last_hop_ip is None:
                    # print u"Hop before the last para {} ({}) - None".format(traceroute.dest_name, traceroute.dest_ip)

                    tcc_mysql.insert_dns_record(
                        domain["name"],
                        domain["position"],
                        traceroute_dest_name,
                        traceroute_dest_ip,
                        None,
                        None,
                        0,
                        None,
                        self.new_version_info
                    )
                    continue

                provider_asn = asn.get_asn_from_ip(before_the_last_hop_ip)
                before_the_last_hop_name = ip_utils.get_host_by_ip_address(before_the_last_hop_ip)

                # print u"Hop before the last para {} ({})".format(traceroute.dest_name, traceroute.dest_ip)
                # print u"{} ({}) [{} - {}]".format(before_the_last_hop.name, before_the_last_hop.ip, provider_asn[0],
                # asn.get_asn_name(provider_asn[0]))
                tcc_mysql.insert_dns_record(
                    domain["name"],
                    domain["position"],
                    traceroute_dest_name,
                    traceroute_dest_ip,
                    before_the_last_hop_name,
                    before_the_last_hop_ip,
                    provider_asn[0] if (provider_asn[0] is not None) else -1,
                    provider_asn[1],
                    self.new_version_info
                )

            except Exception, e:
                print u"Error obtaining hop before the last for {}".format(rdata.target)
                print e

                continue

        self.tasks_done += 1


    def process_domain_list(self, domain_list, thread_pool_size=100):
        pool = ThreadPool(thread_pool_size)
        result = pool.map_async(self.process_domain, domain_list)

        while not result.ready():
            print "Domains processed: " + str(self.tasks_done)
            time.sleep(10)

        pool.close()
        pool.join()

    def start(self, thread_pool_size):
        domains = self.get_domain_list('top-1m.csv')
        self.process_domain_list(domains, thread_pool_size=thread_pool_size)





if __name__ == '__main__':
    new_crawler = Crawler()
    new_crawler.start(1)
