import json
import google.generativeai as genai
import requests
from swagger_helper import SwaggerExtractor
from prompt_helper import TestCasePromptBuilder  
import time
import matplotlib.pyplot as plt

class TestRunner:
    def __init__(self):
        self.passed_count = 0
        self.failed_count = 0
        self.results = []  # Store results for the Markdown file

    def run_test_cases(self, test_cases, limit=None):
        if limit is not None:
            test_cases = test_cases[:limit]
        
        for test_case in test_cases:
            print(f"Running test case: {test_case['description']}")
            try:
                # Make the request
                response = requests.request(
                    method=test_case["request_method"],
                    url=test_case["request"]["url"],
                    headers={"Content-Type": "application/json"},
                    json=test_case.get("request", {}).get("payload", {})
                )

                actual_status_code = response.status_code
                actual_output = response.text

                # Validate the response
                expected_status_code = test_case["expected_response"]["status_code"]

                # Check if the actual status code falls within success or failure ranges
                if (expected_status_code in range(200, 300) and actual_status_code in range(200, 300)) or \
                   (expected_status_code in range(400, 600) and actual_status_code in range(400, 600)):
                    self.passed_count += 1
                    status = "PASSED"
                else:
                    self.failed_count += 1
                    status = "FAILED"

                # Collect results
                self.results.append({
                    "description": test_case['description'],
                    "status": status,
                    "expected": test_case["expected_response"],
                    "actual": {
                        "status_code": actual_status_code,
                        "output": actual_output
                    }
                })

                print(f"Test case '{test_case['description']}' executed with status: {status}")

            except requests.exceptions.RequestException as e:
                self.failed_count += 1
                self.results.append({
                    "description": test_case['description'],
                    "status": "FAILED",
                    "error": str(e)
                })
                print(f"Test case '{test_case['description']}' encountered an error: {e}")

    def generate_results_markdown(self, store_name="Pet Store", author="Your Name", file_name="api-testing-agent-results.md"):
        with open(file_name, 'w', encoding='utf-8') as f:  # Specify utf-8 encoding
            f.write("# Test Results\n\n")
            f.write(f"**Store Name:** {store_name}\n")
            f.write(f"**Author:** {author}\n")
            f.write(f"**Total Passed:** {self.passed_count}\n")
            f.write(f"**Total Failed:** {self.failed_count}\n\n")

            # Add some humor
            f.write("## Summary\n")
            f.write(f"- **Total Test Cases Executed:** {self.passed_count + self.failed_count}\n")
            f.write(f"- **Passed:** {self.passed_count}\n")
            f.write(f"- **Failed:** {self.failed_count}\n")
            f.write("\n### Don't worry, it's just testing!\n")
            f.write("It's not about how many times you fail, but how many times you get up! 🎉\n\n")

            f.write("## Detailed Results\n")
            for result in self.results:
                f.write(f"### Test Case: {result['description']}\n")
                f.write(f"- **Status:** {result['status']}\n")
                if result['status'] == "FAILED":
                    f.write(f"- **Error:** {result.get('error', 'No error details available')}\n")
                else:
                    f.write(f"- **Expected Response:**\n")
                    f.write(f"  ```json\n{json.dumps(result['expected'], indent=4)}\n```\n")
                    f.write(f"- **Actual Response:**\n")
                    f.write(f"  ```json\n{json.dumps(result['actual'], indent=4)}\n```\n")
                f.write("\n")

            # Embed the pie chart image
            f.write("## Test Case Results Pie Chart\n")
            f.write("![Test Case Results](test_case_results_pie_chart.png)\n")  # Adjust the path if needed

            # Optionally, you can add a footer
            f.write("---\n")
            f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    def generate_pie_chart(self):
            labels = 'Passed', 'Failed'
            sizes = [self.passed_count, self.failed_count]
            colors = ['lightgreen', 'salmon']
            explode = (0.1, 0)  # explode the 1st slice (i.e., 'Passed')

            plt.figure(figsize=(8, 5))
            plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.title('Test Case Results')
            plt.savefig('test_case_results_pie_chart.png')  # Save as image
            plt.close()

# Load the Swagger file and extract endpoints
extractor = SwaggerExtractor('petstore_swagger.json')
extractor.extract_endpoints()
transformed_json = extractor.transform_to_json()

# Build prompts for generating test cases
prompt_builder = TestCasePromptBuilder(transformed_json)
prompts = prompt_builder.build_prompts(limit=5)

# Create TestRunner instance and execute the generated test cases
test_runner = TestRunner()

# Execute the test cases
test_runner.run_test_cases(prompts, limit=None)

# Generate pie chart for test case results
test_runner.generate_pie_chart()

# Generate results Markdown file
test_runner.generate_results_markdown(store_name="Pet Store", author="Ibrahim Nasr")







