import os
import argparse
import google.cloud.aiplatform as aip

GCP_PROJECT = YOUR_GCP_PROJECT

print(os.environ)

def main():
    # Define pipeline
    pipeline_job = aip.PipelineJob(
        display_name="iris",
        template_path=f"https://us-west1-kfp.pkg.dev/{GCP_PROJECT}/iris-kfp-repo/iris/latest",
        pipeline_root=f"gs://{GCP_PROJECT}-bucket",
        project=GCP_PROJECT,
        location="us-west1",
        enable_caching=False # Disable cache for demo purposes; creates new artifact for demo
    )

    # Run pipeline
    pipeline_job.run(
        service_account=f"iris-sa@{GCP_PROJECT}.iam.gserviceaccount.com"
    )
    print("Pipeline run finished")


# Main entry point
if __name__ == "__main__":
    main()