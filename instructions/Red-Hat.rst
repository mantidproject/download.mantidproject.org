=========================
Installing Mantid via Yum
=========================

On **RHEL** it is possible to install Mantid and all the required RPMs via the ISIS yum repository. There is an RPM spec file in the `Mantid repo <https://github.com/mantidproject/mantid/tree/master/Code/Mantid/Build/dev-packages/rpm/mantid-developer>`_ to allow you to build an RPM and install all dependencies.

Prior to installing Mantid via Yum you need to enable the `Extra Packages for Enterprise Linux (EPEL) <https://fedoraproject.org/wiki/EPEL>`_ by installing the `relevant rpm <https://fedoraproject.org/wiki/EPEL/FAQ#howtouse>`_.

**Note:** following these procedures will update some default RHEL packages with newer versions on your system.

**Red Hat 7:** Some packages from the *rhel-7-workstation-optional-rpms* repository are required. This can be enabled through the subscription manager with the following command: ::

    subscription-manager repo-override --repo=rhel-7-workstation-optional-rpms --add=enabled:1

Stable release
--------------

To install Mantid via yum, create the file ``/etc/yum.repos.d/isis-rhel.repo`` with the following content: ::

    [isis-rhel]
    name=ISIS Software Repository for Redhat Enterprise Linux $releasever - $basearch
    baseurl=http://yum.isis.rl.ac.uk/rhel/$releasever/$basearch
    failovermethod=priority
    enabled=1
    gpgcheck=0

    [isis-rhel-noarch]
    name=ISIS Software Repository for Redhat Enterprise Linux $releasever - noarch
    baseurl=http://yum.isis.rl.ac.uk/rhel/$releasever/noarch
    failovermethod=priority
    enabled=1
    gpgcheck=0

    [isis-rhel-debuginfo]
    name=ISIS Software Repository for Redhat Enterprise Linux $releasever - $basearch - Debug
    baseurl=http://yum.isis.rl.ac.uk/rhel/$releasever/$basearch/debug
    failovermethod=priority
    enabled=1
    gpgcheck=0

    [isis-rhel-source]
    name=ISIS Software Repository for Redhat Enterprise Linux $releasever - $basearch - Source
    baseurl=http://yum.isis.rl.ac.uk/rhel/$releasever/SRPMS
    failovermethod=priority
    enabled=0
    gpgcheck=0

You can then install the **stable release** of Mantid by typing: ::

    yum install mantid

This will install Mantid into ``/opt/Mantid`` and add bash files to ``/etc/profile.d`` so that next time you create a terminal the correct path to MantidPlot will be defined.

Nightly Build
-------------

To install nightly development builds via yum, create the file ``/etc/yum.repos.d/isis-rhel-testing.repo`` with the following content: ::

    [isis-rhel-testing]
    name=ISIS Software Repository for Redhat Enterprise Linux $releasever - $basearch
    baseurl=http://yum.isis.rl.ac.uk/rhel/testing/$releasever/$basearch
    failovermethod=priority
    enabled=0
    gpgcheck=0

    [isis-rhel-testing-debuginfo]
    name=ISIS Software Repository for Redhat Enterprise Linux $releasever - $basearch - Debug
    baseurl=http://yum.isis.rl.ac.uk/rhel/testing/$releasever/$basearch/debug
    failovermethod=priority
    enabled=0
    gpgcheck=0

    [isis-rhel-testing-source]
    name=ISIS Software Repository for Redhat Enterprise Linux $releasever - $basearch - Source
    baseurl=http://yum.isis.rl.ac.uk/rhel/testing/$releasever/SRPMS
    failovermethod=priority
    enabled=0
    gpgcheck=0

To install the ``nightly release`` run the appropriate setup steps to setup the testing repository above, and then run: ::

    yum install --enablerepo=isis-rhel-testing mantidnightly

This will install Mantid into ``/opt/mantidnightly``. It does **not** update the environment so you must type the following to start it: ::

    ./opt/mantidnightly/bin/MantidPlot

This is to avoid users accidentally running the nightly development build.
