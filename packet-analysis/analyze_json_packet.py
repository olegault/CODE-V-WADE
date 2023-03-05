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

def highlight(term):
    return  f"{Fore.RED}{term}{Style.RESET_ALL}"

def highlight_term(s, term):
    l = len(term)
    i = s.find(term)
    high = f"{s[:i]}{Fore.RED}{s[i:i+l]}{Style.RESET_ALL}{s[i+l:]}"
    return(high)

def terms_search(flows: list[HTTPFlow], query: str, char_buff: int):
    qs = {'reproductive': {'filepath': './search_lists/reproductive.txt',
                           'question': ("Does this line contain " + highlight("reproductive health data") + '?')},
          'delete':       {'filepath': './search_lists/delete.txt',
                           'question': ("Does this line indicate " + highlight("account deletion") + "?")}}
    
    terms = []
    with open(qs[query]['filepath'], 'r') as f:
        terms = [line.rstrip('\n') for line in f]
    
    for flow in flows:
        rsp = str(flow.response.content).lower()
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
    return False

def uses_https(flows: list[HTTPFlow]):
    for flow in flows:
        if 'https' != flow.request.scheme:
            return False
    return True


def unique_urls(flows: list[HTTPFlow]):
    urls = []
    flows_new = []
    for flow in flows:
        if flow.request.url not in urls:
            flows_new.append(flow)
            urls.append(flow.request.url)
    return flows_new

def collects_reproductive_data(flows: list[HTTPFlow]):
    print("\n" + colored("Reproductive Health Data", 'white', 'on_red'))
    return terms_search(flows, 'reproductive', 50)

def can_delete_account(flows: list[HTTPFlow]):
    print("\n" + colored("Account Deletion", 'white', 'on_red'))
    return terms_search(flows, 'delete', 50)

flows = unique_urls(flows)


def report(flows: list[HTTPFlow]):
    encrypted_transit = uses_https(flows)
    can_delete = can_delete_account(flows)
    collects_reproductive = collects_reproductive_data(flows)

    print("\n" + colored("Packet Analysis Report", 'white', 'on_red'))
    print(highlight('Encrypted in transit: ') + str(encrypted_transit))
    print(highlight('Can delete account/history: ') + str(can_delete))
    print(highlight('Collects reproductive health data: ') + str(collects_reproductive))

report(flows)