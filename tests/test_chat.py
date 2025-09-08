from conftest import client

def test_chat_sse(client):
    """Test SSE streaming endpoint."""
    response = client.post("/api/v1/chat/session", headers={"Accept": "text/event-stream"})
    assert response.status_code == 200

    data = response.text
    assert "Hello" in data
    assert "[DONE]" in data