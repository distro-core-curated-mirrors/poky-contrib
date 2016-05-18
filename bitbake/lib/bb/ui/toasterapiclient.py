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

import sys
import os
import logging

import django
import requests
from django.core import serializers
from django.core.urlresolvers import reverse
from rest_framework.parsers import JSONParser

def _configure_paths():
    """ Add toaster to sys path for importing modules """
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'toaster'))
_configure_paths()

os.environ["DJANGO_SETTINGS_MODULE"] = "toaster.toastermain.settings"
django.setup()

from orm.models import Project

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

    def _get(self, view_name, args=(), params={}):
        url = "%s%s" % (self.endpoint, reverse(view_name, args=args))

        # use stream=True so that the Django REST Framework JSON parser can
        # do its job on the response.raw property
        response = requests.get(url,
                                headers=self.json_headers,
                                params=params,
                                stream=True)
        return response

    def get_default_project(self):
        view_name = 'db_api:projects-default'
        response = self._get(view_name)
        data = self.json_parser.parse(response.raw)
        return Project(**data)

    def get_by_pk(self, clazz, pk):
        """
        Get an object of class clazz, using pk for lookup
        """
        view_name = 'db_api:generic-detail'
        params = {'class_name': clazz.__name__}
        response = self._get(view_name, args=(pk,), params=params)
        objects = serializers.deserialize('json', response.json())
        obj = next(objects).object
        return obj