#!/usr/bin/env python
"""pysmartdatamodels builder and installer"""
import os.path
import pathlib
from setuptools import setup, find_packages


def get_version_from_package() -> str:
    """
    Read the package version from the source without importing it.
    """
    path = os.path.join(os.path.dirname(__file__), "pysmartdatamodels/__init__.py")
    path = os.path.normpath(os.path.abspath(path))
    with open(path) as f:
        for line in f:
            if line.startswith("__version__"):
                token, version = line.split(" = ", 1)
                version = version.replace("\"", "").strip()
                return version


HERE = pathlib.Path(__file__).parent
AUTHOR = 'Collaborative, see CONTRIBUTORS.yaml in the original repositories. Coordination alberto.abella@fiware.org'
AUTHOR_EMAIL = 'info@smartdatamodels.org'
URL = 'https://github.com/smart-data-models'

LICENSE = 'Apache License 2.0 or other open source licenses'
DESCRIPTION = 'Hundreds of free data models to model your digital twins, share data in data spaces or develop smart applications'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = ["collections", "datetime", "jsonref", "jsonschema", "pytz", "requests", "sys", "validate"]

if __name__ == '__main__':
    setup(
        name="pysmartdatamodels",
        version=get_version_from_package(),
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESC_TYPE,
        author=AUTHOR,
        license=LICENSE,
        author_email=AUTHOR_EMAIL,
        url=URL,
        install_requires=INSTALL_REQUIRES,
        packages=find_packages(),
        include_package_data=True
    )
