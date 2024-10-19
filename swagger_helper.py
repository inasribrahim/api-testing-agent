import json

class SwaggerExtractor:
    def __init__(self, swagger_file):
        self.swagger_file = swagger_file
        self.swagger_data = self.load_swagger_file()
        self.endpoints_info = []

    def load_swagger_file(self):
        with open(self.swagger_file, 'r') as file:
            return json.load(file)

    def extract_endpoints(self):
        paths = self.swagger_data.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                self.endpoints_info.append({
                    'url': f"{self.swagger_data['host']}{self.swagger_data['basePath']}{path}",
                    'method': method.upper(),
                    'request': self.extract_request_details(details),
                    'response': self.extract_response_details(details)
                })

    def extract_request_details(self, details):
        parameters = details.get('parameters', [])
        request_info = {
            'description': details.get('summary', ''),
            'parameters': []
        }
        
        for param in parameters:
            request_info['parameters'].append({
                'name': param.get('name'),
                'in': param.get('in'),
                'required': param.get('required', False),
                'type': param.get('type'),
                'description': param.get('description', '')
            })

        return request_info

    def extract_response_details(self, details):
        responses = details.get('responses', {})
        response_info = {}
        
        for status_code, response in responses.items():
            response_info[status_code] = {
                'description': response.get('description', ''),
                'schema': response.get('schema', {})
            }

        return response_info

    def generate_output(self):
        output = {
            'endpoints': self.endpoints_info
        }
        return output

    def transform_to_json(self):
        transformed_data = {
            "endpoints": []
        }
    
        for endpoint in self.endpoints_info:
            transformed_data["endpoints"].append({
                "url": endpoint['url'],
                "method": endpoint['method'],
                "request": {
                    "description": endpoint['request']['description'],
                    "parameters": endpoint['request']['parameters']
                },
                "response": endpoint['response']
            })
        
        return transformed_data
