import json
import os
import httpx
import logging
import sys
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging to write to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("rootdata-mcp")

# Initialize FastMCP server
mcp = FastMCP("rootdata")

# Constants
ROOTDATA_API_BASE = "https://api.rootdata.com/open"


# Helper function to make API requests
async def make_request(endpoint: str, data: dict) -> dict[str, any] | None:
    """Make a request to the RootData API with proper error handling."""
    headers = {
        "Content-Type": "application/json",
        "language": "en",
    }
    
    if api_key := os.environ.get("ROOTDATA_API_KEY"):
        headers["apikey"] = api_key
    else:
        return {"Error": "ROOTDATA_API_KEY environment variable is not set"}

    url = f"{ROOTDATA_API_BASE}/{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"Error": str(e)}


@mcp.tool()
async def search(query: str) -> str:
    """Search for Project/VC/People brief information according to keywords.

    Args:
        query: Search keywords, which can be project/institution names, tokens, or other related terms.
    """
    # Prepare request data
    data = {"query": query}
    
    # Fetch data from the API
    response = await make_request("ser_inv", data)
    
    # Check if there was an error
    if "Error" in response:
        return f"Error: {response['Error']}"
    
    # Check if data is found
    if response.get("result") != 200 or not response.get("data"):
        return "No results found for your search query."
    
    # Return the formatted results
    return json.dumps(response["data"], indent=2)


@mcp.tool()
async def get_project(
    project_id: int,
    include_team: bool = False,
    include_investors: bool = False,
) -> str:
    """Obtain project details according to the project ID.

    Args:
        project_id: The unique identifier for the project.
        include_team: Whether to include team member information, default is false.
        include_investors: Whether to include investor information, default is false.
    """
    # Prepare request data
    data = {
        "project_id": project_id,
        "include_team": include_team,
        "include_investors": include_investors,
    }
    
    # Fetch data from the API
    response = await make_request("get_item", data)
    
    # Check if there was an error
    if "Error" in response:
        return f"Error: {response['Error']}"
    
    # Check if data is found
    if response.get("result") != 200 or not response.get("data"):
        return f"No project found with ID {project_id}."
    
    # Return the formatted results
    return json.dumps(response["data"], indent=2)


@mcp.tool()
async def get_organization(
    org_id: int,
    include_team: bool = False,
    include_investments: bool = False,
) -> str:
    """Obtain VC details according to VC ID.

    Args:
        org_id: Organization ID
        include_team: Whether to include team member information, default is false.
        include_investments: Whether it includes investment project information, default is false.
    """
    # Prepare request data
    data = {
        "org_id": org_id,
        "include_team": include_team,
        "include_investments": include_investments,
    }
    
    # Fetch data from the API
    response = await make_request("get_org", data)
    
    # Check if there was an error
    if "Error" in response:
        return f"Error: {response['Error']}"
    
    # Check if data is found
    if response.get("result") != 200 or not response.get("data"):
        return f"No organization found with ID {org_id}."
    
    # Return the formatted results
    return json.dumps(response["data"], indent=2)


if __name__ == "__main__":
    # Log server startup
    logger.info("Starting RootData MCP Server...")
    
    # Initialize and run the server
    mcp.run(transport="stdio")
    
    # This line won't be reached during normal operation
    logger.info("Server stopped")
