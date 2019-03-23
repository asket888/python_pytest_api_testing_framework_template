import pytest


@pytest.fixture(scope='module')
def url(api_conn):
    return api_conn['api_url']['second_api']


@pytest.fixture(scope='module')
def headers(api_conn):
    return api_conn['headers']
