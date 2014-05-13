#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import os
import sys

if __name__ == "__main__":
  RELEASE_DIR = os.path.abspath(os.path.dirname(__file__)) + "/../releases/"

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

  # Use the previous version of paraview if none is provided.
  if not args.paraview:
    with open(RELEASE_DIR + "paraview.txt", "r") as paraviewReleases:
      args.paraview = paraviewReleases.readline().split(",")[1].rstrip()

  # TODO: Update if a build name changes with a release.
  buildnames = [
   "mantid-RNUM-win64.exe",
   "mantid-RNUM-MountainLion.dmg",
   "mantid-RNUM-1.el6.x86_64.rpm",
   "mantid_RNUM-1_amd64.deb",
   "mantid-RNUM.tar.gz"]

  with open(RELEASE_DIR + args.version + "-" + str(args.date) + ".txt", "w") as releaseFile:
    releaseFile.write('\n'.join([name.replace("RNUM",args.version) for name in buildnames]))

  # Write the paraview release to the start of the paraview file
  with open(RELEASE_DIR + "paraview.txt", "r+") as paraviewReleases:
    content = paraviewReleases.read()
    paraviewReleases.seek(0,0)
    paraviewReleases.write(args.version + "," + args.paraview + "\n" + content)

  sys.exit("Success: Created release file (" + args.version + ")" + " in " + RELEASE_DIR)
