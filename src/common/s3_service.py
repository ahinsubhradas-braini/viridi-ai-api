import boto3


class Aws_S3_Service:
    def __init__(self, access_key, secret_key, region):
        print("Initializing S3 class", access_key, secret_key, region)

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def upload_ejs_as_object_to_s3(
        self, bucket_name, key, content, content_type="text/plain", make_public=False
    ):
        """
        Upload string content directly to S3 as a file.

        :param bucket_name: Name of the S3 bucket
        :param key: File path in S3 (e.g., "templates/myTemplate.ejs")
        :param content: String content to upload
        :param content_type: MIME type (default: text/plain)
        :param make_public: If True, makes the file public
        """
        try:
            print("bucket_name --->", bucket_name)
            print("key --->", key)
            print("content --->", content)
            print("aws client --->", self.s3_client)
            extra_args = {"ContentType": content_type}
            if make_public:
                extra_args["ACL"] = "public-read"

            self.s3_client.put_object(
                Bucket=bucket_name, Key=key, Body=content, **extra_args
            )
            print(f"✅ File uploaded successfully to s3://{bucket_name}/{key}")

            if make_public:
                public_url = f"https://{bucket_name}.s3.{self.s3_client.meta.region_name}.amazonaws.com/{key}"
                print(f"🌍 Public URL: {public_url}")
                return public_url

        except Exception as e:
            print("❌ Error found.", e)

    def get_ejs_objects_from_s3(self, bucket_name, prefix=""):
        """
        List all objects in a bucket (optionally filtered by prefix).
        """
        try:
            objects = []
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            if "Contents" in response:
                for obj in response["Contents"]:
                    objects.append(obj["Key"])
            else:
                print("No objects found.")

            print("objects ========>", objects)
            return objects
        except Exception as e:
            print(f"Error listing objects: {e}")
            return []
