"""
ATP/WTA Tour API data source for tennis tournament data.
"""
from typing import Dict, Any, List, Optional
import requests
import json
import os
from datetime import datetime

from .base_data_source import BaseDataSource
from ..app.config import settings


class TennisTourAPISource(BaseDataSource):
    """
    Data source that retrieves tennis tournament data from the ATP/WTA Tour APIs.
    """
    
    def __init__(self):
        """Initialize the ATP/WTA Tour API data source."""
        self.api_key = settings.TENNIS_TOUR_API_KEY
        self.atp_base_url = "https://api.atptour.com/v1"
        self.wta_base_url = "https://api.wtatennis.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Create a cache directory if it doesn't exist
        self.cache_dir = os.path.join(os.path.dirname(__file__), "..", "cache", "tennis_tour_api")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _make_request(self, tour: str, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """
        Make a request to the ATP or WTA Tour API with caching.
        
        Args:
            tour: 'atp' or 'wta'
            endpoint: API endpoint to call
            params: Query parameters
            
        Returns:
            API response as a dictionary
        """
        base_url = self.atp_base_url if tour.lower() == 'atp' else self.wta_base_url
        
        # Create a cache key based on the tour, endpoint and params
        cache_key = f"{tour}_{endpoint}_{json.dumps(params or {})}.json"
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
            url = f"{base_url}/{endpoint}"
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
            tournament_id: ID of the tournament in format 'tour:id' (e.g., 'atp:1234')
            
        Returns:
            Dictionary containing tournament details
        """
        if ":" not in tournament_id:
            return {"error": "Invalid tournament ID format. Expected 'tour:id' (e.g., 'atp:1234')"}
        
        tour, tour_id = tournament_id.split(":", 1)
        return self._make_request(tour, f"tournaments/{tour_id}")
    
    def get_match_info(self, match_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific match.
        
        Args:
            match_id: ID of the match in format 'tour:id' (e.g., 'atp:1234')
            
        Returns:
            Dictionary containing match details
        """
        if ":" not in match_id:
            return {"error": "Invalid match ID format. Expected 'tour:id' (e.g., 'atp:1234')"}
        
        tour, tour_id = match_id.split(":", 1)
        return self._make_request(tour, f"matches/{tour_id}")
    
    def get_player_info(self, player_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific player.
        
        Args:
            player_id: ID of the player in format 'tour:id' (e.g., 'atp:1234')
            
        Returns:
            Dictionary containing player details
        """
        if ":" not in player_id:
            return {"error": "Invalid player ID format. Expected 'tour:id' (e.g., 'atp:1234')"}
        
        tour, tour_id = player_id.split(":", 1)
        return self._make_request(tour, f"players/{tour_id}")
    
    def get_head_to_head(self, player1_id: str, player2_id: str) -> Dict[str, Any]:
        """
        Get head-to-head statistics between two players.
        
        Args:
            player1_id: ID of the first player in format 'tour:id' (e.g., 'atp:1234')
            player2_id: ID of the second player in format 'tour:id' (e.g., 'atp:5678')
            
        Returns:
            Dictionary containing head-to-head statistics
        """
        if ":" not in player1_id or ":" not in player2_id:
            return {"error": "Invalid player ID format. Expected 'tour:id' (e.g., 'atp:1234')"}
        
        tour1, tour_id1 = player1_id.split(":", 1)
        tour2, tour_id2 = player2_id.split(":", 1)
        
        # Both players should be from the same tour for head-to-head
        if tour1 != tour2:
            return {"error": "Players must be from the same tour for head-to-head statistics"}
        
        return self._make_request(tour1, "head-to-head", {
            "player1Id": tour_id1,
            "player2Id": tour_id2
        })
    
    def search_tournaments(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for tournaments matching the query in both ATP and WTA tours.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries containing tournament details
        """
        # Search in both tours
        atp_response = self._make_request("atp", "tournaments/search", {
            "q": query,
            "limit": limit // 2  # Split the limit between both tours
        })
        
        wta_response = self._make_request("wta", "tournaments/search", {
            "q": query,
            "limit": limit // 2
        })
        
        results = []
        
        # Add ATP results
        if "error" not in atp_response:
            for tournament in atp_response.get("tournaments", []):
                tournament["tour"] = "atp"
                results.append(tournament)
        
        # Add WTA results
        if "error" not in wta_response:
            for tournament in wta_response.get("tournaments", []):
                tournament["tour"] = "wta"
                results.append(tournament)
        
        # Sort by date (newest first)
        results.sort(key=lambda x: x.get("startDate", ""), reverse=True)
        
        return results[:limit]
