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

from django.core import serializers
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import list_route

import orm.models
import bldcontrol.models
from orm.models import Project
from toastergui.db_api_serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for retrieving Project objects
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @list_route()
    def default(self, request):
        """
        Return the default (cli builds) project;
        accessible at /toastergui/db_api/projects/default/
        """
        project = Project.objects.get_or_create_default_project()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

class GenericModelViewSet(viewsets.ViewSet):
    """
    A generic ViewSet for retrieving a single or multiple Model objects
    """
    def retrieve(self, request, pk=None):
        pk = int(pk)
        class_name = request.query_params['class_name']

        try:
            clazz = getattr(orm.models, class_name)
        except AttributeError:
            clazz = getattr(bldcontrol.models, class_name)

        model = clazz.objects.get(pk=pk)
        serialized_model = serializers.serialize('json', [model])

        return Response(serialized_model)