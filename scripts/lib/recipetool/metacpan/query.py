import json
import logging
import re
import requests
import scriptutils
import string

DEBUG = False

logger = logging.getLogger('recipetool')

class MetaCPANQuery(object):

    def __init__(self):
        pass

class GetQuery(MetaCPANQuery):

    def __init__(self, params=None):
        self.params = params


class PostQuery(MetaCPANQuery):
    url = "https://fastapi.metacpan.org/v1/_search"

    def __init__(self,
                 url="https://fastapi.metacpan.org/v1/_search",
                 data=None):
        self.url = url
        self.data = data
        super(MetaCPANQuery, self).__init__()


class ReleaseQuery(PostQuery):
    url = 'https://fastapi.metacpan.org/v1/release/_search'

    def __init__(self,
                 url='https://fastapi.metacpan.org/v1/release/_search',
                 data=None, pn=None, pv=None, fields=[]):
        self.pn = pn
        self.pv = pv
        self.fields = fields
        self.release = { 'release': self.pn,
                         'version': self.pv }
        self.query = {"query": { 'match_all':{} }}
        self.query["fields"] = self.fields
        self.query["filter"] = { 'and': 
                     [{'term': {'distribution': '%s' % self.pn}},
                      {'term': {'version': '%s' % self.pv}}]}
        self.data = json.dumps(self.query)
        super(ReleaseQuery, self).__init__(url=url, data=self.data)
        self.url = url

    def _query(self):
        r = requests.post(url=self.url,data=self.data)
        if r.status_code == 200:
            return r
        else:
            logger.error( "ReleaseQuery => Response: %s" % r.status_code )
            return None


class PauseIdQuery(ReleaseQuery):

    def __init__(self, pn, pv):
        self.pn = pn
        self.pv = pv
        self.fields = ["author"]
        super(PauseIdQuery, self).__init__(self, pn=self.pn, pv=self.pv, fields=self.fields)
        self.url = ReleaseQuery.url
        self.pauseid = self._pauseid_query()

    def _pauseid_query(self):
        r = ReleaseQuery._query(self)
        #logger.debug("_pauseid_query: r.json(): %s " % r.json())
        #logger.debug("_pauseid_query: r.json().get('hits'): %s " % r.json().get('hits'))
        if r != None:
            self.pauseid = r.json().get('hits').get('hits')[0].get('fields').get('author')
            # TODO: add to file data : print( "PAUSEID:  %s" % result )
            return self.pauseid
        else:
            logger.error( "PauseIdQuery => Response: %s" % r.status_code )
            self.pauseid = None
            return self.pauseid


class AuthorQuery(PostQuery):

    def __init__(self,
                 url='https://fastapi.metacpan.org/v1/author/_search',
                 pauseid=''):
        self.url = url
        self.pauseid = pauseid
        self.query = {"query": { "match_all":{} }}
        self.query["fields"] = ["name"]
        self.query["filter"] = {"term": {"pauseid": "%s" % self.pauseid}}
        self.data = json.dumps(self.query)
        super(AuthorQuery, self).__init__(url=self.url, data=self.data)
        self.author = self._author_query()

    def _author_query(self):
        logger.debug("metacpan.query._author_query.query = %", self.data )
        r = requests.post(url=self.url,data=self.data)
        if r.status_code == 200:
            logger.debug("metacpan.query._author_query.r = %", r.json())
            self.author = r.json().get('hits').get('hits')[0].get('fields').get('name')
            # TODO: add to file data: print( "AUTHOR = \"%s\"" % result )
            return self.author
        else:
            logger.error( "AuthorQuery => Response: %s" % r.status_code )
            self.author = None
            return self.author

class AbstractQuery(ReleaseQuery):

    def __init__(self, pn, pv):
        self.pn = pn
        self.pv = pv
        self.fields = ["abstract"]
        super(AbstractQuery, self).__init__(self, pn=pn, pv=pv, fields=self.fields)
        self.url = ReleaseQuery.url
        self.abstract = self._abstract_query()

    def _abstract_query(self):
        r = ReleaseQuery._query(self)
        if r != None:
            self.abstract = r.json().get('hits').get('hits')[0].get('fields').get('abstract')
            return self.abstract
        else:
            logger.error( "AbstractQuery => Response: %s" % r.status_code )
            self.abstract = None
            return self.abstract


class HomepageQuery(ReleaseQuery):
    """
    {
      "query": {
          "match_all": {}
            },
          "size": 10,
          "fields": [ "distribution", "version", "resources.homepage" ],
          "filter": {
              "and": [
                 { "term": {"maturity": "released"} },
                 { "term": {"status": "latest"} },
                 {  "exists" : { "field" : "resources.homepage" } }
              ]
          }
    }
    """
    def __init__(self, pn, pv):
        logger.debug("HomepageQuery: __init__")
        self.pn = pn
        self.pv = pv
        self.fields = ["resources.homepage"]
        super(HomepageQuery, self).__init__(self, pn=pn, pv=pv, fields=self.fields)
        self.url = ReleaseQuery.url
        self.homepage = self._homepage_query()

    def _homepage_query(self):
        #logger.debug("HomepageQuery: _homepage_query")
        r = ReleaseQuery._query(self)
        #logger.debug("_homepage_query: r.json().get('hits').get('hits')[0]: %s" % r.json().get('hits').get('hits')[0])
        if r.json().get('hits').get('hits')[0].get('fields') != None:
            self.homepage = r.json().get('hits').get('hits')[0].get('fields').get('resources.homepage')
            return self.homepage
        else:
            if r.status_code == 200:
                logger.warn( "HomepageQuery: No 'homepage' in response")
            else:
                logger.error( "HomepageQuery => Response: %s" % r.status_code )
            self.homepage = None
            return self.homepage


class BugtrackerQuery(ReleaseQuery):

    def __init__(self, pn, pv):
        logger.debug("BugtrackerQuery: __init__")
        self.pn = pn
        self.pv = pv
        self.fields = ["resources.bugtracker.web"]
        super(BugtrackerQuery, self).__init__(self, pn=pn, pv=pv, fields=self.fields)
        self.url = ReleaseQuery.url
        self.bugtracker = self._bugtracker_query()

    def _bugtracker_query(self):
        #logger.debug("BugtrackerQuery: _bugtracker_query")
        r = ReleaseQuery._query(self)
        #logger.debug("_bugtracker_query: r.json().get('hits').get('hits')[0]: %s" % r.json().get('hits').get('hits')[0])
        if r.json().get('hits').get('hits')[0].get('fields') != None:
            self.bugtracker = r.json().get('hits').get('hits')[0].get('fields').get('resources.bugtracker.web')
            return self.bugtracker
        else:
            if r.status_code == 200:
                logger.warn( "BugtrackerQuery: No 'bugtracker' in response")
            else:
                logger.error( "BugtrackerQuery => Response: %s" % r.status_code )
            self.bugtracker = None
            return self.bugtracker


class LicenseQuery(ReleaseQuery):

    def __init__(self, pn, pv):
        self.pn = pn
        self.pv = pv
        self.fields = ["license"]
        super(LicenseQuery, self).__init__(self, pn=pn, pv=pv, fields=self.fields)
        self.url = ReleaseQuery.url
        self.license = self._license_query()

    def _license_query(self):
        r = ReleaseQuery._query(self)
        logger.debug("_license_query: r => %s" % len(r.json().get('hits').get('hits')))
        logger.debug("_license_query: r => %s" % len(r.json().get('hits').get('hits')[0]))
        if len(r.json().get('hits').get('hits')) > 0 and r.json().get('hits').get('hits')[0].get('fields') != None:
            raw_license = r.json().get('hits').get('hits')[0].get('fields').get('license')
            logger.debug("_license_query: raw_license => %s" % raw_license )
            if raw_license == 'perl_5':
                self.license = "Artistic-1.0 | GPL-1.0+"
            return self.license
        else:
            if r.status_code == 200:
                logger.warn( "LicenseQuery: No 'license' in response")
            else:
                logger.error( "LicenseQuery => Response: %s" % r.status_code )
            self.license = "Unknown"
            return self.license


class BuildDependsQuery(ReleaseQuery):

    def __init__(self, pn, pv):
        self.pn = pn
        self.pv = pv
        self.fields = ["prereqs.configure.requires"]
        super(BuildDependsQuery, self).__init__(self, pn=pn, pv=pv, fields=self.fields)
        self.url = ReleaseQuery.url
        self.build_depends = self._build_dependency_query()

    def _build_dependency_query(self):
        r = ReleaseQuery._query(self)
        logger.debug("_build_dependency_query: query => %s " % self.data)
        logger.debug("_build_dependency_query: r.json => %s " % r.json())
        if r.json().get('hits').get('hits')[0].get('fields') != None:
            logger.debug("_build_dependency_query: %s" %  r.json() )
            result = r.json().get('hits').get('hits')[0].get('fields').get('prereqs.configure.requires')
            mylist = list(result)
            deps = ' '.join([dep for dep in mylist if dep is not ''])
            inherit = 'inherit cpan'
            if u'ExtUtils::MakeMaker' in deps:
                inherit = 'inherit cpan'
                deps = re.sub(u'ExtUtils::MakeMaker', '', deps)
            elif u'Module::Build' in deps:
                inherit = 'inherit cpan_build'
                deps = re.sub(u'Module::Build', '', deps)
            else:
                logger.warn('Failed to interpret build engine defaulting to \"cpan\"')
                inherit = 'inherit cpan'
                deps = re.sub(u'ExtUtils::MakeMaker', '', deps)
            deps = deps.strip() # strip leading or trailing whitespace
            modules = deps.split()
            distribution = list()
            for module in modules:
                distribution.append(_module_to_distribution(module)['distribution'])
            if distribution:
                depends = ' '.join([dist for dist in distribution if dist is not ''])
                logger.warn("DEPENDS = \"%s\"" % depends)
                logger.warn( inherit )
                return result
        else:
            if r.status_code == 200:
                logger.warn( "BuildDependsQuery: No 'prereqs.configure.requires' in response")
            else:
                logger.error( "BuildDepndsQuery => Response: %s" % r.status_code )
            return None


class ModuleQuery(GetQuery):

    def __init__(self, module):
        self.module = module
        self.distribution = ''
        self.version = ''


# NOTE: must have exact distribution name and exact version to get only one hit
pn = "Moo"
pv = "2.002004"
#url = "https://fastapi.metacpan.org/v1/release/_search"


""" /module/<module> is a convenience GET URL """
def _module_to_distribution(module):
    module_url = "http://fastapi.metacpan.org/v1/module/%s" % module
    r = requests.get(url=module_url)
    if DEBUG: print( r.url )
    if r.status_code == 200:
        if DEBUG: print( r.json() )
        distribution = r.json().get('distribution')
        version = r.json().get('version')
        if DEBUG: print( "\"%s\" => \"%s\", \"%s\"" % ( module, distribution, version ))
        return { "distribution": distribution, "version": version }
    else:
        print( "Response: %s" % r.status_code )
        return None, None

""" /module/<module> is a convenience GET URL """
def _module_to_debian_naming(module):
    module_url = "http://fastapi.metacpan.org/v1/module/%s" % module
    r = requests.get(url=module_url)
    if DEBUG: print( r.url )
    if r.status_code == 200:
        if DEBUG: print( r.json() )
        name = r.json().get('path')
        if DEBUG: print( "\"%s\" => \"%s\"" % ( module, name ))
        name = re.sub('^lib/', 'lib', name)
        name = re.sub('\.pm$', '-perl', name)
        name = re.sub('/', '-', name)
        name = name.encode('utf-8').lower()
        return name
    else:
        print( "Response: %s" % r.status_code )
        return None

""" /module/<module> is a convenience GET URL """
def _distribution_to_debian_naming(module):
    module_url = "http://fastapi.metacpan.org/v1/module/%s" % module
    r = requests.get(url=module_url)
    if DEBUG: print( r.url )
    if r.status_code == 200:
        if DEBUG: print( r.json() )
        name = r.json().get('path')
        if DEBUG: print( "\"%s\" => \"%s\"" % ( module, name ))
        name = re.sub('^lib/', 'lib', name)
        name = re.sub('\.pm$', '-perl', name)
        name = re.sub('/', '-', name)
        return name
    else:
        print( "Response: %s" % r.status_code )
        return None

""" Returns 'abstract' which is what is known as 'SUMMARY' in OE """
def _abstract_query():
    query = json.dumps({'query': { 'match_all':{} }, 'fields': ['abstract'],  'filter': { 'and': [{'term': {'release.distribution': '%s' % pn}}, {'term': {'release.version': '%s' % pv}}]}})
    if DEBUG: print( query )
    r = requests.post(url=url,data=query)
    if r.status_code == 200:
        if DEBUG: print( r.json() )
        result = r.json().get('hits').get('hits')[0].get('fields').get('abstract')
        print( "SUMMARY = \"%s\"" % result)
        return result
    else:
        print( "Response: %s" % r.status_code )
        return None

""" This is not often populated """
def _homepage_query():
    query = json.dumps({'query': { 'match_all':{} }, 'fields': ['resources.homepage'],  'filter': { 'and': [{'term': {'release.distribution': '%s' % pn}}, {'term': {'release.version': '%s' % pv}}]}})
    if DEBUG: print( query )
    r = requests.post(url=url,data=query)
    if r.status_code == 200:
        if DEBUG: print( r.json() )
        try:
            result = r.json().get('hits').get('hits')[0].get('fields').get('resources.homepage')
        except:
            result = "https://metacpan.org/pod/%s" % pn
        print( "HOMEPAGE = \"%s\"" % result)
        return result
    else:
        print( "Response: %s" % r.status_code )
        return None

""" This query will return the license 'perl_5' """
def _license_query():
    query = json.dumps({'query': { 'match_all':{} }, 'fields': ['license'],  'filter': { 'and': [{'term': {'release.distribution': '%s' % pn}}, {'term': {'release.version': '%s' % pv}}]}})
    if DEBUG: print( query )
    r = requests.post(url=url,data=query)
    if r.status_code == 200:
        if DEBUG: print( r.json() )
        result = r.json().get('hits').get('hits')[0].get('fields').get('license')
        if result == 'perl_5': result = 'Artistic-1.0 | GPL-1.0+'
        print( "LICENSE = \"%s\"" % result)
        return result
    else:
        print( "Response: %s" % r.status_code )
        return None

def _pauseid_query(pn, pv):
    query = json.dumps({'query': { 'match_all':{} }, 'fields': ['author'],  'filter': { 'and': [{'term': {'release.distribution': '%s' % pn}}, {'term': {'release.version': '%s' % pv}}]}})
    logger.debug( query )
    r = requests.post(url=url,data=query)
    if r.status_code == 200:
        logger.debug( r.json() )
        result = r.json().get('hits').get('hits')[0].get('fields').get('author')
        print( "PAUSEID:  %s" % result )
        return result
    else:
        print( "Response: %s" % r.status_code )
        return None

def _author_query(pn, pv):
    author_url = "http://fastapi.metacpan.org/v1/author/_search"
    self.query = {'query': { 'match_all':{} }}
    self.query['fields'] = ['name']
    self.query['filter'] = { 'term': {'pauseid': '%s' % self.pauseid}}
    query = json.dumps(self.query)
    print( query )
    #logger.debug(print( query ))
    r = requests.post(url=author_url,data=query)
    if r.status_code == 200:
        #logger.debug(print( r.json() ))
        result = r.json().get('hits').get('hits')[0].get('fields').get('name')
        print( "AUTHOR = \"%s\"" % result )
        return result
    else:
        print( "Response: %s" % r.status_code )
        return None

def _build_dependency_query():
    query = json.dumps({'query': { 'match_all':{} }, 'fields': ['metadata.prereqs.configure.requires'],  'filter': { 'and': [{'term': {'release.distribution': '%s' % pn}}, {'term': {'release.version': '%s' % pv}}]}})
    if DEBUG: print( query )
    r = requests.post(url=url,data=query)
    if r.status_code == 200:
        if DEBUG: print( r.json() )
        result = r.json().get('hits').get('hits')[0].get('fields').get('metadata.prereqs.configure.requires')
        mylist = list(result)
        deps = ' '.join([dep for dep in mylist if dep is not ''])
        inherit = 'inherit cpan'
        if u'ExtUtils::MakeMaker' in deps:
            inherit = 'inherit cpan'
            deps = re.sub(u'ExtUtils::MakeMaker', '', deps)
        elif u'Module::Build' in deps:
            inherit = 'inherit cpan_build'
            deps = re.sub(u'Module::Build', '', deps)
        else:
            print( 'Failed to interpret build engine defaulting to \"cpan\"')
        deps = deps.strip() # strip leading or trailing whitespace
        modules = deps.split()
        distribution = list()
        for module in modules:
            distribution.append(_module_to_distribution(module)['distribution'])
        if distribution:
            depends = ' '.join([dist for dist in distribution if dist is not ''])
            print( "DEPENDS = \"%s\"" % depends )
        print( inherit )
        return result
    else:
        print( "Response: %s" % r.status_code )
        return None

def _runtime_dependency_query():
    query = json.dumps({'query': { 'match_all':{} }, 'fields': ['metadata.prereqs.runtime.requires'],  'filter': { 'and': [{'term': {'release.distribution': '%s' % pn}}, {'term': {'release.version': '%s' % pv}}]}})
    if DEBUG: print( query )
    r = requests.post(url=url,data=query)
    if r.status_code == 200:
        if DEBUG: print( r.json() )
        result = r.json().get('hits').get('hits')[0].get('fields').get('metadata.prereqs.runtime.requires')
        mylist = list(result)
        deps = ' '.join([dep for dep in mylist if dep is not ''])
        deps.strip()
        modules = deps.split()
        distribution = list()
        for module in modules:
            distribution.append(_module_to_distribution(module)['distribution'])
        if distribution:
            rdepends = ' '.join([dist for dist in distribution if dist is not ''])
            print( "RDEPENDS_${PN} = \"%s\"" % rdepends )
        return rdepends
    else:
        print( "Response: %s" % r.status_code )
        return None

def _test_dependency_query():
    query = json.dumps({'query': { 'match_all':{} }, 'fields': ['metadata.prereqs.test.requires'],  'filter': { 'and': [{'term': {'release.distribution': '%s' % pn}}, {'term': {'release.version': '%s' % pv}}]}})
    if DEBUG: print( query )
    r = requests.post(url=url,data=query)
    if r.status_code == 200:
        if DEBUG: print( r.json() )
        result = r.json().get('hits').get('hits')[0].get('fields').get('metadata.prereqs.test.requires')
        mylist = list(result)
        deps = ' '.join([dep for dep in mylist if dep is not ''])
        modules = deps.split()
        distribution = list()
        for module in modules:
            distribution.append(_module_to_distribution(module)['distribution'])
        if distribution:
            rdepends = ' '.join([dist for dist in distribution if dist is not ''])
            print( "RDEPENDS_${PN}-ptest = \"%s\"" % rdepends )
        return rdepends
    else:
        print( "Response: %s" % r.status_code )
        return None

def _provides_query():
    query = json.dumps({'query': { 'match_all':{} }, 'fields': ['provides'],  'filter': { 'and': [{'term': {'release.distribution': '%s' % pn}}, {'term': {'release.version': '%s' % pv}}]}})
    if DEBUG: print( query )
    r = requests.post(url=url,data=query)
    if r.status_code == 200:
        if DEBUG: print( r.json() )
        result = r.json().get('hits').get('hits')[0].get('fields').get('provides')
        mylist = list(result)
        # 'provides' which start with underscore are always internal only
        provides = ' '.join([provide for provide in mylist if provide is not ''  and not '::_' in provide])
        modules = provides.split()
        for module in modules:
            provides = ' '.join([_module_to_debian_naming( module ) for module in modules])
        print( "PROVIDES_${PN} =  \"%s\"" % provides )
        return result
    else:
        print( "Response: %s" % r.status_code )
        return None

if __name__ == "__main__":
    #DEBUG = True
    _abstract_query()
    _bugtracker_query()
    _homepage_query()
    _license_query()
    _author_query()
    _build_dependency_query()
    _runtime_dependency_query()
    _test_dependency_query()
    _provides_query()
    _module_to_debian_naming()
# TODO: FILES_${PN}-ptest = "/t" and a reasonable run-ptest script
#       perl Makefile.pl / make test => something better?
#       strip makefile and only package test goal?
#
# TODO: map module name to perl-* or lib*-perl
#       use generated lookup table for perl-* mapping
#       might need to build all of meta-perl before mapping lib*-perl
#       or use a versioned generated lookup table
