import requests
import os
from urllib.parse import urljoin
from functools import lru_cache

# Cache for external schemas to avoid redundant downloads
@lru_cache(maxsize=32)
def get_external_schema(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"*** Failed to fetch external schema from {url}")
    return response.json()

def resolve_ref_with_url(repo_files, ref, base_uri):
    """
    Resolve a $ref to its external schema and return the referenced schema AND the resolved URL.
    Handles both remote URLs and JSON Pointers, and recursively resolves nested $refs.
    Prioritizes base_uri for internal references to correctly handle external schemas.
    """
    if "#" in ref:
        url_part, pointer_part = ref.split("#", 1)
    else:
        url_part, pointer_part = ref, ""

    schema = None
    resolved_url = None

    # 1. External reference (Absolute URL)
    if url_part.startswith("http"):
        resolved_url = url_part
        schema = get_external_schema(resolved_url)

    # 2. Relative reference (filename provided)
    elif url_part:
        # Check if it's a file in the repo
        if url_part in repo_files and repo_files[url_part] is not None:
             if "json" in repo_files[url_part]:
                 schema = repo_files[url_part]["json"]
                 resolved_url = url_part # Use filename as base_uri for next level
             else:
                 raise ValueError(f"File {url_part} is not valid JSON")
        
        # If not in repo, try resolving against base_uri if it's an HTTP URL
        elif base_uri and base_uri.startswith("http"):
             resolved_url = urljoin(base_uri, url_part)
             schema = get_external_schema(resolved_url)
        else:
             raise ValueError(f"Could not resolve reference {ref}")

    # 3. Internal reference (url_part is empty, e.g., "#/definitions/...")
    else:
        # If we are in an external schema (base_uri is http), reuse that schema
        if base_uri and base_uri.startswith("http"):
            resolved_url = base_uri
            schema = get_external_schema(resolved_url)
        
        # If we are in a local file
        else:
            # If base_uri is a filename in repo_files, use it
            target_file = base_uri if base_uri and base_uri in repo_files else "schema.json"
            
            if target_file in repo_files and repo_files[target_file] is not None:
                if "json" in repo_files[target_file]:
                    schema = repo_files[target_file]["json"]
                    resolved_url = target_file
                else:
                    raise ValueError(f"File {target_file} is not valid JSON")
            else:
                 raise ValueError(f"Could not resolve local reference {ref} (context: {base_uri})")

    # Resolve the JSON Pointer if it exists
    if pointer_part:
        try:
            from jsonpointer import resolve_pointer
            # Ensure proper pointer format (must start with / but not double //)
            pointer = pointer_part if pointer_part.startswith("/") else "/" + pointer_part
            schema = resolve_pointer(schema, pointer)
        except Exception as e:
            raise ValueError(f"*** Failed to resolve JSON Pointer '{pointer_part}' in schema: {e}")

    return schema, resolved_url

def resolve_ref(repo_files, ref, base_uri):
    """
    Wrapper around resolve_ref_with_url to maintain backward compatibility.
    Returns only the schema.
    """
    schema, _ = resolve_ref_with_url(repo_files, ref, base_uri)
    return schema
