from base import ToasterFunctionalTests

class ToasterProjectDetailPage(ToasterFunctionalTests):
    def test_project_detail_page(self):
        rc = self.driver.get(self._url)
        self.assertNotEqual(rc, None, "Selenium driver get {0} returns None".format(self._url))
