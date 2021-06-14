# The following will run tests prior to building the image.
# Normally you would do this in some DevOps pipeline.
# For a small demonstration, this is fine
FROM python:3-alpine as test

# Setup the application folder and requirements
RUN mkdir -p /app/src
WORKDIR /app
COPY requirements-debug.txt .
RUN pip install -r requirements-debug.txt

# Run the linting and unit tests
COPY src/ /app/src/
WORKDIR /app/src
RUN flake8
RUN pytest

# The following will build a production image for deployment.
FROM python:3-alpine

# Set up the application folder and requirements
RUN mkdir -p /app/src
WORKDIR /app
COPY requirements-production.txt .
RUN pip install -r requirements-production.txt

WORKDIR /app/src
COPY --from=test /app/src/ /app/src/
CMD uvicorn main:app --host 0.0.0.0 --port 8000
