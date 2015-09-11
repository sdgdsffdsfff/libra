# -*- coding:utf-8 -*-
__author__ = 'ty'
import time

from libra.adapters.urllib2 import CreateContext as c1
from libra.adapters.urllib import CreateContext as c2
from libra.adapters.requests import CreateContext as c3
from libra.manager import WeightNodes


if __name__ == '__main__':
    weight_table = {
        'http://www.sohu.com': 20,
        'http://www.baidu.com': 20,
        'http://www.google.com': 10,
        'http://www.facebook.com': 10,
        'http://www.youtube.com': 10,
    }
    node_manager = WeightNodes(weight_table, 100)
    urllib2 = c1(node_manager, 'whatever')
    urllib = c2(node_manager, 'whatever')
    requests = c3(node_manager, 'whatever')
    url = 'whatever'
    start = time.time()
    resp1 = urllib2.urlopen(url)
    resp2 = urllib.urlopen(url)
    resp3 = requests.get(url)
    end = time.time()
    print 'total cost: ', end - start
    print 'urllib2:', resp1.geturl()
    print 'urllib: ', resp2.geturl()
    print 'requests.get: ', resp3.url

