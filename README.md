# NYU DevOps Project Template
3
## Products
[![Build Status](https://github.com/CSCI-GA-2820-SP25-001/products/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP25-001/products/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP25-001/products/graph/badge.svg?token=2KQNKIJORH)](https://codecov.io/gh/CSCI-GA-2820-SP25-001/products)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

## Overview

This is a starter template for the NYU DevOps course project. It includes:

Flask-based service with /service directory

Unit tests in /tests

DevContainer support for VS Code

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

# Product Management Service

## Overview
This service provides a RESTful API for managing product information. It allows users to create, read, update, and delete product records through HTTP endpoints.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Docker (optional)
- PostgreSQL (if running locally)

### Local Development Setup
1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
.\venv\Scripts\activate  # For Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file in the root directory:

DATABASE_URI=postgresql://postgres:postgres@localhost:5432/products
PORT=8000


5. Initialize the database
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

### Docker Setup
```bash
docker-compose up -d
```

## API Reference

### Products API

#### Get Product by ID
```http
GET /api/products/{id}
```
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `integer` | Product ID |

Response Example:
```json
{
    "id": 1,
    "name": "Sample Product",
    "status_code": 200
}
```

#### Get All Products
```http
GET /api/products
```
Returns a list of all products in the database.

Response Example:
```json
{
    "products": [
        {
            "id": 1,
            "name": "Sample Product 1"
        },
        {
            "id": 2,
            "name": "Sample Product 2"
        }
    ],
    "status_code": 200
}
```

### Error Responses

```json
{
    "error": "Product not found",
    "status_code": 404
}
```

## Testing
Run the test suite:
```bash
python -m pytest
```

## Deployment
The application can be deployed using:
- Docker containers
- Kubernetes cluster
- Cloud platforms (AWS, GCP, Azure)

## License

Copyright (c) 2016, 2025 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.

