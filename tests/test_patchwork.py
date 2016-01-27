import unittest
import requests
from patchtestargs import PatchTestArgs as pta
from repo import Repo

@unittest.skipUnless(pta.series, "requires the series argument")
class TestPatchwork(unittest.TestCase):
    def setUp(self):
        self.repo = Repo(pta.repodir)
        self.fullurl = "%s/api/1.0/" % self.repo.url

    def test_instance_alive(self):
        """ Check if patchwork instance is alive """
        response = requests.get(self.fullurl)
        self.assertEqual(response.status_code, 200, "patchwork instance is not alive")

    def test_project_existance(self):
        """ Test if project exist on the patchwork instance """
        projecturl = "%sprojects/%s/" % (self.fullurl, self.repo.project)
        response = requests.get(projecturl)
        self.assertEqual(response.status_code, 200, "patchwork project (%s) does not exist" % projecturl)

    def test_series_existance(self):
        """ Test if series exist on the patchwork instance """
        seriesurl = "%sseries/%s" % (self.fullurl, pta.series)
        response = requests.get(seriesurl)
        self.assertEqual(response.status_code, 200, "patchwork series (%s) does not exist" % seriesurl)

    @unittest.skipUnless(pta.revision, "requires the revision argument")
    def test_revision_existance(self):
        """ Test if series/revision exist on the patchwork instance """
        revisionurl = "%sseries/%s/revisions/%s/" % (self.fullurl, pta.series, pta.revision)
        response = requests.get(revisionurl)
        self.assertEqual(response.status_code, 200, "patchwork revision (%s) does not exist" % revisionurl)

