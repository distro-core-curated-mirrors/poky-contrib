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

from rest_framework import serializers, viewsets
from rest_framework.response import Response
from orm.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project

class DefaultProjectViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = None
        recipe = Project.objects.get_or_create_default_project()
        serializer = ProjectSerializer(recipe)
        return Response(serializer.data)