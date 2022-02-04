========================================================
Install mantid, mantidqt, or mantidworkbench using conda
========================================================

Supported platforms:

* Linux-64: available for 64-bit Linux distributions (tested for Ubuntu and CentOS/RHEL).
* Mac OS X: available for all MacOS versions 10.10 and higher.
* Windows: available for windows 10 and higher.

You need to have a version of conda already installed, we recommend using `mambaforge <https://github.com/conda-forge/miniforge/releases>`_. As it adds support for `conda-forge <https://conda-forge.org/>`_
channels by default, and allows users to by default, use mamba (replace `conda` with `mamba` in commands to use it), which is a faster version of conda for creating 
`conda environments <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_.

If not using mambaforge, add conda-forge to your channels::

  $ conda config --add channels conda-forge 

Installing latest release version of mantid::

  $ conda install mantid -c mantid

Installing latest release version of mantidqt::

  $ conda install mantidqt -c mantid 

Installing latest release version of mantidworkbench::

  $ conda install mantidworkbench -c mantid

To install the nightly build of mantid::

  $ conda install mantid -c mantid/label/nightly

To install the nightly build of mantidqt::

  $ conda install mantidqt -c mantid/label/nightly

To install the nightly build of mantidworkbench::

  $ conda install mantidworkbench -c mantid/label/nightly

