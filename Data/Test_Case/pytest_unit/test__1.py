from .mock import mock_call_client, client, get_call_client, TestClient


def test_(client):
    assert len(client.call_client.requests) == 0
    response  = client.get("/foo")
    assert len(client.call_client.requests) != 0
    req = client.call_client.requests[-1]
    assert req["service"] == "localhost:8080"
    assert response.content == b"mock"
