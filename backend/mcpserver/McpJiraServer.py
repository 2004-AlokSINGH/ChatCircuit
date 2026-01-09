from mcp.server.fastmcp import FastMCP
import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from typing import Optional

# Load environment variables from the .env file in mcpserver directory
load_dotenv()

class DebugResult(BaseModel):
    error_type: str
    root_cause: str
    suggested_fix: str

    jira_ticket_required: bool = Field(
        description="Whether a Jira ticket should be created"
    )

    jira_ticket_id: Optional[str] = None


mcp = FastMCP("jira-server")

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")


async def jira_enrichment(result: DebugResult) -> DebugResult:
    if result.jira_ticket_required:
        ticket = await create_jira_ticket(
            summary=f"{result.error_type} issue detected",
            description=result.root_cause
        )
        # store just the key, or both key+url depending on your schema
        result.jira_ticket_id = ticket["ticket_key"]
    return result


@mcp.tool()
async def create_jira_ticket(summary: str, description: str) -> dict:
    """
    Create a Jira ticket and return key + url
    """
    url = f"{JIRA_BASE_URL}/rest/api/2/issue"
    print("-----------")

    print(f"JIRA Config Check:")
    print(f"API_TOKEN: {JIRA_API_TOKEN[:20]}..." if JIRA_API_TOKEN else "None")
    print(f"BASE_URL: {JIRA_BASE_URL}")
    print(f"EMAIL: {JIRA_EMAIL}")
    print(f"PROJECT_KEY: {JIRA_PROJECT_KEY}")

    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Bug"}
        }
    }

    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )

    response.raise_for_status()
    data = response.json()

    return {
        "tool": "jira",
        "ticket_key": data["key"],
        "ticket_url": f"{JIRA_BASE_URL}/browse/{data['key']}"
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
