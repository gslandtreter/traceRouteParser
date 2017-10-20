
import trparse
import pyasn



def get_trace_route_from_file(file_name):
    with open(file_name, 'r') as traceRouteFile:
        data = traceRouteFile.read()
        return data

def get_hop_before_the_last(traceroute):
    hopBeforeTheLast = traceroute.hops[len(traceroute.hops) - 2]
    return hopBeforeTheLast.probes[0]


def parse_trace_route(tc_string):
    # Parse the traceroute output
    traceroute = trparse.loads(tc_string)
    return traceroute

