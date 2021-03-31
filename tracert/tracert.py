import os
import re
import sys

import requests
from functional import seq

keys: list[str] = 'query|country|isp|as|asname'.split('|')


def traceroute(path: str) -> None:
    os.system(f"traceroute {path} > trace.txt")
    print('number', *keys, sep=' | ')
    with open("trace.txt", "r") as trace_file:
        (seq(trace_file.readlines()[2:])
         .map(lambda s: re.search(r"\([\d.]*\)", s))
         .filter(lambda s: s is not None)
         .map(lambda s: requests.get(f'http://ip-api.com/json/{s.group()[1:-1]}?fields=4255743').json())
         .filter(lambda s: s['status'] != 'fail')
         .zip_with_index()
         .map(lambda tup: print(tup[1], *[tup[0][i] for i in keys], sep=' | '))
         .to_list())


if __name__ == '__main__':
    traceroute(sys.argv[1])
