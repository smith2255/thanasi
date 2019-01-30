#!/usr/bin/env python3

# import ipdb
import json
import requests
import xmltodict

from flask import Flask, jsonify, request

app = Flask(__name__)

REMOTE_HOST = 'http://52.52.253.24:8888'


@app.route('/orders/<order_id>', methods=['GET'])
def order_details(order_id):
    remote_url = ''.join((REMOTE_HOST, request.path))

    xml_response = requests.get(remote_url)

    json_object = xmltodict.parse(xml_response.text)

    return jsonify(json_object.get('order'))


@app.route('/orders', methods=['POST'])
def place_order():
    remote_url = ''.join((REMOTE_HOST, request.path))

    request_body = json.loads(request.get_data())

    if 'data' not in request_body:
        return '{"Error": "data payload not given"}'

    xml_payload = '<order><data>{0}</data></order>'.format(
        request_body['data'])

    # Should actually re-direct to order/{id} after a successful POST
    xml_response = requests.post(remote_url, data=xml_payload)

    json_object = xmltodict.parse(xml_response.text)

    return jsonify(json_object.get('order'))


if __name__ == '__main__':

    print('Running Server')
    app.run(
        host='0.0.0.0',
        port='5789',
        debug=True,
    )
