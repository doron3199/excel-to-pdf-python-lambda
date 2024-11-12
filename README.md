# excel-to-pdf-python-lambda

This project provides an AWS Lambda function in Python 3.12 that converts Excel files to PDFs using Docker and LibreOffice.

## Overview

This repository contains the following components:

- **Dockerfile**: Defines the container environment for AWS Lambda, including dependencies for running LibreOffice.
- **Python Files**:
  - `excel_to_pdf.py`: The main script called by the AWS Lambda function, which triggers the conversion process.
  - `excel_to_pdf_runner.py`: A secondary script executed within the LibreOffice Python runtime to facilitate PDF export.

## Usage

While it’s possible to use LibreOffice’s command-line interface directly within the Docker container to convert files without Python scripts, doing so with the standard command:

```sh
libreoffice --headless --convert-to pdf:file_name_export file_name.xlsx
```

may produce PDFs that do not render optimally. These provided Python scripts address this by simulating a more controlled process in LibreOffice, ensuring each sheet in the Excel file is converted into a separate page in the final PDF.

### Dual Python Runtimes

The project utilizes two different Python runtimes:

1. **AWS Python Runtime (3.12)**: Used for the main Lambda function (`excel_to_pdf.py`).
2. **LibreOffice Python Runtime**: Used within the LibreOffice environment to handle more complex actions.

Using separate runtimes allows LibreOffice's built-in Python to access specific libraries, which may not be directly compatible with the standard AWS Python runtime. If you’d like, you’re welcome to explore consolidating these into a single runtime, though this has presented compatibility challenges in the current setup.
