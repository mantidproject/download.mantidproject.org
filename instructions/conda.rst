===========================================
Install mantid (framework-only) using conda
===========================================

Supported platforms:

* Linux-64: latest ubuntu/fedora/redhat (see below for distribution-specific instructions)
* Mac OS X: experimental

Installation::

  $ conda config --add channels conda-forge      # add conda-forge channel
  $ conda install -c mantid mantid-framework     # install


To install the nightly build::

  $ conda install -c mantid/label/nightly mantid-framework


Ubuntu
------

A caveat for using conda build of mantid-framework at an ubuntu distribution is
that you will need to import matplotlib before mantid to get the correct backend
initialized::

  import matplotlib
  import mantid
