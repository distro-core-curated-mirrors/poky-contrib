import requests
import logging
from utils import get_branch

logger = logging.getLogger('patchtest')

class MboxItem(object):
    """ mbox item containing all data extracted from an mbox, and methods
        to extract this data. This base class and should be inherited
        from, not directly instantiated.
    """
    MERGE_STATUS_INVALID = 'INVALID'
    MERGE_STATUS_NOT_MERGED = 'NOTMERGED'
    MERGE_STATUS_MERGED_SUCCESSFULL = 'PASS'
    MERGE_STATUS_MERGED_FAIL = 'FAIL'
    MERGE_STATUS = (MERGE_STATUS_INVALID,
                    MERGE_STATUS_NOT_MERGED,
                    MERGE_STATUS_MERGED_SUCCESSFULL,
                    MERGE_STATUS_MERGED_FAIL)

    def __init__(self, resource, args=None, forcereload=False):
        self._resource = resource
        self._args = args
        self._forcereload = forcereload

        self._contents = ''
        self._status = MboxItem.MERGE_STATUS_NOT_MERGED

    @property
    def contents(self):
        raise(NotImplementedError, 'Please do not instantiate MboxItem')

    @property
    def is_empty(self):
        return not(self.contents.strip())

    def getresource(self):
        resource = self._resource
        if self._args:
            resource %= self._args
        return resource
    def setresource(self, resouce):
        self._resource = resource
    resource = property(getresource, setresource)

    def getargs(self):
        return self._args
    def setargs(self, args):
        self._args = args
    args = property(getargs, setargs)

    def getstatus(self):
        return self._status
    def setstatus(self, status):
        if not status in MboxItem.MERGE_STATUS:
            logger.warn('Status (%s) not valid' % status)
        else:
            self._status = status
    status = property(getstatus, setstatus)

    def getbranch(self):
        return get_branch(self.contents)

class MboxURLItem(MboxItem):
    """ Mbox item based on a URL"""

    @property
    def contents(self):
        if self._forcereload or (not self._contents):
            logger.debug('Reading %s contents' % self.resource)
            try:
                _r = requests.get(self.resource)
                self._contents = _r.text
            except requests.RequestException:
                logger.warn("Request to %s failed" % self.resource)
        return self._contents

class MboxFileItem(MboxItem):
    """ Mbox item based on a file"""

    @property
    def contents(self):
        if self._forcereload or (not self._contents):
            logger.debug('Reading %s contents' % self.resource)
            try:
                with open(self.resource) as _f:
                    self._contents = _f.read()
            except IOError:
                logger.warn("Reading the mbox %s failed" % self.resource)
        return self._contents

