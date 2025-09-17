
from urllib.request import Request
from fastapi import Request, HTTPException
import hmac, hashlib, time

from src.common.sm_service import get_any_secret
from src.core.config import settings
from rich import print

async def hmac_auth_middleware(request:Request):
    # Without auth middleware api path's
    # Skip all paths that do NOT start with /api/v1/
    if not request.url.path.startswith("/api/v1/"):
        return None
    
    signature = request.headers.get("X-Signature")
    expiry = request.headers.get("X-Expiry")
    nonce = request.headers.get("X-Nonce")

    print(f"[bold blue]<========= HMAC signature expiry nonce {signature,expiry,nonce} ==========> [/bold blue]")

    if not all([signature, expiry, nonce]):
        raise HTTPException(status_code=401, detail="Missing auth headers")

    # Reject expired requests
    if int(expiry) < time.time():
        raise HTTPException(status_code=401, detail="Request expired")

    # Get secret key
    SECRET_KEY =await get_secret_key()

    print("request.method",request.method)
    print("request.url.path",request.url.path)
    print("expiry",expiry)
    print("nonce",nonce)
    # Must match exactly what we used in Node.js
    message = f"{request.method}|{request.url.path}|{expiry}|{nonce}".encode("utf-8")

    # Compute expected signature
    expected_sig = hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()
    print("Expected:", expected_sig)

    if not hmac.compare_digest(signature, expected_sig):
        print("[bold red] <========= HMAC Signature mismatch ==========> [/bold red]")
        raise HTTPException(status_code=401, detail="Invalid signature")
    else:
        print("[bold green] <========= HMAC Signature matched ==========> [/bold green]")

    return request

async def get_secret_key():
    # secret_key = get_any_secret(settings.aws_sm_hmac_secret_key_name)

    secret_key = b"test1234"
    return secret_key