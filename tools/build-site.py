#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jinja2
import os
import re

ROOT_DIR = os.path.join(os.path.dirname(__file__) + "../")
RELEASE_DIR = os.path.join(ROOT_DIR,"releases/")
PARAVIEW_DIR = os.path.join(RELEASE_DIR, "paraview/")

SAMPLES_DATASETS = {
  "ISIS" : "http://sourceforge.net/projects/mantid/files/Sample%20Data/SampleData-ISIS.zip/download",
  "Muon" : "http://sourceforge.net/projects/mantid/files/Sample%20Data/SampleData-Muon.zip/download",
  "ORNL" : "http://sourceforge.net/projects/mantid/files/Sample%20Data/SampleData-ORNL.zip/download",
  "Training" :"http://sourceforge.net/projects/mantid/files/Sample%20Data/WorkshopData.zip/download"
}

def mantid_releases():
  """
  Reads and stores release information for each release file in the releases folder. This includes the nightly build.

  Returns:
    list: A list that contains dictionaries of release information for each release. The list is sorted by release date.
  """
  releases = []
  release_files = [name for name in os.listdir(RELEASE_DIR) if "paraview" not in name]
  for file_name in release_files:
    release = {}
    release['version'], release['date'] = os.path.splitext(file_name)[0].split("-",1)
    # Read the build names of each release file.
    with open(os.path.join(RELEASE_DIR,file_name), 'r') as content:
      build_names = {}
      for build_name in content:
        build_names[get_os_name(build_name)] = build_name.rstrip()
      release['build_names'] = build_names
    releases.append(release)
  return sorted(releases, key=lambda k : k['date'],reverse=True)

def latest_paraview_version():
  """
  Obtains the latest version of paraview in use by reading the first line of the paraview versions file.

  Returns:
    The version number of the latest paraview in use.
  """
  with open(os.path.join(PARAVIEW_DIR, "paraviewVersions.txt"), "r") as paraviewReleases:
    return paraviewReleases.readline().split(",")[1].rstrip()

def latest_paraview_release():
  """
  Reads the latest paraview release file, and writes the contents (which is the build names) to a list

  Returns:
    list: The build names for the latest version of paraview.
  """
  build_names = {}
  filename = "paraview-" + latest_paraview_version() + ".txt"
  with open(os.path.join(PARAVIEW_DIR, filename), "r") as latest_release:
    for build_name in latest_release:
      build_names[get_os_name(build_name)] = build_name.rstrip()
  return build_names

def get_os_name(build_name):
  """
  Obtains the operating system name from a given build name.

  Args:
    build_name (str): The name of the Mantid build for a given operating system, e.g. "mantid-2.3.2-SnowLeopard.dmg"

  Returns:
    str: The name of the operating system that the Mantid build will run on.
  """
  osname = "unknown"
  if "win64" in build_name or "Windows-64bit" in build_name: osname = "windows"
  elif "win32" in build_name or "Windows-32bit" in build_name: osname = "win32"
  elif "MountainLion" in build_name: osname = "mac"
  elif "SnowLeopard" in build_name: osname = "snow-leopard"
  elif ".rpm" in build_name: osname = "red-hat"
  elif ".deb" in build_name or "Linux" in build_name: osname = "ubuntu"
  elif "tar.gz" in build_name: osname = "source"
  return osname

def get_osx_code_name(url):
  """
  Obtains the OSX code name from a given download url.
  This is used as a custom filter in the jinja2 templating engine.

  Args:
    url (str): The download url of a mantid OSX build.

  Returns:
    str: The OSX code name, e.g. "Mountain Lion".
  """
  url = url.replace(".dmg","")
  url = url.replace("-64bit","") # Required as some urls (paraview) have this
  url = url.rsplit("-",1)[1] # Obtain codename by splitting on last hyphen
  # Add space before uppercase (not first, e.g. MountainLion => Mountain Lion)
  url = re.sub(r"(\w)([A-Z])",r"\1 \2",url)
  return url

if __name__ == "__main__":
  # Build information for each release file in the "releases" folder
  mantid_releases = mantid_releases()
  # Note: [0] is version, and [1] is build_names.
  latest_paraview = latest_paraview_release()

  # Variables to output on the archives page
  archiveVars = { "title" : "Mantid archive downloads",
                "description" : "Downloads for current and previous releases of Mantid.",
                "releases" : mantid_releases[1:] # Remove nightly (first item) build from releases
                }

  downloadVars = { "title" : "Mantid downloads",
                 "description" : "Download the latest release of Mantid.",
                 "sample_datasets" : SAMPLES_DATASETS,
                 "paraview_version" : latest_paraview_version(),
                 "paraview_build_names" : latest_paraview,
                 "releases" : mantid_releases[0:2] # Only use first (nightly) and second (latest)
                 }

  # Setup up the jinja environment and load the templates
  env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=os.path.join(ROOT_DIR,"templates")))
  # Add a filter to output the osx code name based on a given url
  env.filters["get_osx_code_name"] = get_osx_code_name
  # Write the contents of variables to the templates and dump the output to an HTML file.
  env.get_template("archives.html").stream(archiveVars).dump(os.path.join(ROOT_DIR + "static/archives.html"))
  env.get_template("downloads.html").stream(downloadVars).dump(os.path.join(ROOT_DIR + "static/index.html"))
