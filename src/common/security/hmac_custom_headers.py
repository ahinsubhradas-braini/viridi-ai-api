from fastapi import Header, HTTPException

def hmac_headers(
    x_signature: str = Header(..., alias="X-Signature"),
    x_expiry: str = Header(..., alias="X-Expiry"),
    x_nonce: str = Header(..., alias="X-Nonce")
):
    """
    Extracts custom HMAC headers from every request.
    Raises an error if any are missing.
    """
    if not x_signature or not x_expiry or not x_nonce:
        raise HTTPException(status_code=400, detail="Missing HMAC headers")

    # You can add any additional checks or logging here
    return {
        "X-Signature": x_signature,
        "X-Expiry": x_expiry,
        "X-Nonce": x_nonce
    }
