# -*- coding:utf-8 -*-
from __future__ import absolute_import

import logging
import urllib

logging.basicConfig(
    level=logging.DEBUG,
)


class CreateContext(object):
    RETRIES = 4

    def __init__(self, node_manager, placeholder='__node__'):
        self.node_manager = node_manager
        self.placeholder = placeholder

    def urlopen(self, url, data=None, proxies=None, context=None):
        count = 0
        fp = None
        while count < self.RETRIES:
            count += 1
            node = self.node_manager.get_node()
            url_new = url.replace(self.placeholder, node)
            try:
                fp = urllib.urlopen(url_new, data=data, proxies=proxies, context=context)
            except:
                logging.error('LIBRA: dead node, %s', node)
                self.node_manager.dead_node(node)
                continue

            logging.debug('LIBRA: release node, %s', node)
            self.node_manager.release_node(node)
            return fp

        return fp
