import os
from kfp import dsl
from kfp.compiler import Compiler
import google.cloud.aiplatform as aip
from google_cloud_pipeline_components.v1.custom_job import create_custom_training_job_from_component


print(os.environ)

# Define components
@dsl.container_component
def train_component():
    return dsl.ContainerSpec(
        image='us-west1-docker.pkg.dev/simple-pipeline-415719/test-repo/train_model'
    )

# Convert container component above into Vertex AI Custom Job component
vertex_component = create_custom_training_job_from_component(
    train_component
)

# Define pipeline
@dsl.pipeline(name='iris')
def pipeline():
    vertex_component()

# Compile pipeline
Compiler().compile(
    pipeline_func=pipeline, package_path="iris.yaml"
)
print("Pipeline compilation finished")

# Run pipeline
aip.init(
    project="simple-pipeline-415719",
    location="us-west1",
    staging_bucket="gs://simple-pipeline-415719-bucket",
)

pipeline_job = aip.PipelineJob(
    display_name="iris",
    template_path="iris.yaml",
    enable_caching=True,
)

pipeline_job.run()
print("Pipeline run finished")