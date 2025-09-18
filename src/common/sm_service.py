import base64
import json

import boto3

from src.core.config import settings


def get_any_secret(secret_key_name):
    try:
        print("secret_key_name", secret_key_name)
        client = boto3.client(
            "secretsmanager",
            aws_access_key_id=settings.aws_translate_sm_access_key,
            aws_secret_access_key=settings.aws_translate_sm_secret_key,
            region_name=settings.aws_translate_sm_region,
        )

        response = client.get_secret_value(SecretId=settings.aws_sm_secret_name)

        secret_dict = json.loads(response["SecretString"])

        secret_in_sm = secret_dict[secret_key_name]
        secret_key = ""
        print("secret_in_sm", secret_in_sm)

        if secret_key_name == settings.aws_sm_hmac_secret_key_name:
            # Decode Base64 secret into raw bytes for HMAC
            secret_key = base64.b64decode(secret_in_sm)
            print("After decoding ", secret_key)
        else:
            secret_key = secret_in_sm

        return secret_key
    except Exception as e:
        print("Error ---", e)
