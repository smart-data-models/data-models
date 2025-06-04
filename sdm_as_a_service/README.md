# Smart Data Models API and Demo

This project consists of two main components:
1. A FastAPI-based web service (`pysdm_api3.py`) that provides access to Smart Data Models functionality
2. A demo script (`demo_script2.py`) that demonstrates the API endpoints
3. A requirements file for the components use
4. A bash script to run it

## API Service (`pysdm_api3.py`)

A RESTful API that interfaces with the `pysmartdatamodels` library to provide access to Smart Data Models functionality.

### Key Features

- **Payload Validation**: Validate JSON payloads against Smart Data Models schemas
- **Data Model Exploration**: Browse subjects, data models, and their attributes
- **Search Functionality**: Find data models by exact or approximate name matching
- **Context Retrieval**: Get @context information for data models
- if you need other please email us to info @ smartdatamodels. org

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/validate-url` | GET | Validate a JSON payload from a URL against Smart Data Models |
| `/subjects` | GET | List all available subjects |
| `/datamodels/{subject_name}` | GET | List data models for a subject |
| `/datamodels/{subject_name}/{datamodel_name}/attributes` | GET | Get attributes of a data model |
| `/datamodels/{subject_name}/{datamodel_name}/example` | GET | Get an example payload of a data model |
| `/search/datamodels/{name_pattern}/{likelihood}` | GET | Search for data models by approximate name |
| `/datamodels/exact-match/{datamodel_name}` | GET | Find a data model by exact name |
| `/subjects/exact-match/{subject_name}` | GET | Check if a subject exists by exact name |
| `/datamodels/{datamodel_name}/contexts` | GET | Get @context(s) for a data model name |

### Validation Process

The `/validate-url` endpoint performs comprehensive validation:
1. Fetches JSON from the provided URL
2. Normalizes NGSI-LD payloads to key-values format
3. Extracts the payload type
4. Finds all subjects containing this type
5. Retrieves schemas for each subject
6. Validates against all schemas
7. Returns consolidated results

## Demo Script (`demo_script2.py`)

A simple interactive script that demonstrates the API endpoints by opening a series of pre-configured URLs in your default web browser.

### Features

- Opens each URL in a new browser tab
- Pauses between URLs for user input
- Allows early termination with 'exit' command
- Provides clear progress indicators

### Usage

1. Configure the URLs in the `my_web_urls` list
2. Run the script: `python demo_script2.py`
3. Follow the on-screen instructions

The demo includes examples of:
- Payload validation
- Subject listing
- Data model exploration
- Attribute retrieval
- Example payloads
- Search functionality
- Exact matching
- Context retrieval

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- httpx
- pydantic
- jsonschema
- webbrowser (standard library)

## Installation

```bash
pip install fastapi uvicorn httpx pydantic jsonschema
```

## Running the API
```bash
python pysdm_api3.py
```

## Running the demo
```bash
python demo_script2.py
```

## Configuration
Edit the my_web_urls list in demo_script2.py to change which endpoints are demonstrated.

## License
Apache 2.0
