FROM python:3.11-slim-bullseye

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables to disable .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /pipeline

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir "uv~=0.4.11" && \
    uv pip install --system --no-cache -r requirements.txt

COPY .dlt/config.toml .dlt/config.toml
COPY main.py ./
COPY src/ ./src
COPY schemas/ schemas/
COPY court_data/ court_data/

# - Grant root and others read, write, and execute permissions
RUN chmod -R 775 /pipeline

ENTRYPOINT ["python", "-m", "main"]
