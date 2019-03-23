import pytest
import requests


class TestHealth:

    @pytest.mark.first_api
    @pytest.mark.health
    def test_health(self, url, headers):
        response = requests.get(url=''.join([url, '/health']),
                                headers=headers)

        response_data = response.json()

        assert response.status_code == 200
        assert response_data['status'] == 'healthy'
