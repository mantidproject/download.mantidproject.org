=========================
Installing Mantid via apt
=========================

The debian packages for the current release are built for Ubuntu 12.04 (Precise Pangolin).

In order to install them you will need to add the ISIS apt repository and `Mantid PPA <https://launchpad.net/~mantid/+archive/ubuntu/mantid>`__ 
to your repository configuration. **Note:** This only has to be done once.

Open a terminal and add the repositories: ::

    sudo apt-add-repository "deb http://apt.isis.rl.ac.uk precise main"
    sudo apt-add-repository ppa:mantid/mantid

To update and install the latest version of Mantid type: ::

    sudo apt-get update
    sudo apt-get install mantid

To download and install a package manually, first install gdebi: ::

    sudo apt-get install gdebi

then install mantid using: ::

    sudo gdebi pkgname.deb


Installing ParaView
~~~~~~~~~~~~~~~~~~~~~~~~~

To install the latest `version <index.html>`_ of ParaView you will need to manually build it from source as Kitware no longer provide Debian packages.

Remove previous paraview installations and dependencies: ::

    sudo apt-get purge paraview
    sudo apt-get purge qt-at-spi

Move the contents of the downloaded paraview to the opt directory: ::

    cd /opt && sudo tar xzf $HOME/Downloads/ParaView-X.Y.Z-Linux-64bit.tar.gz

Add the new ParaView to your path to ensure it is used: ::

    echo "export PATH=/opt/ParaView-X.Y.Z-Linux-64bit/lib/paraview-X.Y:$PATH" >> $HOME/.bashrc
    echo "export LD_LIBRARY_PATH=/opt/ParaView-X.Y.Z-Linux-64bit/lib/paraview-X.Y:$LD_LIBRARY_PATH" >> $HOME/.bashrc

Loads the new ParaView path into your current sessions: ::

    source $HOME/.bashrc

**Note:** **X.Y.Z** should be replaced with the version number of ParaView.
