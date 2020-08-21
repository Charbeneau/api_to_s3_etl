import boto3
from botocore.exceptions import ClientError
import pandas as pd
import io
import datetime


def check_or_create_bucket(bucket_name, **kwargs):
    '''Create an S3 bucket in AWS_DEFAULT_REGION
    if it doesn't exist already.

    Parameters
    ----------
    bucket_name:  (str)
                  Bucket to create.
    Returns
    -------
    True if bucket created, else False
    '''

    s3_resource = boto3.resource('s3')

    if s3_resource.Bucket(bucket_name).creation_date is None:

        print('S3 bucket {0} does not exist.'.format(bucket_name))
        print('Creating bucket.')

        try:
            s3_resource.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            print(e)
            return False
    else:
        print('S3 bucket {0} exists.'.format(bucket_name))

    return True


def get_sources(language, news_api, **kwargs):
    '''Gets sources list for specified language.

    Parameters
    -------
    language: (str)
              Language(s) of sources.

    news_api:  (newsapi.NewsApiClient)
               NewsAPI client.

    Returns
    -------
    sources:  (list)
              [{'id': 'abc-news',
                'name': 'ABC News',
                'description': 'Your trusted source...',
                'url': 'https://abcnews.go.com',
                'category': 'general',
                'language': 'en',
                'country': 'us'},
               ...]
    '''

    print('Getting all sources.')
    response = news_api.get_sources(language=language)
    sources = response['sources']

    return sources


def make_sources_param(**context):
    '''Get the sources ids from the
    list returned by newsapi.NewsApiClient.get_sources(),
    and create the sources parameter for the
    get_top_headlines() method.

    Parameters via **context
    ------------------------
    sources:  (list)
              [{'id': 'abc-news',
                'name': 'ABC News',
                'description': 'Your trusted source...',
                'url': 'https://abcnews.go.com',
                'category': 'general',
                'language': 'en',
                'country': 'us'},
                 ...]
    Returns
    -------
    sources:  (str)
              String of comma-separated sources.
    '''
    print('Creating sources parameter string.')
    sources_list = context['task_instance'].xcom_pull(task_ids='get_sources')
    print('sources_list:')
    print(sources_list)
    sources = ','.join([ele['id'] for ele in sources_list])

    return sources


def get_top_headlines(language, news_api, **context):
    '''Gets top headlines for self.language,
    using self.sources_param.

    Parameters
    ----------
    language:  (str)
               Language(s) of sources.

    news_api:  (newsapi.NewsApiClient)
               NewsAPI client.

    Parameters via **context
    ------------------------
    sources:  (str)
              Comma separated sources.

    Returns
    -------
    top_headlines:  (list)
                    [{'source': {'id': 'news-com-au', 'name': 'News.com.au'},
                      'author': 'https://www.news.com.au/...',
                      'title': 'Coronavirus Australia...:',
                      'description': 'Victorian students...',
                      'url': 'https://www.news.com.au/...',
                      'urlToImage': 'https://content.api.news/...',
                      'publishedAt': '2020-05-12T00:06:17Z',
                      'content': 'Victorian students will...'},
                     ...]
    '''

    print('Getting top {0} headlines.'.format(language))
    response = news_api.get_top_headlines(sources=context['task_instance'].xcom_pull(task_ids='make_sources_param'),  # noqa: E501
                                          language=language)
    top_headlines = response['articles']

    return top_headlines


def transform_headlines(**context):
    '''Transforms NewsAPI top headlines
    data appropriately.

    Parameters via **context
    ------------------------
    top_headlines:  (list)
                    [{'source': {'id': 'news-com-au', 'name': 'News.com.au'},
                      'author': 'https://www.news.com.au/...',
                      'title': 'Coronavirus Australia...:',
                      'description': 'Victorian students...',
                      'url': 'https://www.news.com.au/...',
                      'urlToImage': 'https://content.api.news/...',
                      'publishedAt': '2020-05-12T00:06:17Z',
                      'content': 'Victorian students will...'}},
                     ...]
    Returns
    -------
    df:             (pandas.DataFrame)
                    DataFrame with columns 'source_id', 'source_name',..., 'content'  # noqa: E501
    '''

    print('Transforming headlines.')
    df = pd.DataFrame(context['task_instance'].xcom_pull(task_ids='get_top_headlines'))
    df['source_id'] = df['source'].apply(lambda row: row['id'])
    df['source_name'] = df['source'].apply(lambda row: row['name'])
    df = df[['source_id', 'source_name', 'author', 'title', 'description',
             'url', 'urlToImage', 'publishedAt', 'content']]
    return df


def transform_headlines_for_unit_test(top_headlines):
    '''Transforms NewsAPI top headlines
    data appropriately.

    Parameters
    ----------
    top_headlines:  (list)
                    [{'source': {'id': 'news-com-au', 'name': 'News.com.au'},
                      'author': 'https://www.news.com.au/...',
                      'title': 'Coronavirus Australia...:',
                      'description': 'Victorian students...',
                      'url': 'https://www.news.com.au/...',
                      'urlToImage': 'https://content.api.news/...',
                      'publishedAt': '2020-05-12T00:06:17Z',
                      'content': 'Victorian students will...'}},
                     ...]
    Returns
    -------
    df:             (pandas.DataFrame)
                    DataFrame with columns 'source_id', 'source_name',..., 'content'  # noqa: E501
    '''

    print('Transforming headlines.')
    df = pd.DataFrame(top_headlines)
    df['source_id'] = df['source'].apply(lambda row: row['id'])
    df['source_name'] = df['source'].apply(lambda row: row['name'])
    df = df[['source_id', 'source_name', 'author', 'title', 'description',
             'url', 'urlToImage', 'publishedAt', 'content']]
    return df


def df_to_s3(bucket_name, **context):
    '''Put a DataFrame to S3 as a csv.

    Parameters
    ----------
    bucket_name:  (str)
                  S3 bucket.

    Parameters via **context
    ------------------------
    sources:  (str)
              Comma separated sources.

    df:  (pandas.DataFrame)
         DataFrame with columns 'source_id', 'source_name',..., 'content'

    Returns
    -------
    True if csvs are all put, else False
    '''

    # This is a string like 'abc-news,cbs-news,...'
    sources = context['task_instance'].xcom_pull(task_ids='make_sources_param')

    df = context['task_instance'].xcom_pull(task_ids='transform_headlines')

    for subset in sources.split(','):

        try:
            csv_buffer = io.StringIO()
            print('Creating {0} subset.'.format(subset))
            df_subset = df[df['source_id'] == subset]
            print('{0} has {1} headlines.'.format(subset, df_subset.shape[0]))
            df_subset.to_csv(csv_buffer, index=False)
            today = datetime.datetime.today().strftime('%Y%m%d')
            key = '{0}/{1}_top_headlines.csv'.format(subset, today)
            s3_resource = boto3.resource('s3')
            print('Writing to s3://{0}/{1}'.format(bucket_name, key))
            s3_resource.Object(bucket_name=bucket_name,
                               key=key).put(Body=csv_buffer.getvalue())
        except Exception as e:
            print(e)
            return False

    return True
