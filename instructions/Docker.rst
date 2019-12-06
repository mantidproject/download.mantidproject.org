======
Docker
======

Note that this is an unofficial distribution channel and not suitable for production use.
It may not work as described and may disappear with little notice.

Docker images are published to `Docker Hub <https://hub.docker.com/r/mantidproject/mantid/>`_.

Tags are available for each release (starting from 3.13.0).

Platform support:

* Linux: full support for Mantid Python scripting and MantidPlot
* Mac OS X and Windows: support for Mantid Python scripting, limited/experimental GUI support

Linux usage example
-------------------

Requires having `x11docker <https://github.com/mviereck/x11docker>`_ and `Xpra <https://xpra.org/>`_ installed.

Launch MantidPlot giving access to the ``/media/data`` directory:
  ``x11docker --hostipc --xpra --sharedir /media/data/ mantidproject/mantid mantidplot``
