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

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

from orm.models import Project
from toastergui.db_api_serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    @list_route()
    def default(self, request):
        """
        Return the default (cli builds) project;
        accessible at /toastergui/db_api/projects/default/
        """
        project = Project.objects.get_or_create_default_project()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)