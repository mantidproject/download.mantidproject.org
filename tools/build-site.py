#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import docutils.core
import jinja2
import os
import re
import sys

# Repo folder structure
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
RELEASE_DIR = os.path.join(ROOT_DIR,"releases")
PARAVIEW_DIR = os.path.join(RELEASE_DIR, "paraview")
INSTRUCTIONS_DIR = os.path.join(ROOT_DIR, "instructions")

NIGHTLY_TARBALL_RE = re.compile("^mantidnightly-\d+\.\d+\.(\d{8})\.\d+-Source\.tar\.gz$")

# General globals
MANTID_NEWS = "http://developer.mantidproject.org/"
RELEASE_NOTES_PRE_37 = "http://www.mantidproject.org/Release_Notes_"
RELEASE_NOTES = "http://docs.mantidproject.org/{version}/release/{version}/index.html"

# Download specific variables
SOURCEFORGE_FILES = "http://sourceforge.net/projects/mantid/files/"
#The sourceforge upload is down so use our server for now
SOURCEFORGE_NIGHTLY = SOURCEFORGE_FILES + "Nightly/"

SOURCEFORGE_SAMPLES = SOURCEFORGE_FILES + "Sample%20Data/"
SOURCEFORGE_PARAVIEW = SOURCEFORGE_FILES + "ParaView/"
SOURCEFORGE_IPYTHON_NOTEBOOK = SOURCEFORGE_FILES + "IPython%20Notebook/"

# Must be in the name : downloadurl format.
SAMPLES_DATASETS = [
  ["Usage Examples", SOURCEFORGE_SAMPLES + "UsageData.zip/download"],
  ["ISIS", SOURCEFORGE_SAMPLES + "SampleData-ISIS.zip/download"],
  ["ORNL", SOURCEFORGE_SAMPLES + "SampleData-ORNL.zip/download"],
  ["Muon", SOURCEFORGE_SAMPLES + "SampleData-Muon.zip/download"],
  ["Training", SOURCEFORGE_SAMPLES + "TrainingCourseData.zip/download"]
]

IPYTHON_NOTEBOOK = [
  ["IPython Notebook Example", SOURCEFORGE_IPYTHON_NOTEBOOK + "Introduction%20to%20using%20Mantid%20with%20IPython%20Notebook.ipynb/download" ]
]

SUPPORTED_OSX_BUILDS = ["MountainLion", "Mavericks"]
LATEST_SUPPORTED_OSX_VERSION = "10.9"
SUPPORTED_UBUNTU_VERSION = "14.04"
SUPPORTED_UBUNTU_VERSION_NIGHTLY = "14.04"

def mantid_releases():
  """
  Reads and stores release information for each release file in the releases folder. This does not include the nightly build.

  Returns:
    list: A list that contains dictionaries of release information for each release. The list is sorted by release date.

    Example of list structure:

    [
      {
        "date" : "2014-02-28",
        "mantid_version" : "3.1.1",
        "paraview_version" : "3.98.1",
        "build_info" : {
          # (key) operating system name : (value) [mantid_download_url, paraview_download_url]
          "windows" : ["http://...mantid-3.1.1-win64.exe/download", "http://...paraview-win64.exe/download"],
          "..." : "...", # Shortened for simplicity
        }
      }
      ...
    ]
  """
  releases = []
  release_files = [name for name in os.listdir(RELEASE_DIR) if "paraview" not in name and "nightly" not in name]
  for file_name in release_files:
    release = {}
    release['mantid_version'] = os.path.splitext(file_name)[0]
    release["mantid_formatted_version"] = format_release_str(release['mantid_version'])
    release['paraview_version'] = paraview_version(release['mantid_version'])
    date, mantid_builds = parse_build_names(os.path.join(RELEASE_DIR, file_name), release['mantid_version'], "release")
    release['date'] = date
    pv_version = release['paraview_version']
    paraview_builds = paraview_build_names(pv_version) if pv_version is not None else {}

    # Add the related paraview download url to the dict, based on the osname.
    # Value of dict must be changed to a list to accommodate multiple values.
    for osname,downloadurl in mantid_builds.iteritems():
      if osname in paraview_builds:
        mantid_builds[osname] = [downloadurl, paraview_builds.get(osname, "")]
      else:
        # Required as value must now be a list in the template.
        mantid_builds[osname] = [downloadurl, paraview_builds.get("source", "")]

    release['build_info'] = mantid_builds
    releases.append(release)
  return sorted(releases, key=lambda k : k['date'],reverse=True)

def parse_build_names(file_location, version, build_option):
  """
  Parses a file that contains build names (e.g. those in /releases/) and stores the contents in a dictionary.
  The key of the dictionary is the operating system, which is obtained based on the build's file extension.
  The date on the first line is optional, if it is not present the date is extracted from the first filename if
  possible, else it raises an error.

  Args:
    file_location (str): The location of the release file to parse.
    version (str): Used when building the URL.
    build_option (str): The name of the build, which is used when building the URL, e.g. "release", "nightly" or "paraview".

  Returns:
    tuple: (date, builds) - A dictionary containing OS names as keys, and the related download url as a value.
           Key : Obtained from get_os_name, and is output on the downloads page as CSS classes.
           Value : The download url for that specific operating system.
  """
  manifest = open(file_location, 'r')
  date = None
  builds = {}
  for line in manifest:
    line = line.rstrip()
    if line == "":
      continue

    try:
      datetime.datetime.strptime(line, "%Y-%m-%d")
      date = line
    except ValueError:
      pass
    #endtry

    build = line
    builds[get_os_name(build)] = get_download_url(build,version,build_option)
    if date is None and build.endswith(".tar.gz"):
      date = get_date_from_tarball(build)
  #endfor

  return (date, builds)

def paraview_version(mantid_version):
  """
  Obtains the paraview version for a specific mantid release from the paraview versions file.

  Args:
    mantid_version (str): The version of Mantid to search for in the paraview versions file.

  Returns:
    str: The paraview version that the given release of mantid requires.
  """
  with open(os.path.join(PARAVIEW_DIR, "paraviewVersions.txt"), "r") as paraviewReleases:
    for line in paraviewReleases:
      m_version, paraview_version = line.rstrip("\n").split(",")
      if m_version == mantid_version:
        return paraview_version
      else:
        return None

def paraview_build_names(paraview_version):
  """
  Reads and stores paraview build names from the paraview release file, which is parsed based on version.

  Args:
    paraview_version (str): The paraview version

  Returns:
    dict: The paraview build names for the given version.
  """
  file_location = os.path.join(PARAVIEW_DIR, "paraview-" + paraview_version + ".txt")
  return parse_build_names(file_location, paraview_version, "paraview")[1]

def nightly_release():
  """
  Reads and stores release information for the nightly build from the nightly text file in the releases folder.
  The date on the first line is optional, if it is not present the date is extracted from the first filename.

  Return:
    dict: A dictionary containing release information for the nightly build.
    A similar format (see inner dict) of mantid_releases above is returned.
  """
  release_info = {}
  filename = [name for name in os.listdir(RELEASE_DIR) if "nightly" in name]
  release_info['version'] = os.path.splitext(filename[0])[0]
  date, builds = parse_build_names(os.path.join(RELEASE_DIR,filename[0]),release_info['version'],"nightly")
  release_info['date'] = date
  release_info['build_info'] = builds

  return release_info

def get_os_name(build_name):
  """
  Obtains the operating system name from a given build name.
  The osnames output as CSS classes in the 'alternative downloads' <li> in the jinja template (They are the key in the 'build_names' dict).
  This is required to allow switching of the href from the download button and the users os via JavaScript.

  Args:
    build_name (str): The name of the Mantid build for a given operating system, e.g. "mantid-2.3.2-SnowLeopard.dmg"

  Returns:
    str: The name of the operating system that the Mantid build will run on.
    If no os can be detected 'source' is returned.
  """
  build_name = build_name.lower()
  if "win64" in build_name or "windows-64bit" in build_name: osname = "windows"
  elif "win32" in build_name or "windows-32bit" in build_name: osname = "win32"
  elif "mavericks" in build_name: osname = "mac"
  elif "mountainlion" in build_name: osname = "mac"
  elif "snowleopard" in build_name or ".dmg" in build_name: osname = "snow-leopard"
  elif ".rpm" in build_name: osname = "red-hat"
  elif ".deb" in build_name or "linux" in build_name: osname = "ubuntu"
  else: osname = "source"
  return osname

def get_download_url(build_name, version, build_option):
  """
  Builds a download url for a given mantid buildname.
  This is used as the value in the 'build_names' dictionary, which is output in the jinja template.

  Args:
    buildname (str): The Mantid build name from a release file, e.g. mantid-3.1.1-win64.exe
    version (str): The version of the release, e.g. 3.1.1
    build_option (str): Used to determine the type of URL to build.

  Returns:
    str: The download url for a given build.
  """
  if build_option is "nightly":
    build_name = build_name.rstrip()
    return SOURCEFORGE_NIGHTLY + build_name
  elif build_option is "paraview":
    build_name = build_name.rstrip() + "/download"
    return SOURCEFORGE_PARAVIEW + version + "/" + build_name
  else:
    build_name = build_name.rstrip() + "/download"
    return SOURCEFORGE_FILES + version[0:3] + "/" + build_name

def tidy_build_name(url, osname, nightly=False):
  """
  Obtains the build name from a given download url if possible, otherwise uses the osname provided.
  This is used as a custom filter in the jinja2 templating engine.

  Args:
    url (str): The download url of a mantid build.
    osname (str): The osname set in get_os_name above, e.g. red-hat
    nightly (bool): True if this is for the nightly section

  Returns:
    str: The os name obtained from the url string, e.g. "Mountain Lion".
  """
  # The osname set on "get_os_name" is sufficient.
  if ".rpm" in url or ".tar.gz" in url or ".deb" in url:
    name = osname.title().replace("-"," ")
    if ".deb" in url:
      if nightly: name += " " + SUPPORTED_UBUNTU_VERSION_NIGHTLY
      else: name += " " + SUPPORTED_UBUNTU_VERSION
    return name

  url = url.replace("/download","")

  if ".dmg" in url:
    url = url.replace(".dmg","")
    url = url.replace("-64bit","") # Required as some urls (paraview) have this
    url = url.rsplit("-",1)[1] # Obtain codename by splitting on last hyphen
    # Use version numbers rather than names for simplicity.
    if url in SUPPORTED_OSX_BUILDS: url = "OSX (" + LATEST_SUPPORTED_OSX_VERSION + "+)"
    else: url = "OSX (<" + LATEST_SUPPORTED_OSX_VERSION +")"

  if ".exe" in url:
    # Cannot split like above as paraview has hyphen between Windows and bit, e.g. ..-Windows-64bit
    url = url[url.lower().index("win"):len(url)]
    # Usability improvements
    url = url.replace(".exe","").replace("-","")
    url = url.replace("bit","")
    url = url.replace("win","Windows")
    url = url.replace("32"," XP")
    url = url.replace("64"," 7/8")

  return url

def get_date_from_tarball(filename):
  """
  Attempts to parse a date from from a source tarball with the following format: mantidnightly-3.1.20140528.2000-Source.tar.gz

  Args:
    filename (str): A string giving the filename

  Returns:
    str: A date string in the format YYYY-MM-DD
  """
  match = NIGHTLY_TARBALL_RE.match(filename)
  if match:
    date = match.group(1)
    formatted_date = "%s-%s-%s" % (date[:4], date[4:6], date[6:])
  else:
    raise RuntimeError("Unable to extract date from source tarball '%s'" % filename)

  return formatted_date

def format_release_str(release_str):
  """
  Takes a release string, and formats it using the convention we use elsewhere
  in Mantid, for example DOI's.  Essentially, the patch number is removed if
  it is zero.  I.e. 2.1.0 becomes 2.1, 3.0.0 becomes 3.0, but 3.0 is left alone.

  Args:
    release_str (str) :: the release string to format.

  Returns:
    str: the formatted release string
  """
  if re.match("\d\.\d\.0", release_str):
    return release_str[:-2]
  return release_str

#========================================================================================================

if __name__ == "__main__":
  # Build information for each release file in the "releases" folder
  mantid_releases = mantid_releases()

  # Variables to output on the archives page
  archive_vars = { "title" : "Mantid - Previous Releases",
                "description" : "Downloads for current and previous releases of Mantid.",
                "release_notes" : RELEASE_NOTES_PRE_37,
                "releases" : mantid_releases[1:]
                }

  latest_version = mantid_releases[0]
  release_notes = RELEASE_NOTES.format(version=('v' + latest_version['mantid_formatted_version']))
  paraview_version = mantid_releases[0]['paraview_version']
  download_vars = { "title" : "Mantid - Downloads",
                 "description" : "Download the latest release of Mantid.",
                 "sample_datasets" : SAMPLES_DATASETS,
                 "mantid_news" : MANTID_NEWS,
                 "release_notes" : release_notes,
                 "latest_release" : latest_version,
                 "nightly_release" : nightly_release(),
                 "paraview_version" : paraview_version,
                 "paraview_build_names" : None if paraview_version is None else paraview_build_names(paraview_version),
                 "instructions" : [os.path.splitext(filename)[0] for filename in sorted(os.listdir(INSTRUCTIONS_DIR))],
                 "ipython_notebook" : IPYTHON_NOTEBOOK
                 }

  # Setup up the jinja environment and load the templates
  env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=os.path.join(ROOT_DIR,"templates")))
  # Add a filter to output the os name based on a given url
  env.filters["tidy_build_name"] = tidy_build_name
  # Write the contents of variables to the templates and dump the output to an HTML file.
  env.get_template("archives.html").stream(archive_vars).dump(os.path.join(ROOT_DIR, "static", "archives.html"))
  env.get_template("downloads.html").stream(download_vars).dump(os.path.join(ROOT_DIR, "static", "index.html"))

  for instruction_file in sorted(os.listdir(INSTRUCTIONS_DIR)):
    with open(os.path.join(INSTRUCTIONS_DIR, instruction_file), "r") as content:
      # Converts ReST file contents to HTML.
      parts = docutils.core.publish_parts(
          content.read(),
          writer_name = 'html',
          settings_overrides = {'doctitle_xform' : False}); # Required to disable promotion of top level header to section title.

      # Remove extension from instruction filename
      filename = os.path.splitext(instruction_file)[0]
      # If filename is "Red-Hat" reformat it to "Red Hat"
      if "Red" in filename: filename = filename.replace("-"," ")

      instruction_vars = {"title" : filename + " installation instructions for Mantid.",
                         "description" : "Mantid installation instructions for " + filename + ".",
                         "instructions" : parts["html_body"]}

      env.get_template("instructions.html").stream(instruction_vars).dump(os.path.join(ROOT_DIR, "static", filename.replace(" ", "").lower() + ".html"))
