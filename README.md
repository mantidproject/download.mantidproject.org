Mantid downloads
================

[Scripts](/tools/) for building the Mantid [download page](http://download.mantidproject.org).

## Building locally

To build locally run the `build-site.py` script located in the `tools` folder:

    python tools/build-site.py

When finished the final HTML files will be output to the `static` directory.

## Workflow

### Adding a new release

To add a new release run the `create-manifest` script with the release __version__. This generates a new release file in the [releases](/releases/) folder, and relevant paraview file if desired:

    # Generates a file in /releases/ with the release version and todays date as the name.
    python tools/create-manifest.py 3.2.0

It is possible to override the date using the `date` option, for example:

    python tools/create-manifest.py 3.2.0 --date=25/12/2000

By default, the previous version of ParaView is assigned to the release. This can be overriden using the `paraview` option. Once overriden an additonal paraview file is created in the [paraview folder](/releases/paraview/), which is used as the _latest_ version on the downloads page, for example:

    python tools/create-manifest.py 3.2.0 --paraview=3.4.0

## Requirements:

- [jinja2](http://jinja.pocoo.org/) Python templating package.
- Python 2.7 or greater is required to make use of [argparse](https://pypi.python.org/pypi/argparse).
