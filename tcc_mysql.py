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

        cursor.execute("select count(distinct(domain)) as domain_count from domain_dnss")
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

        cursor.execute("select count(*) as domain_count from domain_dnss where domain = %s", (domain_name,))
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