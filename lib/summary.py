import os
import utils
from tabulate import tabulate
from jinja2 import Template

class BaseSummary(object):
    FAIL = 'FAIL'
    SUCCESS = 'PASS'
    SKIP = 'SKIP'

    def __init__(self, project='', mailinglist=''):
        self._project = project
        self._mailinglist = mailinglist

        self._results = list()

    def addFailure(self, test):
        self._results.append((self.FAIL, test))

    def addSuccess(self, test):
        self._results.append((self.SUCCESS, test))

    def addSkip(self, test):
        self._results.append((self.SKIP, test))

    def generate(self, items):
        raise Exception

class TabulateSummary(BaseSummary):
    merge_header = ['Merge Status', 'Item']
    result_header = ['Result', 'Test Description']
    tablefmt = 'simple'

    def generate(self, items):
        text = str()
        merge_results = [[item.status, item.resource] for item in items]
        if merge_results:
            text += "\n\n%s\n" % tabulate(merge_results, self.merge_header, tablefmt=self.tablefmt)

        test_results = [(result, test.shortDescription()) for result, test in self._results]
        if test_results:
            text += "\n\n%s\n" % tabulate(test_results, self.result_header, tablefmt=self.tablefmt)

        return text


class TemplateSummary(BaseSummary):

    # TODO: the template should be located in a separate file
    template = """
Thanks for your patch submission {% if resource %} of {{ resource }} {% endif %}to {{ project }} - this is an automated response. The results of some tests on the patch(es) are as follows:

{% for result, description in testresults %}
    {{ result }} {{ description }}
{% endfor %}

If you believe any of these test results are incorrect, please reply to the mailing list ({{ mailinglist }}) raising your concerns. Otherwise we
would appreciate you correcting the issues and submitting a new version of the patchset if applicable. Please ensure you add/increment the version number
when sending the new version (i.e. [PATCH] -> [PATCH v2] -> [PATCH v3] -> ...).
"""

    def generate(self, items):
        resource = None
        testresults = [(result, test.shortDescription()) for result, test in self._results]
        try:
            item = items[0]
            resource = item.resource
        except:
            pass

        return Template(self.template).render(project=self._project,
                                              mailinglist=self._mailinglist,
                                              resource=resource,
                                              testresults=testresults)
