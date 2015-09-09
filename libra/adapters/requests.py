# -*- coding:utf-8 -*-

from __future__ import absolute_import

import logging
import requests


LOGGER = logging.getLogger(__name__)


class CreateContext(object):
    """
    :type node_manager: WeightNodes
    """
    RETRY = 3

    def __init__(self, node_manager=None, placeholder='__node__'):
        self.node_manager = node_manager
        self.placeholder = placeholder

    def get(self, url, parameters=None, **kwargs):
        response = requests.get(url, params=parameters, **kwargs)

        if response.status_code == 200:
            return response

        node = self.placeholder
        LOGGER.error('LIBRA: dead node, %s', node)
        self.node_manager.dead_node(node)

        # 如果请求默认服务器失败就向其他服务器请求，最多进行三次
        count = 0
        while count < self.RETRY:
            node = self.node_manager.get_node()
            response = requests.get(
                url.replace(self.placeholder, node), params=parameters, **kwargs
            )
            count += 1
            if response.status_code == 200:
                LOGGER.debug('LIBRA: release node, %s', node)
                self.node_manager.release_node(node)
                return response
            else:
                LOGGER.error('LIBRA: dead node, %s', node)
                self.node_manager.dead_node(node)

        return response
