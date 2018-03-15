from peewee import *
from config import crawler_config
from playhouse.pool import PooledMySQLDatabase

database = PooledMySQLDatabase(

    crawler_config.mysql["db"],

    max_connections=5,
    stale_timeout=60,
    timeout=0,

    **{
        'passwd': crawler_config.mysql["passwd"],
        'host': crawler_config.mysql["host"],
        'charset': 'utf8',
        'user': crawler_config.mysql["user"],
        'use_unicode': True
    }

)

class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Asn(BaseModel):
    name = CharField(null=True)

    class Meta:
        table_name = 'asn'
        schema = 'tcc'


class VersionInfo(BaseModel):
    end_date = DateTimeField(null=True)
    start_date = DateTimeField()
    worker_ip = CharField(null=True)

    class Meta:
        table_name = 'version_info'
        schema = 'tcc'


class DomainDnss(BaseModel):
    domain = CharField(index=True, null=True)
    hbtl_asn = IntegerField(index=True, null=True)
    hbtl_ip = CharField(null=True)
    hbtl_name = CharField(null=True)
    hbtl_subnet = CharField(index=True, null=True)
    ns_asn = IntegerField(null=True)
    ns_ip = CharField(index=True, null=True)
    ns_ipv6 = CharField(null=True)
    ns_name = CharField(null=True)
    ns_subnet = CharField(null=True)
    position = IntegerField(null=True)
    trace_version = ForeignKeyField(column_name='trace_version', field='id', model=VersionInfo, null=True)

    class Meta:
        table_name = 'domain_dnss'
        indexes = (
            (('domain', 'ns_name', 'trace_version'), True),
            (('hbtl_asn', 'hbtl_subnet'), False),
            (('ns_asn', 'hbtl_asn'), False),
        )
        schema = 'tcc'
        primary_key = False


class DomainDnss1(BaseModel):
    domain = CharField(null=True)
    hbtl_asn = IntegerField(null=True)
    hbtl_ip = CharField(null=True)
    hbtl_name = CharField(null=True)
    hbtl_subnet = CharField(null=True)
    ns_asn = IntegerField(null=True)
    ns_ip = CharField(null=True)
    ns_ipv6 = CharField(null=True)
    ns_name = CharField(null=True)
    ns_subnet = CharField(null=True)
    position = IntegerField(null=True)

    class Meta:
        table_name = 'domain_dnss_1'
        schema = 'tcc'
        primary_key = False


class Parameters(BaseModel):
    key = CharField(primary_key=True)
    value = CharField(null=True)

    class Meta:
        table_name = 'parameters'
        schema = 'tcc'
