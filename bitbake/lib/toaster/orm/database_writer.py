#
# Toaster database access
#
# Copyright (C) 2013-2016        Intel Corporation
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

import collections
import logging
logger = logging.getLogger("ToasterLogger")

from orm.models import Project

class DatabaseWriter(object):
    """
    Object which abstracts database writes so that they are not done
    directly on Django models.

    The purpose of this is to allow database write actions to be queued,
    preventing multiple concurrent writes against the database.
    """

    def __init__(self):
        self.method_calls = {}

    def record_method_call(self, method_call, data=None):
        if not method_call in self.method_calls:
            self.method_calls[method_call] = 0
        if data and isinstance(data, collections.Iterable):
            self.method_calls[method_call] += len(data)
        else:
            self.method_calls[method_call] += 1

    def get_or_create_default_project(self):
        """
        Get or create the default Project model instance
        """
        logger.info('DATABASE WRITER: get_or_create_default_project()')
        self.record_method_call('get_or_create_default_project')
        return Project.objects.get_or_create_default_project()

    def save_object(self, obj):
        """
        Call save() on the Django Model object obj
        """
        logger.info('DATABASE WRITER: save_object(); class: %s' % obj.__class__.__name__)
        self.record_method_call('save_object')
        method_to_call = getattr(obj, 'save')
        return method_to_call()

    def bulk_create(self, clazz, data):
        """
        Call bulk_create() on the Django Model class clazz, passing data
        (list of model instances)
        """
        logger.info('DATABASE WRITER: bulk_create(); class: %s' % clazz.__name__)
        self.record_method_call('bulk_create', data)
        return clazz.objects.bulk_create(data)