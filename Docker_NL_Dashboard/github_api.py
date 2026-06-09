import requests
from typing import Dict, List
from datetime import datetime

class GitHubAPI:
    BASE_URL = "https://api.github.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Docker-NL-Dashboard"
        })
    
    def get_status(self) -> Dict:
        """Get GitHub status from status.github.com"""
        try:
            response = requests.get(
                "https://www.githubstatus.com/api/v2/status.json",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "status": data.get("status", {}),
                "description": data.get("status", {}).get("description", "Unknown"),
                "indicator": data.get("status", {}).get("indicator", "none"),
                "updated_at": datetime.utcnow().isoformat()
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to fetch GitHub status"
            }
    
    def get_public_events(self, limit: int = 10) -> Dict:
        """Get recent public events from GitHub"""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/events",
                timeout=10
            )
            response.raise_for_status()
            events = response.json()
            
            parsed_events = []
            for event in events[:limit]:
                parsed_events.append({
                    "id": event.get("id", ""),
                    "type": event.get("type", ""),
                    "actor": event.get("actor", {}).get("login", "unknown"),
                    "repo": event.get("repo", {}).get("name", "unknown"),
                    "created_at": event.get("created_at", ""),
                    "public": event.get("public", True)
                })
            
            return {
                "success": True,
                "events": parsed_events,
                "count": len(parsed_events)
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to fetch GitHub events",
                "events": []
            }
    
    def get_rate_limit(self) -> Dict:
        """Get API rate limit information"""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/rate_limit",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            core = data.get("resources", {}).get("core", {})
            
            return {
                "success": True,
                "limit": core.get("limit", 0),
                "remaining": core.get("remaining", 0),
                "reset": core.get("reset", 0),
                "used": core.get("used", 0)
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to fetch rate limit"
            }
    
    def search_repositories(self, query: str, limit: int = 10) -> Dict:
        """Search GitHub repositories"""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/search/repositories",
                params={"q": query, "per_page": limit, "sort": "stars"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            repos = []
            for repo in data.get("items", []):
                repos.append({
                    "name": repo.get("full_name", ""),
                    "description": repo.get("description", ""),
                    "stars": repo.get("stargazers_count", 0),
                    "language": repo.get("language", ""),
                    "url": repo.get("html_url", "")
                })
            
            return {
                "success": True,
                "repositories": repos,
                "total_count": data.get("total_count", 0)
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to search repositories",
                "repositories": []
            }
