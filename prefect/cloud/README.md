# Overview

This is the first thing I've done with [Prefect](https://www.prefect.io/).

It uses [Prefect Cloud 'Developer'](https://docs.prefect.io/orchestration/) access, which is free.

The [Flow](./src/flows/api_to_s3_etl_flow.py) hits an [API](https://newsapi.org/), transforms the results, and puts them into [S3](https://aws.amazon.com/s3/).

# Requirements

- Prefect Cloud 'Developer' access.
  - Sign up [here](https://cloud.prefect.io/)
- Python 3
  - This was written using version 3.7.6 [Clang 10.0.0 (clang-1000.11.45.5)] on darwin
- [NewsAPI access](https://newsapi.org/docs/get-started)  
- An [S3 bucket](https://aws.amazon.com/s3/)
- Environment Variables
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - NEWS_API_KEY
  - API_TO_S3_ETL_BUCKET
  - PREFECT_CLOUD_USER_TOKEN
    - See [here](https://cloud.prefect.io/user/tokens)

# Usage

0. Create a Python virtual environment, here called **prefect_cloud_env** and done with [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).
```
mkvirtualenv prefect_cloud_env
pip install -r prefect_cloud_env_requirements.txt
```

1. From inside the prefect_cloud_env virtual environment, Configure Prefect for Cloud orchestration and log in.
```
prefect backend cloud
```
Backend switched to cloud

```
prefect auth login --token $PREFECT_CLOUD_USER_TOKEN
```
Login successful!

2. Create a new 'APItoS3ETL' project.
```
prefect create project APItoS3ETL
```
APItoS3ETL created

3. Create a Prefect Cloud Runner token.
```
prefect auth create-token --name PREFECT_CLOUD_RUNNER_TOKEN --scope RUNNER
```
[UUID]

4. Create a new PREFECT_CLOUD_RUNNER_TOKEN environment variable, and set it to the [UUID] value returned above.

5. Start the Prefect Local Agent.
```
prefect agent start local --token $PREFECT_CLOUD_RUNNER_TOKEN --env AUTH=$PREFECT_CLOUD_USER_TOKEN
```

You should see this.
```
 ____            __           _        _                    _
|  _ \ _ __ ___ / _| ___  ___| |_     / \   __ _  ___ _ __ | |_
| |_) | '__/ _ \ |_ / _ \/ __| __|   / _ \ / _` |/ _ \ '_ \| __|
|  __/| | |  __/  _|  __/ (__| |_   / ___ \ (_| |  __/ | | | |_
|_|   |_|  \___|_|  \___|\___|\__| /_/   \_\__, |\___|_| |_|\__|
                                           |___/

[2020-08-27 20:08:16,013] INFO - agent | Starting LocalAgent with labels ['jeffs-mbp.lan', 'azure-flow-storage', 'gcs-flow-storage', 's3-flow-storage', 'github-flow-storage', 'webhook-flow-storage']
[2020-08-27 20:08:16,013] INFO - agent | Agent documentation can be found at https://docs.prefect.io/orchestration/
[2020-08-27 20:08:16,013] INFO - agent | Agent connecting to the Prefect API at https://api.prefect.io
[2020-08-27 20:08:16,139] INFO - agent | Waiting for flow runs...
```

6. Open a new terminal, enter the prefect_cloud_env virtual environment, **make sure the PREFECT_CLOUD_RUNNER_TOKEN exists**, and run the flow.
```
python src/flows/api_to_s3_etl_flow.py
```

You should see this.
```
Result check: OK
Flow: https://cloud.prefect.io/[YOUR_ACCOUNT]/flow/[UUID]
```

7. Log in to Prefect Cloud, go to the 'APItoS3ETL" project, and click on the 'api_to_s3_etl_flow' flow.

When you do, you should see a 'QUICK RUN' icon next to a blue rocket ship in the upper right corner.  

Click 'QUICK RUN'.

8. If everything worked, you'll see the Flow running and be able to click on each of its Tasks and view their logs.
