import re
from distutils.version import LooseVersion
from typing import Optional

from impl.static_vars import NIGHTLY_NAME_SUFFIX

# URLS
SOURCEFORGE_FILES = "https://sourceforge.net/projects/mantid/files/"
GITHUB_RELEASE_FILES = "https://github.com/mantidproject/mantid/releases/download/"

SOURCEFORGE_SAMPLES = SOURCEFORGE_FILES + "Sample%20Data/"
SOURCEFORGE_PARAVIEW = SOURCEFORGE_FILES + "ParaView/"
SOURCEFORGE_IPYTHON_NOTEBOOK = SOURCEFORGE_FILES + "IPython%20Notebook/"

# Must be in the name : downloadurl format.
SAMPLES_DATASETS = [["Usage Examples", SOURCEFORGE_SAMPLES + "UsageData.zip/download"],
                    ["ISIS", SOURCEFORGE_SAMPLES + "SampleData-ISIS.zip/download"],
                    ["ORNL", SOURCEFORGE_SAMPLES + "SampleData-ORNL.zip/download"],
                    ["Muon", SOURCEFORGE_SAMPLES + "SampleData-Muon.zip/download"],
                    ["Training", SOURCEFORGE_SAMPLES + "TrainingCourseData.zip/download"]]

IPYTHON_NOTEBOOK = [[
    "IPython Notebook Example", SOURCEFORGE_IPYTHON_NOTEBOOK +
    "Introduction%20to%20using%20Mantid%20with%20IPython%20Notebook.ipynb/download"
]]

RELEASE_NOTES_SPHINX_MIN = "3.8.0"


def get_download_url(file_name: str, version: str, is_nightly: bool) -> str:
    """
    Builds a download url for a given mantid buildname.
    This is used as the value in the 'build_names' dictionary, which is output in the jinja template.

    Args:
      buildname (str): The Mantid build name from a release file, e.g. mantid-3.1.1-win64.exe
      version (str): The version of the release, e.g. 3.1.1
      is_nightly (str): Used to determine the type of URL to build.

    Returns:
      str: The download url for a given build.
    """
    if is_nightly:
        if file_name.endswith(".dmg") or file_name.endswith(".exe"):
            return GITHUB_RELEASE_FILES + "nightly/" + file_name
        else:
            return SOURCEFORGE_FILES + "Nightly/" + file_name
    else:
        download_url = file_name + "/download"
        pattern = r"^\d\.\d+"
        found = re.search(pattern, version)
        return SOURCEFORGE_FILES + found.group(0) + "/" + download_url


def release_notes_url(version: str) -> Optional[str]:
    """Return the release notes URL for the given version"""
    if version.casefold() == NIGHTLY_NAME_SUFFIX.casefold():
        # No dedicated release notes
        return None
    elif version >= LooseVersion(RELEASE_NOTES_SPHINX_MIN):
        return f"https://docs.mantidproject.org/v{version}/release/v{version}/index.html"
    else:
        return "https://www.mantidproject.org/Category:Release_Notes"
