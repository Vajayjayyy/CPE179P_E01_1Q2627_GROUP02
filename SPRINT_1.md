# Sprint 1

## Objective
Build a working baseline for the container ID recognition project and verify that the model pipeline, preprocessing flow, and validation logic function correctly.

## Scope
This sprint covers the foundation of the project:

- project setup
- dataset inspection
- baseline model execution
- preprocessing verification
- validation logic review
- documentation of current blockers and results

## Repository focus

- `Dataset/` for dataset understanding
- `Main Project/container-bic-ocr/` for scripts and pipeline logic
- `Source Codes/Requirements.txt` for environment dependencies

## Sprint backlog

### 1) Environment and dependency setup
Story:
As a developer, I want a repeatable Python environment so the project can run consistently across machines.

Tasks:
- install the required Python packages from `Source Codes/Requirements.txt`
- create a virtual environment
- confirm that the main scripts run without missing dependencies
- document setup commands for future team members

Acceptance criteria:
- the environment installs successfully
- at least one script runs in the environment without import errors
- setup instructions are stored in the repo

### 2) Dataset analysis and quality review
Story:
As a team member, I want to understand the dataset to ensure the model is trained and tested on usable samples.

Tasks:
- inspect `Dataset/README.md`
- review image count and annotation format
- identify data quality issues, missing labels, or incomplete image sets
- document assumptions about dataset structure

Acceptance criteria:
- dataset structure is summarized
- at least one known issue or gap is documented
- the team understands how dataset images are intended to be used

### 3) Reproduce the current OCR pipeline
Story:
As a developer, I want to validate the current end-to-end OCR pipeline so we know what works before improving it.

Tasks:
- run `pipeline_test.py`
- run other relevant scripts such as `auto_detect.py` and `easyocr_test.py`
- record outputs, errors, and confidence issues
- determine which stage fails or produces weak results

Acceptance criteria:
- the pipeline can be run from the repo
- output is captured for comparison
- failure points are documented

### 4) Preprocessing baseline verification
Story:
As a developer, I want to verify the image preprocessing workflow so OCR results are consistent and repeatable.

Tasks:
- review `auto_preprocess.py`, `batch_preprocess.py`, and related scripts
- confirm resizing and normalization logic
- validate on sample container images
- check if preprocessing produces better OCR input quality

Acceptance criteria:
- preprocessing steps are documented
- sample images are processed successfully
- output quality is reviewed and recorded

### 5) ISO validation check-digit review
Story:
As a project stakeholder, I want a reliable container validation rule so detected IDs can be accepted only when they conform to the correct standard.

Tasks:
- inspect `iso_validator.py`
- review the validation pattern and check-digit logic
- test valid and invalid examples
- confirm which container IDs are accepted or rejected

Acceptance criteria:
- valid ISO 6346 IDs pass validation
- invalid IDs fail validation
- edge cases are documented

### 6) Baseline documentation and sprint handoff
Story:
As a team, we need a clear summary of the current state so the next sprint can focus on improvements instead of re-discovery.

Tasks:
- summarize what works
- list blockers and technical limitations
- prepare a sprint review note
- identify improvements for Sprint 2

Acceptance criteria:
- a project status summary exists
- key issues are tracked
- next actions are prioritized

## Definition of done for Sprint 1
The sprint is complete when:
- Python dependencies are working
- dataset structure is understood
- baseline OCR pipeline is run successfully or its failures are documented
- preprocessing workflow has been reviewed
- validation logic has been checked against real examples
- a summary of current results is available for the team

## Expected output by end of Sprint 1
A stable baseline project state that clearly shows:
- what is already implemented
- what is working
- what is failing
- what should be improved next

## Suggested sprint review questions
- Can the repo be set up easily by another developer?
- Does the current OCR workflow produce usable output?
- Are preprocessing steps consistent and dependable?
- Is validation logic correct and explainable?
- What should be prioritized in Sprint 2?
