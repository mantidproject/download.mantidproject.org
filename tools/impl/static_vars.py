import pathlib
import git

# Repo folder structure
ROOT_DIR = pathlib.Path(git.Repo(".", search_parent_directories=True).working_tree_dir)
RELEASE_DIR = ROOT_DIR / "releases"
INSTRUCTIONS_DIR = ROOT_DIR / "instructions"

NIGHTLY_NAME_SUFFIX = "nightly"
