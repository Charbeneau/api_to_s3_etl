# Overview

This is the first thing I've done with [Prefect](https://www.prefect.io/).

The [Flow] hits an [API](https://newsapi.org/), transforms the results, and puts them into [S3](https://aws.amazon.com/s3/).

# Requirements

- Python 3
  - This was written using version 3.7.6 [Clang 10.0.0 (clang-1000.11.45.5)] on darwin
- [Docker](https://www.docker.com/products/docker-desktop)
  - This was written using version 19.03.5, build 633a0ea.
- [Docker Compose](https://docs.docker.com/compose/)
  - This was written using version 1.24.1, build 4667896b.
- [NewsAPI access](https://newsapi.org/docs/get-started)  
- An [S3 bucket](https://aws.amazon.com/s3/)
- Environment Variables
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - NEWS_API_KEY
  - S3_BUCKET

## Usage

0. Create a Python virtual environment, here called **prefect_env** and done with [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).
```
mkvirtualenv prefect_env
pip install -r prefect_env_requirements.txt
```

1. Configure Prefect for local orchestration.
```
prefect backend server
```

2. Start the server, UI, and all required infrastructure.
```
prefect server start
```

3. Open a new terminal, hop in the prefect_env virtual environment, and start the Prefect Agent.
```
prefect agent start
```

4. View the UI by visiting [http://localhost:8080](http://localhost:8080).

5. In the UI, create a new 'APItoS3ETL' project.

6. Again, open a new terminal, enter in the prefect_env virtual environment, and run the following.
```
cd prefect/
python src/flows/api_to_s3_etl_flow.py
```

7. Go back to the UI, and click "QUICK RUN" in the upper right.
