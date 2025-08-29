[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/pyright-checked-informational.svg)](https://github.com/microsoft/pyright/)
[![CI/CD Pipeline](https://github.com/musashimiyomoto/questions-app/actions/workflows/ci.yml/badge.svg)](https://github.com/musashimiyomoto/questions-app/actions/workflows/ci.yml)

------------------------------------------------------------------------

# Questions App

A FastAPI-based REST API application for managing questions and answers. This application provides endpoints for creating, reading, updating, and deleting questions and their associated answers with a clean, modern architecture.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
- Python 3.11
- Poetry (for dependency management)
- Docker and Docker Compose
```

### Installing

A step by step series of examples that tell you how to get a development env running

Clone the repository:

```
git clone https://github.com/musashimiyomoto/questions-app.git
cd questions-app
```

Create an environment file:

```
cp .env.example .env
```

Edit the `.env` file with your settings and install dependencies:

```
poetry install --with dev,test
```

Install pre-commit hooks:

```
pre-commit install
```

Start the application with Docker Compose:

```
docker compose up --build
```

End with an example of getting some data out of the system or using it for a little demo:

- Access the API documentation: http://localhost:8000/docs

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
poetry run pytest tests/
```

These tests cover the complete API endpoints, database operations, and business logic validation.

### And coding style tests

Explain what these tests test and why

```
poetry run ruff check .
poetry run black --check .
poetry run isort --check-only .
```

These tests ensure code quality, formatting consistency, and adherence to Python standards.

## Built With

* [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
* [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for database operations
* [PostgreSQL](https://www.postgresql.org/) - Database system
* [Poetry](https://python-poetry.org/) - Dependency Management
* [Docker](https://www.docker.com/) - Containerization
* [Alembic](https://alembic.sqlalchemy.org/) - Database migration tool
