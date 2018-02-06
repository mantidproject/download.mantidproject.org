
# Install mantid (framework-only) using [conda](https://conda.io/docs/)

Supported platforms:
* Linux-64: latest ubuntu/fedora/redhat (see below for distribution-specific instructions)
* Mac OS X: experimental

Installation:
```
$ conda config --add channels conda-forge      # add conda-forge channel
$ conda install -c mantid mantid-framework     # install
```

To install the nightly build:
```
$ conda install -c mantid/label/nightly mantid-framework
```
