
from urllib.request import Request
from fastapi import Request, HTTPException
import hmac, hashlib, time
import json

async def hmac_auth_middleware(request:Request):
    # Without auth middleware api path's
    if request.url.path == "/":
        return request
    elif request.url.path == "/docs":
        return request
    elif request.url.path == "/openapi.json":
        return request
    elif request.url.path == "/favicon.ico":
        return request
    elif request.url.path == "/api/v1/ai-translator/translate":
        return request
    
    signature = request.headers.get("X-Signature")
    expiry = request.headers.get("X-Expiry")
    nonce = request.headers.get("X-Nonce")

    print("signature expiry nonce",signature,expiry,nonce)

    if not all([signature, expiry, nonce]):
        raise HTTPException(status_code=401, detail="Missing auth headers")

    # Reject expired requests
    if int(expiry) < time.time():
        raise HTTPException(status_code=401, detail="Request expired")

    # Get secret key
    SECRET_KEY =await get_secret_key()

    # Must match exactly what we used in Node.js
    message = f"{request.method}|{request.url.path}|{expiry}|{nonce}".encode("utf-8")

    # Compute expected signature
    expected_sig = hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(signature, expected_sig):
        print("Signature mismatch")
        print("Expected:", expected_sig)
        print("Got:", signature)
        raise HTTPException(status_code=401, detail="Invalid signature")
    else:
        print("Signature matched")


    return request

async def get_secret_key():
    # TODO: Need to fetch secret from aws secret manager

    secret_key = b"test1234"
    
    return secret_key