import os
import json

from typing import Union


def get_json(path: str) -> dict:
    """
    Returns the JSON file pointed by ``path``.

    :param path: path to the JSON file
    :type path: ``str``

    :return: content of the JSON file
    :rtype: ``dict``
    """

    return json.load(open(path))


def get_file_path(path: str, extension: str, number: int = 1) -> Union[list, str]:
    """
    Search in ``path`` for files of type ``extension`` and returns the first ``number`` files.

    :param path: target path
    :type path: ``str``
    :param extension: extension of files to be returned
    :type extension: ``str``
    :param number: number of files to be returned, passing "0" will return all found files
    :type number: ``int``

    :return: a list of filenames or a filename if ``number`` equals 1
    :rtype: ``list[str]`` or ``str``
    """

    list_of_files = [f for f in os.listdir(path) if f.endswith(extension)]

    if number == 0:
        return list_of_files
    elif number == 1:
        return list_of_files[0]
    else:
        return list_of_files[:number]
