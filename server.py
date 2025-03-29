import os
import json
import uvicorn
import socket
import random
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv

from rootdata_api import RootDataAPI

# Load environment variables
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv("ROOTDATA_API_KEY")
if not API_KEY:
    raise ValueError("ROOTDATA_API_KEY environment variable is not set")

# Initialize RootData API client
rootdata_api = RootDataAPI(api_key=API_KEY)

# Initialize FastAPI app
app = FastAPI(title="RootData MCP Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP Server configuration
MCP_SERVER_NAME = "rootdata"

# Define tool schemas
class SearchArguments(BaseModel):
    query: str = Field(..., title="Query", description="Search keywords")

class GetProjectArguments(BaseModel):
    project_id: int = Field(..., title="Project ID", description="Project ID")
    include_team: bool = Field(False, title="Include Team", description="Whether to include team information")
    include_investors: bool = Field(False, title="Include Investors", description="Whether to include investor information")

class GetOrganizationArguments(BaseModel):
    org_id: int = Field(..., title="Organization ID", description="Organization ID")
    include_team: bool = Field(False, title="Include Team", description="Whether to include team information")
    include_investments: bool = Field(False, title="Include Investments", description="Whether to include investment information")

# Define MCP request model
class MCPRequest(BaseModel):
    server_name: str
    tool_name: str
    arguments: Dict[str, Any]

# Define MCP tools
@app.post("/mcp")
async def handle_mcp_request(request: MCPRequest):
    # Validate server name
    if request.server_name != MCP_SERVER_NAME:
        raise HTTPException(status_code=400, detail=f"Unknown server name: {request.server_name}")
    
    # Route to appropriate tool handler
    if request.tool_name == "search":
        args = SearchArguments(**request.arguments)
        result = rootdata_api.search(args.query)
        return result
    
    elif request.tool_name == "get_project":
        args = GetProjectArguments(**request.arguments)
        result = rootdata_api.get_project(
            project_id=args.project_id,
            include_team=args.include_team,
            include_investors=args.include_investors
        )
        return result
    
    elif request.tool_name == "get_organization":
        args = GetOrganizationArguments(**request.arguments)
        result = rootdata_api.get_organization(
            org_id=args.org_id,
            include_team=args.include_team,
            include_investments=args.include_investments
        )
        return result
    
    else:
        raise HTTPException(status_code=400, detail=f"Unknown tool name: {request.tool_name}")

# Define MCP manifest endpoint
@app.get("/manifest.json")
async def get_manifest():
    manifest = {
        "schema_version": "v1",
        "server_name": MCP_SERVER_NAME,
        "server_version": "1.0.0",
        "description": "RootData API integration for MCP",
        "tools": [
            {
                "name": "search",
                "description": "Search for Project/VC/People brief information according to keywords",
                "input_schema": json.loads(SearchArguments.schema_json())
            },
            {
                "name": "get_project",
                "description": "Obtain project details according to the project ID",
                "input_schema": json.loads(GetProjectArguments.schema_json())
            },
            {
                "name": "get_organization",
                "description": "Obtain VC details according to VC ID",
                "input_schema": json.loads(GetOrganizationArguments.schema_json())
            }
        ]
    }
    return manifest

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

def find_available_port(start_port=8000, max_port=9000):
    """Find an available port by checking a range of ports"""
    # First try the specified start_port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('localhost', start_port)) != 0:
            return start_port
    
    # If start_port is not available, try random ports in the range
    ports_to_try = list(range(start_port + 1, max_port))
    random.shuffle(ports_to_try)  # Randomize to reduce collision chance
    
    for port in ports_to_try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    
    raise RuntimeError(f"No available ports found in range {start_port}-{max_port}")

# Run the server
if __name__ == "__main__":
    # Get port from environment variable or find an available port
    port = os.getenv("PORT")
    if port:
        port = int(port)
    else:
        port = find_available_port()
        print(f"Using available port: {port}")
    
    # Disable reload mode to avoid port conflicts
    use_reload = os.getenv("RELOAD", "false").lower() == "true"
    
    print(f"Starting server on port {port} (reload mode: {use_reload})")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=use_reload)
