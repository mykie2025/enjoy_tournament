"""
Data source manager for tennis tournament data integration.
"""
from typing import Dict, Any, List, Optional, Type
import logging
from sqlalchemy.orm import Session

from .base_data_source import BaseDataSource
from .local_db_data_source import LocalDBDataSource
from .sportradar_api_source import SportRadarAPISource
from .tennis_data_api_source import TennisDataAPISource
from .tennis_tour_api_source import TennisTourAPISource
from ..app.config import settings
from ..database.database import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataSourceManager:
    """
    Manager for multiple tennis tournament data sources.
    
    Provides a unified interface for accessing tennis tournament data from various sources.
    Handles data integration, caching, and fallback mechanisms.
    """
    
    def __init__(self, db: Session = None):
        """
        Initialize the data source manager.
        
        Args:
            db: Database session. If None, a new session will be created.
        """
        self.db = db or next(get_db())
        self.sources = {}
        
        # Initialize data sources
        self._init_sources()
        
        logger.info("DataSourceManager initialized with sources: %s", list(self.sources.keys()))
    
    def _init_sources(self):
        """Initialize all available data sources."""
        # Always add local database source
        self.sources["local"] = LocalDBDataSource(self.db)
        
        # Add SportRadar API source if API key is available
        if hasattr(settings, "SPORTRADAR_API_KEY") and settings.SPORTRADAR_API_KEY:
            self.sources["sportradar"] = SportRadarAPISource()
        
        # Add Tennis-Data API source if API key is available
        if hasattr(settings, "TENNIS_DATA_API_KEY") and settings.TENNIS_DATA_API_KEY:
            self.sources["tennis_data"] = TennisDataAPISource()
        
        # Add Tennis Tour API source if API key is available
        if hasattr(settings, "TENNIS_TOUR_API_KEY") and settings.TENNIS_TOUR_API_KEY:
            self.sources["tennis_tour"] = TennisTourAPISource()
    
    def get_tournament_info(self, tournament_id: str, source: str = None) -> Dict[str, Any]:
        """
        Get detailed information about a specific tournament.
        
        Args:
            tournament_id: ID of the tournament
            source: Specific data source to use. If None, all sources will be tried.
            
        Returns:
            Dictionary containing tournament details
        """
        if source and source in self.sources:
            return self.sources[source].get_tournament_info(tournament_id)
        
        # Try SportRadar first if available
        if "sportradar" in self.sources:
            result = self.sources["sportradar"].get_tournament_info(tournament_id)
            if result and "error" not in result:
                return result
        
        # Try other external sources
        for source_name, source in self.sources.items():
            if source_name != "local" and source_name != "sportradar":
                result = source.get_tournament_info(tournament_id)
                if result and "error" not in result:
                    return result
        
        # Fall back to local database
        return self.sources["local"].get_tournament_info(tournament_id)
    
    def get_match_info(self, match_id: str, source: str = None) -> Dict[str, Any]:
        """
        Get detailed information about a specific match.
        
        Args:
            match_id: ID of the match
            source: Specific data source to use. If None, all sources will be tried.
            
        Returns:
            Dictionary containing match details
        """
        if source and source in self.sources:
            return self.sources[source].get_match_info(match_id)
        
        # Try SportRadar first if available
        if "sportradar" in self.sources:
            result = self.sources["sportradar"].get_match_info(match_id)
            if result and "error" not in result:
                return result
        
        # Try other external sources
        for source_name, source in self.sources.items():
            if source_name != "local" and source_name != "sportradar":
                result = source.get_match_info(match_id)
                if result and "error" not in result:
                    return result
        
        # Fall back to local database
        return self.sources["local"].get_match_info(match_id)
    
    def get_player_info(self, player_id: str, source: str = None) -> Dict[str, Any]:
        """
        Get detailed information about a specific player.
        
        Args:
            player_id: ID of the player
            source: Specific data source to use. If None, all sources will be tried.
            
        Returns:
            Dictionary containing player details
        """
        if source and source in self.sources:
            return self.sources[source].get_player_info(player_id)
        
        # Try SportRadar first if available
        if "sportradar" in self.sources:
            result = self.sources["sportradar"].get_player_info(player_id)
            if result and "error" not in result:
                return result
        
        # Try other external sources
        for source_name, source in self.sources.items():
            if source_name != "local" and source_name != "sportradar":
                result = source.get_player_info(player_id)
                if result and "error" not in result:
                    return result
        
        # Fall back to local database
        return self.sources["local"].get_player_info(player_id)
    
    def get_head_to_head(self, player1_id: str, player2_id: str, source: str = None) -> Dict[str, Any]:
        """
        Get head-to-head statistics between two players.
        
        Args:
            player1_id: ID of the first player
            player2_id: ID of the second player
            source: Specific data source to use. If None, all sources will be tried.
            
        Returns:
            Dictionary containing head-to-head statistics
        """
        if source and source in self.sources:
            return self.sources[source].get_head_to_head(player1_id, player2_id)
        
        # Try SportRadar first if available
        if "sportradar" in self.sources:
            result = self.sources["sportradar"].get_head_to_head(player1_id, player2_id)
            if result and "error" not in result:
                return result
        
        # Try other external sources
        for source_name, source in self.sources.items():
            if source_name != "local" and source_name != "sportradar":
                result = source.get_head_to_head(player1_id, player2_id)
                if result and "error" not in result:
                    return result
        
        # Fall back to local database
        return self.sources["local"].get_head_to_head(player1_id, player2_id)
    
    def search_tournaments(self, query: str, limit: int = 10, source: str = None) -> List[Dict[str, Any]]:
        """
        Search for tournaments matching the query.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            source: Specific data source to use. If None, all sources will be tried.
            
        Returns:
            List of dictionaries containing tournament details
        """
        if source and source in self.sources:
            return self.sources[source].search_tournaments(query, limit)
        
        # Combine results from all sources
        results = []
        
        # Try SportRadar first if available
        if "sportradar" in self.sources:
            sportradar_results = self.sources["sportradar"].search_tournaments(query, limit)
            if sportradar_results:
                for result in sportradar_results:
                    result["source"] = "sportradar"
                results.extend(sportradar_results)
        
        # Try other external sources
        for source_name, source in self.sources.items():
            if source_name != "local" and source_name != "sportradar":
                source_results = source.search_tournaments(query, limit)
                if source_results:
                    for result in source_results:
                        result["source"] = source_name
                    results.extend(source_results)
        
        # Include local database results
        local_results = self.sources["local"].search_tournaments(query, limit)
        if local_results:
            for result in local_results:
                result["source"] = "local"
            results.extend(local_results)
        
        # Remove duplicates based on tournament name and date
        unique_results = {}
        for result in results:
            key = f"{result.get('name', '')}-{result.get('start_date', '')}"
            if key not in unique_results:
                unique_results[key] = result
        
        # Return limited number of results
        return list(unique_results.values())[:limit]
    
    def get_tournament_seasons(self, tournament_id: str) -> Dict[str, Any]:
        """
        Get seasons for a specific tournament.
        
        Args:
            tournament_id: ID of the tournament
            
        Returns:
            Dictionary containing tournament seasons
        """
        # Only SportRadar supports this endpoint
        if "sportradar" in self.sources:
            return self.sources["sportradar"].get_tournament_seasons(tournament_id)
        return {"error": "No data source available for tournament seasons"}
    
    def get_tournament_schedule(self, tournament_id: str) -> Dict[str, Any]:
        """
        Get schedule for a specific tournament.
        
        Args:
            tournament_id: ID of the tournament
            
        Returns:
            Dictionary containing tournament schedule
        """
        # Only SportRadar supports this endpoint
        if "sportradar" in self.sources:
            return self.sources["sportradar"].get_tournament_schedule(tournament_id)
        return {"error": "No data source available for tournament schedule"}
    
    def get_tournament_results(self, tournament_id: str) -> Dict[str, Any]:
        """
        Get results for a specific tournament.
        
        Args:
            tournament_id: ID of the tournament
            
        Returns:
            Dictionary containing tournament results
        """
        # Only SportRadar supports this endpoint
        if "sportradar" in self.sources:
            return self.sources["sportradar"].get_tournament_results(tournament_id)
        return {"error": "No data source available for tournament results"}
    
    def get_match_timeline(self, match_id: str) -> Dict[str, Any]:
        """
        Get timeline for a specific match.
        
        Args:
            match_id: ID of the match
            
        Returns:
            Dictionary containing match timeline
        """
        # Only SportRadar supports this endpoint
        if "sportradar" in self.sources:
            return self.sources["sportradar"].get_match_timeline(match_id)
        return {"error": "No data source available for match timeline"}
    
    def get_player_statistics(self, player_id: str) -> Dict[str, Any]:
        """
        Get statistics for a specific player.
        
        Args:
            player_id: ID of the player
            
        Returns:
            Dictionary containing player statistics
        """
        # Only SportRadar supports this endpoint
        if "sportradar" in self.sources:
            return self.sources["sportradar"].get_player_statistics(player_id)
        return {"error": "No data source available for player statistics"}
    
    def get_rankings(self, type: str = "atp") -> Dict[str, Any]:
        """
        Get current rankings.
        
        Args:
            type: Type of rankings ('atp' or 'wta')
            
        Returns:
            Dictionary containing rankings
        """
        # Only SportRadar supports this endpoint
        if "sportradar" in self.sources:
            return self.sources["sportradar"].get_rankings(type)
        return {"error": "No data source available for rankings"}
    
    def get_current_tournaments(self) -> Dict[str, Any]:
        """
        Get currently active tournaments.
        
        Returns:
            Dictionary containing current tournaments
        """
        # Only SportRadar supports this endpoint
        if "sportradar" in self.sources:
            return self.sources["sportradar"].get_current_tournaments()
        return {"error": "No data source available for current tournaments"}


# Create a singleton instance
data_source_manager = DataSourceManager()
