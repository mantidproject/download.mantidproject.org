import datetime

import pytest

from impl import release_parsing
from impl.os_details import OsDetails
from impl.package_details import PackageDetails
from impl.release_info import ReleaseInfo


@pytest.mark.parametrize("filename, expected",
                         [("mantidnightly-6.2.20211009.2323-1.el7.x86_64.rpm",
                           datetime.date(year=2021, month=10, day=9)),
                          ("mantidnightly-6.2.20220120.2323-1.el7.x86_64.rpm",
                           datetime.date(year=2022, month=1, day=20)),
                          ("mantidnightly_6.2.20220120.1649-0ubuntu1~bionic1_amd64.deb",
                           datetime.date(year=2022, month=1, day=20)),
                          ("mantidnightly_6.2.1.20220120.1649-0ubuntu1~bionic1_amd64.deb",
                           datetime.date(year=2022, month=1, day=20)),
                          ("mantidnightly-6.2.20220120.1649-win64.exe", datetime.date(year=2022, month=1, day=20)),
                          # Malformed cases
                          ("mantid_6.20220120.1649-0ubuntu1~bionic1_amd64.deb",
                           datetime.date(year=2022, month=1, day=20)),
                          ("mantid.20220120.1649-0ubuntu1~bionic1_amd64.deb",
                           datetime.date(year=2022, month=1, day=20))])
def test_get_date_can_handle_filenames(filename, expected):
    assert release_parsing.get_nightly_date(filename) == expected


@pytest.mark.parametrize("filename",
                         ["mantidnightly-6.2", "mantid-6.2", "mantid-6.2.1",
                          "mantidnightly-6.2.deb", "mantid-6.2.exe", "mantid-6.2.1.rpm"])
def test_without_date_time(filename):
    assert release_parsing.get_nightly_date(filename) is None


def test_mantid_nightly():
    nightlies = release_parsing.get_nightly_releases()
    for found in nightlies:
        assert isinstance(found, ReleaseInfo)
        assert found.version == "nightly"
        assert all("Nightly" in i.download_url for i in found.package_details)
        assert found.release_notes_url is None


def test_mantid_releases():
    found = release_parsing.get_mantid_releases()
    assert len(found) > 20
    assert all(isinstance(i, ReleaseInfo) for i in found)

    # Pick two random packages to ensure the format doesn't change
    assert ReleaseInfo(date=datetime.date(2021, 9, 29), version='6.2.0', package_details=[
        PackageDetails(download_url='https://sourceforge.net/projects/mantid/files/6.2/mantid-6.2.0-win64.exe/download',
                       os_details=OsDetails(name='Windows 10', type='Windows')), PackageDetails(
            download_url='https://sourceforge.net/projects/mantid/files/6.2/mantid-6.2.0-HighSierra.dmg/download',
            os_details=OsDetails(name='OSX (10.13)', type='OSX')), PackageDetails(
            download_url='https://sourceforge.net/projects/mantid/files/6.2/mantid-6.2.0-1.el7.x86_64.rpm/download',
            os_details=OsDetails(name='Red Hat 7', type='Linux')), PackageDetails(
            download_url='https://sourceforge.net/projects/mantid/files/6.2/mantid_6.2.0-0ubuntu1~bionic1_amd64.deb/download',
            os_details=OsDetails(name='Ubuntu 18.04', type='Linux')), PackageDetails(
            download_url='https://sourceforge.net/projects/mantid/files/6.2/mantid-6.2.0-Source.tar.xz/download',
            os_details=OsDetails(name='Source code', type='Source'))], formatted_version='6.2',
                       release_notes_url=None) in found

    assert ReleaseInfo(date=datetime.date(2015, 5, 18), version='3.4.0', package_details=[
        PackageDetails(download_url='https://sourceforge.net/projects/mantid/files/3.4/mantid-3.4.0-win64.exe/download',
                       os_details=OsDetails(name='Windows 7/8/10', type='Windows')), PackageDetails(
            download_url='https://sourceforge.net/projects/mantid/files/3.4/mantid-3.4.0-Mavericks.dmg/download',
            os_details=OsDetails(name='OSX (10.9)', type='OSX')), PackageDetails(
            download_url='https://sourceforge.net/projects/mantid/files/3.4/mantid-3.4.0-1.el6.x86_64.rpm/download',
            os_details=OsDetails(name='Red Hat 6', type='Linux')), PackageDetails(
            download_url='https://sourceforge.net/projects/mantid/files/3.4/mantid_3.4.0-1_amd64.deb/download',
            os_details=OsDetails(name='Ubuntu', type='Linux')), PackageDetails(
            download_url='https://sourceforge.net/projects/mantid/files/3.4/mantid-3.4.0-Source.tar.gz/download',
            os_details=OsDetails(name='Source code', type='Source'))], formatted_version='3.4',
                       release_notes_url=None) in found
