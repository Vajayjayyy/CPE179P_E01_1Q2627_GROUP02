# Sprint 2

## Objective
Move from a working prototype to a more robust, automated, and evidence-based end-to-end container ID processing workflow. This sprint improves reliability, repeatability, and project readiness.

## Scope
This sprint covers:

- standardized workflow execution
- debugging and logging
- batch processing
- OCR accuracy improvement
- evaluation metrics
- user-facing project packaging

## Repository focus

- `Main Project/container-bic-ocr/`
- `Dataset/`
- `Source Codes/Requirements.txt`

## Sprint backlog

### 1) Standardize the full project pipeline
Story:
As a developer, I want a single clear workflow so the project can run from start to finish without confusion between multiple scripts.

Tasks:
- review `auto_detect.py`, `auto_detect_v2.py`, `pipeline_test.py`, and batch scripts
- define the preferred end-to-end order: preprocess → detect → OCR → validate
- document the main command or script to run the full process
- clean up confusing or duplicate execution paths

Acceptance criteria:
- one workflow is clearly established
- team members know which script is primary
- input and output folders are consistent

### 2) Improve debugging and failure handling
Story:
As a developer, I want clear logs and error messages so failed runs are easier to diagnose.

Tasks:
- review failed-image handling patterns in `inspect_failed.py`
- add clearer validation messages and logging at key pipeline stages
- save outputs for failed examples
- identify recurring failure types

Acceptance criteria:
- logs explain where a run fails
- invalid or poor-quality inputs are handled gracefully
- failed cases are easy to inspect and classify

### 3) Implement batch processing for multiple images
Story:
As a user, I want the system to process many images in one run so it is useful beyond single-sample testing.

Tasks:
- review `batch_detection_230.py` and `batch_preprocess.py`
- define a folder-based input/output workflow
- create a batch execution configuration for multiple images
- record output summaries for each processed image

Acceptance criteria:
- batch runs process multiple images in one command
- output files are organized clearly
- batch outputs can be reviewed systematically

### 4) Improve OCR accuracy and cleaning
Story:
As a project stakeholder, I want better OCR recognition so the output container IDs are more accurate and reliable.

Tasks:
- compare OCR results from different methods in the repo
- clean extracted IDs before validation
- test common OCR errors such as spacing, punctuation, or character confusion
- determine the best-performing approach for this dataset

Acceptance criteria:
- OCR output is cleaned before validation
- a recommended OCR method is identified
- improvements are measured against sample results

### 5) Add metrics and result evaluation
Story:
As a project owner, I want measurable performance results so I can judge if the project is improving and whether it is ready for demonstration.

Tasks:
- define key success metrics such as:
  - OCR success rate
  - valid ID detection rate
  - number of failed samples
  - average processing time
- record results from a sample set
- store evaluation summary in a report or output folder

Acceptance criteria:
- metrics are tracked automatically or via a repeatable script
- a result summary is produced
- the team can compare baseline and improved results

### 6) Finalize documentation and project packaging
Story:
As a user, I want clear project instructions and a polished structure so the repo is understandable and demo-ready.

Tasks:
- refine the main `README.md`
- document environment setup, run steps, and expected outputs
- add known limitations and future improvement areas
- organize scripts and result folders more clearly

Acceptance criteria:
- a user can follow the repo steps without confusion
- expected outputs are understandable
- project is ready for a demo or review

## Definition of done for Sprint 2
The sprint is complete when:
- the end-to-end workflow is defined and standardized
- batch processing works for multiple images
- failure reporting is improved
- OCR output quality is evaluated and improved where possible
- metrics are captured and reviewed
- the project is documented clearly enough for demo use

## Expected output by end of Sprint 2
A more reliable, automated, structured, and documented container ID recognition workflow suitable for project evaluation and demonstration.

## Suggested sprint review questions
- Does the project run smoothly end-to-end?
- Can multiple images be processed without manual intervention?
- Are OCR and validation results accurate enough for a demo?
- Are logs and failure handling clear?
- Is the project ready for a presentation or handoff?

## Recommended next phase after Sprint 2
After finishing Sprint 2, the team can move into:
- model optimization and accuracy tuning
- deployment or API integration
- test automation
- production-style result reporting
- live demo preparation
