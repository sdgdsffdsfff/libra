# -*- coding:utf-8 -*-
from __future__ import absolute_import

import logging
import requests
from requests.exceptions import ConnectionError

logging.basicConfig(
    level=logging.DEBUG,
)


class CreateContext(object):
    """
    :type node_manager: WeightNodes
    """
    RETRIES = 4

    def __init__(self, node_manager=None, placeholder='__node__'):
        self.node_manager = node_manager
        self.placeholder = placeholder

    def get(self, url, parameters=None, **kwargs):
        # 如果请求默认服务器失败就向其他服务器请求，重请求最多三次
        count = 0
        response = None
        while count < self.RETRIES:
            node = self.node_manager.get_node()
            url_new = url.replace(self.placeholder, node)
            try:
                response = requests.get(url_new, params=parameters, **kwargs)
            except ConnectionError:
                logging.error('LIBRA: dead node, %s', node)
                self.node_manager.dead_node(node)
                continue

            count += 1
            logging.debug('LIBRA: release node, %s', node)
            self.node_manager.release_node(node)
            return response

        return response

    def post(self, url, data=None, json=None, **kwargs):
        count = 0
        response = None
        while count < self.RETRIES:
            node = self.node_manager.get_node()
            url_new = url.replace(self.placeholder, node)
            try:
                response = requests.post(url_new, data=data, json=json, **kwargs)
            except ConnectionError:
                logging.error('LIBRA: dead node, %s', node)
                self.node_manager.dead_node(node)
                continue

            count += 1
            logging.debug('LIBRA: release node, %s', node)
            self.node_manager.release_node(node)
            return response

        return response
