import pytest

from impl import os_handling
from impl.os_details import OsDetails


@pytest.mark.parametrize("codename",
                         ["SnowLeopard", "Mavericks", "Mojave",
                          "mantidnightly-6.2.20220120.2323-HighSierra.dmg",
                          "mantidnightly-6.2.20220120.2323-Mojave.dmg"])
def test_valid_codename(codename):
    assert os_handling.get_osx_codename(codename)


def test_between_high_sierra_and_sierra():
    assert os_handling.get_osx_codename("Sierra") == "10.12"
    assert os_handling.get_osx_codename("HighSierra") == "10.13"


def test_missing_codename_returns_10_9():
    assert os_handling.get_osx_codename("Unknown") == "10.9"


@pytest.mark.parametrize("filename, expected",
                         [("el7", "Red Hat 7"),
                          ("bionic", "Ubuntu 18.04"),
                          ("mantidnightly-6.2.20220120.2323-1.el7.x86_64.rpm", "Red Hat 7"),
                          ("mantidnightly_6.2.20220120.2323-0ubuntu1~bionic1_amd64.deb", "Ubuntu 18.04")])
def test_identify_linux(filename, expected):
    assert os_handling.identify_linux(filename) == expected


def test_identify_windows():
    assert os_handling.identify_windows("3.1.1") == "Windows 7/8/10"
    assert os_handling.identify_windows("4.1.0") == "Windows 7/8/10"
    assert os_handling.identify_windows("4.2.0") == "Windows 10"
    assert os_handling.identify_windows("5.2.1") == "Windows 10"
    # Nightly is always Windows 10
    assert os_handling.identify_windows("nightly") == "Windows 10"


@pytest.mark.parametrize("filename, expected",
                         [("mantidnightly-6.2.20220120.2323-win64.exe",
                           OsDetails(type="Windows", name="Windows 10")),
                          ("mantidnightly-6.2.20220120.2323-HighSierra.dmg",
                           OsDetails(type="OSX", name="OSX (10.13)")),
                          ("mantidnightly-6.2.20220120.2323-1.el7.x86_64.rpm",
                           OsDetails(type="Linux", name="Red Hat 7")),
                          ("mantidnightly_6.2.20220120.2323-0ubuntu1~bionic1_amd64.deb",
                           OsDetails(type="Linux", name="Ubuntu 18.04"))])
def test_get_os(filename, expected):
    assert os_handling.get_os(filename, version="5.0.0") == expected
