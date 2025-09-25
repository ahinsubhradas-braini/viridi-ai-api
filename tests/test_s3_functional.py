import uuid

import pytest

from src.common.s3_service import Aws_S3_Service  # replace with your actual import
from src.core.config import settings


@pytest.fixture(scope="module")
def s3_helper():
    # Replace these with real AWS credentials and region
    access_key = settings.aws_access_key
    secret_key = settings.aws_secret_key
    region = settings.aws_region
    return Aws_S3_Service(access_key, secret_key, region)


@pytest.fixture(scope="module")
def bucket_name():
    return "viridi-ai"


@pytest.fixture(scope="module")
def prefix():
    return "templates/"


@pytest.fixture
def ejs_content():
    # Example EJS content for testing
    return "<h1>Hello <%= name %></h1>"


@pytest.fixture
def test_key():
    # Unique key for each test run to avoid conflicts
    return f"templates/testnew_{uuid.uuid4().hex}.ejs"


def test_upload_ejs_functional(s3_helper, bucket_name, ejs_content, test_key):
    """
    Functional test: Upload EJS content to S3 and verify listing
    """
    # 1️⃣ Upload the EJS content
    s3_response = s3_helper.upload_ejs_as_object_to_s3(
        bucket_name=bucket_name,
        key=test_key,
        content=ejs_content,
        content_type="text/plain",
    )

    print("s3_response", s3_response)
