# api/langflow_handler.py
import json
import requests
import uuid
from typing import Dict, Any, Optional

class LangFlowHandler:
    def __init__(self, langflow_url: str):
        self.langflow_url = langflow_url
        self.session = requests.Session()
    
    def get_flows(self):
        """Get all flows from LangFlow"""
        response = self.session.get(f"{self.langflow_url}/api/v1/flows/")
        response.raise_for_status()
        return response.json()
    
    def process_query(self, query: str, flow_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a query using the specified LangFlow flow"""
        if not session_id:
            session_id = str(uuid.uuid4())
        output_type = "chat"
        input_type = "chat"
        # API endpoint for the specific flow
        endpoint = f"{self.langflow_url}/api/v1/run/{flow_id}"
        
        # payload = {
        #     "input": {"input": query},
        #     "session_id": session_id,
        #     "tweaks": {}
        # }
        payload = {
        "input_value": query,
        "output_type": output_type,
        "input_type": input_type,
        }
        headers = None
        response = self.session.post(endpoint, json=payload,headers=headers)
        response.raise_for_status()
        result = response.json()
        
        # Extract the response from the LangFlow output
        output = json.loads((json.dumps(result, indent=2)))
        output=output["outputs"]
        output=output[0]["outputs"][0]
        # The structure of the output depends on how the flow is configured
        # Typically it would be under a key like 'output' or the name of the final node
        response_text = ""
        if isinstance(output, dict):
            # Try to find the response in common output patterns
            if "outputs" in output:
                response_text = output["outputs"]
            elif "results" in output:
                response_text = output["results"]
            elif "text" in output["outputs"]:
                response_text = output["outputs"]["message"]
            else:
                # If we can't find a standard key, just use the first string value
                for key, value in output.items():
                    if isinstance(value, str) and value:
                        response_text = value
                        break
                if not response_text:
                    # Fallback - convert the whole output to string
                    response_text = str(output)
        elif isinstance(output, str):
            response_text = output
        else:
            response_text = str(output)
        
        return {
            "response": response_text,
            "session_id": session_id,
            "metadata": {
                "flow_id": flow_id,
                "raw_output": result
            }
        }