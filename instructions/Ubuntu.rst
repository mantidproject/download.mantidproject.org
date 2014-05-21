=========================
Installing Mantid via apt
=========================

The current release debian packages provided are built for the long term support release of **Ubuntu**, which is currently **12.04** (Precise Pangolin).

In order to install them you will need to add the ISIS apt repository to your repository configuration. **Note:** This only has to be done once.

Open a terminal and add the repository: ::

    sudo apt-add-repository "deb http://apt.isis.rl.ac.uk precise main"

To update and install the latest version of Mantid type: ::

    sudo apt-get update
    sudo apt-get install mantid

To download and install the package manually run the following: ::

    # Assumes package is in the Downloads directory
    sudo gdebi $HOME/Downloads/mantid_X.Y.Z-1_amd64.deb

where **X.Y.Z** should be replaced with the version number of Mantid.

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
