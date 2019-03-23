import pytest
import requests

from db.statements import advertiser_db_statement as advertiser_db, account_db_statement as account_db
from utils.math_util import get_random_integer

_GET_ACCOUNT_ENDPOINT = '/api/v2/endpoint/{account_id}'
_PUT_ACCOUNT_ENDPOINT = '/api/v2/endpoint/{account_id}'
_POST_ACCOUNT_ENDPOINT = '/api/v2/endpoint'

_ADVERTISER_NAME = '[API] Advertiser'
_ACCOUNT_NAME = '[API] Account'


@pytest.fixture(autouse=True)
def db_cleanup(db_conn):
    advertiser_db.delete_advertiser_by_name(db_conn, _ADVERTISER_NAME)
    account_db.delete_account_by_name(db_conn, _ACCOUNT_NAME)
    yield
    advertiser_db.delete_advertiser_by_name(db_conn, _ADVERTISER_NAME)
    account_db.delete_account_by_name(db_conn, _ACCOUNT_NAME)


@pytest.mark.first_api
@pytest.mark.accounts
class TestAccounts:

    # positive tests
    @pytest.mark.smoke
    def test_account_get_by_id(self, db_conn, url, headers):
        _db_setup(db_conn)
        advertiser = advertiser_db.select_advertiser_by_name(db_conn, _ADVERTISER_NAME)
        account = account_db.select_account_by_name(db_conn, _ACCOUNT_NAME)

        response = requests.get(url=''.join([url, _GET_ACCOUNT_ENDPOINT.format(account_id=account['id'])]),
                                headers=headers)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data['id'] == account['id']
        assert response_data['name'] == _ACCOUNT_NAME
        assert response_data['advertisers'][0]['id'] == advertiser['id']
        assert response_data['advertisers'][0]['name'] == _ADVERTISER_NAME
        assert response_data['advertisers'][0]['status'] == advertiser['status']
        assert len(response_data['advertisers']) == 1

    @pytest.mark.smoke
    def test_account_create(self, url, headers):
        request_body = {
            'name': _ACCOUNT_NAME
        }

        response = requests.post(url=''.join([url, _POST_ACCOUNT_ENDPOINT]),
                                 headers=headers,
                                 json=request_body)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data['name'] == _ACCOUNT_NAME
        assert response_data['id'] > 0

    @pytest.mark.smoke
    def test_account_update(self, db_conn, url, headers):
        _db_setup(db_conn)
        account = account_db.select_account_by_name(db_conn, _ACCOUNT_NAME)
        request_body = {
            'id': account['id'],
            'name': _ACCOUNT_NAME + ' Updated',
        }

        response = requests.put(url=''.join([url, _PUT_ACCOUNT_ENDPOINT.format(account_id=account['id'])]),
                                headers=headers,
                                json=request_body)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data['id'] == account['id']
        assert response_data['name'] == _ACCOUNT_NAME + ' Updated'

    # negative tests
    def test_account_create_duplicated_name_validation(self, db_conn, url, headers):
        _db_setup(db_conn)
        self._test_account_create_validation(url, headers,
                                             {}, 'name',
                                             'Your account name must be unique')

    def test_account_create_invalid_parameter_1_validation(self, url, headers):
        self._test_account_create_validation(url, headers,
                                             {'param_1': 1.0}, 'param_1',
                                             'Your account default_margin should be between 0.00 and 0.9999')

    def test_account_create_invalid_parameter_2_validation(self, url, headers):
        self._test_account_create_validation(url, headers,
                                             {'param_2': "invalid"}, 'param_2',
                                             "'invalid' is not one of ['Budget', 'Investment']")

    # Bug KEV-3483
    @pytest.mark.xfail
    def test_account_create_invalid_parameter_3_validation(self, url, headers):
        self._test_account_create_validation(url, headers,
                                             {'param_2': 'invalid'}, 'param_2',
                                             "'invalid' is not of type 'boolean'")

    def _test_account_create_validation(self, url, headers, request_update, expected_field, expected_msg):
        request_body = {
            'name': _ACCOUNT_NAME,
            'parameter_1': 0.25,
            'parameter_2': 'Budget',
            'parameter_3': True
        }
        request_body.update(request_update)

        response = requests.post(url=''.join([url, _POST_ACCOUNT_ENDPOINT]),
                                 headers=headers,
                                 json=request_body)
        response_data = response.json()

        assert response.status_code == 400
        assert response_data['code'] == 400
        assert response_data['messages'][0]['field'] == expected_field
        assert response_data['messages'][0]['message'] == expected_msg


def _db_setup(db_conn):
    advertiser_db.insert_advertiser(db_conn,
                                    advertiser_name=_ADVERTISER_NAME,
                                    param_1=get_random_integer(10000, 99999),
                                    param_2=str(get_random_integer(10000, 99999)),
                                    param_3=True)
    account_db.insert_account(db_conn,
                              account_name=_ACCOUNT_NAME,
                              param_1='1',
                              param_2='0.1',
                              param_3='Budget')
