"""
SportRadar API data source for tennis tournament data.
"""
from typing import Dict, Any, List, Optional
import requests
import json
import os
from datetime import datetime

from .base_data_source import BaseDataSource
from ..app.config import settings


class SportRadarAPISource(BaseDataSource):
    """
    Data source that retrieves tennis tournament data from the SportRadar API.
    
    SportRadar provides comprehensive tennis data including tournaments, matches,
    players, rankings, and statistics.
    """
    
    def __init__(self):
        """Initialize the SportRadar API data source."""
        self.api_key = settings.SPORTRADAR_API_KEY
        self.base_url = "https://api.sportradar.com/tennis/production/v3"
        
        # Create a cache directory if it doesn't exist
        self.cache_dir = os.path.join(os.path.dirname(__file__), "..", "cache", "sportradar_api")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """
        Make a request to the SportRadar API with caching.
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            
        Returns:
            API response as a dictionary
        """
        # Add API key to parameters
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        
        # Create a cache key based on the endpoint and params
        cache_key = f"{endpoint}_{json.dumps(params)}.json"
        cache_path = os.path.join(self.cache_dir, cache_key.replace("/", "_"))
        
        # Check if we have a cached response
        if os.path.exists(cache_path):
            # Check if the cache is less than 6 hours old
            cache_time = os.path.getmtime(cache_path)
            if (datetime.now().timestamp() - cache_time) < 21600:  # 6 hours
                try:
                    with open(cache_path, "r") as f:
                        return json.load(f)
                except Exception:
                    # If there's an error reading the cache, proceed with the API call
                    pass
        
        # Make the API request
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, params=params)
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
            tournament_id: ID of the tournament (season_id in SportRadar terminology)
            
        Returns:
            Dictionary containing tournament details
        """
        # In SportRadar API, tournament info is accessed via season ID
        return self._make_request(f"en/seasons/{tournament_id}/summaries.json")
    
    def get_match_info(self, match_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific match.
        
        Args:
            match_id: ID of the match (sport_event_id in SportRadar terminology)
            
        Returns:
            Dictionary containing match details
        """
        return self._make_request(f"en/sport_events/{match_id}/summary.json")
    
    def get_player_info(self, player_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific player.
        
        Args:
            player_id: ID of the player (competitor_id in SportRadar terminology)
            
        Returns:
            Dictionary containing player details
        """
        return self._make_request(f"en/competitors/{player_id}/profile.json")
    
    def get_head_to_head(self, player1_id: str, player2_id: str) -> Dict[str, Any]:
        """
        Get head-to-head statistics between two players.
        
        Args:
            player1_id: ID of the first player
            player2_id: ID of the second player
            
        Returns:
            Dictionary containing head-to-head statistics
        """
        return self._make_request(f"en/competitors/{player1_id}/versus/{player2_id}/summaries.json")
    
    def search_tournaments(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for tournaments matching the query.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries containing tournament details
        """
        # SportRadar doesn't have a direct search endpoint, so we'll get all seasons
        # and filter them client-side
        response = self._make_request("en/seasons.json")
        
        if "error" in response:
            return []
        
        # Filter seasons by name
        seasons = response.get("seasons", [])
        filtered_seasons = []
        
        for season in seasons:
            name = season.get("name", "").lower()
            if query.lower() in name:
                filtered_seasons.append(season)
                if len(filtered_seasons) >= limit:
                    break
        
        return filtered_seasons
    
    def get_tournament_schedule(self, tournament_id: str) -> Dict[str, Any]:
        """
        Get the schedule for a specific tournament.
        
        Args:
            tournament_id: ID of the tournament (season_id in SportRadar terminology)
            
        Returns:
            Dictionary containing tournament schedule
        """
        # In SportRadar API, tournament schedule is accessed via season ID
        return self._make_request(f"en/seasons/{tournament_id}/summaries.json")
    
    def get_tournament_results(self, tournament_id: str) -> Dict[str, Any]:
        """
        Get the results for a specific tournament.
        
        Args:
            tournament_id: ID of the tournament (season_id in SportRadar terminology)
            
        Returns:
            Dictionary containing tournament results
        """
        # In SportRadar API, tournament results are accessed via season ID
        return self._make_request(f"en/seasons/{tournament_id}/summaries.json")
    
    def get_tournament_seasons(self, tournament_id: str) -> Dict[str, Any]:
        """
        Get the seasons for a specific tournament.
        
        Args:
            tournament_id: ID of the tournament (competition_id in SportRadar terminology)
            
        Returns:
            Dictionary containing tournament seasons
        """
        return self._make_request(f"en/competitions/{tournament_id}/seasons.json")
    
    def get_match_timeline(self, match_id: str) -> Dict[str, Any]:
        """
        Get the timeline for a specific match.
        
        Args:
            match_id: ID of the match (sport_event_id in SportRadar terminology)
            
        Returns:
            Dictionary containing match timeline
        """
        return self._make_request(f"en/sport_events/{match_id}/timeline.json")
    
    def get_player_statistics(self, player_id: str) -> Dict[str, Any]:
        """
        Get statistics for a specific player.
        
        Args:
            player_id: ID of the player (competitor_id in SportRadar terminology)
            
        Returns:
            Dictionary containing player statistics
        """
        # Player statistics are included in the profile
        return self._make_request(f"en/competitors/{player_id}/profile.json")
    
    def get_player_rankings(self, player_id: str) -> Dict[str, Any]:
        """
        Get rankings for a specific player.
        
        Args:
            player_id: ID of the player (competitor_id in SportRadar terminology)
            
        Returns:
            Dictionary containing player rankings
        """
        # Player rankings are included in the profile
        return self._make_request(f"en/competitors/{player_id}/profile.json")
    
    def get_rankings(self, type: str = "atp") -> Dict[str, Any]:
        """
        Get rankings for a specific type.
        
        Args:
            type: Type of rankings ('atp' or 'wta')
            
        Returns:
            Dictionary containing rankings
        """
        return self._make_request(f"en/rankings/{type}.json")
    
    def get_current_tournaments(self) -> Dict[str, Any]:
        """
        Get currently active tournaments.
        
        Returns:
            Dictionary containing current tournaments
        """
        return self._make_request("en/schedules/live/summaries.json")
    
    def get_daily_summaries(self, date: str = None) -> Dict[str, Any]:
        """
        Get daily summaries for a specific date.
        
        Args:
            date: Date in format 'YYYY-MM-DD' (defaults to today)
            
        Returns:
            Dictionary containing daily summaries
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        return self._make_request(f"en/schedules/{date}/summaries.json")
