import os
from utils import (
    get_sources_task,
    make_sources_param_task,
    get_top_headlines_task,
    transform_headlines_task,
    df_to_s3_task
)
from prefect import Flow
from newsapi import NewsApiClient


API_TO_S3_ETL_BUCKET = os.environ.get('API_TO_S3_ETL_BUCKET', None)
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', None)
LANGUAGE = 'en'

news_api = NewsApiClient(NEWS_API_KEY)


with Flow('api_to_s3_etl_flow') as flow:
    sources_list = get_sources_task(language=LANGUAGE, news_api=news_api)
    sources = make_sources_param_task(sources_list=sources_list)
    top_headlines = get_top_headlines_task(language=LANGUAGE, news_api=news_api,
                                           sources=sources)
    df = transform_headlines_task(top_headlines=top_headlines)
    df_to_s3_task(bucket_name=API_TO_S3_ETL_BUCKET, sources=sources, df=df)


if __name__ == '__main__':
    flow.register(project_name='APItoS3ETL')
    flow.run_agent()
