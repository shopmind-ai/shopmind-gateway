def test_create_and_verify_access_token():
    from utils.jwt import create_access_token, verify_token
    token = create_access_token("demo")
    payload = verify_token(token)
    assert payload["sub"] == "demo"
    assert payload["type"] == "access"


def test_verify_invalid_token_returns_none():
    from utils.jwt import verify_token
    result = verify_token("not.a.valid.token")
    assert result is None


def test_create_and_verify_refresh_token():
    from utils.jwt import create_refresh_token, verify_token
    token = create_refresh_token("demo")
    payload = verify_token(token)
    assert payload["sub"] == "demo"
    assert payload["type"] == "refresh"
