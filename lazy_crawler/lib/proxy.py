import json
import pathlib
import random
import time
import urllib
import urllib.request


def get_proxy(n=1000):
    '''
    Fetches n number of proxies from lazy api and returns it into a usable 2D list for scrapy
    input:
        n (int) (optional): number of proxies to pull
    output:
        path of proxy file
    '''

    # creating a directory in /tmp for our proxy file to be stored
    if not (pathlib.Path('/tmp/vtx_scrapy_proxies').exists()):
        pathlib.Path('/tmp/vtx_scrapy_proxies').mkdir()
    url = '{}'.format(n)
    # reading the proxy list from the api
    proxys = urllib.request.urlopen(url).read()
    # converting to json/dict as the proxy list is  bytes type
    proxys = json.loads(proxys)
    # parsing proxy from json
    proxy_list = proxys['payload']
    proxy_list_parsed = []
    random.shuffle(proxy_list)
    for proxyObj in proxy_list:
        host = proxyObj['host']
        port = proxyObj['port']
        username = proxyObj['username']
        password = proxyObj['password']
        proxy_type = (proxyObj['type']).lower()
        proxy_list_parsed.append('{proxy_type}://{username}:{password}@{host}:{port}'.format(proxy_type=proxy_type,
                                                                                             username=username,
                                                                                             password=password,
                                                                                             host=host, port=port))

    # writing a temp file of current proxies
    file_name = '/tmp/vtx_scrapy_proxies/' + str(time.time()).replace('.', '') + str(len(proxy_list_parsed)) + \
                str(str(random.random()).replace('.', '')) + '.txt'

    with open(file_name, 'w') as proxyWrite:
        proxyWrite.write('\n'.join(proxy_list_parsed))
    return file_name


def get_proxy_manual(n: int = 1) -> list:
    '''
    Fetches n number of proxies from  api and returns it into a usable list
    input:
        n (int) (optional): number of proxies to pull
    output:
       list of proxy
    '''

    url = '{}'.format(
        1000)
    # reading the proxy list from the api
    proxys = urllib.request.urlopen(url).read()
    # converting to json/dict as the proxy list is  bytes type
    proxys = json.loads(proxys)
    # parsing proxy from json
    proxy_list = proxys['payload']
    random.shuffle(proxy_list)
    proxy_list_parsed = []

    for proxyObj in proxy_list:
        host = proxyObj['host']
        port = proxyObj['port']
        username = proxyObj['username']
        password = proxyObj['password']
        proxy_type = (proxyObj['type']).lower()
        proxy_list_parsed.append('{proxy_type}://{username}:{password}@{host}:{port}'.format(proxy_type=proxy_type,
                                                                                             username=username,
                                                                                             password=password,
                                                                                             host=host, port=port))

    # writing a temp file of current proxies

    return proxy_list_parsed[:n]


