import re
import MySQLdb

db = MySQLdb.connect(host="tcc-mysql.ctpoo1wonzcp.sa-east-1.rds.amazonaws.com",
                     user="tcc",
                     passwd="tcc",
                     db="tcc")
db.autocommit(True)
db.ping(True)

def insert_asn_record(id, name):
    try:

        cursor = db.cursor()
        ret = cursor.execute("INSERT INTO asn (id, name) VALUES (%s, %s)", (int(id), name))

        return ret
    except Exception, e:
        print e

    finally:
        if cursor is not None:
            cursor.close()



if __name__ == '__main__':
    with open('asn_names.txt') as data_file:
        data = data_file.readlines()

        for line in data:
            line = line.rstrip('\n')
            tokens = re.split('\W+', line, 2)
            if len(tokens) == 3:
                asn_id = tokens[1]
                asn_name = tokens[2]
            elif len(tokens) == 2:
                asn_id = tokens[0]
                asn_name = tokens[1]
            else:
                raise Exception

            print "{} - {}".format(asn_id, asn_name)
            insert_asn_record(asn_id, asn_name)


