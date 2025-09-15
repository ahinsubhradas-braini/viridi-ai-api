
from urllib.request import Request
from fastapi import Request, HTTPException
import hmac, hashlib, time

def hmac_auth_middleware(request:Request,call_next):

    if request.url.path == "/":
        return call_next(request)
    
    signature = request.headers.get("X-Signature")
    expiry = request.headers.get("X-Expiry")
    nonce = request.headers.get("X-Nonce")

    if not all([signature, expiry, nonce]):
        raise HTTPException(status_code=401, detail="Missing auth headers")

    # Reject expired requests
    if int(expiry) < time.time():
        raise HTTPException(status_code=401, detail="Request expired")

    # Get secret key
    SECRET_KEY = get_secret_key()

    # Message must be same as Node.js
    message = f"{request.method}|{request.url.path}|{expiry}|{nonce}".encode()
    expected_sig = hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(signature, expected_sig):
        raise HTTPException(status_code=401, detail="Invalid signature")

    return call_next(request)

def get_secret_key():
    # TODO: Need to fetch secret from aws secret manager

    secret_key = "test1234"
    return secret_key