# Specifies base image and tag.
# https://cloud.google.com/vertex-ai/docs/training/pre-built-containers
FROM us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-14.py310:latest

# Sets the container working directory.
WORKDIR /root

# Copies the requirements.txt into the container to reduce network calls.
COPY requirements.txt .

# Installs additional packages.
RUN pip install -U -r requirements.txt

# Invoke the trainer.
ENTRYPOINT ["python", "task.py"]