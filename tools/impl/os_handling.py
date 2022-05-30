from distutils.version import LooseVersion

from impl.os_details import OsDetails
from impl.static_vars import NIGHTLY_NAME_SUFFIX

_OSX_CODENAME_VERSIONS = {
    'SnowLeopard': '10.6',
    'Lion': '10.7',
    'MountainLion': '10.8',
    'Mavericks': '10.9',
    'Yosemite': '10.10',
    'ElCapitan': '10.11',
    'Sierra': '10.12',
    'HighSierra': '10.13',
    'Mojave': '10.14',
    'Catalina': '10.15'
}


def get_osx_codename(filename: str) -> str:
    if "HighSierra".casefold() in filename.casefold():
        # HighSierra will match with *Sierra*. We could code some complex logic, or simply
        # hardcode this exception to the rule...
        return _OSX_CODENAME_VERSIONS["HighSierra"]

    found_version = [
        value for key, value in _OSX_CODENAME_VERSIONS.items()
        if key.casefold() in filename.casefold()
    ]

    if not found_version:
        # Assume that this is a conda-build that supports 10.9+
        return "10.9"

    return found_version[-1]


def identify_linux(filename: str) -> str:
    if "el7" in filename:
        return "Red Hat 7"
    elif "el6" in filename:
        return "Red Hat 6"
    elif "trusty" in filename:
        return "Ubuntu 14.04"
    elif "xenial" in filename:
        return "Ubuntu 16.04"
    elif "bionic" in filename:
        return "Ubuntu 18.04"
    elif filename.endswith(".deb"):
        # Last debian file name without a distribution in the filename was trusty so just print "Ubuntu"
        return "Ubuntu"
    else:
        # If you hit this, we need to add the new variant to the list above
        raise KeyError("Unknown Linux Variant")


def identify_windows(version: str) -> str:
    if NIGHTLY_NAME_SUFFIX.casefold() not in version.casefold(
    ) and LooseVersion(version) <= LooseVersion("4.1.0"):
        return "Windows 7/8/10"
    else:
        return "Windows 10"


def get_os(build_name: str, version: str) -> OsDetails:
    """
    Obtains the operating system name from a given build name.
    The osnames output as CSS classes in the 'alternative downloads' <li> in the jinja template (They are the key in the 'build_names' dict).
    This is required to allow switching of the href from the download button and the users os via JavaScript.

    Args:
      build_name (str): The name of the Mantid build for a given operating system, e.g. "mantid-2.3.2-SnowLeopard.dmg"
      version (str): The version of Mantid this build_name represents

    Returns:
      The name of the operating system and its type that the Mantid build will run on. Type={Linux,Windows,OSX}

    Raises:
      If the OS is unknown
    """
    if build_name.endswith('.tar.gz') or build_name.endswith('.tar.xz'):
        osname = "Source code"
        ostype = "Source"
    elif build_name.endswith('.exe'):
        ostype = "Windows"
        osname = identify_windows(version)
    elif build_name.endswith(".dmg"):
        ostype = "OSX"
        osname = f"OSX ({get_osx_codename(build_name)})"
    else:
        ostype = "Linux"
        osname = identify_linux(build_name)

    return OsDetails(osname, ostype)
