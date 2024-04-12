from google.cloud import aiplatform as aip

def main(request):
    aip.init(
        project=project_id,
        location=PROJECT_REGION,
    )

    # Prepare the pipeline job
    job = aip.PipelineJob(
        display_name="automl-image-training-v2",
        template_path="image_classif_pipeline.yaml",
        pipeline_root=pipeline_root_path,
        parameter_values={
            'project_id': project_id
        }
    )

    job.submit()

# Main entry point
if __name__ == "__main__":
    main()