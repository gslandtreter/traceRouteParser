
import dns.resolver
from subprocess import Popen, PIPE

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


def process_domain_list(domain_list):
    for domain in domain_list:
        for rdata in dns.resolver.query(domain["name"], 'NS'):
            tr = trace_route(rdata.target)
            print tr

def trace_route(target):
    return traceroute(str(target))

def traceroute(url,):
    result = ''
    p = Popen(['traceroute', '-n', url], stdout=PIPE)
    while True:
        line = p.stdout.readline()

        if not line:
            break

        result += line
    return result

if __name__ == '__main__':
    domains = get_domain_list('top-1m.csv')
    process_domain_list(domains)