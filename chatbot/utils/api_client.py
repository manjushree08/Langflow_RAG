# chatbot/utils/api_client.py
import requests
from typing import Dict, Any, Optional

class APIClient:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.session = requests.Session()
    
    def get_flows(self) -> Dict[str, Any]:
        """Get all available flows from the API"""
        response = self.session.get(f"{self.api_url}/flows")
        response.raise_for_status()
        return response.json()
    
    def send_query(self, query: str, flow_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Send a query to the API and get a response"""
        endpoint = f"{self.api_url}/chat"
        payload = {
            "query": query,
            "flow_id": flow_id
        }
        
        if session_id:
            payload["session_id"] = session_id
        
        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()