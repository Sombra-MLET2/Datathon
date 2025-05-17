"""
Service for Ollama integration
"""
import json
import requests
from src.infra.configs import logger, OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_REQUEST_TIMEOUT

class OllamaService:

    def __init__(self, host=None, model=None):
        self.host = host or OLLAMA_HOST
        self.model = model or OLLAMA_MODEL
        self.base_url = f"http://{self.host}/api"

    def generate(self, prompt, system=None):
        url = f"{self.base_url}/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 2048
            }
        }
        
        if system:
            payload["system"] = system
        
        try:
            logger.info(f"Sending request to Ollama at {url}({self.model})")

            response = requests.post(
                url, 
                json=payload, 
                timeout=OLLAMA_REQUEST_TIMEOUT
            )
            
            response.raise_for_status()
            
            result = response.json()

            return result.get("response", "")
        except requests.exceptions.Timeout:
            error_msg = f"Request to Ollama timed out after {OLLAMA_REQUEST_TIMEOUT} seconds"
            logger.error(error_msg)
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Error calling Ollama API: {e}"
            logger.error(error_msg)
            raise Exception(f"Failed to communicate with Ollama: {str(e)}")
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse Ollama response as JSON: {e}"
            logger.error(error_msg)
            logger.error(f"Response content: {response.text[:500]}...")
            raise Exception(error_msg)
