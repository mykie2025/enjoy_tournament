"""
Base data source interface for tennis tournament data.
All data sources should implement this interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseDataSource(ABC):
    """
    Base interface for all tennis tournament data sources.
    
    Data sources are responsible for retrieving tennis tournament data
    from various external APIs, websites, or local databases.
    """
    
    @abstractmethod
    def get_tournament_info(self, tournament_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific tournament.
        
        Args:
            tournament_id: Identifier for the tournament
            
        Returns:
            Dictionary containing tournament details
        """
        pass
    
    @abstractmethod
    def get_match_info(self, match_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific match.
        
        Args:
            match_id: Identifier for the match
            
        Returns:
            Dictionary containing match details
        """
        pass
    
    @abstractmethod
    def get_player_info(self, player_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific player.
        
        Args:
            player_id: Identifier for the player
            
        Returns:
            Dictionary containing player details
        """
        pass
    
    @abstractmethod
    def get_head_to_head(self, player1_id: str, player2_id: str) -> Dict[str, Any]:
        """
        Get head-to-head statistics between two players.
        
        Args:
            player1_id: Identifier for the first player
            player2_id: Identifier for the second player
            
        Returns:
            Dictionary containing head-to-head statistics
        """
        pass
    
    @abstractmethod
    def search_tournaments(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for tournaments matching the query.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries containing tournament details
        """
        pass
