import os
import boto3
from newsapi import NewsApiClient


S3_BUCKET = os.environ.get('S3_BUCKET', None)
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', None)


def test_connect_to_bucket(bucket_name=S3_BUCKET):
    '''Confirm existance of and connection to the
    S3 bucket in AWS_DEFAULT_REGION.

    Parameters
    ----------
    bucket_name:  (str)
                  S3 bucket.
    Returns
    -------
    True if bucket exists and could be connected to, else raises a ConnectionError
    '''

    s3_resource = boto3.resource('s3')

    if s3_resource.Bucket(bucket_name).creation_date is None:
        print('S3 bucket {0} does not exist!'.format(bucket_name))
        raise ConnectionError
    else:
        print('S3 bucket {0} exists.'.format(bucket_name))
    return True


def test_connect_to_api():
    '''Confirm connection to the NewsAPI.

    Returns
    -------
    True if API sources retrieved, else raises a ConnectionError
    '''

    news_api = NewsApiClient(NEWS_API_KEY)

    print('Getting all NewsAPI sources.')
    response = news_api.get_sources()  # noqa: F841
    assert response['status'] == 'ok'
