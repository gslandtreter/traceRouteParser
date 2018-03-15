import MySQLdb
from netaddr import *
import requests

db = MySQLdb.connect(host="tcc-mysql.ctpoo1wonzcp.sa-east-1.rds.amazonaws.com",
                     user="tcc",
                     passwd="tcc",
                     db="tcc")
db.autocommit(True)
db.ping(True)

def get_invalid_records():
    try:

        cursor = db.cursor()
        cursor.execute("select distinct(hbtl_ip) from domain_dnss where hbtl_asn = -1")
        domains = cursor.fetchall()
        return domains
    except Exception, e:
        print e

    finally:
        if cursor is not None:
            cursor.close()

def update_invalid_record(ip, asn, asn_subnet):
    try:

        cursor = db.cursor()
        cursor.execute("update domain_dnss set hbtl_asn=%s, hbtl_subnet=%s where hbtl_ip = %s", (asn, subnet, ip))
    except Exception, e:
        print e

    finally:
        if cursor is not None:
            cursor.close()

def get_subnet(first_ip, last_ip):
    i = 15
    while i < 32:
        ip_addr = IPNetwork(str(first_ip) + '/' + str(i))
        if str(ip_addr[-1]) == last_ip:
            return str(first_ip) + '/' + str(i)
        i += 1

    return None

def get_asn_and_subnet(ip_address):

    url = "https://api.iptoasn.com/v1/as/ip/" + str(ip_address)
    response = requests.get(url)

    response = response.json()
    if response["announced"] is False:
        return None, None

    asn = response["as_number"]
    subnet = get_subnet(response["first_ip"], response["last_ip"])

    return asn, subnet

if __name__ == '__main__':

    invalid_records = get_invalid_records()

    for record in reversed(invalid_records):
        ip = record[0]
        print "Atualizando IP {}".format(ip)

        asn, subnet = get_asn_and_subnet(ip)
        print "ASN: {} IP: {}".format(asn, subnet)

        if asn is None or subnet is None:
            continue

        update_invalid_record(ip, asn, subnet)



