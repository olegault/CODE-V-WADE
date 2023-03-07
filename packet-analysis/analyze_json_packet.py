"""
Read a mitmproxy dump file.
"""
from mitmproxy.io import FlowReader
from mitmproxy.http import HTTPFlow
from colorama import Fore, Style, init
from termcolor import colored
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)
args = parser.parse_args()

filename = args.filename

flows = []
init()

with open(filename, 'rb') as fp:
    reader = FlowReader(fp)

    for flow in reader.stream():
        flows.append(flow)

# Filters list of flows by method (GET, POST, etc.)
def filter_flows_method(flows: list[HTTPFlow], methods: list[str]):
    filt = []
    for flow in flows:
        if flow.request.method in methods:
            filt.append(flow)
    return filt

# Returns a string highlighted in red
def highlight(term):
    return  f"{Fore.RED}{term}{Style.RESET_ALL}"

# Searches a string and highlights all occurences of a term in red
def highlight_term(s, term):
    return s.replace(term, highlight(term))

# Searches a list of flows according to a selected query
def terms_search(flows: list[HTTPFlow], query: str, char_buff: int):
    qs = {'health':       {'filepath': './search_lists/health.txt',
                           'question': ("Does this line contain " + highlight("general health data") + '?')},
          'reproductive': {'filepath': './search_lists/reproductive.txt',
                           'question': ("Does this line contain " + highlight("reproductive health data") + '?')},
          'delete':       {'filepath': './search_lists/delete.txt',
                           'question': ("Does this line indicate " + highlight("account deletion") + "?")}}
    
    terms = []
    with open(qs[query]['filepath'], 'r') as f:
        terms = [line.rstrip('\n') for line in f]
    
    for flow in flows:
        # Get response content if available
        rsp = flow.response
        if not rsp: continue

        rsp = str(rsp.content).lower()
        for term in terms:
            res = [i.start() for i in re.finditer(term, rsp)]
            for i in res:
                print(qs[query]['question'])
                print(highlight_term(rsp[i-char_buff:i+char_buff], term))
                cont = input("[y/n]: ") == 'y'
                if cont:
                    return True
                print('\n')
                
        rq = str(flow.request.content).lower()
        for term in terms:
            res = [i.start() for i in re.finditer(term, rq)]
            for i in res:
                print(qs[query]['question'])
                print(highlight_term(rq[i-char_buff:i+char_buff], term))
                cont = input("[y/n]: ") == 'y'
                if cont:
                    return True
                print('\n')

    return input('No more flows. Enter yes or no for this query [y/n]: ') == 'y'
    # return False

# Boolean: are all POST flows using https?
def uses_https(flows: list[HTTPFlow]):
    flows = filter_flows_method(flows, ['POST'])
    for flow in flows:
        if 'https' != flow.request.scheme:
            return False
    return True

# Returns a list of flows with unique urls
def unique_urls(flows: list[HTTPFlow]):
    urls = []
    flows_new = []
    for flow in flows:
        if flow.request.url not in urls:
            flows_new.append(flow)
            urls.append(flow.request.url)
    return flows_new


buff = 70

# Conducts a terms search for general health data
def collects_health_data(flows: list[HTTPFlow]):
    print("\n" + colored("General Health Data", 'white', 'on_red'))
    return terms_search(flows, 'health', buff)

# Conducts a terms search for reproductive health data
def collects_reproductive_data(flows: list[HTTPFlow]):
    print("\n" + colored("Reproductive Health Data", 'white', 'on_red'))
    return terms_search(flows, 'reproductive', buff)

# Conducts a terms search for account deletion
def can_delete_account(flows: list[HTTPFlow]):
    print("\n" + colored("Account Deletion", 'white', 'on_red'))
    return terms_search(flows, 'delete', buff)

flows = unique_urls(flows)
# flows = filter_flows_method(flows, 'POST')

def report(flows: list[HTTPFlow]):
    encrypted_transit = uses_https(flows)
    can_delete = can_delete_account(flows)
    collects_health = collects_health_data(filter_flows_method(flows, ['POST']))
    collects_reproductive = collects_reproductive_data(filter_flows_method(flows, ['POST', 'GET']))

    print("\n" + colored("Packet Analysis Report", 'white', 'on_red'))
    print(highlight('Encrypted in transit: ') + str(encrypted_transit))
    print(highlight('Can delete account/history: ') + str(can_delete))
    print(highlight('Collects general health data: ') + str(collects_health))
    print(highlight('Collects reproductive health data: ') + str(collects_reproductive))

report(flows)

# print(flows[0].response.headers)