import unittest
import requests
from patchtestdata import PatchTestInput as pti

@unittest.skipUnless(pti.series, "requires the series argument")
class TestPatchwork(unittest.TestCase):
    def setUp(self):
        self.repo = pti.repo
        self.fullurl = "%s/api/1.0/" % self.repo.url

    def test_instance_alive(self):
        """ Check if patchwork instance is alive """
        response = requests.get(self.fullurl)
        self.assertEqual(response.status_code, 200, "patchwork instance is not alive")

    def test_project_existence(self):
        """ Test if project exist on the patchwork instance """
        projecturl = "%sprojects/%s/" % (self.fullurl, self.repo.project)
        response = requests.get(projecturl)
        self.assertEqual(response.status_code, 200, "patchwork project (%s) does not exist" % projecturl)

    def test_series_existence(self):
        """ Test if series exist on the patchwork instance """
        for series in pti.series:
            seriesurl = "%sseries/%s" % (self.fullurl, series)
            response = requests.get(seriesurl)
            self.assertEqual(response.status_code, 200, "patchwork series (%s) does not exist" % seriesurl)

    @unittest.skipUnless(pti.series and pti.revision, "requires the revision argument")
    def test_revision_existence(self):
        """ Test if series/revision exist on the patchwork instance """
        for series, revision in zip(pti.series, pti.revision):
            revisionurl = "%sseries/%s/revisions/%s/" % (self.fullurl, series, revision)
            response = requests.get(revisionurl)
            self.assertEqual(response.status_code, 200, "patchwork revision (%s) does not exist" % revisionurl)

