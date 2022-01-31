import pathlib

import pytest

from impl import static_vars


@pytest.mark.parametrize("path", [static_vars.INSTRUCTIONS_DIR, static_vars.RELEASE_DIR, static_vars.ROOT_DIR])
def test_path_exists(path):
    assert isinstance(path, pathlib.Path)
    path.resolve(strict=True)
    assert path.exists()
