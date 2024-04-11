from kfp import dsl
from kfp import compiler

# Build image

# Training pipeline
@dsl.pipeline(name="bert-sentiment-classification", pipeline_root=PIPELINE_ROOT)
def pipeline(
    project: str = PROJECT_ID,
    location: str = REGION,
    staging_bucket: str = GCS_BUCKET,
    display_name: str = DISPLAY_NAME,    
    container_uri: str = IMAGE_URI,
    model_serving_container_image_uri: str = SERVING_IMAGE_URI,    
    base_output_dir: str = GCS_BASE_OUTPUT_DIR,
):
    pass

# Compile pipeline
compiler.Compiler().compile(
    pipeline_func=pipeline, package_path="bert-sentiment-classification.json"
)

# Run pipeline
vertex_pipelines_job = vertexai.pipeline_jobs.PipelineJob(
    display_name="bert-sentiment-classification",
    template_path="bert-sentiment-classification.json",
    parameter_values={
        "project": PROJECT_ID,
        "location": REGION,
        "staging_bucket": GCS_BUCKET,
        "display_name": DISPLAY_NAME,        
        "container_uri": IMAGE_URI,
        "model_serving_container_image_uri": SERVING_IMAGE_URI,        
        "base_output_dir": GCS_BASE_OUTPUT_DIR},
    enable_caching=True,
)
vertex_pipelines_job.run()
