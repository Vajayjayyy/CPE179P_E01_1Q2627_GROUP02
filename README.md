# Edge-Optimized Container Identification for Automated Port Logistics

This repository contains the project work for container identification using computer vision and OCR. The system focuses on reading container IDs from images, validating them against ISO 6346 rules, and preparing the pipeline for automated port logistics use.

## Project structure

- `Dataset/` – exported dataset used for training and validation
- `Main Project/container-bic-ocr/` – OCR, detection, preprocessing, and validation scripts
- `Source Codes/Requirements.txt` – Python dependencies for the project

## Active sprint documentation

- [Sprint 1](./SPRINT_1.md)
- [Sprint 2](./SPRINT_2.md)

## Project goals

- Build a repeatable image preprocessing pipeline
- Detect container IDs from images
- Use OCR to read container numbers
- Validate IDs using the ISO 6346 check-digit rule
- Run the workflow efficiently for batch processing
- Produce a demo-ready and well-documented project

## Technical notes

The repository currently includes scripts such as:

- `auto_detect.py`
- `auto_detect_v2.py`
- `auto_preprocess.py`
- `batch_detection_230.py`
- `batch_preprocess.py`
- `iso_validator.py`
- `pipeline_test.py`

These scripts form the baseline for the OCR and validation pipeline. The sprints below turn that prototype work into a structured, testable project delivery.

## Sprint plan summary

### Sprint 1
Focus: environment setup, data review, and baseline verification.

See: [SPRINT_1.md](./SPRINT_1.md)

### Sprint 2
Focus: automation, robustness, evaluation, and final project packaging.

See: [SPRINT_2.md](./SPRINT_2.md)
