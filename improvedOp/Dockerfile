FROM python:3.11-slim

# Can add sections here to add tools if needed
#RUN apt update 

# Otherwise install the dependencies for this API tool
WORKDIR /app

# Copy pyproject.toml and install dependencies
COPY pyproject.toml .
COPY ./src/ src/
RUN ls -la .
RUN pip install .
WORKDIR /app/src/

# Run it all. 
ENTRYPOINT ["python", "app.py"]
