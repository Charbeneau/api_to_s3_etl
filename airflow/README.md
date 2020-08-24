# api_to_s3_etl
Let's hit an API, transforms the results, and put them in S3!

# Overview

This is the first thing I've done with [Airflow](https://airflow.apache.org/).

I used the "LocalExecutor" method in [this repo](https://github.com/puckel/docker-airflow) as a starting point.

The [DAG](./src/dags/api_to_s3_etl_dag.py) hits an [API](https://newsapi.org/), transforms the results, and puts them into [S3](https://aws.amazon.com/s3/).

# Requirements

- [Docker](https://www.docker.com/products/docker-desktop)
  - This was written using version 19.03.5, build 633a0ea.
- [Docker Compose](https://docs.docker.com/compose/)
  - This was written using version 1.24.1, build 4667896b.
- [make](https://www.gnu.org/software/make/manual/make.html)
  - This was written using version 3.81.
- [NewsAPI access](https://newsapi.org/docs/get-started)  
- An [S3 bucket](https://aws.amazon.com/s3/)
- Environment Variables
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - NEWS_API_KEY
  - S3_BUCKET

# Usage

0. For a clean start with Docker containers, run
```
make docker-clean-unused
```

1. Build the containers.
```
make build
```

2. Run the tests.
```
make test
```

3. Start the services.
```
make up
```

You should see something like [this](./stack_traces/make_run.txt).

4. Go to [http://localhost:8080/admin/](http://localhost:8080/admin/).

5. Turn on the api_to_s3_etl_dag DAG, click on it, and click on "Graph View".

6. Click "Trigger DAG" to run it.

7. End the services.
```
make down
```
