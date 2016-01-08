Patchtest
=========

**patchtest** is a simple test framework which takes a series/revision from a
`**patchwork** <https://github.com/dlespiau/patchwork>` instance, apply it
into  the corresponding repository, then execute
any tests discovered in a folder indicated through an argument. Results may be
posted to patchwork, which in turn can send notifications to the
submitter/maintainer if configured. It is important to notice that the test
cases to be created for a particular repo are not part of patchtest itself;
these should be kept in a separate repository.

Download
--------

The latest version of patchtest is available with git. To download:

::

    $ git clone https://github.com/lsandoval/patchtest.git

Design
------

The design of **patchwork** did not intend to test patches/series. **patchtest** in
turn takes care of the testing part, working closely with a patchwork instance
to fetch S/R and post results. 

patchtest is a **testing framework** (as the ``unittest`` python
module), thus it is **not intended as a repository to create unit tests on it**. The
single test case under the `tests` folder is intended to be sample code, not
real code, so real tests should not reside under this folder.

Getting Started
---------------

You should check out the :ref:`installation` and :ref:`development` guides for
information on how to install **patchtest** and start creating your tests.

Support
-------

For questions and contributions, please use the `Github project <https://github.com/lsandoval/patchtest>`__.

