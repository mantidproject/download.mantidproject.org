Mantid downloads
================

[Scripts](/tools/) for building the Mantid [download page](http://download.mantidproject.org).


## Building locally

Requirements:

* [jinja2](http://jinja.pocoo.org/) Python package.

To build locally run the `build-site.py` script located in the `tools` folder:

    python tools/build-site.py

When finished the final HTML files will be output to the `static` directory.
