# -*- coding:utf-8 -*-
import sys
import logging

from urllib2 import URLError
from requests.exceptions import ConnectionError

logging.basicConfig(
    level=logging.DEBUG,
)


class CreateContext(object):
    def __init__(self, node_manager, placeholder='__node__'):
        self.node_manager = node_manager
        self.placeholder = placeholder
        self.error = (ConnectionError, URLError, ValueError)


def auto_switch(func):
    def wrapper(self, url, *args, **kwargs):
        count = 0
        while count < self.RETRIES:
            node = self.context.node_manager.get_node()
            url_new = url.replace(self.context.placeholder, node)
            try:
                count += 1
                response = func(self, url_new, *args, **kwargs)
            except self.context.error:
                logging.error('LIBRA: dead node, %s', node)
                self.context.node_manager.dead_node(node)
                exc_info = sys.exc_info()
                continue
            except Exception:
                logging.debug('LIBRA: release node, %s', node)
                self.context.node_manager.release_node(node)
                raise
            else:
                logging.debug('LIBRA: release node, %s', node)
                self.context.node_manager.release_node(node)
                return response
        raise exc_info[0], exc_info[1], exc_info[2]
    return wrapper
