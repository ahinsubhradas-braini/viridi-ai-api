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

# Set the env first & then run the server

uvicorn main:app --reload