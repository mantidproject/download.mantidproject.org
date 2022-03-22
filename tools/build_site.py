#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

import docutils.core
import jinja2

# General globals
from impl import url_handling
from impl.release_parsing import get_mantid_releases, get_nightly_releases
from impl.static_vars import INSTRUCTIONS_DIR, ROOT_DIR

MANTID_NEWS = "https://developer.mantidproject.org/"

if __name__ == "__main__":
    # Build information for each release file in the "releases" folder
    release_info = get_mantid_releases()

    # Variables to output on the archives page
    archive_vars = {
        "title": "Mantid - Previous Releases",
        "description": "Downloads for current and previous releases of Mantid.",
        "releases": release_info[1:]
    }

    latest_version = release_info[0]
    download_vars = {
        "title": "Mantid - Downloads",
        "description": "Download the latest release of Mantid.",
        "sample_datasets": url_handling.SAMPLES_DATASETS,
        "mantid_news": MANTID_NEWS,
        "release_notes": latest_version.release_notes_url,
        "latest_release": latest_version,
        "nightly_releases": get_nightly_releases(),
        "instructions": [
            os.path.splitext(filename)[0] for filename in sorted(os.listdir(INSTRUCTIONS_DIR))
        ],
        "ipython_notebook": url_handling.IPYTHON_NOTEBOOK
    }

    # Setup up the jinja environment and load the templates
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(ROOT_DIR, "templates")))
    # Write the contents of variables to the templates and dump the output to an HTML file.
    env.get_template("archives.html").stream(archive_vars).dump(
        os.path.join(ROOT_DIR, "docs", "archives.html"))
    env.get_template("downloads.html").stream(download_vars).dump(
        os.path.join(ROOT_DIR, "docs", "index.html"))

    for instruction_file in sorted(os.listdir(INSTRUCTIONS_DIR)):
        with open(os.path.join(INSTRUCTIONS_DIR, instruction_file), "r") as content:
            # Converts ReST file contents to HTML.
            parts = docutils.core.publish_parts(content.read(),
                                                writer_name='html',
                                                settings_overrides={'doctitle_xform': False})
            # Required to disable promotion of top level header to section title.

            # Remove extension from instruction filename
            filename = os.path.splitext(instruction_file)[0]
            filename = filename.replace("-", " ")

            instruction_vars = {
                "title": filename + " installation instructions for Mantid.",
                "description": "Mantid installation instructions for " + filename + ".",
                "instructions": parts["html_body"]
            }

            env.get_template("instructions.html").stream(instruction_vars).dump(
                os.path.join(ROOT_DIR, "docs",
                             filename.replace(" ", "").lower() + ".html"))
