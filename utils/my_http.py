from http import client
from config import SERVER_HOST, SERVER_PORT, SERVER_BASE_URL
import json

def get(url):
    conn = client.HTTPConnection(SERVER_HOST, SERVER_PORT)
    conn.request('GET', SERVER_BASE_URL + url)
    response = conn.getresponse()
    py_response = {
        "code": response.status,
        "data": json.loads(response.read().decode("utf-8"))
    }
    client.HTTPConnection.close(conn)
    print(f'| GET | {url} | {py_response}')
    return py_response

def post(url, data):
    conn = client.HTTPConnection(SERVER_HOST, SERVER_PORT)
    data_bytes = bytes(json.dumps(data), encoding="utf-8")
    conn.request('POST', SERVER_BASE_URL + url, data_bytes, headers={"Content-Type": "application/json"})
    response = conn.getresponse()
    py_response = {
        "code": response.status,
        "data": json.loads(response.read().decode("utf-8"))
    }
    client.HTTPConnection.close(conn)
    print(f'| POST | {url} | {py_response}')
    return py_response

def delete(url):
    conn = client.HTTPConnection(SERVER_HOST, SERVER_PORT)
    conn.request('DELETE', SERVER_BASE_URL + url)
    response = conn.getresponse()
    py_response = {
        "code": response.status,
        "data": json.loads(response.read().decode("utf-8"))
    }
    client.HTTPConnection.close(conn)
    print(f'| DELETE | {url} | {py_response}')
    return py_response

def put(url, data):
    conn = client.HTTPConnection(SERVER_HOST, SERVER_PORT)
    conn.request('PUT', SERVER_BASE_URL + url, data_bytes, headers={"Content-Type": "application/json"})
    response = conn.getresponse()
    py_response = {
        "code": response.status,
        "data": json.loads(response.read().decode("utf-8"))
    }
    client.HTTPConnection.close(conn)
    print(f'| PUT | {url} | {py_response}')
    return py_response