# Levels of MLOps automation
Please read [MLOps: Continuous delivery and automation pipelines in machine learning](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) before beginning this tutorial.

To summarize the MLOps levels:
1. MLOps level 0: Manual process
2. MLOps level 1: ML pipeline automation
3. MLOps level 2: CI/CD pipeline automation

The goal of MLOps level 2 is to achieve the same velocity and quality of the DevOps teams: new web applications and features are created, tested, deployed, and destroyed every day, if not multiple times a day, all with zero impact to a user. For example, Google constantly adds or updates products across its entire portfolio, which means there are hundreds to thousands of new deployments on any given day. Even if your company is not as big as Google, you and your AI/ML team can and should aspire to the same velocity as the application development teams. This means adopting the practices and principles of DevOps.


## MLOps level 0: Manual process
### Topics
- Jupyter Notebooks

### Data Scientist workflow
1. I iterate on model in training notebook
1. I run training notebook to output model


## MLOps level 1: ML pipeline automation
### Topics
- Non-Jupyter IDE: Code is written in .py files to accomodate containers, not .ipynb
- Docker Containers: Runs custom code repeatedly
- Pipelines

### Data Scientist workflow
1. I may iterate on training container
    1. Manually build Docker image and push to Artifact Repository
1. I may modify Vertex Pipeline
    1. Manually recompile pipeline.yaml
1. I may need new bucket
    1. Manually create a new bucket in Console


## MLOps level 2: CI/CD pipeline automation
### Topics
- Unit testing
- Production environments: Production environments should not be manually touched, only vetted code can deploy
- Terraform: Infrastructure as Code e.g. create new buckets using code instead of console
- Code Build: Build service e.g. docker build and push
- Git automation: When source code changes, changes are automatically tested and applied

### Data Scientist workflow
1. I iterate on training container locally
1. I git push the changes to dev
1. Code Build detects that change, then runs the cloudbuild.yaml
1. cloudbuild.yaml runs unit tests
1. cloudbuild.yaml runs gcloud builds submit
1. cloudbuild.yaml runs terraform apply
1. cloudbuild.yaml runs function tests
1. Once all code passes is dev, new changes are automatically pushed to Production
1. The above checks and builds take place in Production and your new model is launched

### Best practices
* Use .gitignore in same directory as cloudbuild yaml to ignore temp files e.g. terraform
    * https://cloud.google.com/sdk/gcloud/reference/builds/submit

### Resources
* https://google-cloud-pipeline-components.readthedocs.io/en/google-cloud-pipeline-components-2.13.1/api/v1/custom_job.html#v1.custom_job.create_custom_training_job_from_component
* https://cloud.google.com/docs/terraform/resource-management/managing-infrastructure-as-code
* OLDER: https://cloud.google.com/architecture/architecture-for-mlops-using-tfx-kubeflow-pipelines-and-cloud-build