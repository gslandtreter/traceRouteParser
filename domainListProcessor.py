
import dns.resolver
import time

import parser
import asn
import tcc_mysql

from multiprocessing.dummy import Pool as ThreadPool

from subprocess import Popen, PIPE

tasksDone = 0

# Basic query
for rdata in dns.resolver.query('www.yahoo.com', 'CNAME'):
    print rdata.target


def get_domain_list(file_name):
    domainList = []
    with open(file_name) as fp:
        for line in fp:
            line_split = line.split(',');
            domainList.append({"position": int(line_split[0]), "name": line_split[1].rstrip()})
        return domainList

def query_domain_nameservers(domain_name):
    return dns.resolver.query(domain_name, 'NS')

def process_domain(domain):

    global tasksDone
    print "Querying Position {} [{}]".format(domain["position"], domain["name"])
    nameservers = None

    try:
        nameservers = query_domain_nameservers(domain["name"])
    except:
        #print u"{} has no DNS servers. Skipping...".format(domain["name"])
        tasksDone += 1
        return

    for rdata in nameservers:
        try:
            tr_text = trace_route(rdata.target)
            traceroute = parser.parse_trace_route(tr_text)
            before_the_last_hop = parser.get_hop_before_the_last(traceroute)

            if (before_the_last_hop.ip is None):
                #print u"Hop before the last para {} ({}) - None".format(traceroute.dest_name, traceroute.dest_ip)

                tcc_mysql.insert_dns_record(
                    domain["name"],
                    domain["position"],
                    traceroute.dest_name,
                    traceroute.dest_ip,
                    None,
                    None,
                    0,
                    None
                )
                continue

            provider_asn = asn.get_asn_from_ip(before_the_last_hop.ip)
            #print u"Hop before the last para {} ({})".format(traceroute.dest_name, traceroute.dest_ip)
            #print u"{} ({}) [{} - {}]".format(before_the_last_hop.name, before_the_last_hop.ip, provider_asn[0],
                                             # asn.get_asn_name(provider_asn[0]))
            tcc_mysql.insert_dns_record(
                domain["name"],
                domain["position"],
                traceroute.dest_name,
                traceroute.dest_ip,
                before_the_last_hop.name,
                before_the_last_hop.ip,
                provider_asn[0] if (provider_asn[0] is not None) else -1,
                provider_asn[1]
            )

        except Exception, e:
            print u"Error obtaining hop before the last for {}".format(rdata.target)
            print e

            continue


    tasksDone += 1



def process_domain_list(domain_list):
    pool = ThreadPool(100)
    result = pool.map_async(process_domain, domain_list)

    while not result.ready():
        print "Domains processed: " + str(tasksDone)
        time.sleep(10)

    pool.close()
    pool.join()

def trace_route(target):
    return traceroute(str(target))

def traceroute(url,):
    result = ''
    p = Popen(['traceroute', '-I', '-w 2', url], stdout=PIPE)
    while True:
        line = p.stdout.readline()

        if not line:
            break

        result += line
    return result

if __name__ == '__main__':
    domains = get_domain_list('top-1m.csv')
    process_domain_list(domains)
