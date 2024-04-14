import os
import argparse
import google.cloud.aiplatform as aip


print(os.environ)


def main():
    # Run pipeline
    aip.init(
        project="simple-pipeline-415719",
        location="us-west1",
        staging_bucket="gs://simple-pipeline-415719-bucket",
    )

    pipeline_job = aip.PipelineJob(
        display_name="iris",
        template_path="https://us-west1-kfp.pkg.dev/simple-pipeline-415719/iris-kfp-repo/iris/latest"
    )

    pipeline_job.run(
        service_account="iris-sa@simple-pipeline-415719.iam.gserviceaccount.com"
    )
    print("Pipeline run finished")


# Main entry point
if __name__ == "__main__":
    main()