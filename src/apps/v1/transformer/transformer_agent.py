# Import python core libary dependices
import json
import logging
import os
import re
import time
from typing import Any, Dict

# Imports from project or 3rd party libary dependices
from openai import OpenAI
from openai.types.chat import ChatCompletion

from src.apps.v1.transformer.lib.prompt_manager import PromptManager
from src.common.s3_service import Aws_S3_Service
from src.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransformerAgent:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        timeout: int = 60,
        prompts_dir: str = "prompts",
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize the TransformerAgent.

        :param api_key: OpenAI API key
        :param base_url: Base URL for the API
        :param model: Model name to use
        :param timeout: Request timeout in seconds
        :param prompts_dir: Directory containing prompt templates
        :param max_retries: Maximum number of retries for failed requests
        :param retry_delay: Delay between retries in seconds
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        print("api_key", api_key)
        print("base_url", base_url)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.prompts_dir = os.path.join(current_dir, "prompts")

        # Initialize components
        self.prompt_manager = PromptManager(self.prompts_dir)
        self.client = OpenAI(
            api_key=self.api_key, base_url=self.base_url, timeout=timeout
        )

        # Performance tracking
        self._request_count = 0
        self._total_response_time = 0.0

    def _clean_jinja_code(self, code: str) -> str:
        """
        Clean Jinja2 code by removing markdown code blocks and unnecessary whitespace.

        :param code: Raw code from LLM response
        :return: Cleaned Jinja2 template code
        """
        if not code:
            return ""

        # Remove common markdown code block markers
        code_markers = [
            ("```jinja2", "```"),
            ("```jinja", "```"),
            ("```json", "```"),
            ("```", "```"),
            ("`", "`"),
        ]

        for start_marker, end_marker in code_markers:
            if code.startswith(start_marker):
                code = code[len(start_marker) :].strip()
            if code.endswith(end_marker):
                code = code[: -len(end_marker)].strip()

        return code.strip()

    def _clean_ejs_code(self, code: str) -> str:
        print("<--- Start cleaning ejs --->")
        if not code:
            return ""

        # Remove code block markers
        code_markers = [("```ejs", "```"), ("```", "```"), ("`", "`")]
        for start_marker, end_marker in code_markers:
            if code.startswith(start_marker):
                code = code[len(start_marker) :].strip()
            if code.endswith(end_marker):
                code = code[: -len(end_marker)].strip()

        # Decode unicode sequences safely (keeps quotes in JSON.stringify intact)
        def decode_unicode(match):
            return match.group(0).encode("utf-8").decode("unicode_escape")

        code = re.sub(r"(\\u[0-9a-fA-F]{4})", decode_unicode, code)

        return code.strip()

    def _validate_schemas(
        self, input_schema: Dict[str, Any], output_schema: Dict[str, Any]
    ) -> None:
        """
        Validate input and output schemas.

        :param input_schema: Input data schema
        :param output_schema: Output data schema
        :raises ValueError: If schemas are invalid
        """
        if not isinstance(input_schema, dict):
            raise ValueError("Input schema must be a dictionary")
        if not isinstance(output_schema, dict):
            raise ValueError("Output schema must be a dictionary")
        if not input_schema:
            raise ValueError("Input schema cannot be empty")
        if not output_schema:
            raise ValueError("Output schema cannot be empty")

    def _make_api_request(self, prompt: str) -> ChatCompletion:
        """
        Make API request with retry logic and error handling.

        :param prompt: The prompt to send to the model
        :return: API response
        :raises Exception: If all retries fail
        """
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                print(self.prompts_dir)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert at creating EJS templates for data transformation. Return only the EJS template code without any explanations, markdown formatting, backslash (\\), forward Slash (/), new line(/n)  wrapper like JSON.stringify or variable.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.1,  # Lower temperature for more consistent output
                    max_tokens=2600,  # Reasonable limit for template generation
                )

                # Track performance
                response_time = time.time() - start_time
                self._request_count += 1
                self._total_response_time += response_time

                logger.info(
                    f"API request completed in {response_time:.2f}s (attempt {attempt + 1})"
                )
                return response

            except Exception as e:
                last_exception = e
                logger.warning(
                    f"API request failed (attempt {attempt + 1}/{self.max_retries}): {str(e)}"
                )

                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2**attempt))  # Exponential backoff

        raise Exception(
            f"All {self.max_retries} API requests failed. Last error: {str(last_exception)}"
        )

    def generate_transformer(
        self,
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any],
        api_provider_name: str,
    ) -> str:
        """
        Generate a Ejs transformer template using the AI model.

        :param input_schema: Schema or sample of the input data
        :param output_schema: Schema of the desired output data
        :return: Generated Ejs template as string
        :raises ValueError: If schemas are invalid or response is empty
        :raises Exception: If API request fails
        """
        # Validate inputs
        self._validate_schemas(input_schema, output_schema)

        # Minify JSON to reduce token usage
        minified_input_schema = json.dumps(input_schema, separators=(",", ":"))
        # Render the prompt
        try:
            prompt = self.prompt_manager.render_prompt(
                "transformer",
                input_schema=json.dumps(minified_input_schema, indent=2),
                output_schema=json.dumps(output_schema, indent=2),
            )
        except Exception as e:
            raise ValueError(f"Failed to render prompt template: {str(e)}")

        # Make API request
        response = self._make_api_request(prompt)

        # Validate response
        if not response.choices or not response.choices[0].message:
            raise ValueError("No valid response from the model")

        # Extract and clean the response
        rendering_code = response.choices[0].message.content

        if not rendering_code:
            raise ValueError("Empty response from the model")
        cleaned_code = self._clean_ejs_code(rendering_code.strip())

        if not cleaned_code:
            raise ValueError("No valid Ejs code found in the response")

        logger.info("Successfully generated transformer template")

        # Creating templates in local templates
        templates_dir = "templates"
        template_path = os.path.join(templates_dir, f"{api_provider_name}.ejs")
        os.makedirs(templates_dir, exist_ok=True)
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(cleaned_code)

        S3_Helper = Aws_S3_Service(
            settings.aws_access_key, settings.aws_secret_key, settings.aws_region
        )

        public_url = S3_Helper.upload_ejs_as_object_to_s3(
            "templates", f"{api_provider_name}.ejs", cleaned_code
        )

        return public_url

    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for the agent.

        :return: Dictionary containing performance metrics
        """
        avg_response_time = (
            self._total_response_time / self._request_count
            if self._request_count > 0
            else 0
        )

        return {
            "total_requests": self._request_count,
            "total_response_time": self._total_response_time,
            "average_response_time": avg_response_time,
        }

    def reset_performance_stats(self) -> None:
        """Reset performance tracking statistics."""
        self._request_count = 0
        self._total_response_time = 0.0
