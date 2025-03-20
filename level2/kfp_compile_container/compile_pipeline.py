import os
from kfp import dsl
from kfp.compiler import Compiler
from kfp.registry import RegistryClient

GCP_PROJECT = YOUR_GCP_PROJECT

print(os.environ)

# Define components
@dsl.container_component
def vertex_train():
    return dsl.ContainerSpec(
        image=f'us-west1-docker.pkg.dev/{GCP_PROJECT}/iris-docker-repo/vertex_train_container'
    )

# Define pipeline
@dsl.pipeline(name='iris')
def pipeline():
    vertex_train()

# Compile pipeline
Compiler().compile(
    pipeline_func=pipeline, package_path="iris.yaml"
)
print("Pipeline compilation finished")

# Push pipeline to Artifact Registry
client = RegistryClient(host=f"https://us-west1-kfp.pkg.dev/{GCP_PROJECT}/iris-kfp-repo")
templateName, versionName = client.upload_pipeline(
    file_name="iris.yaml",
    tags=["v1", "latest"]
)
print("Pipeline pushed to Artifact Registry")