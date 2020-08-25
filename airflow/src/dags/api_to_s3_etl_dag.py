import os
from utils import (
    get_sources,
    make_sources_param,
    get_top_headlines,
    transform_headlines,
    df_to_s3
)
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import timedelta
from newsapi import NewsApiClient


API_TO_S3_ETL_BUCKET = os.environ.get('API_TO_S3_ETL_BUCKET', None)
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', None)

news_api = NewsApiClient(NEWS_API_KEY)

# Failures that this solution should be designed to handle:
# 0. No top headlines for a given source for a given day.

default_args = {'owner': 'airflow',
                'depends_on_past': False,
                'start_date': days_ago(1),
                'email': ['airflow@airflow.com'],
                'email_on_failure': False,
                'email_on_retry': False,
                'retries': 1,
                'retry_delay': timedelta(minutes=1)}

dag = DAG(dag_id='api_to_s3_etl_dag', default_args=default_args,
          schedule_interval=timedelta(days=1), catchup=False)

get_sources_task = PythonOperator(task_id='get_sources',
                                  python_callable=get_sources,
                                  provide_context=True,
                                  op_kwargs={'language': 'en', 'news_api': news_api},  # noqa: E501
                                  dag=dag)

make_sources_param_task = PythonOperator(task_id='make_sources_param',
                                         python_callable=make_sources_param,
                                         provide_context=True,
                                         dag=dag)

get_top_headlines_task = PythonOperator(task_id='get_top_headlines',
                                        python_callable=get_top_headlines,
                                        provide_context=True,
                                        op_kwargs={'language': 'en', 'news_api': news_api},  # noqa: E501
                                        dag=dag)

transform_headlines_task = PythonOperator(task_id='transform_headlines',
                                          python_callable=transform_headlines,
                                          provide_context=True,
                                          dag=dag)

df_to_s3_task = PythonOperator(task_id='df_to_s3',
                               python_callable=df_to_s3,
                               provide_context=True,
                               op_kwargs={'bucket_name': API_TO_S3_ETL_BUCKET},
                               dag=dag)

end = DummyOperator(task_id='end', dag=dag)

get_sources_task >> make_sources_param_task >> get_top_headlines_task >> \
    transform_headlines_task >> df_to_s3_task >> end
