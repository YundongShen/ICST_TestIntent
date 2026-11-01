from .mock import mock_call_client, client, get_call_client, TestClient


def test_headers(client: TestClient):
    response = client.get(
        "/foo",
        headers={"here":"There"}
        )
    req = client.call_client.requests[-1]
    assert "headers" in req
    assert req["headers"]["here"] == "There"    
    assert "here" in response.headers
    assert response.headers["here"] == "There"
