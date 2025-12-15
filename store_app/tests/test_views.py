from http.client import responses

import pytest
from django.urls import reverse


def test_home_view(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200

    assert 'вашего магазина' in response.content.decode('utf-8')


