import pytest

from impl import url_handling


def test_download_url_nightly():
    build_name = "foo_bar.xyz"
    url = url_handling.get_download_url(build_name, version="", is_nightly=True)
    assert url == f"https://sourceforge.net/projects/mantid/files/Nightly/{build_name}"


@pytest.mark.parametrize("version", ["5.0.0", "5.0.1", "5.0.2"])
def test_download_url_main(version):
    build_name = "bar_main.xyz"
    url = url_handling.get_download_url(build_name, version=version, is_nightly=False)
    assert url == f"https://sourceforge.net/projects/mantid/files/5.0/{build_name}/download"


def test_release_notes_url():
    assert url_handling.release_notes_url("3.7.0") == "https://www.mantidproject.org/Category:Release_Notes"
    assert url_handling.release_notes_url("3.8.0") == "https://docs.mantidproject.org/v3.8.0/release/v3.8.0/index.html"
    assert url_handling.release_notes_url("5.1.1") == "https://docs.mantidproject.org/v5.1.1/release/v5.1.1/index.html"
