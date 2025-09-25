# Project Detials:

    Project Name: Fastapi Boilerplate

    # Api url: http://localhost:8000/

    # Swagger api docs: http://localhost:8000/docs

        *** username and password is in .env

# Create virtual env

python -m venv venv

# Activate venv

Go to cmd: venv\Scripts\activate.bat # For current settings

# Install all requirements

pip install -r requirements.txt

pip install -r dev_requirements.txt

run pip install torch==2.2.2+cpu --index-url https://download.pytorch.org/whl/cpu before 'pip install sentence-transformers'


# Set the env first & then run the server

uvicorn main:app --reload

uvicorn src.server:app --host 0.0.0.0 --port 8012 --reload

# To run test cases

pytest tests/

pytest --cov=src tests/

pytest --cov=src --cov-report=html tests/

    open htmlcov/index.html      # macOS
    xdg-open htmlcov/index.html   # Linux
    start htmlcov/index.html      # Windows

pytest -vv -s tests/test_hmac_functional.py

# S3 url

https://viridi-ai.s3.ap-south-1.amazonaws.com/templates/test_04c07ab34b004fe684ce281ba7aed6e8.ejs


# Pre-Commit hooks

    1. Install pre commit hooks

    pre-commit install

    pre-commit autoupdate

    pre-commit run --all-files

    --no-verify