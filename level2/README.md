# MLOps level 2: CI/CD pipeline automation

## What are the important things in here?
1. `stack.tf`: this is the Terraform configuration file(s) that will create or update infrastructure in Google Cloud such as GCP Buckets, databases, Cloud Run jobs, etc. Generally for Production environments, users cannot go in Console and click "Create Bucket" or click "Edit Cloud Run". In fact only select users can see the Production environment, and very few can modify it. Instead, all of the infrastructure chances are made through a thoroughly tested and reviewed Terraform configuration file(s).
2. `train_container`: this container contains the model training code. This code trains the model, saves the model, and uploads the model to a Cloud Storage bucket.
3. `vertex_train_container`: this container submits a Vertex AI Custom Job to run `train_container`. It also defines Job parameters such as machine(s), accelerator(s), locations, and more.
4. `kfp_compile_container`: this container defines, compiles, and pushes the Kubeflow Pipeline (KFP) template. In this case the KFP template includes `vertex_train_container`.
5. `kfp_run_container`: this container submits a Vertex AI Pipeline Job to run the KFP template. This pipeline run then runs the code in `vertex_train_container`, which in turn runs the code in `train_container`.
6. `cloudbuild.yaml`: this is the Cloud Build configuration file that will be triggered by a `git push` and is the file that will automate your build processes. This not only includes the building and pushing of Docker containers, but also running the Terraform config file(s), calling any necessary CLI commands (e.g. executing `kfp_compile_container` via Cloud Build), and more.

## What about prediction?
Now that you have container that outputs a trained model artifact, you can also create a prediction container that runs input data through the trained model. The same above patterns can then be modified or duplicated to deploy the prediction container.

## FAQ?
- Why do you need `train_container` and `vertex_train_container`?
    - You don't, it is possible for a single container to house both the code to train the model and the code to submit a Vertex AI Custom Job. However, it maybe be easier to debug two separate containers versus a single larger container.