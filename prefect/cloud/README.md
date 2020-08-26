# Overview

This is the first thing I've done with [Prefect](https://www.prefect.io/).

It uses [Prefect Cloud 'Developer'](https://docs.prefect.io/orchestration/) access, which is free.

The [Flow](./src/flows/api_to_s3_etl_flow.py) hits an [API](https://newsapi.org/), transforms the results, and puts them into [S3](https://aws.amazon.com/s3/).

# Requirements

- Prefect Cloud 'Developer' access.
- [Docker](https://www.docker.com/products/docker-desktop)
  - This was written using version 19.03.5, build 633a0ea.
- [NewsAPI access](https://newsapi.org/docs/get-started)  
- An [S3 bucket](https://aws.amazon.com/s3/)
- Environment Variables
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - NEWS_API_KEY
  - API_TO_S3_ETL_BUCKET
  - PREFECT_CLOUD_TOKEN
    - See [here](https://cloud.prefect.io/user/tokens)
  - PREFECT_CLOUD_RUNNER_TOKEN
    - See [here](https://docs.prefect.io/orchestration/concepts/tokens.html#token-types)

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
prefect auth login -t $PREFECT_CLOUD_TOKEN
```
Login successful!

2. Start the Prefect Agent.
```
prefect agent start docker -t $PREFECT_CLOUD_RUNNER_TOKEN
```

 ____            __           _        _                    _
|  _ \ _ __ ___ / _| ___  ___| |_     / \   __ _  ___ _ __ | |_
| |_) | '__/ _ \ |_ / _ \/ __| __|   / _ \ / _` |/ _ \ '_ \| __|
|  __/| | |  __/  _|  __/ (__| |_   / ___ \ (_| |  __/ | | | |_
|_|   |_|  \___|_|  \___|\___|\__| /_/   \_\__, |\___|_| |_|\__|
                                           |___/

[2020-08-26 20:27:50,619] INFO - agent | Starting DockerAgent with labels []
[2020-08-26 20:27:50,620] INFO - agent | Agent documentation can be found at https://docs.prefect.io/orchestration/
[2020-08-26 20:27:50,620] INFO - agent | Agent connecting to the Prefect API at https://api.prefect.io
[2020-08-26 20:27:50,736] INFO - agent | Waiting for flow runs..
