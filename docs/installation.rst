.. _installation:

Installation
============

patchwork and ``git-pw``
------------------------

To be useful, patchtest requires a patchwork instance running. In case you
want to launch a patchwork instance, please check the `patchwork documentation
<http://patchwork-freedesktop.readthedocs.org/en/latest/>`__. In the other
hand, patchtest requires **git-pw** tool which comes
in patchwork, so even if you already have a patchwork instance
running somewhere else, you will need to clone it locally and follow the
``git-pw`` `setup
<http://patchwork-freedesktop.readthedocs.org/en/latest/manual.html#git-pw>`__. The
``git-pw`` basically consists of setting up a soft link and install
dependencies

::

    $ pip install -r $PWD/git-pw/requirements.txt
    $ ln -s $PWD/git-pw/git-pw ~/.local/bin/

where ``PWD`` corresponds to the directory where patchwork source code resides.

patchtest
---------

The ``patchtest`` script is install in the same way as ``git-pw``

::

    $ ln -s $PWD/patchtest ~/.local/bin/

in this case, ``PWD`` is the directory where patchtest repository is
located. No need to install extra packages.

Target Repository
-----------------

Once the tools are installed (``git-pw`` and ``patchtest``), the target repository
to be tested must be configured, and this is done in the same way as `git-pw
<http://patchwork-freedesktop.readthedocs.org/en/latest/manual.html#setup>`__

::

    $ git config patchwork.default.url https://patchwork.freedesktop.org
    $ git config patchwork.default.project intel-gfx

In case results need to be posted, credentials must be set

::

    $ git config patchwork.default.user <pathcwork user>
    $ git config patchwork.default.password <patchwork password>

Currently, patches are applied on top of the ``origin/master`` which is
usually the name of the stable branch, but for some upstream repostories this
is not the case and one can change it through

::

    $ git config patchtest.default.stable origin/stable

Because this is a patchtest related configuration, ``patchtest.*`` is used
instead of ``patchwork.*``.
