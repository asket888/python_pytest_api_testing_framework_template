import pytest
import requests

from db.statements import advertiser_db_statement as advertiser_db
from utils.math_util import get_random_integer

_GET_ADVERTISER_ENDPOINT = '/api/endpoint/{advertiser_id}'
_PUT_ADVERTISER_ENDPOINT = '/api/endpoint/{advertiser_id}'

_ADVERTISER_NAME = '[API] Advertiser'


@pytest.fixture(autouse=True)
def db_cleanup(db_conn):
    advertiser_db.delete_advertiser_by_name(db_conn, _ADVERTISER_NAME)
    yield
    advertiser_db.delete_advertiser_by_name(db_conn, _ADVERTISER_NAME)


@pytest.mark.first_api
@pytest.mark.advertisers
class TestAdvertiser:

    # positive tests
    def test_advertiser_get_by_id(self, db_conn, url, headers):
        _db_setup(db_conn)
        advertiser = advertiser_db.select_advertiser_by_name(db_conn, _ADVERTISER_NAME)

        response = requests.get(url=''.join([url, _GET_ADVERTISER_ENDPOINT
                                            .format(advertiser_id=advertiser['id'])]),
                                headers=headers)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data['id'] > 0
        assert response_data['name'] == _ADVERTISER_NAME
        assert response_data['param_1'] == advertiser['param_1']
        assert response_data['param_2'] == advertiser['param_2']
        assert response_data['param_3'] == advertiser['param_3']

    def test_advertiser_update(self, db_conn, url, headers):
        _db_setup(db_conn)
        advertiser = advertiser_db.select_advertiser_by_name(db_conn, _ADVERTISER_NAME)
        request_body = {
            'id': advertiser['id'],
            'param_1': 111,
            'param_2': '999',
            'param_3': False,
            'name': _ADVERTISER_NAME + ' Updated'
        }

        response = requests.put(url=''.join([url, _PUT_ADVERTISER_ENDPOINT
                                            .format(advertiser_id=advertiser['id'])]),
                                headers=headers,
                                json=request_body)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data['id'] == advertiser['id']
        assert response_data['name'] == _ADVERTISER_NAME + ' Updated'
        assert response_data['param_1'] == 111
        assert response_data['param_2'] == '999'
        assert response_data['param_3'] is False

    # negative tests
    def test_advertiser_get_by_not_exist_id(self, db_conn, url, headers):
        self._test_advertiser_update_validation(db_conn, url, headers,
                                                {'id': 9999}, 'id',
                                                'Advertiser not found.')

    def test_advertiser_update_invalid_param_1_validation(self, db_conn, url, headers):
        self._test_advertiser_update_validation(db_conn, url, headers,
                                                {'param_1': 9999}, 'param_1',
                                                'Entity with param_1 does not exist.')

    def test_advertiser_update_wrong_data_type_param_2_validation(self, db_conn, url, headers):
        self._test_advertiser_update_validation(db_conn, url, headers,
                                                {'param_2': 111}, 'param_2',
                                                "111 is not of type 'string'")

    def _test_advertiser_update_validation(self, db_conn, url, headers, request_update, expected_field, expected_msg):
        _db_setup(db_conn)
        advertiser = advertiser_db.select_advertiser_by_name(db_conn, _ADVERTISER_NAME)
        request_body = {
            'id': advertiser['id'],
            'param_1': 1111111,
            'param_2': '999999',
            'param_3': True,
            'name': _ADVERTISER_NAME + ' Updated',
        }
        request_body.update(request_update)

        response = requests.put(url=''.join([url, _PUT_ADVERTISER_ENDPOINT.format(advertiser_id=advertiser['id'])]),
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
