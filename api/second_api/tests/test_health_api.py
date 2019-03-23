import pytest
import requests


class TestHealth:

    @pytest.mark.second_api
    @pytest.mark.health
    def test_health(self, url, headers):
        response = requests.get(url=''.join([url, '/health']),
                                headers=headers)

        assert response.status_code == 200
        assert response.text == 'Healthy'
