import pytest
from lib.routes import app

def test_crud_operations():
    client = app.test_client()
    response = client.get('/inventory')
    assert response.status_code == 200
    assert response.get_json() == []

    data = {'product_name': 'Test', 'quantity': 0, 'price': 1.00, 'details': 'N/A'}
    response = client.post('/inventory', json=data)
    assert response.status_code == 201
    item = response.get_json()
    
    item_id = item['id']
    response = client.get(f'/inventory/{item_id}')
    assert response.status_code == 200
    assert response.get_json()['product_name'] == 'Test'

    response = client.patch(f'/inventory/{item_id}', json={'quantity': 1})
    assert response.status_code == 200
    assert response.get_json()['quantity'] == 1

    response = client.delete(f'/inventory/{item_id}')
    assert response.status_code == 204

    resp = client.get(f'/inventory/{item_id}')
    assert resp.status_code == 404