#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import distutils.version
import os
import re
import sys

# TODO: Update if a build name changes with a release.
MANTID_BUILD_NAMES = [
  "mantid%s-%s-win64.exe",
  "mantid%s-%s-Mavericks.dmg",
  "mantid%s-%s-1.el6.x86_64.rpm",
  "mantid%s-%s-1.el7.x86_64.rpm",
  "mantid%s_%s-1_amd64.deb",
  "mantid%s-%s-Source.tar.gz"
]

TIMESTAMP_RE = r'\d+.\d+.\d{8}.\d+'
NIGHTLY_BUILD_REGEXES = [
  "mantid-{0}-win64.exe".format(TIMESTAMP_RE),
  "mantid-{0}-Mavericks.dmg".format(TIMESTAMP_RE),
  "mantidnightly-{0}-1.el6.x86_64.rpm".format(TIMESTAMP_RE),
  "mantidnightly-{0}-1.el7.x86_64.rpm".format(TIMESTAMP_RE),
  "mantidnightly_{0}-1_amd64.deb".format(TIMESTAMP_RE),
  "mantidnightly-{0}-Source.tar.gz".format(TIMESTAMP_RE)
]

# TODO: Update if a paraview build name changes with a new supported release.
PARAVIEW_BUILD_NAMES = [
  "ParaView-%s-Windows-64bit.exe",
  "ParaView-%s-Windows-32bit.exe",
  "ParaView-%s-SnowLeopard-64bit.dmg",
  "ParaView-%s-MountainLion-64bit.dmg",
  "ParaView-%s-Linux-64bit.tar.gz",
  "ParaView-%s-source.tar.gz"]

def update_paraview_versions(mantid_version, paraview_version):
  """
  Adds the mantid release code and paraview version to the top of the paraviewReleases file.
  If paraview_version is greater than previous paraview version a new paraview build file is created.

  Args:
    mantid_version (str): The version number of the given Mantid release.
    paraview_version (str): The paraview version that this release of Mantid will use.
  """
  with open(os.path.join(PARAVIEW_DIR, "paraviewVersions.txt"), "r+") as paraview_versions:
    # Read entire file to enable insertion to start of file.
    content = paraview_versions.read()
    # If no paraview version is provided, then the previous paraview version is used.
    previous_version = content.split("\n",1)[0].split(",")[1]
    if not paraview_version:
      paraview_version = previous_version
    # Add the new release and paraview version to the top of the file
    paraview_versions.seek(0,0)
    paraview_versions.write(mantid_version + "," + paraview_version + "\n" + content)
    print "The following was added to the paraviewVersions file: " + mantid_version + " " + paraview_version
    # Compare paraview versions, and create a new ('latest') paraview file if provided version is greater than previous
    if distutils.version.StrictVersion(paraview_version) > distutils.version.StrictVersion(previous_version):
      create_paraview_file(paraview_version)

def create_release_file(version, date, overwrite):
  """
  Creates a file in the release folder and writes the build names to it for a given release.

  Args:
    version (str): The version code for this release.
    date (str): The date that this version of Mantid was released.
    overwrite (bool): If true, overwrite a file if it already exists
  """
  filename = version + ".txt"
  filepath = os.path.join(RELEASE_DIR, version + ".txt")
  if os.path.exists(filepath) and not overwrite:
    raise RuntimeError("File '%s' already exists, use --force to overwrite." % filename)

  suffix = ""
  with open(filepath, "w") as release_file:
    release_file.write(date + "\n\n")
    release_file.write('\n'.join([build_name % (suffix, version) for build_name in MANTID_BUILD_NAMES]))
    print "New release manifest created in releases directory: %s" % (version + ".txt")

def create_nightly_file(nightly_package_dir):
  """
  Creates a file in the release folder called nightly.txt that contains the current package versions
  for the nightly builds

  Args:
    nightly_package_dir (str): A directory containing new nightly build packages. The existing file is
                               only *updated* with packages
  """
  filepath = os.path.join(RELEASE_DIR, "nightly.txt")
  current_packages = create_current_nightly_package_list(filepath)
  updated_packages = create_updated_package_list(nightly_package_dir)
  if len(updated_packages) == 0:
    raise RuntimeError("No nightly packages found in '{0}'".format(nightly_package_dir))

  # filter out those from current list that have no updated version
  def no_update(filename):
    for updated in updated_packages:
      for build_re_str in NIGHTLY_BUILD_REGEXES:
        build_re = re.compile(build_re_str)
        if build_re.match(filename) and build_re.match(updated):
          return False
    return True
  #end
  nightlies = filter(no_update, current_packages)
  nightlies.extend(updated_packages)
  nightlies.sort()
  open(filepath, 'w').write("\n".join(nightlies))

def create_current_nightly_package_list(manifest_filename):
  """
  Create a list of builds/source files that are current listed in the nightly section

  Args:
    manifest_filename (str): A file path pointing to the manifest for the current nightly build
  """
  if os.path.exists(manifest_filename):
    file_contents = open(manifest_filename).read()
    current_packages = file_contents.strip().split("\n")
  else:
    current_packages = []

  return current_packages

def create_updated_package_list(nightly_package_dir):
  """
  Create a list of builds/source files for the page

  Args:
    nightly_package_dir (str): A directory path to list for nightly packages
  """
  if not os.path.exists(nightly_package_dir):
    raise RuntimeError("Invalid directory for nightly build artifacts '{0}'".format(nightly_package_dir))
  updated_packages = os.listdir(nightly_package_dir)

  def is_binary_or_source(item):
    for build_re_str in NIGHTLY_BUILD_REGEXES:
      build_re = re.compile(build_re_str)
      if build_re.match(item):
        return True
    return False
  #end
  return filter(is_binary_or_source, updated_packages)

def create_paraview_file(version):
  """
  Creates a new paraview build file in the paraview folder with a given version name.

  Args:
    version (str): Used to name the file, and name the builds within the file.
  """
  with open(os.path.join(PARAVIEW_DIR, "paraview-" + version + ".txt"), "w+") as release_file:
    release_file.write('\n'.join([build_name%(version) for build_name in PARAVIEW_BUILD_NAMES]))

if __name__ == "__main__":

  RELEASE_DIR = os.path.join(os.path.dirname(__file__), "..", "releases")
  PARAVIEW_DIR = os.path.join(RELEASE_DIR, "paraview")

  parser = argparse.ArgumentParser(prog='create-manifest', usage='%(prog)s [options]',
      description='Creates a release file in the "releases" folder with the name provided.')
  parser.add_argument('version',
                      help="The version of the release to name the file being saved in the 'releases' folder.")
  parser.add_argument('--force', action='store_true', # defaults to false
                      help="Overwrite any existing file")
  parser.add_argument('--date',
                      help="The date of the release. This option overrides the current date, which is used by default.")
  parser.add_argument('--paraview',
                      help="The version of paraview for the release. Uses the previous version if not changed.")
  parser.add_argument('--dir', default="artifacts",
                      help="If provided then look in this directory for night build packages")
  args = parser.parse_args()

  # Validate version
  if args.version != "nightly" and len(args.version) != 5:
    sys.exit("Error: Invalid version number provided. The format expected is X.Y.Z or the word 'nightly'")

  if args.version == "nightly":
    create_nightly_file(os.path.join(os.path.dirname(__file__), args.dir))
  else:
    # Use current date if none provided
    if not args.date:
      args.date = datetime.date.today()
    else:
      # Validate the date provided is the correct format.
      try:
        datetime.datetime.strptime(args.date, "%Y-%m-%d")
      except ValueError:
        sys.exit("The date you have provided is invalid. It must be in Y-M-D format.")
    #
    create_release_file(args.version,str(args.date), args.force)
    if args.paraview:
      update_paraview_versions(args.version,args.paraview)
