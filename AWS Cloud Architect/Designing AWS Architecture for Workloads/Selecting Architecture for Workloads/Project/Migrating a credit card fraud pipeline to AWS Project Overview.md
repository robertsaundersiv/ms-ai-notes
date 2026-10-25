## Migrating a Credit Card Fraud Pipeline to AWS

In this project, you will work as a cloud architect at a credit card company. The company's data scientists have developed a fraud detection pipeline on-premises, which includes:

1. A Spark pipeline running on a Hadoop cluster that transforms incoming data and trains the model.
2. A containerized API running on an on-premises server that returns a fraud/no-fraud response.
3. A function or workflow that updates the data used to train the model and triggers model retraining.

Your task is to migrate this pipeline to AWS Cloud, ensuring improved security, scalability, performance, and cost-efficiency. You will use the skills learned in this course to:

1. **Evaluate each workload and select appropriate AWS services** for storage, model training, API deployment, retraining, and monitoring/logging.
2. **Modify the starter source code** so the training job, prediction API, and retraining workflow run with your selected AWS services instead of relying on local-only execution.
3. **Deploy and configure the selected AWS services**, including the IAM roles or service permissions needed for the services to run and interact securely.
4. **Provide evidence that the migrated pipeline works in AWS** by completing the project template with short explanations and screenshots showing the training job, model artifact, running API service, retraining workflow, and IAM/service permission configuration.