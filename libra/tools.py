# -*- coding:utf-8 -*-
import sys
import logging

logging.basicConfig(
    level=logging.DEBUG,
)


def auto_switch(func):
    def wrapper(self, url, *args, **kwargs):
        count = 0
        while count < self.RETRIES:
            node = self.node_manager.get_node()
            url_new = url.replace(self.placeholder, node)
            try:
                count += 1
                response = func(self, url_new, *args, **kwargs)
            except self.error:
                logging.error('LIBRA: dead node, %s', node)
                self.node_manager.dead_node(node)
                exc_info = sys.exc_info()
                continue
            except Exception as err:
                logging.debug('LIBRA: release node, %s', node)
                self.node_manager.release_node(node)
                raise err
            else:
                logging.debug('LIBRA: release node, %s', node)
                self.node_manager.release_node(node)
                return response
        raise exc_info[0], exc_info[1], exc_info[2]
    return wrapper
