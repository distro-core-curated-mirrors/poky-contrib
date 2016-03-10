import os
import utils
from tabulate import tabulate
from jinja2 import Template

class BaseSummary(object):
    FAIL = 'FAIL'
    SUCCESS = 'PASS'
    SKIP = 'SKIP'

    def __init__(self, project='', mailinglist='', branchname='', commit=''):
        self._project = project
        self._mailinglist = mailinglist
        self._branchname = branchname
        self._commit = commit

        self._results = list()

    def addFailure(self, test):
        self._results.append((self.FAIL, test))

    def addSuccess(self, test):
        self._results.append((self.SUCCESS, test))

    def addSkip(self, test):
        self._results.append((self.SKIP, test))

    def generate(self, items, mergefailure=False):
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
    testtemplate = """Displaying test summary:

----------------------------------------------------------------------

Thank you for your patch submission {% if resource %}of:

  {{ resource }}

{% endif %}to {{ project }} - this is an automated {% if not resource %}
{% endif %}response. {% if resource %}
{% endif %}Results of some tests on the patch(es) are as follows:

{% if testresults %}  Result Description
  ------ -------------------------------------------------------------
{% for result, description in testresults %}   {{ result }}  {{ description }}
{% endfor %}
----------------------------------------------------------------------

{% endif %}If you believe any of these test results are incorrect, please reply
to the mailing list ({{ mailinglist }}) raising
your concerns. Otherwise we would appreciate you correcting the issues
and submitting a new version of the patchset if applicable. Please
ensure you add/increment the version number when sending the new
version (i.e. [PATCH] -> [PATCH v2] -> [PATCH v3] -> ...).
"""
    mergefailuretemplate = """
Thanks for your patch submission to {{ project }} - this is an automated
response. Unfortunately your patch series does not apply cleanly to the
{{ branchname }} branch (currently revision {{ commit }}). Please rebase it on the tip
of the {{ branchname }} branch, resolve any conflicts and resubmit a new version.

Please ensure you add/increment the version number
when sending the new version (i.e. [PATCH] -> [PATCH v2] -> [PATCH v3] ->
...).
"""

    def generate(self, items, mergefailure=False):
        content = ''
        if mergefailure:
            content = Template(self.mergefailuretemplate).render(project=self._project,
                                                              branchname=self._branchname,
                                                              commit=self._commit)
        else:
            resource = None
            testresults = [(result, test.shortDescription()) for result, test in self._results]
            try:
                item = items[0]
                resource = item.pretty_resource
                raise AssertionError(item.resource)
                print item.pretty_resource
            except:
                pass

            content = Template(self.testtemplate).render(project=self._project,
                                                         mailinglist=self._mailinglist,
                                                         resource=resource,
                                                         testresults=testresults)
        return content
