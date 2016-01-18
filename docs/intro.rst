Patchtest
=========

**patchtest** is a test framework which takes a single series/revision from a
`patchwork <https://github.com/dlespiau/patchwork>`__ instance, apply it
into the corresponding repository, then execute any tests discovered in a
specific folder. Results may be posted to **patchwork**, which in turn can send
notifications  to the submitter/maintainer. It is important to notice that the test
cases to be created for a particular repo are not part of patchtest itself:
these should be kept in a **separate repository**.

Download
--------

The latest version of patchtest is available with git. To download:

::

    $ git clone https://github.com/lsandoval/patchtest.git

Design
------

**patchwork** is not intended to test patches/series. **patchtest** in
turn takes care of the testing part, working closely with a patchwork instance
to fetch series/revision and post results. patchtest is a **testing
framework**  (as the ``unittest`` python module) and it should **not contain
any tests cases**  to be executed against a
project's series/revision. The single test case under the ``tests`` folder is
a sample code, so real tests should not reside under this folder.

Getting Started
---------------

You should check out the :ref:`installation` and :ref:`development` guides for
information on how to install **patchtest** and start creating your tests.

Support
-------

For questions, issues and contributions, please use the `Github project
<https://github.com/lsandoval/patchtest>`__.

