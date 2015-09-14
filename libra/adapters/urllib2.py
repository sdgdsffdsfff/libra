# -*- coding:utf-8 -*-
from __future__ import absolute_import

import urllib2
import socket
from urllib2 import URLError

from ..tools import auto_switch


class Urllib2Context(object):
    RETRIES = 3
    from urllib2 import URLError

    def __init__(self, node_manager, placeholder='__node__'):
        self.node_manager = node_manager
        self.placeholder = placeholder
        self.error = URLError

    @auto_switch
    def urlopen(self, url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                cafile=None, capath=None, cadefault=False, context=None):
        return urllib2.urlopen(
            url, data=data, timeout=timeout, cafile=cafile,
            capath=capath, cadefault=cadefault, context=context
        )
