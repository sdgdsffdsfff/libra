# -*- coding:utf-8 -*-
from __future__ import absolute_import

import logging
import urllib2
import socket
from urllib2 import URLError, HTTPError

logging.basicConfig(
    level=logging.DEBUG,
)


class Urllib2Context(urllib2):
    RETRIES = 4

    def __init__(self, node_manager, placeholder='__node__'):
        self.node_manager = node_manager
        self.placeholder = placeholder

    def urlopen(self, url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                cafile=None, capath=None, cadefault=False, context=None):
        count = 0
        fp = None
        while count < self.RETRIES:
            count += 1
            node = self.node_manager.get_node()
            url_new = url.replace(self.placeholder, node)
            try:
                fp = urllib2.urlopen(
                    url_new, data=data, timeout=timeout,
                    cafile=cafile, capath=capath, cadefault=cadefault, context=context
                )
            except URLError:
                logging.error('LIBRA: dead node, %s', node)
                self.node_manager.dead_node(node)
                continue

            logging.debug('LIBRA: release node, %s', node)
            self.node_manager.release_node(node)
            return fp

        return fp
