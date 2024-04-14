import os
import argparse
import google.cloud.aiplatform as aip


print(os.environ)


aip.init(
    project='simple-pipeline-415719',
    location='us-west1',
    staging_bucket='simple-pipeline-415719-bucket',
)

my_job = aip.CustomJob(
    display_name='iris_train',
    worker_pool_specs=[
        {
            "machine_spec":{
                "machine_type": "n1-standard-4",
                # "accelerator_type": "NVIDIA_TESLA_K80",
                # "accelerator_count": 1,
            },
            "replica_count": 1,
            "container_spec": {
                "image_uri": 'us-west1-docker.pkg.dev/simple-pipeline-415719/iris-docker-repo/train_container',
                # "command": [],
                # "args": [],
            },
        }
    ],
)

print()

my_job.run()