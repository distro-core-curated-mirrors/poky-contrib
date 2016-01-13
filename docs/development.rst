.. _development:

Developing patchtest
====================

Quick start
-----------

``patchtest`` can be used to test a single series/revision

::

    $ patchtest --series 919 --revision 1

This command assumes that the command is executed inside the repo
folder but one can run it somewhere but using the ``-C`` to indicate where the
repository resides. By default, the tests executed are the ones from the
``patchtest\tests`` directory, consisting of a simple (and useless) sample
test case.  The latter at least tell us if the series applies to the repository cleanly.
``patchtest`` also gets its input from ``git pw poll-events``, which can be
used to constantly test new events

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

As mentioned before, ``patchtest`` is test case and project **agnostic**: it tests whatever it
discovers under the indicated test folder and for any project being monitored
by patchwork. This feature implies that any project can use ``patchtest`` and just
focus on the tests, not on the testing framework. The only **restriction** is that test cases must
be written using the ``unittest`` python framework and test cases (class) should inherit from ``PatchTestBase``
(defined on ``base.py``). The latter inheritance can be ommited in case the mbox should be tested without
being merged to the stable branch. The base class ``PatchTestBase`` is a test
fixture, with the only purpose of patching the mbox on a new branch (named
``patchtest-<series>-<revision>`` created from the latest stable branch.

Results
-------

Commands and their corresponding outputs are stored under
``--temp-base-dir``. As its name implies, this is a base folder, where
logs of the corresponding series/revision are located on
``<temp-base-dir>/patchtest-<series>-<revision>``. The summary of all tests executed is
stored in the same folder and it is also posted to the patchwork
instance, unless the ``--no-post`` argument is given.


patchwork & patchtest integration
---------------------------------

TODO
