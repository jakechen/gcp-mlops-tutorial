from kfp import dsl
from kfp import compiler

def main():
    # Training pipeline
    @dsl.pipeline(name="iris", pipeline_root=PIPELINE_ROOT)
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
        pipeline_func=pipeline, package_path="iris.json"
    )

# Main entry point
if __name__ == "__main__":
    main()