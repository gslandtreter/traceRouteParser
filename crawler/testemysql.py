
from crawlerDB.crawler_model import *

if __name__ == '__main__':
    print [asn.id for asn in Asn.select()]