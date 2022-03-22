import re
import datetime
from pathlib import Path
from typing import Optional, List

from dateutil import parser

from impl.os_handling import get_os
from impl.package_details import PackageDetails
from impl.release_info import ReleaseInfo
from impl.static_vars import RELEASE_DIR, NIGHTLY_NAME_SUFFIX
from impl.url_handling import get_download_url


def get_nightly_date(package_name: str) -> Optional[datetime.date]:
    split_names = package_name.split('.')
    for name in split_names:
        try:
            date = parser.isoparse(name)
            return date.date()  # drop time data
        except ValueError:
            pass


def format_release_str(release_str: str) -> str:
    """
    Takes a release string, and formats it using the convention we use elsewhere
    in Mantid, for example DOI's.  Essentially, the patch number is removed if
    it is zero.  I.e. 2.1.0 becomes 2.1, 3.0.0 becomes 3.0, but 3.0 is left alone.

    Args:
      release_str (str) :: the release string to format.

    Returns:
      str: the formatted release string
    """
    if re.match(r"\d\.\d\.0", release_str):
        return release_str[:-2]
    return release_str


def _parse_build_names(file_path: Path) -> List[ReleaseInfo]:
    """
    Parses a file that contains build names (e.g. those in /releases/) and stores the contents in a dictionary.
    The key of the dictionary is the operating system, which is obtained based on the build's file extension.
    The date on the first line is optional, if it is not present the date is extracted from the first filename if
    possible, else it raises an error.

    Args:
      file_path (str): The location of the release file to parse.

    Returns:
      List[ReleaseInfo] object containing details about a release
    """
    file_name = file_path.name
    is_nightly = NIGHTLY_NAME_SUFFIX.casefold() in file_name.casefold()

    if is_nightly:
        version = "nightly"
    else:
        version = file_path.with_suffix("").name

    formatted_version = None if is_nightly else format_release_str(version)

    with open(file_path) as handle:
        # Strip and get non-empty lines
        parsed_file_names = [line.strip() for line in handle if line.strip()]

    # All non-nightly files have the date as their first line and they will all be on the same date
    if not is_nightly:
        release_date = datetime.date.fromisoformat(parsed_file_names.pop(0))
        # For an official release we have a single ReleaseInfo and multiple packages
        package_details: List[PackageDetails] = []
        for executable_name in parsed_file_names:
            package_details.append(
                PackageDetails(os_details=get_os(executable_name, version),
                               download_url=get_download_url(executable_name, version, is_nightly)))
        releases = [
            ReleaseInfo(date=release_date,
                        version=version,
                        formatted_version=formatted_version,
                        package_details=package_details)
        ]
    else:
        # For nightlies we have separate releases per file as sometimes not all builds complete
        releases: List[ReleaseInfo] = []
        for filename in parsed_file_names:
            releases.append(
                ReleaseInfo(date=get_nightly_date(filename),
                            version=version,
                            package_details=[
                                PackageDetails(os_details=get_os(filename, version),
                                               download_url=get_download_url(
                                                   filename, version, is_nightly))
                            ]))

    return releases


def get_nightly_releases() -> List[ReleaseInfo]:
    """
    Reads and stores release information for the nightly build from the nightly text file in the releases folder.

    Returns:
      list: A list that contains release information for each release. The list is sorted by release date.
    """
    filename = [name for name in RELEASE_DIR.iterdir() if NIGHTLY_NAME_SUFFIX in str(name)]
    assert len(filename) == 1
    return _parse_build_names(filename[0])


def get_mantid_releases() -> List[ReleaseInfo]:
    """
    Reads and stores release information for each release file in the releases folder.
    This does not include the nightly build.

    Returns:
      list: A list that contains release information for each release. The list is sorted by release date.
    """
    releases: List[ReleaseInfo] = []
    release_files = [path for path in RELEASE_DIR.iterdir() if NIGHTLY_NAME_SUFFIX not in str(path)]
    for release_txt_file in release_files:
        releases.extend(_parse_build_names(release_txt_file))

    return sorted(releases, key=lambda k: k.date, reverse=True)
