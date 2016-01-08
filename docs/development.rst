.. _development:

Developing patchtest
====================

Quick start
-----------

``patchtest`` can be used to test a single series/revision

::
    $ patchtest --series 919 --revision 1

This command assumes that the command is executed being inside the repository
folder but one can run it somewhere else except that the ``-C`` parameter must
be used. By default, the tests executed are the ones from the
``patchtest\tests`` directory, consisting of a simple sample test case. The latter
at least tell us if the series applies to the repository cleanly.

``patchtest`` also gets its input from ``git pw poll-events``

::

    $ git pw poll-events | patchtest

running the set of tests for each event (series/revision) found by the
``git-pw``. There are other parameters that patchtest can take as shown with
the ``--help`` command:

::
    $ patchtest --help
      usage: patchtest [-h] [--series SERIES] [--revision REVISION] [-C REPODIR]
                       [--temp-base-dir TEMPBASEDIR] [--test-name TESTNAME]
                       [--no-post] [--test-dir TESTDIR]

      optional arguments:
        -h, --help            show this help message and exit
        --series SERIES, -s SERIES
                              Series number
        --revision REVISION, -r REVISION
                              Revision number
        -C REPODIR            Name of the repository where mboxs are applied
        --temp-base-dir TEMPBASEDIR
                              Name of the directory where logs are created
        --test-name TESTNAME  Test name to be used if results are POSTed
        --no-post             Do not POST the results to the PW instance
        --test-dir TESTDIR    Directory where tests are located

Writing Tests
-------------

As mentioned before, ``patchtest`` is test case **agnostic**: it tests whatever it
discovers under the indicated test folder. With this in mind, the only
restriction is that test cases must be written using the ``unittest`` python
framework. If tests are done against the patched repository, which is commonly
the case (we want to test series that can be at least merge into the repo,
otherwise the submitter should resend the series previously rebased from
master), then new tests cases should inherit from ``PatchTestBase`` class
defined in ``base.py``. The latter is basically a test fixture, with two main
tasks: create & configure the repository and merge the series/revision into it.

Results
-------

Commands and their corresponding outputs are stored under the folder defined
on ``--temp-base-dir``. As its name implies, this is a base folder, where
logs of the corresponding series/revision are located on
``<temp-base-dir>/<series>-<revision>``. The summary of all tests executed is
stored in the same folder and its contents are posted to the patchwork
instance, unless the ``--no-post`` argument is present.


patchwork & patchtest integration
---------------------------------

TODO
