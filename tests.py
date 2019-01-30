#!/usr/bin/env python3

import requests


def test_get_order(host, expected_value):
    url = ''.join((host, '/orders/', expected_value['id']))

    response = requests.get(url)

    assert response.status_code == 200

    assert response.json() == expected_value


def test_post_order(host, expected_value):
    url = ''.join((host, '/orders'))

    payload = '{"data": "my_Order_Data_For_The_XML_Server"}'

    response = requests.post(url, data=payload)

    assert response.ok

    # Reset the id after each post.
    expected_value['id'] = response.json()['id']

    assert response.json() == expected_value


def test_empty_order(host):
    url = ''.join((host, '/orders'))

    expected_value = {'Error': 'data payload not given'}

    payload = '""'

    response = requests.post(url, data=payload)

    assert response.ok

    assert response.json() == expected_value


if __name__ == '__main__':
    print('Running tests......')

    host = 'http://0.0.0.0:5789'

    expected_value = {
        'id': '49aaf035-c5bc-4a40-993e-5a872105fd38',
        'data': 'my_Order_Data_For_The_XML_Server',
        'createdAt': '0001-01-01T00:00:00Z',
        'updatedAt': '0001-01-01T00:00:00Z'
    }

    # The order of these requests matters, as it set the OrderId
    test_empty_order(host)
    test_post_order(host, expected_value)
    test_get_order(host, expected_value)

    print('All tests passed!')
