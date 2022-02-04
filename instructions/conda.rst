========================================================
Install mantid, mantidqt, or mantidworkbench using conda
========================================================

Supported platforms:

* Linux-64: available for 64-bit Linux distributions (tested for Ubuntu and CentOS/RHEL).
* Mac OS X: available for all MacOS versions 10.10 and higher.
* Windows: available for windows 10 and higher.

You need to have Conda, via either miniconda, mambaforge, or miniforge. You can easily check by typing `conda --help` in the terminal.
We recommend using `mambaforge <https://github.com/conda-forge/miniforge/releases>`_. It adds support for `conda-forge <https://conda-forge.org/>`_
channels by default, comes with mamba pre-installed (replace `conda` with `mamba` in commands to use it), which is a faster version of Conda for creating 
`conda environments <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_, and it doesn't include the channels with 
license restrictions by default.

The default channels on miniconda come with license agreements which you may need to be aware of.

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

