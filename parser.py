
import trparse
import pyasn

asndb = pyasn.pyasn('ipasn_20171004.db', 'teste.json')

def get_trace_route_from_file(file_name):
    with open(file_name, 'r') as traceRouteFile:
        data = traceRouteFile.read()
        return data

def get_asn_from_ip(ip):
    return asndb.lookup(ip)

def get_asn_name(asn):
    return asndb.get_as_name(asn[0])

if __name__ == '__main__':
    tcString = get_trace_route_from_file('/tmp/teste')

    # Parse the traceroute output
    traceroute = trparse.loads(tcString)
    # You can print the result

    # Or travel the tree
    hopBeforeTheLast = traceroute.hops[len(traceroute.hops) -2]
    probe = hopBeforeTheLast.probes[0]
    # And print the IP address

    print u"Hop before the last para {} ({})".format(traceroute.dest_name, traceroute.dest_ip)
    asn = get_asn_from_ip(probe.ip)
    print u"{} ({}) [{} - {}]".format(probe.name, probe.ip, asn[0], get_asn_name(asn),)