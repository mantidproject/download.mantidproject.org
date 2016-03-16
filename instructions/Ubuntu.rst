=========================
Installing Mantid via apt
=========================

The debian packages for the current release are built for Ubuntu 14.04 (Trusty Tahr).

In order to install them you will need to add the ISIS apt repository
to your repository configuration. **Note:** This only has to be done once.

Open a terminal and add the repositories: ::

    sudo apt-add-repository "deb [arch=amd64] http://apt.isis.rl.ac.uk trusty main"
    sudo apt-add-repository ppa:mantid/mantid

To update and install the latest version of Mantid type: ::

    sudo apt-get update
    sudo apt-get install mantid

To download and install a package manually, first install gdebi: ::

    sudo apt-get install gdebi

then install mantid using: ::

    sudo gdebi pkgname.deb
