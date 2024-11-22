from rptree.rptree import _TreeGenerator

import pytest
from unittest.mock import MagicMock, patch
import pathlib

# Mock constants used in the class
ELBOW = "└──"
TEE = "├──"
PIPE = "|"
PIPE_PREFIX = "|   "
SPACE_PREFIX = "    "


@patch("pathlib.Path.iterdir")
@patch("pathlib.Path.is_dir")
def test_build_tree(mock_is_dir, mock_iterdir):
    # Mock the file structure
    root_dir = pathlib.Path("root")
    sub_dir = root_dir / "sub_dir"
    file1 = root_dir / "file1.txt"
    file2 = sub_dir / "file2.txt"

    # Define mocked behaviors
    def mock_iterdir_func(self):
        if self == root_dir:
            return [file1, sub_dir]
        elif self == sub_dir:
            return [file2]
        else:
            return []

    mock_is_dir.side_effect = lambda path: path in [root_dir, sub_dir]
    mock_iterdir.side_effect = mock_iterdir_func  # Updated to use the correct `self` argument.

    # Expected output
    expected_tree = [
        pathlib.Path(root_dir) / "",
        PIPE,
        f"{TEE} file1.txt",
        f"{ELBOW} {sub_dir.name} /",
        f"{PIPE_PREFIX}{ELBOW} file2.txt",
        f"{PIPE_PREFIX.rstrip()}",
    ]

    # Initialize and test the _TreeGenerator
    generator = _TreeGenerator(str(root_dir))
    tree = generator.build_tree()

    assert tree == expected_tree
