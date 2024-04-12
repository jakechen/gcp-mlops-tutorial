# Levels of MLOps automation
Levels based on [MLOps: Continuous delivery and automation pipelines in machine learning](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning).

In summary:
1. MLOps level 0: Manual process
1. MLOps level 1: ML pipeline automation
1. MLOps level 2: CI/CD pipeline automation


## MLOps level 0: Manual process
### Topics
- Jupyter Notebooks

### Data Scientist workflow
1. I iterate on model in training notebook
1. I run training notebook to output model


## MLOps level 1: ML pipeline automation
### Topics
- Docker Containers
- Pipelines w/ scheduling

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
- Git automation
- Development and Production environments
- Code Build
- Terraform

### Data Scientist workflow
1. I iterate on training container
1. I git push to dev
1. Code Build detects that change, then runs the cloudbuild.yaml
1. cloudbuild.yaml runs unit tests
1. cloudbuild.yaml runs gcloud builds submit
1. cloudbuild.yaml runs terraform apply
1. cloudbuild.yaml runs function tests

### Best practices
* Use .gitignore in same directory as cloudbuild yaml to ignore temp files e.g. terraform
    * https://cloud.google.com/sdk/gcloud/reference/builds/submit

### Resources
* https://cloud.google.com/docs/terraform/resource-management/managing-infrastructure-as-code
* OLDER: https://cloud.google.com/architecture/architecture-for-mlops-using-tfx-kubeflow-pipelines-and-cloud-build