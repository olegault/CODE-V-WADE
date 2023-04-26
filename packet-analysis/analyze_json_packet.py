"""
Read a mitmproxy dump file.
"""
from mitmproxy.io import FlowReader
from mitmproxy.http import HTTPFlow
from colorama import Fore, Style, init
from termcolor import colored
from pathlib import Path
import os, sys, re, sqlite3, argparse

sys.path.append('../mysite/')

from appstoreresults.m3 import update_scores

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILEPATH = os.path.join(BASE_DIR, 'mysite/appstoreresults/db-final.db')
print(DB_FILEPATH)

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
    qs = {'pii':          {'filepath': './search_lists/pii.txt',
                           'question': ("Does this line contain " + highlight("PII") + '?')},
          'health':       {'filepath': './search_lists/health.txt',
                           'question': ("Does this line contain " + highlight("general health data") + '?')},
          'reproductive': {'filepath': './search_lists/reproductive.txt',
                           'question': ("Does this line contain " + highlight("reproductive health data") + '?')},
          'calendar':     {'filepath': './search_lists/period_calendar.txt',
                           'question': ("Does this line contain " + highlight("period calendar data") + '?')},
          'delete':       {'filepath': './search_lists/delete.txt',
                           'question': ("Does this line indicate " + highlight("account deletion") + "?")},
          'request':      {'filepath': './search_lists/request.txt',
                           'question': ("Does this line indicate " + highlight("a data request") + "?")},
          'controlData':  {'filepath': './search_lists/control_data.txt',
                           'question': ("Does this line indicate " + highlight("control over which data is collected") + "?")},
          'controlSharing':      {'filepath': './search_lists/control_sharing.txt',
                           'question': ("Does this line indicate " + highlight("control over who data is shared with") + "?")}
        }
    
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
                ch = input("[y/n/skip]: ")
                if ch == 'y':
                    return True
                if ch == 'skip':
                    return False
                print('\n')
                
        rq = str(flow.request.content).lower()
        for term in terms:
            res = [i.start() for i in re.finditer(term, rq)]
            for i in res:
                print(qs[query]['question'])
                print(highlight_term(rq[i-char_buff:i+char_buff], term))
                ch = input("[y/n/skip]: ")
                if ch == 'y':
                    return True
                if ch == 'skip':
                    return False
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
        try:
            if flow.request.url not in urls:
                flows_new.append(flow)
                urls.append(flow.request.url)
        except:
            pass
    return flows_new


buff = 70

# Conducts a terms search for general health data
def collects_pii(flows: list[HTTPFlow]):
    print("\n" + colored("Personal Identifying Information", 'white', 'on_red'))
    return terms_search(flows, 'pii', buff)

# Conducts a terms search for general health data
def collects_health_data(flows: list[HTTPFlow]):
    print("\n" + colored("General Health Data", 'white', 'on_red'))
    return terms_search(flows, 'health', buff)

# Conducts a terms search for reproductive health data
def collects_reproductive_data(flows: list[HTTPFlow]):
    print("\n" + colored("Reproductive Health Data", 'white', 'on_red'))
    terms_search(flows, 'reproductive', buff)

# Conducts a terms search for period calendar data
def collects_period_calendar(flows: list[HTTPFlow]):
    print("\n" + colored("Period Calendar Data", 'white', 'on_red'))
    terms_search(flows, 'calendar', buff)

# Conducts a terms search for account deletion
def can_delete_account(flows: list[HTTPFlow]):
    print("\n" + colored("Account Deletion", 'white', 'on_red'))
    return terms_search(flows, 'delete', buff)

# Conducts a terms search for account deletion
def can_request_data(flows: list[HTTPFlow]):
    print("\n" + colored("Data Request", 'white', 'on_red'))
    return terms_search(flows, 'request', buff)

# Conducts a terms search for account deletion
def can_control_data(flows: list[HTTPFlow]):
    print("\n" + colored("Control Data", 'white', 'on_red'))
    return terms_search(flows, 'controlData', buff)

# Conducts a terms search for account deletion
def can_control_sharing(flows: list[HTTPFlow]):
    print("\n" + colored("Control Sharing", 'white', 'on_red'))
    return terms_search(flows, 'controlSharing', buff)

# flows = filter_flows_method(flows, 'POST')

def report(flows: list[HTTPFlow]):
    encrypted_transit = uses_https(flows)
    can_delete = can_delete_account(flows)
    data_request = can_request_data(flows)
    control_data = can_control_data(flows)
    control_sharing = can_control_sharing(flows)
    collects_personal = collects_pii(flows)
    collects_health = collects_health_data(filter_flows_method(flows, ['POST']))
    collects_reproductive = collects_reproductive_data(filter_flows_method(flows, ['POST', 'GET']))
    collects_calendar = collects_period_calendar(filter_flows_method(flows, ['POST', 'GET']))

    print("\n" + colored("Packet Analysis Report", 'white', 'on_red'))
    print(highlight('Encrypted in transit: ') + str(encrypted_transit))
    print(highlight('Can delete account/history: ') + str(can_delete))
    print(highlight('Can request a copy of your data: ') + str(data_request))
    print(highlight('Can control which data is collected: ') + str(control_data))
    print(highlight('Can control who data is shared with: ') + str(control_sharing))
    print(highlight('Collects PII: ') + str(collects_personal))
    print(highlight('Collects general health data: ') + str(collects_health))
    print(highlight('Collects reproductive health data: ') + str(collects_reproductive))
    print(highlight('Collects period calendar data: ') + str(collects_calendar))

    metrics = {"collectPII": collects_pii,
               "collectHealthInfo": collects_health,
               "collectReproductiveInfo": collects_reproductive,
               "collectPeriodCalendarInfo": collects_calendar,
               "requestDeletion": can_delete,
               "requestData": data_request,
               "controlData": control_data,
               "controlSharing": control_sharing,
               "encryptedTransit": encrypted_transit}
    return metrics

def update_db_entry(package, metrics):
    sqliteConnection = sqlite3.connect(DB_FILEPATH)
    sqliteConnection.row_factory = sqlite3.Row
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    cursor = sqliteConnection.execute("SELECT * FROM 'App Matrix' WHERE appID = ?", (package,))
    res = cursor.fetchall()
    app_db = res[0]

    for metric in metrics:
        if metrics[metric]: val = 1
        else: val = 0

        print(metric, val, package)
        try:
            cursor = sqliteConnection.execute(f'''UPDATE 'App Matrix' SET {metric}=? WHERE UID = ?''', (val, app_db['UID']))
            sqliteConnection.commit()
        except BaseException as e:
            print(e)
    update_scores(app_db['appID'])
    return True



# manual_metrics = report(flows)
# update_db_entry(package_name, manual_metrics)

# print(flows[0].response.headers)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('package', type=str)
    # args = parser.parse_args()

    # package_name = args.package.strip()
    # filename = f"./app-flows/{package_name}/flows"

    # flows = []

    # init()

    # with open(filename, 'rb') as fp:
    #     reader = FlowReader(fp)

    #     for flow in reader.stream():
    #         if isinstance(flow, HTTPFlow):
    #             flows.append(flow)

    # flows = unique_urls(flows)

    manual_metrics = {"encryptedTransit": True}
    update_db_entry('org.iggymedia.periodtracker', manual_metrics)