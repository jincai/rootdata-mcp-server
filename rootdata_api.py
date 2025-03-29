import requests
import os
from typing import Dict, Any, Optional, List, Union

class RootDataAPI:
    """Client for RootData API"""
    
    def __init__(self, api_key: str, language: str = 'en'):
        """Initialize the RootData API client
        
        Args:
            api_key: The API key for RootData
            language: Language for responses ('en' for English, 'cn' for Chinese)
        """
        self.api_key = api_key
        self.language = language
        self.base_url = "https://api.rootdata.com/open"
        
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the RootData API
        
        Args:
            endpoint: API endpoint
            data: Request data
            
        Returns:
            API response as dictionary
        """
        headers = {
            "apikey": self.api_key,
            "language": self.language,
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "data": {},
                "result": response.status_code,
                "message": f"Error: {response.text}"
            }
    
    def search(self, query: str) -> Dict[str, Any]:
        """Search for Project/VC/People
        
        Args:
            query: Search keywords
            
        Returns:
            Search results
        """
        data = {"query": query}
        return self._make_request("ser_inv", data)
    
    def get_project(self, 
                    project_id: Optional[int] = None, 
                    contract_address: Optional[str] = None,
                    include_team: bool = False,
                    include_investors: bool = False) -> Dict[str, Any]:
        """Get project details
        
        Args:
            project_id: Project ID
            contract_address: Ethereum contract address
            include_team: Whether to include team information
            include_investors: Whether to include investor information
            
        Returns:
            Project details
        """
        data = {
            "include_team": include_team,
            "include_investors": include_investors
        }
        
        if project_id is not None:
            data["project_id"] = project_id
        elif contract_address is not None:
            data["contract_address"] = contract_address
        else:
            return {
                "data": {},
                "result": 400,
                "message": "Either project_id or contract_address must be provided"
            }
            
        return self._make_request("get_item", data)
    
    def get_organization(self,
                         org_id: int,
                         include_team: bool = False,
                         include_investments: bool = False) -> Dict[str, Any]:
        """Get VC/organization details
        
        Args:
            org_id: Organization ID
            include_team: Whether to include team information
            include_investments: Whether to include investment information
            
        Returns:
            Organization details
        """
        data = {
            "org_id": org_id,
            "include_team": include_team,
            "include_investments": include_investments
        }
        
        return self._make_request("get_org", data)
