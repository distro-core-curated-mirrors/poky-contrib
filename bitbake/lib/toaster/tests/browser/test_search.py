#! /usr/bin/env python
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# BitBake Toaster Implementation
#
# Copyright (C) 2013-2016 Intel Corporation
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

from django.core.urlresolvers import reverse
from tests.browser.selenium_helpers import SeleniumTestCase, Wait

from orm.models import BitbakeVersion, Release, Project, Layer, Layer_Version
from orm.models import ProjectLayer

class TestSearch(SeleniumTestCase):
    def setUp(self):
        """ Create a project with layers so we can search its layers page """
        bitbake_version = BitbakeVersion.objects.create(name='bb1')

        release = Release.objects.create(
            name='v1',
            bitbake_version=bitbake_version
        )

        self.project = Project.objects.create(name='foo', release=release)

        layer1 = Layer.objects.create(name='layer_bar')
        layer2 = Layer.objects.create(name='layer_moo')
        layer3 = Layer.objects.create(name='layer_moo2')

        layer_version1 = Layer_Version.objects.create(
          layer=layer1,
          project=self.project
        )
        layer_version2 = Layer_Version.objects.create(
          layer=layer2,
          project=self.project
        )
        layer_version3 = Layer_Version.objects.create(
          layer=layer3,
          project=self.project
        )

        project_layer1 = ProjectLayer.objects.create(
          project=self.project,
          layercommit=layer_version1
        )
        project_layer2 = ProjectLayer.objects.create(
          project=self.project,
          layercommit=layer_version2
        )
        project_layer3 = ProjectLayer.objects.create(
          project=self.project,
          layercommit=layer_version3
        )

    def _get_last_layer_name_cell_id(self):
        """
        Get the Selenium ID of the last layer name cell in the table
        """
        cells = self.find_all('td.layer__name')
        last_cell = cells[-1]
        return last_cell.id

    def test_search_clear(self):
        """
        Show the layers page for the project, do a search, then clear it
        """
        url = reverse('projectlayers', args=(self.project.id,))
        self.get(url)

        search_box = self.find('#search-input-layerstable')
        search_box.clear()
        search_box.send_keys('moo')

        self.click('#search-submit-layerstable')

        selector = '#table-container-layerstable .remove-search-btn-layerstable'
        self.wait_until_visible(selector)

        # get the Selenium ID of the current last td element in the layer name
        # column; this will enable us to wait for the table to redraw, as its
        # ID will change on the redraw
        current_element_id = self._get_last_layer_name_cell_id()

        # click "layer" heading to sort by layer name
        selector = '#layerstable th.layer__name a'
        element = self.wait_until_visible(selector)
        element.click()

        selector = '#layerstable th.layer__name i.icon-caret-up'
        icon = self.wait_until_visible(selector)

        # when the table is sorted, the last layer name table cell is
        # redrawn, which changes its ID; wait for that to happen
        has_changed = lambda driver: \
            self._get_last_layer_name_cell_id() != current_element_id
        Wait(self.driver).until(has_changed)
