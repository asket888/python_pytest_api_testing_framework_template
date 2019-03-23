import psycopg2

import pytest

from utils.config_util import get_env


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="DEV", help="env: DEV, UAT or LOCALHOST"
    )


@pytest.fixture(scope='session')
def env(request):
    return get_env(request.config.getoption("--env"))


@pytest.fixture(scope='session')
def api_conn(env):
    api_url = env['data']['api']
    headers = env['headers']
    return {'api_url': api_url,
            'headers': headers}


@pytest.fixture(scope='session')
def db_conn(env):
    db = env['data']['db']
    return psycopg2.connect(host=db['host_db'],
                            database=db['name_db'],
                            port=db['port_db'],
                            user=db['user_db'],
                            password=db['password_db'])
