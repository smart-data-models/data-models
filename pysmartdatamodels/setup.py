import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.2.3'
PACKAGE_NAME = 'pysmartdatamodels'
AUTHOR = 'Collaborative, see CONTRIBUTORS.yaml in the original repositories. Coordination alberto.abella@fiware.org'
AUTHOR_EMAIL = 'info@smartdatamodels.org'
URL = 'https://github.com/smart-data-models'

LICENSE = 'Apache License 2.0 or other open source licenses'
DESCRIPTION = 'Hundreds of free data models to model your digital twins, share data in data spaces or develop smart applications'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = ["collections", "json", "jsonref", "jsonschema", "pytz", "requests", "sys", "validate", "datetime"]

setup(name=PACKAGE_NAME,
      version=VERSION,
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
