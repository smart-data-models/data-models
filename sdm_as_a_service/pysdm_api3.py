from pysmartdatamodels import pysmartdatamodels as sdm # Assuming this is how you import your main functions
from fastapi import FastAPI,  HTTPException, Body
from pydantic import HttpUrl, BaseModel
import httpx
from typing import List, Optional, Dict, Any
from jsonschema import validate, ValidationError


app = FastAPI(
    title="Smart Data Models API",
    description="An API for accessing and interacting with Smart Data Models.",
    version="1.0.0"
)


class ValidationResult(BaseModel):
    valid: bool
    payload_url: str
    payload_type: str
    found_subjects: List[str]
    schemas_checked: List[str]
    validation_details: List[Dict[str, Any]]
    all_valid: bool
    payload: dict


import json


def is_ngsi_ld_normalized(payload: dict) -> bool:
    """
    Accurate NGSI-LD normalized format detection for single entities
    """
    try:
        if not isinstance(payload, dict):
            return False
        if 'id' not in payload or 'type' not in payload:
            return False
        for key, value in payload.items():
            if key in ['id', 'type', '@context']:
                continue
            if not isinstance(value, dict):
                return False
            if 'type' not in value:
                return False
            if not any(v in value for v in ['value', '@value', 'object']):
                return False
        return True
    except Exception:
        return False


def normalize_to_keyvalues(payload: dict) -> dict:
    """
    Convert single NGSI-LD entity to key-values format with proper date handling
    """
    if not is_ngsi_ld_normalized(payload):
        return payload

    keyvalues = {
        'id': payload['id'],
        'type': payload['type']
    }

    if '@context' in payload:
        keyvalues['@context'] = payload['@context']

    for attr_name, attr_value in payload.items():
        if attr_name in ['id', 'type', '@context']:
            continue

        if isinstance(attr_value, dict):
            # Special handling for DateTime values
            if 'value' in attr_value and isinstance(attr_value['value'], dict):
                if '@type' in attr_value['value'] and attr_value['value']['@type'] == 'DateTime':
                    keyvalues[attr_name] = attr_value['value']['@value']
                    continue

            # Handle regular properties
            if 'value' in attr_value:
                keyvalues[attr_name] = attr_value['value']
            elif '@value' in attr_value:
                keyvalues[attr_name] = attr_value['@value']
            elif 'object' in attr_value:  # For relationships
                keyvalues[attr_name] = attr_value['object']
            else:
                keyvalues[attr_name] = attr_value
        else:
            keyvalues[attr_name] = attr_value

    return keyvalues
async def fetch_json(url: str) -> Dict[str, Any]:
    """Fetch JSON from a URL with error handling"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to fetch payload from URL: {str(e)}"
            )
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid JSON received from URL: {str(e)}"
            )


@app.get("/validate-url")
async def validate_payload_from_url(
        url: str
) -> ValidationResult:
    """
    Validate a JSON payload from a URL against Smart Data Models.

    Full process:
    1. Fetch JSON from URL
    2. Extract 'type' attribute
    3. Find all subjects containing this type
    4. Retrieve schemas for each subject
    5. Validate against all schemas
    6. Return consolidated results

    Example: /validate-url?url=https://example.com/payload.json
    """
    try:
        # Step 1: Fetch payload
        raw_payload = await fetch_json(url)

        # Example usage (you would get the payload from your actual variable)
        try:
            # Try to parse the payload if it's a JSON string
            if isinstance(raw_payload, str):
                raw_payload = json.loads(raw_payload)
        except json.JSONDecodeError:
            pass  # Not a JSON string, assume it's already a dict or other format

        # Process the payload
        payload = normalize_to_keyvalues(raw_payload) if is_ngsi_ld_normalized(raw_payload) else raw_payload

        # Step 2: Extract type
        payload_type = payload.get('type')
        if not payload_type:
            raise HTTPException(
                status_code=400,
                detail="Payload must contain a 'type' attribute"
            )

        # Step 3: Find matching subjects
        all_models = sdm.load_all_datamodels()
        if not all_models:
            raise HTTPException(
                status_code=503,
                detail="Could not load Smart Data Models repository"
            )

        matching_subjects = [
            model["repoName"] for model in all_models
            if payload_type in model.get("dataModels", [])
        ]

        if not matching_subjects:
            return ValidationResult(
                valid=False,
                payload_url=url,
                payload_type=payload_type,
                found_subjects=[],
                schemas_checked=[],
                validation_details=[],
                all_valid=False,
                payload = payload
            )

        # Step 4-5: Validate against each schema
        validation_details = []
        all_valid = True

        async with httpx.AsyncClient() as client:
            for subject in matching_subjects:
                try:
                    # Get schema URL
                    metadata = sdm.list_datamodel_metadata(payload_type, subject)
                    if not metadata or not metadata.get("jsonSchemaUrl"):
                        validation_details.append({
                            "subject": subject,
                            "status": "missing_schema",
                            "error": "No schema URL found"
                        })
                        all_valid = False
                        continue

                    schema_url = metadata["jsonSchemaUrl"]

                    # Fetch and validate schema
                    schema = await fetch_json(schema_url)
                    try:
                        validate(instance=payload, schema=schema)
                        validation_details.append({
                            "subject": subject,
                            "schema_url": schema_url,
                            "status": "valid"
                        })
                    except ValidationError as e:
                        validation_details.append({
                            "subject": subject,
                            "schema_url": schema_url,
                            "status": "invalid",
                            "error": str(e),
                            "error_path": list(e.path)
                        })
                        all_valid = False

                except Exception as e:
                    validation_details.append({
                        "subject": subject,
                        "status": "error",
                        "error": str(e)
                    })
                    all_valid = False

        # Step 6: Return results
        return ValidationResult(
            valid=all_valid,
            payload_url=url,
            payload_type=payload_type,
            found_subjects=matching_subjects,
            schemas_checked=[d["schema_url"] for d in validation_details
                             if "schema_url" in d],
            validation_details=validation_details,
            all_valid=all_valid,
            payload=payload
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@app.get("/subjects", summary="List all available subjects")
async def list_subjects():
    """
    Retrieves a list of all available subjects in the Smart Data Models.
    """
    try:
        subjects = sdm.list_all_subjects() # Replace with actual function call
        return {"subjects": subjects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/datamodels/{subject_name}", summary="List data models for a subject")
async def list_datamodels_for_subject(subject_name: str):
    """
    Retrieves a list of all data models available for the given subject.
    """
    try:
        # Check if subject exists (optional, but good practice)
        # all_subjects = sdm.list_subjects()
        # if subject_name not in all_subjects:
        #     raise HTTPException(status_code=404, detail=f"Subject '{subject_name}' not found.")

        datamodels = sdm.datamodels_subject(subject_name) # Replace with actual function call
        if not datamodels: # If the function returns an empty list for a non-existent/empty subject
            raise HTTPException(status_code=404, detail=f"No data models found for subject '{subject_name}' or subject does not exist.")
        return {"subject": subject_name, "data_models": datamodels}
    except Exception as e:
        # More specific error handling can be added here based on pysmartdatamodels exceptions
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/datamodels/{subject_name}/{datamodel_name}/attributes", summary="Get attributes of a data model")
async def get_datamodel_attributes(subject_name: str, datamodel_name: str):
    """
    Retrieves the attributes for a specific data model.
    """
    try:
        attributes = sdm.attributes_datamodel(subject_name, datamodel_name) # Replace with actual function call
        if attributes is None: # Or however your function indicates "not found"
            raise HTTPException(status_code=404, detail=f"Data model '{datamodel_name}' in subject '{subject_name}' not found or has no attributes.")
        return {"subject": subject_name, "data_model": datamodel_name, "attributes": attributes}
    except FileNotFoundError: # Example of specific exception handling
        raise HTTPException(status_code=404, detail=f"Schema file not found for {subject_name}/{datamodel_name}.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/datamodels/{subject_name}/{datamodel_name}/example", summary="Get an example payload of a data model")
async def get_datamodel_example(subject_name: str, datamodel_name: str):
    """
    Retrieves an example payload (NGSI-LD by default, or harmonised if specified)
    for a specific data model.
    """
    try:
        # Assuming your function might look like: sdm.example_payload(subject, datamodel, harmonised=False)
        schema = sdm.list_datamodel_metadata(datamodel_name, subject_name)
        schemaurl = schema["jsonSchemaUrl"]
        example = sdm.ngsi_ld_example_generator(schemaurl) # Replace with actual function call
        if example is None: # Or however your function indicates "not found"
            raise HTTPException(status_code=404, detail=f"Example for data model '{datamodel_name}' in subject '{subject_name}' not found.")
        return {"subject": subject_name, "data_model": datamodel_name, "example": example}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Schema or example file not found for {subject_name}/{datamodel_name}.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 1) Function to look for a data model given an approximate name
@app.get("/search/datamodels/{name_pattern}/{likelihood}", summary="Search for data models by approximate name, optionally with likelihood")
async def search_datamodels_by_approximate_name(
        name_pattern: str,
        likelihood: int
):
    """
    Searches for data models based on an approximate name or pattern.
    Optionally accepts a 'likelihood' parameter (0-100).
    This maps to `pysmartdatamodels.look_for_datamodel(pattern, [likelihood=value,] official_list=False, verbose=False)`.
    """
    try:
        # Prepare arguments for the sdm.look_for_datamodel function
        likelihood = int(likelihood)

        if likelihood is not None:
            # IMPORTANT: The standard pysmartdatamodels.look_for_datamodel function
            # in the public repository (as of June 2025) does NOT accept a 'likelihood' parameter.
            # It uses a fixed cutoff for difflib.get_close_matches.
            # This implementation passes 'likelihood' as a keyword argument
            # assuming you are using a version of the pysmartdatamodels library
            # that supports this parameter, as per your specific instruction.
            # If not, this call might raise a TypeError.
            if likelihood < 0 or likelihood > 100:
                return {"query": name_pattern, "matches_found": 0,  "results": "wrong likelihood"}

        matching_models = sdm.look_for_datamodel(name_pattern, likelihood)

        # Prepare the base response payload
        response_payload = {
            "query": name_pattern,
            "matches_found": 0,
            "results": []
        }

        if not matching_models:  # Handles None or empty list from sdm function
            return response_payload

        response_payload["matches_found"] = len(matching_models)
        response_payload["results"] = matching_models
        return response_payload

    except TypeError as te:  # Catch potential TypeError if 'likelihood' is an unexpected kwarg
        print(
            f"TypeError in /search/datamodels: {te}. This might be due to the 'likelihood' parameter not being supported by your version of pysmartdatamodels.look_for_datamodel.")
        raise HTTPException(status_code=501, detail=f"Server-side configuration error with search function: {str(te)}")
    except Exception as e:
        print(f"Error in /search/datamodels: {e}")
        raise HTTPException(status_code=500, detail=f"Error during data model search: {str(e)}")

# 2) Function to look for a data model based on the exact name
@app.get("/datamodels/exact-match/{datamodel_name}", summary="Find a specific data model by exact subject and model name")
async def get_datamodel_by_exact_name(datamodel_name: str):
    """
    Retrieves the full information for a data model if it exactly matches the given subject and data model name.
    Uses `pysmartdatamodels.load_all_datamodels()` and filters the result.
    """
    try:
        all_models_data = sdm.load_all_datamodels()
        if not all_models_data:
            raise HTTPException(status_code=404, detail="No data models loaded or available.")
        found_subjects = []
        for model_info in all_models_data:
            if model_info.get("dataModels"):
                for datamodel in model_info.get("dataModels"):
                    if datamodel == datamodel_name:
                        found_subjects.append(model_info.get("repoName"))
        if found_subjects:
            return {"match_found": True, "subjects": found_subjects}
        else:
            return {"match_found": False, "data_model_info": datamodel_name}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in /datamodels/exact-match: {e}")
        raise HTTPException(status_code=500, detail=f"Error finding exact data model: {str(e)}")

# 3) Function to look for a subject based on the exact name
@app.get("/subjects/exact-match/{subject_name}", summary="Check if a subject exists by exact name")
async def get_subject_by_exact_name(subject_name: str ):
    """
    Checks if a subject with the exact given name exists.
    Uses `pysmartdatamodels.load_all_datamodels()` and checks for the subject's presence.
    """
    try:
        all_models_data = sdm.load_all_datamodels()
        if not all_models_data:
            return {"subject_name": subject_name, "exists": False, "message": "No subjects loaded or available."}

        for model_info in all_models_data:
            if model_info.get("repoName") == subject_name:
                return {"subject_name": subject_name, "exists": True, "message": f"Subject '{subject_name}' found."}

        return {"subject_name": subject_name, "exists": False, "message": f"Subject '{subject_name}' not found."}
    except Exception as e:
        print(f"Error in /subjects/exact-match: {e}")
        raise HTTPException(status_code=500, detail=f"Error checking subject existence: {str(e)}")

# 4) Function to give the @context once given the data model
@app.get("/datamodels/{datamodel_name}/contexts", summary="Get @context(s) for a data model name across all subjects")
async def get_datamodel_contexts(datamodel_name: str):
    """
    Retrieves the "@context" object for all occurrences of a specific data model name,
    searching across all subjects.
    Uses `pysmartdatamodels.load_all_datamodels()` to find subjects and
    `pysmartdatamodels.list_datamodel_metadata(dataModel, subject)` for each.
    """
    found_contexts = []
    try:
        all_models_data = sdm.load_all_datamodels()
        if not all_models_data:
            # This case implies the entire SDM repository is empty or inaccessible
            raise HTTPException(status_code=503, detail="Could not load any data models from the source.")

        # Filter for models matching the datamodel_name
        matching_models_info = [
            model_info for model_info in all_models_data
            if datamodel_name in model_info.get("dataModels")
        ]

        if not matching_models_info:
            raise HTTPException(status_code=404, detail=f"Data model named '{datamodel_name}' not found in any subject.")

        for model_info in matching_models_info:
            current_subject_name = model_info.get("repoName")
            try:
                # The function is list_datamodel_metadata(dataModel, subject)
                metadata = sdm.list_datamodel_metadata(datamodel_name, current_subject_name)
                if metadata:
                    model_context = metadata.get("@context")
                    if model_context is not None: # Check for None explicitly, as empty context {} could be valid
                        found_contexts.append({
                            "subject": current_subject_name,
                            "data_model": datamodel_name,
                            "@context": model_context
                        })
                # If metadata is None or context is None for a specific subject/model, we just skip it.
                # The user is interested in successfully retrieved contexts.
            except FileNotFoundError:
                # Log this, but don't stop the process for other subjects
                print(f"Metadata file not found for {datamodel_name} in subject {current_subject_name}. Skipping.")
            except Exception as e_inner:
                # Log other errors during metadata retrieval for a specific model, but continue
                print(f"Error retrieving metadata for {datamodel_name} in subject {current_subject_name}: {e_inner}. Skipping.")

        # If matching_models_info was not empty, but found_contexts is,
        # it means the model(s) existed but none had a retrievable '@context'.
        # In this case, returning an empty list is appropriate (HTTP 200).
        return found_contexts

    except HTTPException: # Re-raise HTTPExceptions (like the 404 or 503 above)
        raise
    except Exception as e: # Catch-all for unexpected errors during the process
        print(f"Error in /datamodels/{datamodel_name}/contexts: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred while retrieving contexts: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)