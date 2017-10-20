import pyasn

asndb = pyasn.pyasn('ipasn_20171004.db', 'teste.json')

def get_asn_from_ip(ip):
    return asndb.lookup(ip)

def get_asn_name(as_number):
    return asndb.get_as_name(as_number)
