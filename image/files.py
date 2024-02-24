"""
Convenient File handling utilities.

This module has some file handling functions that are available for convenience or to jog your
memory.

In your implementation of the cache, you may choose to use all, some or none of the functions
listed here.
"""

from pathlib import Path


def write(path: Path, content: bytes) -> None:
    """
    Utility function to write bytes to a file Path.

    Args:
        path: The Path of the file.
        content: The binary content.
    Raises:
        FileNotFoundError if the Path does not exist.
        PermissionError if the filesystem permissions deny the operation.
    """
    path.write_bytes(content)


def delete(path: Path) -> None:
    """
    Utility function to delete a file Path.

    Args:
        path: The Path of the file.

    Raises:
        FileNotFoundError if the Path does not exist.
    """
    path.unlink()


def exists(path: Path) -> bool:
    """
    Utility function to confirm whether a file Path exists or not.

    Args:
        path: The Path of the file.

    Raises:
        PermissionError if the filesystem permissions deny the operation.
    """
    return path.exists()
