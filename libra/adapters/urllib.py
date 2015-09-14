# -*- coding:utf-8 -*-
from __future__ import absolute_import

import urllib

from ..tools import auto_switch


class UrllibContext(object):
    RETRIES = 3

    def __init__(self, node_manager, placeholder='__node__'):
        self.node_manager = node_manager
        self.placeholder = placeholder
        self.error = IOError

    @auto_switch
    def urlopen(self, url, data=None, proxies=None, context=None):
        return urllib.urlopen(url, data=data, proxies=proxies, context=context)
