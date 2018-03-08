import MySQLdb
import ns_asn_processor
import asn_via_api

currentVersion = None

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
        ret = cursor.execute("INSERT INTO domain_dnss (domain, position, ns_name, ns_ip, hbtl_name, hbtl_ip, hbtl_asn, hbtl_subnet, trace_version) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (domain_name, int(position), ns_name, ns_ip, hbtl_name, hbtl_ip, int(hbtl_asn), hbtp_subnet, get_current_version()))

        ns_asn_processor.process_list([ns_ip, ns_name])

        if hbtl_asn == -1:
            asn, subnet = asn_via_api.get_asn_and_subnet(hbtl_ip)
            print "ASN: {} IP: {}".format(asn, subnet)

            if asn is not None and subnet is not None:
                asn_via_api.update_invalid_record(hbtl_ip, asn, subnet)

        return ret
    except Exception, e:
        print e

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()





def get_processed_domain_count():
    try:

        # Connect
        db = MySQLdb.connect(host="tcc-mysql.ctpoo1wonzcp.sa-east-1.rds.amazonaws.com",
                             user="tcc",
                             passwd="tcc",
                             db="tcc")
        db.autocommit(True)
        db.ping(True)

        cursor = db.cursor()

        cursor.execute("select count(distinct(domain)) as domain_count from domain_dnss where trace_version = %s", (get_current_version(),))
        ret = cursor.fetchone()[0]

        return ret
    except Exception, e:
        print e

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()


def get_if_domain_already_processed(domain_name):
    try:

        # Connect
        db = MySQLdb.connect(host="tcc-mysql.ctpoo1wonzcp.sa-east-1.rds.amazonaws.com",
                             user="tcc",
                             passwd="tcc",
                             db="tcc")
        db.autocommit(True)
        db.ping(True)

        cursor = db.cursor()

        cursor.execute("select count(*) as domain_count from domain_dnss where domain = %s and trace_version = %s", (domain_name, get_current_version()))
        totalCount = cursor.fetchone()[0]

        if totalCount > 0:
            ret = True
        else:
            ret = False

        return ret
    except Exception, e:
        print e

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()


def update_ns_asn(ns, asn, subnet, ipv6):
    try:

        # Connect
        db = MySQLdb.connect(host="tcc-mysql.ctpoo1wonzcp.sa-east-1.rds.amazonaws.com",
                             user="tcc",
                             passwd="tcc",
                             db="tcc")
        db.autocommit(True)
        db.ping(True)

        cursor = db.cursor()
        ret = cursor.execute("UPDATE domain_dnss set ns_asn = %s, ns_subnet = %s, ns_ipv6 = %s where ns_ip = %s and trace_version = %s",(asn, subnet, ipv6, ns, get_current_version()))

        return ret
    except Exception, e:
        print e

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()


def update_ns_ipv6(ns, ipv6):
    try:

        # Connect
        db = MySQLdb.connect(host="tcc-mysql.ctpoo1wonzcp.sa-east-1.rds.amazonaws.com",
                             user="tcc",
                             passwd="tcc",
                             db="tcc")
        db.autocommit(True)
        db.ping(True)

        cursor = db.cursor()
        ret = cursor.execute("UPDATE domain_dnss set ns_ipv6 = %s where ns_ip = %s and trace_version = %s",(ipv6, ns, get_current_version()))

        return ret
    except Exception, e:
        print e

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()


def get_ns_without_asn(limit):
    try:

        # Connect
        db = MySQLdb.connect(host="tcc-mysql.ctpoo1wonzcp.sa-east-1.rds.amazonaws.com",
                             user="tcc",
                             passwd="tcc",
                             db="tcc")
        db.autocommit(True)
        db.ping(True)

        cursor = db.cursor()

        cursor.execute("select ns_ip, ns_name from domain_dnss where ns_asn is null and trace_version = %s LIMIT %s", (get_current_version(), limit))
        results = cursor.fetchall()

        return results
    except Exception, e:
        print e

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()


def get_current_version():

    global currentVersion
    if currentVersion is not None:
        return currentVersion

    try:

        # Connect
        db = MySQLdb.connect(host="tcc-mysql.ctpoo1wonzcp.sa-east-1.rds.amazonaws.com",
                             user="tcc",
                             passwd="tcc",
                             db="tcc")
        db.autocommit(True)
        db.ping(True)

        cursor = db.cursor()

        cursor.execute("select id from version_info where end_date is null")
        currentVersion = cursor.fetchone()[0]

        return currentVersion
    except Exception, e:
        print e

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()