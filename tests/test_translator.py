import pytest


@pytest.mark.asyncio
async def test_translate(client, translate_fake_request):
    """
    Test case for translator ai.
    """
    print("translate_fake_request ===>", translate_fake_request)
    response = client.post(
        "/api/v1/ai-translator/translate",
        json=translate_fake_request,
        headers={"Accept": "application/json"},
    )

    assert response.status_code == 200
    data = response.json()
    print("response data =======>", data)
    assert data["translated_data"] is not None
