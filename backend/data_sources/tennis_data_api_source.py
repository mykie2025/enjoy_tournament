"""
Tennis-Data API data source for tennis tournament data.
"""
from typing import Dict, Any, List, Optional
import requests
import json
import os
from datetime import datetime

from .base_data_source import BaseDataSource
from ..app.config import settings


class TennisDataAPISource(BaseDataSource):
    """
    Data source that retrieves tennis tournament data from the Tennis-Data API.
    """
    
    def __init__(self):
        """Initialize the Tennis-Data API data source."""
        self.api_key = settings.TENNIS_DATA_API_KEY
        self.base_url = "https://api.tennis-data.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Create a cache directory if it doesn't exist
        self.cache_dir = os.path.join(os.path.dirname(__file__), "..", "cache", "tennis_data_api")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """
        Make a request to the Tennis-Data API with caching.
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            
        Returns:
            API response as a dictionary
        """
        # Create a cache key based on the endpoint and params
        cache_key = f"{endpoint}_{json.dumps(params or {})}.json"
        cache_path = os.path.join(self.cache_dir, cache_key.replace("/", "_"))
        
        # Check if we have a cached response
        if os.path.exists(cache_path):
            # Check if the cache is less than 24 hours old
            cache_time = os.path.getmtime(cache_path)
            if (datetime.now().timestamp() - cache_time) < 86400:  # 24 hours
                try:
                    with open(cache_path, "r") as f:
                        return json.load(f)
                except Exception:
                    # If there's an error reading the cache, proceed with the API call
                    pass
        
        # Make the API request
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Cache the response
            with open(cache_path, "w") as f:
                json.dump(data, f)
            
            return data
        except requests.exceptions.RequestException as e:
            # If the API call fails, return an error response
            return {"error": str(e)}
    
    def get_tournament_info(self, tournament_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific tournament.
        
        Args:
            tournament_id: ID of the tournament
            
        Returns:
            Dictionary containing tournament details
        """
        return self._make_request(f"tournaments/{tournament_id}")
    
    def get_match_info(self, match_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific match.
        
        Args:
            match_id: ID of the match
            
        Returns:
            Dictionary containing match details
        """
        return self._make_request(f"matches/{match_id}")
    
    def get_player_info(self, player_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific player.
        
        Args:
            player_id: ID of the player
            
        Returns:
            Dictionary containing player details
        """
        return self._make_request(f"players/{player_id}")
    
    def get_head_to_head(self, player1_id: str, player2_id: str) -> Dict[str, Any]:
        """
        Get head-to-head statistics between two players.
        
        Args:
            player1_id: ID of the first player
            player2_id: ID of the second player
            
        Returns:
            Dictionary containing head-to-head statistics
        """
        return self._make_request("head-to-head", {
            "player1": player1_id,
            "player2": player2_id
        })
    
    def search_tournaments(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for tournaments matching the query.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries containing tournament details
        """
        response = self._make_request("tournaments/search", {
            "q": query,
            "limit": limit
        })
        
        if "error" in response:
            return []
        
        return response.get("tournaments", [])
