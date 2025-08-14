import requests
import json

class WatsonxService:
    def __init__(self, api_key: str, project_id: str, model_id: str = "granite-3-instruct-8b"):
        self.api_key = api_key
        self.project_id = project_id
        self.model_id = model_id
        self.url = "https://us-south.ml.cloud.ibm.com/ml/v1-beta/generation/text?version=2023-05-29"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.get_token()}"
        }

    def get_token(self):
        url = "https://iam.cloud.ibm.com/identity/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        data = f"apikey={self.api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    def get_completion(self, prompt: str, temperature: float = 0.5, max_tokens: int = 250) -> str:
        payload = {
            "model_id": self.model_id,
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy", # "sample" or "greedy"
                "max_new_tokens": max_tokens,
                "min_new_tokens": 10,
                "temperature": temperature,
                "repetition_penalty": 1.0,
            },
            "project_id": self.project_id
        }
        
        response = requests.post(self.url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()["results"][0]["generated_text"]
