# Expenses Tracker Backend

FastAPI backend for the expenses tracker application.

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Environment Variables

Create a `.env` file in the `backend/` directory with the following content:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/expenses_tracker

# API Configuration
API_TITLE=Expenses Tracker API
API_VERSION=1.0.0
```

Replace `user`, `password`, `localhost`, and `5432` with your PostgreSQL credentials and connection details.

### 4. Database Setup

Make sure PostgreSQL is running and create a database:

```sql
CREATE DATABASE expenses_tracker;
```

The application will create tables automatically on first run.

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- OpenAPI Schema: `http://localhost:8000/openapi.json`

## Testing

Run behavioral tests with pytest-bdd:

```bash
pytest tests/
```

## Troubleshooting

### Installation Errors with pydantic-core and psycopg2-binary

If you encounter errors building `pydantic-core` or `psycopg2-binary` wheels (common on Python 3.13 or ARM64 Macs), you have a few options:

**Option 1: Install build dependencies (Recommended)**

Install Rust (required for pydantic-core) and PostgreSQL libraries:

```bash
# Install Rust
brew install rust

# Install PostgreSQL (if not already installed)
brew install postgresql

# Then retry installation
pip install -r requirements.txt
```

**Option 2: Use Python 3.11 or 3.12**

Python 3.13 is very new and some packages may not have pre-built wheels yet. Consider using Python 3.11 or 3.12:

```bash
# Create venv with specific Python version
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Option 3: Upgrade pip and install build tools**

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── repositories/        # Data access layer
│   └── routers/             # API endpoints
└── tests/                   # Behavioral tests
```
