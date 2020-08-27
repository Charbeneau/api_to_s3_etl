from src.flows.utils import transform_headlines_task_for_unit_test
import pandas as pd


def test_transform_headlines_task_for_unit_test():
    data = [{'source': {'id': 'news-com-au', 'name': 'News.com.au'},
             'author': 'https://www.news.com.au/...',
             'title': 'Coronavirus Australia...:',
             'description': 'Victorian students...',
             'url': 'https://www.news.com.au/...',
             'urlToImage': 'https://content.api.news/...',
             'publishedAt': '2020-05-12T00:06:17Z',
             'content': 'Victorian students will...'},
            {'source': {'id': 'news-com', 'name': 'News.com'},
             'author': 'https://www.news.com/...',
             'title': 'Coronavirus US...:',
             'description': 'US students...',
             'url': 'https://www.news.com/...',
             'urlToImage': 'https://content.api.news/...',
             'publishedAt': '2020-05-12T00:06:17Z',
             'content': 'US students will...'}]

    observed = transform_headlines_task_for_unit_test(top_headlines=data)
    expected = pd.DataFrame({'source_id': ['news-com-au', 'news-com'],
                             'source_name': ['News.com.au', 'News.com'],
                             'author': ['https://www.news.com.au/...', 'https://www.news.com/...'],  # noqa: E501
                             'title': ['Coronavirus Australia...:', 'Coronavirus US...:'],  # noqa: E501
                             'description': ['Victorian students...', 'US students...'],  # noqa: E501
                             'url': ['https://www.news.com.au/...', 'https://www.news.com/...'],  # noqa: E501
                             'urlToImage': ['https://content.api.news/...'] * 2,  # noqa: E501
                             'publishedAt': ['2020-05-12T00:06:17Z'] * 2,
                             'content': ['Victorian students will...', 'US students will...']})  # noqa: E501

    pd.testing.assert_frame_equal(left=observed, right=expected)
