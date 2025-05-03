"""
Local database data source for tennis tournament data.
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .base_data_source import BaseDataSource
from ..database.models import Tournament, Match, Point
from ..database.database import get_db


class LocalDBDataSource(BaseDataSource):
    """
    Data source that retrieves tennis tournament data from the local database.
    """
    
    def __init__(self, db: Session = None):
        """
        Initialize the local database data source.
        
        Args:
            db: Database session. If None, a new session will be created.
        """
        self.db = db or next(get_db())
    
    def get_tournament_info(self, tournament_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific tournament from the local database.
        
        Args:
            tournament_id: ID of the tournament
            
        Returns:
            Dictionary containing tournament details
        """
        tournament = self.db.query(Tournament).filter(Tournament.id == int(tournament_id)).first()
        if not tournament:
            return {"error": "Tournament not found"}
        
        # Get matches for this tournament
        matches = self.db.query(Match).filter(Match.tournament_id == int(tournament_id)).all()
        
        # Format response
        return {
            "id": tournament.id,
            "name": tournament.name,
            "location": tournament.location,
            "start_date": tournament.start_date.isoformat() if tournament.start_date else None,
            "end_date": tournament.end_date.isoformat() if tournament.end_date else None,
            "surface": tournament.surface,
            "category": tournament.category,
            "matches": [
                {
                    "id": match.id,
                    "round": match.round,
                    "player1": match.player1,
                    "player2": match.player2,
                    "score": match.score,
                    "date": match.date.isoformat() if match.date else None,
                    "duration": match.duration
                }
                for match in matches
            ]
        }
    
    def get_match_info(self, match_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific match from the local database.
        
        Args:
            match_id: ID of the match
            
        Returns:
            Dictionary containing match details
        """
        match = self.db.query(Match).filter(Match.id == int(match_id)).first()
        if not match:
            return {"error": "Match not found"}
        
        # Get points for this match
        points = self.db.query(Point).filter(Point.match_id == int(match_id)).all()
        
        # Get tournament info
        tournament = self.db.query(Tournament).filter(Tournament.id == match.tournament_id).first()
        
        # Format response
        return {
            "id": match.id,
            "tournament": {
                "id": tournament.id,
                "name": tournament.name,
                "surface": tournament.surface,
                "category": tournament.category
            },
            "round": match.round,
            "player1": match.player1,
            "player2": match.player2,
            "score": match.score,
            "date": match.date.isoformat() if match.date else None,
            "duration": match.duration,
            "points": [
                {
                    "id": point.id,
                    "point_number": point.point_number,
                    "game_score": point.game_score,
                    "point_score": point.point_score,
                    "server": point.server,
                    "winner": point.winner,
                    "first_serve_in": point.first_serve_in,
                    "serve_type": point.serve_type,
                    "return_type": point.return_type,
                    "rally_length": point.rally_length,
                    "winning_shot": point.winning_shot
                }
                for point in points
            ]
        }
    
    def get_player_info(self, player_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific player from the local database.
        Note: In the current schema, players are stored as strings in the Match table,
        not as separate entities. This method uses the player name as the ID.
        
        Args:
            player_id: Name of the player
            
        Returns:
            Dictionary containing player details
        """
        # Find matches where this player participated
        matches = self.db.query(Match).filter(
            (Match.player1 == player_id) | (Match.player2 == player_id)
        ).all()
        
        if not matches:
            return {"error": "Player not found"}
        
        # Calculate basic stats
        total_matches = len(matches)
        wins = sum(1 for match in matches if 
                  (match.player1 == player_id and match.score.split('-')[0] > match.score.split('-')[1]) or
                  (match.player2 == player_id and match.score.split('-')[1] > match.score.split('-')[0]))
        
        # Format response
        return {
            "name": player_id,
            "matches_played": total_matches,
            "wins": wins,
            "losses": total_matches - wins,
            "win_percentage": (wins / total_matches) * 100 if total_matches > 0 else 0,
            "recent_matches": [
                {
                    "id": match.id,
                    "tournament_id": match.tournament_id,
                    "opponent": match.player2 if match.player1 == player_id else match.player1,
                    "score": match.score,
                    "result": "win" if 
                            (match.player1 == player_id and match.score.split('-')[0] > match.score.split('-')[1]) or
                            (match.player2 == player_id and match.score.split('-')[1] > match.score.split('-')[0])
                            else "loss"
                }
                for match in matches[:5]  # Last 5 matches
            ]
        }
    
    def get_head_to_head(self, player1_id: str, player2_id: str) -> Dict[str, Any]:
        """
        Get head-to-head statistics between two players from the local database.
        
        Args:
            player1_id: Name of the first player
            player2_id: Name of the second player
            
        Returns:
            Dictionary containing head-to-head statistics
        """
        # Find matches between these two players
        matches = self.db.query(Match).filter(
            ((Match.player1 == player1_id) & (Match.player2 == player2_id)) |
            ((Match.player1 == player2_id) & (Match.player2 == player1_id))
        ).all()
        
        if not matches:
            return {
                "player1": player1_id,
                "player2": player2_id,
                "total_matches": 0,
                "player1_wins": 0,
                "player2_wins": 0,
                "matches": []
            }
        
        # Calculate head-to-head stats
        player1_wins = sum(1 for match in matches if 
                         (match.player1 == player1_id and match.score.split('-')[0] > match.score.split('-')[1]) or
                         (match.player2 == player1_id and match.score.split('-')[1] > match.score.split('-')[0]))
        
        # Format response
        return {
            "player1": player1_id,
            "player2": player2_id,
            "total_matches": len(matches),
            "player1_wins": player1_wins,
            "player2_wins": len(matches) - player1_wins,
            "matches": [
                {
                    "id": match.id,
                    "tournament_id": match.tournament_id,
                    "round": match.round,
                    "score": match.score,
                    "date": match.date.isoformat() if match.date else None,
                    "winner": player1_id if 
                             (match.player1 == player1_id and match.score.split('-')[0] > match.score.split('-')[1]) or
                             (match.player2 == player1_id and match.score.split('-')[1] > match.score.split('-')[0])
                             else player2_id
                }
                for match in matches
            ]
        }
    
    def search_tournaments(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for tournaments matching the query in the local database.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries containing tournament details
        """
        # Search for tournaments by name or location
        tournaments = self.db.query(Tournament).filter(
            (Tournament.name.ilike(f"%{query}%")) |
            (Tournament.location.ilike(f"%{query}%")) |
            (Tournament.category.ilike(f"%{query}%"))
        ).limit(limit).all()
        
        # Format response
        return [
            {
                "id": tournament.id,
                "name": tournament.name,
                "location": tournament.location,
                "start_date": tournament.start_date.isoformat() if tournament.start_date else None,
                "end_date": tournament.end_date.isoformat() if tournament.end_date else None,
                "surface": tournament.surface,
                "category": tournament.category
            }
            for tournament in tournaments
        ]
