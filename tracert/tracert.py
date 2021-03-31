import os
import re
import sys

import requests
from functional import seq

keys: list[str] = 'query|country|isp|as|asname'.split('|')


def traceroute(path: str) -> None:
    os.system(f"traceroute {path} > trace.txt")  # посылаем в систему команду, которая все записывает в файл trace.txt
    print('number', *keys, sep=' | ')
    with open("trace.txt", "r") as trace_file:
        (seq(trace_file.readlines()[2:])
         .map(lambda s: re.search(r"\([\d.]*\)", s))  # находим все IP-шники в каждой строке
         .filter(lambda s: s is not None)  # избавляемся от пустых строк
         .map(lambda s: requests.get(
            f'http://ip-api.com/json/{s.group()[1:-1]}?fields=4255743').json())  # идем в АПИшку за информацией об IP-адресе
         .filter(lambda s: s['status'] != 'fail')  # Берем только удавшиеся запросы, т.е. по "белым" IP
         .zip_with_index()  # для вывода номера
         .map(lambda tup: print(tup[1], *[tup[0][i] for i in keys],
                                sep=' | '))  # выводим все поля по ключам, указанным в keys
         .to_list())  # вызываем все, что мы сделали


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print(
                """Usage: 
    python tracert.py <domain name/ip adress>
                """)
        else:
            traceroute(sys.argv[1])
