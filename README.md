
# LabTrace - Laboratory Sample Tracking System

LabTrace is a laboratory sample management application built with Python, Streamlit, and SQLite.

It helps laboratory personnel organize and monitor laboratory samples by providing a centralized system for registering specimens, viewing records, searching samples, updating processing statuses, and managing sample information.

The application also provides a summary dashboard that displays the total number of registered samples and their distribution across different processing stages.

## Features

- Sample management dashboard
- Total number of registered samples
- Sample distribution by processing status
- Laboratory sample registration
- Sample listing and record retrieval
- Search samples by Sample ID or sample type
- Update sample processing status
- Delete samples with confirmation
- Sample input validation
- Unique Sample ID enforcement
- Processing status validation
- SQLite database storage
- Persistent sample records
- Database error handling

## Technologies Used

- Python
- Streamlit
- SQLite
- Regular Expressions
- Object-Oriented Programming
- Git and GitHub

## Project Structure

```text
LabTrace/
│
├── main.py
├── database.py
├── sample.py
├── labtrace.db
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/JohnnyKhayo/labtrace.git
```

### 2. Navigate into the project directory

```bash
cd LabTrace
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run main.py
```

The application will open in your default web browser.

## Application Architecture

LabTrace separates its responsibilities into three main Python modules.

### main.py

Handles the Streamlit user interface and application logic.

It includes:

- Sample listing and searching
- Sample registration forms
- Sample status update controls
- Sample deletion with confirmation
- Summary statistics
- User input handling and feedback messages

### database.py

Handles SQLite database operations, including:

- Establishing database connections
- Initializing the samples table
- Adding new sample records
- Retrieving registered samples
- Updating sample statuses
- Deleting sample records

### sample.py

Contains the `Sample` class and sample validation logic.

It is responsible for:

- Representing individual laboratory samples
- Validating sample identifiers
- Checking required sample information
- Validating processing statuses
- Managing sample status transitions

## Database

LabTrace uses SQLite to store laboratory sample records.

The `samples` table contains the following fields:

| Field | Description |
|---|---|
| ID | Unique database record identifier |
| Sample ID | Unique laboratory sample identifier |
| Sample Type | Type of laboratory specimen |
| Collected By | Person responsible for collecting the specimen |
| Status | Current sample processing status |
| Notes | Optional additional sample information |

SQLite provides persistent local storage without requiring a separate database server.

## Sample Processing Workflow

Each registered sample is assigned a processing status to help monitor its progress through the laboratory.

The application supports four statuses:

- **Collected:** The sample has been registered in the system.
- **Processing:** The sample is undergoing laboratory processing.
- **Completed:** Processing has been completed.
- **Archived:** The sample has reached the archived stage.

The `Sample` class defines the permitted statuses and validates status changes.

## Sample Validation

Sample records are validated before being added to the database.

Validation checks include:

- Sample IDs must not be empty.
- Sample IDs can only contain letters, numbers, and hyphens.
- Sample type must be provided.
- Sample type must contain at least one letter.
- Collector information must be provided.
- Collector information must contain at least one letter.
- Sample status must be one of the predefined statuses.

The database also enforces constraints such as unique Sample IDs and non-null required fields.

## Search and Filtering

The application provides a search field that allows users to find registered samples using:

- Sample ID
- Sample type

Searches are case-insensitive, making it easier to locate records without needing to match the exact capitalization.

## Summary Dashboard

The summary section provides an overview of registered laboratory samples.

It displays:

- Total number of registered samples
- Number of samples in each processing status

This provides a quick overview of sample distribution across the laboratory workflow.

## Future Improvements

- Sample collection date and time tracking
- Sample rejection and rejection reasons
- Advanced search and filtering
- Export sample records to CSV
- Dashboard charts and visual analytics
- User authentication and access control
- Sample processing history
- Laboratory staff management
- Database backup and recovery
- Automated testing

## License

This project is licensed under the MIT License. Feel free to use and modify this script as you see fit.