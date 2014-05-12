#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jinja2
import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

def releases():
  releaseDir = THIS_DIR + "/../releases"
  releases = [] # Stores build info for each release in the "releases" folder

  for fileName in os.listdir(releaseDir):
    release = {}
    release['version'], release['date'] = os.path.splitext(fileName)[0].split("-",1) # Split filename into version/date
    # Read the buildInfo names of each file/release
    with open(os.path.join(releaseDir,fileName), 'r') as fileContent:
      buildInfo = {} # Stores content of each release file
      for buildName in fileContent:
        buildInfo[getOSName(buildName)] = buildName.rstrip()
      release['buildInfo'] = buildInfo
    releases.append(release)
  return sorted(releases, key=lambda k : k['date'],reverse=True)

def getOSName(buildname):
  osname = "unknown"
  if "win64" in buildname: osname = "windows"
  elif "win32" in buildname: osname = "windows-32"
  elif "MountainLion" in buildname: osname = "osx"
  elif "SnowLeopard" in buildname: osname = "snow-leopard"
  elif ".rpm" in buildname: osname = "red-hat"
  elif ".deb" in buildname: osname = "ubuntu"
  elif "tar.gz" in buildname: osname = "source"
  return osname

if __name__ == "__main__":
  # Build information for each release file in the "releases" folder
  releases = releases()

  # Variables to output on the archives page
  archiveVars = { "title" : "Mantid archive downloads",
                "description" : "Downloads for current and previous releases of Mantid.",
                "releases" : releases[1:] # Remove nightly (first item) build from releases
                }

  downloadVars = { "title" : "Mantid downloads",
                 "description" : "Download the latest release of Mantid.",
                 "releases" : releases[0:2] # Only use first (nightly) and second (latest)
                 }

  # Setup up the jinja environment and load the templates
  env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=THIS_DIR + "/../templates"))
  # Write the contents of variables to the templates and dump the output to an HTML file.
  env.get_template("archives.html").stream(archiveVars).dump(THIS_DIR +   "/../static/archives.html")
  env.get_template("downloads.html").stream(downloadVars).dump(THIS_DIR + "/../static/index.html")
