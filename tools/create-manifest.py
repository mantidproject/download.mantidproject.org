#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import os
import sys

def update_paraview_versions(mantid_version, paraview_version):
  """
  Adds the mantid release code and paraview version to the top of the paraviewReleases file.

  Args:
    mantid_version (str): The version number of the given Mantid release.
    paraview_version (str): The paraview version that this release of Mantid will use.

  """
  with open(os.path.join(RELEASE_DIR, "paraview/paraviewVersions.txt"), "r+") as paraview_versions:
    # Read entire file to enable insertion to start of file.
    content = paraview_versions.read()
    # If no paraview version is provided, then the previous paraview version is used.
    previous_version = content.split("\n",1)[0].split(",")[1]
    if not paraview_version: paraview_version = previous_version
    # Add the new release and paraview version to the top of the file
    paraview_versions.seek(0,0)
    paraview_versions.write(mantid_version + "," + paraview_version + "\n" + content)
    print "The following was added to the paraviewVersions file: " + mantid_version + " " + paraview_version

def create_release_file(version, date):
  """
  Creates a file in the release folder and writes the build names to it for a given release.

  Args:
    version (str): The version code for this release.
    date (str): The date that this version of Mantid was released.

  """
  with open(os.path.join(RELEASE_DIR, version + "-" + date + ".txt"), "w+") as release_file:
    release_file.write('\n'.join([build_name%(args.version) for build_name in MANTID_BUILD_NAMES]))
    print "The new release file was created successfully."

if __name__ == "__main__":

  # TODO: Update if a build name changes with a release.
  MANTID_BUILD_NAMES = [
   "mantid-%s-win64.exe",
   "mantid-%s-MountainLion.dmg",
   "mantid-%s-1.el6.x86_64.rpm",
   "mantid_%s-1_amd64.deb",
   "mantid-%s.tar.gz"]

  RELEASE_DIR = os.path.join(os.path.dirname(__file__),"../releases")

  parser = argparse.ArgumentParser(prog='create-manifest', usage='%(prog)s [options]',
      description='Creates a release file in the "releases" folder with the name provided.')
  parser.add_argument('version', help="The version of the release to name the file being saved in the 'releases' folder.")
  parser.add_argument('--date', help="The date of the release. This option overrides the current date, which is used by default.")
  parser.add_argument('--paraview', help="The version of paraview for the release. Used the previous version if not changed.")
  args = parser.parse_args()

  # Validate version
  if len(args.version) > 5: sys.exit("Error: Invalid version number provided.")

  # Use current date if none provided
  if not args.date:
    args.date = datetime.date.today()
  else:
    # Validate the date provided is the correct format.
    try:
      datetime.datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
      sys.exit("The date you have provided is invalid. It must be in Y-M-D format.")

  update_paraview_versions(args.version,args.paraview)
  create_release_file(args.version,str(args.date))
