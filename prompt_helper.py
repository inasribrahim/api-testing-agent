import json
import google.generativeai as genai
from swagger_helper import SwaggerExtractor 
import time
import random
from google.api_core.exceptions import ResourceExhausted


class TestCasePromptBuilder:
    def __init__(self, transformed_data):
        self.transformed_data = transformed_data
        self.genai_key = "genai_key"  # Replace with your actual API key

        if not self.genai_key:
            raise ValueError("genai_key must be set in the environment variables")

        genai.configure(api_key=self.genai_key)

    def build_prompts(self, limit=None):
        prompts = []
        
        # Shuffle the endpoints for random selection
        endpoints = self.transformed_data["endpoints"]
        random.shuffle(endpoints)

        for endpoint in endpoints:
            if limit is not None and len(prompts) >= limit:
                break  # Stop if the limit is reached

            url = endpoint["url"]
            method = endpoint["method"]
            request = endpoint["request"]

            # Ensure URL has the correct scheme
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url  # Add HTTPS if missing

            # Generate test case for the happy path
            happy_case, expected_status_code = self.__genai_suggest(
                f"Generate a test case for the happy path of {method} {url}.",
                request["parameters"]
            )
            prompts.append({
                "description": happy_case,
                "functional_type": "happy_path",
                "request_method": method,
                "request": {
                    "url": url,
                    "parameters": request["parameters"]
                },
                "expected_response": {
                    "status_code": expected_status_code,
                    "description": "successful operation"
                }
            })

            # Generate test case for the error path
            error_case, expected_status_code = self.__genai_suggest(
                f"Generate a test case for the error path of {method} {url}.",
                request["parameters"]
            )
            prompts.append({
                "description": error_case,
                "functional_type": "error_path",
                "request_method": method,
                "request": {
                    "url": url,
                    "parameters": request["parameters"]
                },
                "expected_response": {
                    "status_code": expected_status_code,  # Dynamic based on generated content
                    "description": "Invalid input"
                }
            })

        return prompts

    def __genai_suggest(self, prompt, parameters):
        model = genai.GenerativeModel('gemini-pro')
        # Construct a prompt for generating a specific test case
        prompt_content = f"""
        {prompt}
        
        Please include the following mandatory parameters: {parameters}.
        Provide a detailed test case including request payload and expected response.
        """
        retry_attempts = 3  # Set the number of retry attempts
        for attempt in range(retry_attempts):
            try:
                suggestions = model.generate_content(prompt_content)
                generated_text = suggestions.text

                # Determine expected status code based on content (you can refine this logic)
                if "success" in generated_text.lower():
                    expected_status_code = 200 if "GET" in prompt else 201  # Assume 200 for GET, 201 for POST
                else:
                    expected_status_code = 400  # Default to 400 for error cases

                return generated_text, expected_status_code
            except genai.exceptions.ResourceExhausted as e:
                if attempt < retry_attempts - 1:  # Don't wait on the last attempt
                    print("Quota exceeded. Retrying...")
                    time.sleep(10)  # Wait for a while before retrying
                else:
                    raise e  # Re-raise the exception after all attempts
