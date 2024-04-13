from google.cloud import aiplatform as vertexai
import google.cloud.aiplatform as aip
from kfp.v2 import dsl,compiler
from google_cloud_pipeline_components.v1.custom_job import utils


PATH=%env PATH
%env PATH={PATH}:/home/jupyter/.local/bin

PROJECT_ID = "spatial-tempo-418521"
REGION = "us-west1"

GCS_BUCKET = f"gs://{PROJECT_ID}"

vertexai.init(project=PROJECT_ID, location=REGION, staging_bucket=GCS_BUCKET)

MODEL_DIR = "train_container"
ARTIFACT_REGISTRY="iris"

IMAGE_NAME="train_container"
IMAGE_TAG="latest"
IMAGE_URI=f"{REGION}-docker.pkg.dev/{PROJECT_ID}/{ARTIFACT_REGISTRY}/{IMAGE_NAME}:{IMAGE_TAG}"

# create image
cloudbuild_yaml = f"""steps:
- name: 'gcr.io/cloud-builders/docker'
  args: [ 'build', '-t', '{IMAGE_URI}', '.' ]
images: 
- '{IMAGE_URI}'"""

with open(f"{MODEL_DIR}/cloudbuild.yaml", "w") as fp:
    fp.write(cloudbuild_yaml)

# submit to cloud build
con = f"{MODEL_DIR}/cloudbuild.yaml"
!gcloud builds submit --config=$con --timeout=1200 $MODEL_DIR

dsl.container_component
def custom_model():
    return dsl.ContainerSpec(image=IMAGE_URI)

custom_job = utils.create_custom_training_job_op_from_component(custom_model)

# building pipeline
@dsl.pipeline(name="iris")
def pipeline():        
    custom_producer_task = custom_job()    
    
compiler.Compiler().compile(
    pipeline_func=pipeline, package_path="iris.json"
)

# run pipeline
job = aip.PipelineJob(
    display_name='aaa',
    template_path="iris.json",    
)
job.run()
