# Run pipeline
def main():
    vertex_pipelines_job = vertexai.pipeline_jobs.PipelineJob(
        display_name="iris",
        template_path="iris.json",
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

# Main entry point
if __name__ == "__main__":
    main()