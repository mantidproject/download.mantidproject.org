=========================
Installing Mantid via Apt
=========================

The debian packages for the current release are built for Ubuntu 14.04 (Trusty Tahr).

Stable Release
--------------

To install the current release via apt, first add the required repositories to the `sources.list`. This only needs to be done once.
Open a terminal and run ::

    sudo apt-add-repository "deb [arch=amd64] http://apt.isis.rl.ac.uk trusty main"
    sudo apt-add-repository ppa:mantid/mantid

and then install package with: ::

    sudo apt-get update
    sudo apt-get install mantid

This will install Mantid into ``/opt/Mantid`` and add bash files to ``/etc/profile.d`` so that next time you create a terminal the correct path to MantidPlot will be defined.

Nightly Build
-------------

To install the current release via apt, first add the required repositories to the `sources.list`. This only needs to be done once.
Open a terminal and run ::

    sudo apt-add-repository "deb [arch=amd64] http://apt.isis.rl.ac.uk trusty-testing main"
    sudo apt-add-repository ppa:mantid/mantid

and then install package with: ::

    sudo apt-get update
    sudo apt-get install mantidnightly

This will install Mantid into ``/opt/mantidnightly``. It does **not** update the environment so you must type the following to start it: ::

    ./opt/mantidnightly/bin/MantidPlot

This is to avoid users accidentally running the nightly development build.

Manual Install
--------------

To download and install a package manually, first install gdebi: ::

    sudo apt-get install gdebi

then install mantid using: ::

    sudo gdebi pkgname.deb
