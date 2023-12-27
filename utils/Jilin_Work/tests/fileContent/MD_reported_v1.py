# Check whether the metadata is properly reported in schema.json

from validator_collection import checkers
from utils.utils import *

# TODO: import the function from python package by "from pysmartdatamodel.utils import *"

def is_metadata_properly_reported(output, schemaDict):
    try:
        metadata = "metadata"
        output[metadata] = {}
        if "derivedFrom" in schemaDict:
            derivedFrom = schemaDict["derivedFrom"]
            if derivedFrom != "":
                # check that it is a valid url
                if not checkers.is_url(derivedFrom):
                    output["metadata"]["derivedFrom"] = {"warning": "derivedFrom is not a valid url"}
                else:
                    if not is_url_existed(derivedFrom)[0]:
                        output["metadata"]["derivedFrom"] = {"warning": "derivedFrom url is not reachable"}
        else:
            output["metadata"]["derivedFrom"] = {"warning": "not derivedFrom clause, include derivedFrom = '' in the header"}
    except:
        output["metadata"]["derivedFrom"] = {"warning": "not possible to check derivedFrom clause, Does it exist a derivedFrom = '' clause in the header?"}

    # check that the header license is properly reported
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "license" in schemaDict:
            license = schemaDict["license"]
            if license != "":
                # check that it is a valid url
                if not checkers.is_url(license):
                    output["metadata"]["license"] = {"warning": "License is not a valid url. It should be a link to the license document"}
                else:
                    if not is_url_existed(license)[0]:
                        output["metadata"]["license"] = {"warning": "license url is not reachable"}
            else:
                output["metadata"]["license"] = {"warning": "license is empty, include a license = '' in the header "}
        else:
            output["metadata"]["license"] = {"warning": "not license clause, does it exist a license = '' in the header?"}
    except:
        output["metadata"]["license"] = {"warning": "not possible to check license clause"}

    return output
