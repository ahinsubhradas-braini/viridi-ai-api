import hmac, hashlib, time, json, secrets

SECRET_KEY = b"test1234"

def generate_signature(method, path, expiry_secs=60):
    now = int(time.time())
    expiry = now + expiry_secs
    nonce = secrets.token_hex(8)

    # Message format same as in FastAPI
    message = f"{method}|{path}|{expiry}|{nonce}".encode() 
    signature = hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

    return {
        "signature": signature,
        "expiry": expiry,
        "nonce": nonce
    }