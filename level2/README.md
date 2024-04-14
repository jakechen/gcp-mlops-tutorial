# MLOps level 2: CI/CD pipeline automation

## What are the important things in here?
1. `stack.tf`: this is a Terraform template that will create or update infrastructure in Google Cloud such as GCP Buckets, databases, Cloud Run jobs, etc. Generally for Production environments, users cannot go in Console and click "Create Bucket" or click "Edit Cloud Run". In fact only select users can see the Production environment, and very few can modify it. Instead, all of the infrastructure chances are made through a thoroughly tested and reviewed Terraform template.
2. `train_container`: this container contains the model training code. This code trains the model, saves the model, and uploads the model to a Cloud Storage bucket.
3. `vertex_container`: this container submits a Vertex Job to run `train_container`. It also defines Job parameters such as machine(s), accelerator(s), locations, and more. 

## What about prediction?
Now that you have container that outputs a trained model artifact, you can also create a prediction container that runs input data through the trained model. The same above patterns can then be modified or duplicated to deploy the prediction container.