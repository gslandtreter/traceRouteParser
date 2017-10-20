import MySQLdb

def insert_dns_record(domain_name, position, ns_name, ns_ip, hbtl_name, hbtl_ip, hbtl_asn, hbtp_subnet):
    try:

        # Connect
        db = MySQLdb.connect(host="tcc-mysql.ctpoo1wonzcp.sa-east-1.rds.amazonaws.com",
                             user="tcc",
                             passwd="tcc",
                             db="tcc")
        db.autocommit(True)
        db.ping(True)

        cursor = db.cursor()
        ret = cursor.execute("INSERT INTO domain_dnss (domain, position, ns_name, ns_ip, hbtl_name, hbtl_ip, hbtl_asn, hbtl_subnet) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (domain_name, int(position), ns_name, ns_ip, hbtl_name, hbtl_ip, int(hbtl_asn), hbtp_subnet))
        cursor.close()

        db.close()

        return ret
    except Exception, e:
        print e