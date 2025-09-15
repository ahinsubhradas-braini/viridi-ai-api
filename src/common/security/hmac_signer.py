import hmac, hashlib, time, json, secrets

SECRET_KEY = b"test1234"

def generate_signature(method, path, body=None, expiry_secs=60):
    now = int(time.time())
    expiry = now + expiry_secs
    nonce = secrets.token_hex(8)

    body = {
        "test_field": 1
    }
    # Message format same as in FastAPI
    message = f"{method}|{path}|{expiry}|{nonce}".encode()
    signature = hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

    return {
        "signature": signature,
        "expiry": expiry,
        "nonce": nonce,
        "body": body
    }
