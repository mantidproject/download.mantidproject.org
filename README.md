Mantid downloads
================

## Download Docs

The [html pages](/docs/) for the [download pages](https://download.mantidproject.org) are built from the related [rst files](/instructions/), apart from [index.html](/docs/index.html). The index page is built from [downloads.html](/templates/downloads.html)

The index page has links, that are held in text files, for the current [release](/releases/) and most recent [nightly](/releases/nightly.txt). These can be updated manually, or in the case of the Nightly builds, they are updated by @mantid-builder. If any download pages wish to point users towards a download link, they should just be pointed towards the relevant part of the [index of the downloads website](https://download.mantidproject.org).

Links to past [releases](/releases/) are referenced [here](/templates/archives.html).

## Building locally

[Scripts](/tools/) for building the Mantid [download page](https://download.mantidproject.org).

To build locally run the `build-site.py` script located in the `tools` folder:

    python tools/build-site.py

When finished the final HTML files will be output to the `docs` directory.

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
