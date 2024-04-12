# Select base image
# Good starting point is Vertex AI prebuilt containers:
# https://cloud.google.com/vertex-ai/docs/training/pre-built-containers
FROM us-docker.pkg.dev/vertex-ai/training/sklearn-cpu.1-0:latest

# Copy files
COPY . .

# Pip install
# RUN pip install -r requirements.txt

# Run script
ENTRYPOINT ["python", "train.py"]