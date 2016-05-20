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
import json

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

        # number of method calls
        self.method_calls = {}

        # model classes touched
        self.touched_models = []

    def _record_method_call(self, method_name, clazz=None):
        """
        Models can either be a single model or a list of models/dictionaries
        used to created models
        """
        if clazz:
            class_name = clazz.__name__
            if not class_name in self.touched_models:
                self.touched_models.append(class_name)

        if not method_name in self.method_calls:
            self.method_calls[method_name] = 0

        self.method_calls[method_name] += 1

    def _get(self, view_name, args=(), params={}):
        url = "%s%s" % (self.endpoint, reverse(view_name, args=args))

        # use stream=True so that the Django REST Framework JSON parser can
        # do its job on the response.raw property
        response = requests.get(url,
                                headers=self.json_headers,
                                params=params,
                                stream=True)
        return response

    def dump_stats(self):
        print('')
        print('************************** DATABASE ACCESS STATS')
        print('')
        print('Method calls:')
        print(json.dumps(self.method_calls, indent=2))
        print('')
        print('Model classes for create/bulk_create/get_or_create/filter:')
        print(json.dumps(self.touched_models, indent=2))
        print('')

    def get_default_project(self):
        self._record_method_call('get_or_create_default_project', Project)
        view_name = 'db_api:projects-default'
        response = self._get(view_name)
        data = self.json_parser.parse(response.raw)
        return Project(**data)

    def get_by_pk(self, clazz, pk):
        """
        Get an object of class clazz, using pk for lookup
        """
        self._record_method_call('get_by_pk', clazz)
        view_name = 'db_api:generic-detail'
        params = {'class_name': clazz.__name__}
        response = self._get(view_name, args=(pk,), params=params)
        objects = serializers.deserialize('json', response.json())
        obj = next(objects).object
        return obj

    # methods still to be converted
    def get_or_create(self, clazz, **kwargs):
        obj = clazz.objects.get_or_create(**kwargs)
        self._record_method_call('get_or_create', clazz)
        return obj

    def get(self, clazz, **kwargs):
        obj = clazz.objects.get(**kwargs)
        self._record_method_call('get')
        return obj

    def get_buildrequest_layers(self, buildrequest):
        layers = buildrequest.brlayer_set.all()
        self._record_method_call('get_buildrequest_layers')
        return layers

    def get_project_layers(self, buildrequest, buildrequest_layer):
        layers = buildrequest.project.projectlayer_set.filter(layercommit__layer__name=buildrequest_layer.name)
        self._record_method_call('get_project_layers')
        return layers

    def filter(self, clazz, **kwargs):
        self._record_method_call('filter', clazz)
        return clazz.objects.filter(**kwargs)

    def create(self, clazz, **kwargs):
        obj = clazz.objects.create(**kwargs)
        self._record_method_call('create', clazz)
        return obj

    def bulk_create(self, clazz, dicts):
        objs = clazz.objects.bulk_create(dicts)
        self._record_method_call('bulk_create', clazz)
        return objs

    def save(self, obj):
        self._record_method_call('save', obj.__class__)
        obj.save()
        return obj

    def remove_package_dependencies(self, package):
        self._record_method_call('remove_package_dependencies')
        package.package_dependencies_target.all().delete()
        package.package_dependencies_source.all().delete()