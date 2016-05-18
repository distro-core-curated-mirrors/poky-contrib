#
# BitBake ToasterUI Implementation
#
# Copyright (C) 2016        Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

os.environ["DJANGO_SETTINGS_MODULE"] = "toaster.toastermain.settings"

import sys
import os
import logging

import django
import requests
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser

from orm.models import Project

def _configure_paths():
    """ Add toaster to sys path for importing modules """
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'toaster'))
_configure_paths()

django.setup()

logger = logging.getLogger("ToasterLogger")

class ToasterApiClient(object):
    """
    Client for the Toaster database API
    """
    def __init__(self, endpoint='http://localhost:8000'):
        self.endpoint = endpoint
        self.json_parser = JSONParser()

        # HTTP headers to send when requesting JSON
        self.json_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def _get(self, view_name):
        url = "%s%s" % (self.endpoint, reverse(view_name))
        response = requests.get(url, headers=self.json_headers, stream=True)
        return response

    def _parse_response(self, response):
        """
        Parse response with JSON stream to Python dict

        response: must have been fetched with stream=True, so that it has a raw
        stream property

        returns a Python dict
        """
        return self.json_parser.parse(response.raw)

    def get_default_project(self):
        response = self._get('db_api:projects-default')
        data = self._parse_response(response)
        return Project(**data)