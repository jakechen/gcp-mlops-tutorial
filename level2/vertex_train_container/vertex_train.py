import os
import argparse
import google.cloud.aiplatform as aip

GCP_PROJECT = YOUR_GCP_PROJECT

print(os.environ)

# Define Vertex AI Custom Job
my_job = aip.CustomJob(
    display_name="iris_train",
    project=GCP_PROJECT,
    location="us-west1",
    staging_bucket=f"{GCP_PROJECT}-bucket",
    worker_pool_specs=[
        {
            "machine_spec": {
                "machine_type": "n1-standard-4",
                # "accelerator_type": "NVIDIA_TESLA_K80",
                # "accelerator_count": 1,
            },
            "replica_count": 1,
            "container_spec": {
                "image_uri": f"us-west1-docker.pkg.dev/{GCP_PROJECT}/iris-docker-repo/train_container",
                # "command": [],
                # "args": [],
            },
        }
    ],
)

# Run Vertex AI Custom Job
my_job.run()