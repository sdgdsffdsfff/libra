# -*- coding:utf-8 -*-
from __future__ import absolute_import

import requests
from requests.exceptions import ConnectionError

from ..tools import auto_switch


class RequestsContext(object):
    """
    :type node_manager: WeightNodes
    """
    RETRIES = 3
    from requests.exceptions import ConnectionError

    def __init__(self, context):
        self.context = context

    @auto_switch
    def get(self, url, parameters=None, **kwargs):
        return requests.get(url, params=parameters, **kwargs)

    @auto_switch
    def post(self, url, data=None, json=None, **kwargs):
        return requests.post(url, data=data, json=json, **kwargs)
