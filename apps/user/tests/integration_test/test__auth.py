import json

import requests


def test__login():
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "username": "admin",
        "password": "admin"
    }
    response = requests.post(
        url='http://localhost:8000/api/login/',
        json=data,
        headers=headers
    )
    assert response.status_code == 200
    print(response.json())
    assert response.json().get('data') == {'username': 'admin', 'email': 'admin@root.com'}
