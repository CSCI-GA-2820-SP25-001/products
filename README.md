# NYU DevOps Products Service (Spring 2025)

[![Build Status](https://github.com/CSCI-GA-2820-SP25-001/products/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP25-001/products/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP25-001/products/graph/badge.svg?token=2KQNKIJORH)](https://codecov.io/gh/CSCI-GA-2820-SP25-001/products)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This repository contains a microservice for managing **products**, developed as part of the NYU CSCI-GA 2820 DevOps course. The service is built using **Flask**, deployed via **OpenShift**, and includes full CI/CD pipelines and automated tests.

> ⚠️ **Note:** This is a student project hosted on limited OpenShift resources. The live demo may be unavailable due to automatic cleanup or inactivity limits.

---

## 🔧 Features

- Full CRUD support for product resources
- Search by name, category, availability, and price
- Product "like" endpoint to increment popularity
- RESTful API with Swagger UI documentation (`/apidocs`)
- 99%+ unit test coverage and BDD feature tests
- Docker + Kubernetes support
- DevContainer for VSCode

---

## 🚀 Quick Start (Local Dev)

### Prerequisites

Make sure the following tools are installed:

- [Docker](https://www.docker.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Steps

```bash
git clone https://github.com/CSCI-GA-2820-SP25-001/products.git
cd products
code .
```

> VSCode will prompt to reopen in container. Click "Yes".

Once inside the container, run the Flask server:

```bash
flask run
```

Visit: [http://localhost:8000/apidocs](http://localhost:8000/apidocs) for API documentation.

---

## ✅ Testing

### Unit Tests

```bash
nosetests
```

### BDD Tests

```bash
honcho start  # Start server in one terminal
behave        # Run tests in another terminal
```

---

## 📘 API Endpoints

| Method | Endpoint                  | Description                |
|--------|---------------------------|----------------------------|
| GET    | `/products`               | List all products          |
| GET    | `/products/<id>`          | Retrieve a product by ID   |
| POST   | `/products`               | Create a new product       |
| PUT    | `/products/<id>`          | Update an existing product |
| DELETE | `/products/<id>`          | Delete a product           |
| PUT    | `/products/<id>/like`     | "Like" a product           |
| GET    | `/products?name=Shoes`    | Search products by name    |

---

## 🗂 Project Structure

```
.
├── service/              # Main Flask application
│   ├── models.py         # SQLAlchemy models
│   ├── routes.py         # Route handlers
│   └── common/           # Logging, error handlers
├── tests/                # Unit & BDD tests
├── k8s/                  # Kubernetes deployment configs
├── .devcontainer/        # VSCode DevContainer
├── Dockerfile            # Docker image config
├── Makefile              # Common CLI tasks
├── .flaskenv             # Flask env variables
└── README.md             # This file
```

---

## License

Copyright (c) 2016, 2025 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.

