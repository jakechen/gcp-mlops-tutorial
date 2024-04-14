import os
from kfp import dsl
from kfp.compiler import Compiler
from kfp.registry import RegistryClient
from google_cloud_pipeline_components.v1.custom_job import create_custom_training_job_from_component


print(os.environ)

# Define components
@dsl.container_component
def train_component():
    return dsl.ContainerSpec(
        image='us-west1-docker.pkg.dev/simple-pipeline-415719/iris-docker-repo/train_container'
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

# Push pipeline to Artifact Registry
client = RegistryClient(host=f"https://us-west1-kfp.pkg.dev/simple-pipeline-415719/iris-kfp-repo")
templateName, versionName = client.upload_pipeline(
    file_name="iris.yaml",
    tags=["v1", "latest"]
)
print("Pipeline pushed to Artifact Registry")