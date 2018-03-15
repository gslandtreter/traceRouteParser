from scapy.all import *
import traceback
import os

def tracert(host, maxhops=64):
    ttl = 1
    hops = []
    while ttl <= maxhops:
        try:
            p = sr1(IP(dst=host, ttl=ttl) / ICMP(id=os.getpid()),
                    verbose=0)
            # if time exceeded due to TTL exceeded
            if p[ICMP].type == 11 and p[ICMP].code == 0:
                hops.append(p.src)
                ttl += 1
            elif p[ICMP].type == 0:
                hops.append(p.src)
                break

        except Exception, e:
            print e
            traceback.print_exc()
            hops.append(None)
            ttl += 1
    return hops


def get_hop_before_the_last(hops):
    if len(hops) < 2:
        return None
    else:
        return hops[-2]


