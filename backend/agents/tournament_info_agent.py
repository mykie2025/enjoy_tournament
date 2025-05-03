from .base_agent import BaseAgent
from backend.app.config import settings
from backend.data_sources.data_source_manager import data_source_manager
from typing import Dict, Any, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TournamentInfoAgent(BaseAgent):
    """
    Tournament Info Agent - Tennis match and tournament analysis specialist
    
    Responsibilities:
    - Analyze tournament matches and key points
    - Extract player tactics and patterns
    - Compile match statistics and highlights
    - Identify critical moments and decision points
    """
    
    def __init__(self):
        """Initialize the Tournament Info Agent with the appropriate model"""
        super().__init__(model_name=settings.TOURNAMENT_INFO_MODEL)
        
        # System prompt for the tournament info agent
        self.system_prompt = """
        You are the Tournament Info Agent in a Tennis Tournament Analysis System.
        Your role is to analyze tennis matches and tournaments, extracting key patterns and insights.
        
        Your responsibilities include:
        1. Analyzing tournament matches and key points
        2. Extracting player tactics and patterns
        3. Compiling match statistics and highlights
        4. Identifying critical moments and decision points
        5. Integrating data from multiple sources to provide comprehensive analysis
        6. Comparing historical tournament data to identify trends and patterns
        7. Analyzing player head-to-head records and performance under different conditions
        
        Provide detailed, objective analysis of tennis matches that can help players understand
        professional tactics and strategies.
        """
        
        # Initialize data source manager
        self.data_manager = data_source_manager
    
    def process(self, input_data):
        """
        Process input data and analyze tournament/match information
        
        Args:
            input_data (dict): Input data containing:
                - match_data: Information about the match to analyze
                - player_stats: Statistics for the players in the match
                - query: Specific aspect to focus on (optional)
                
        Returns:
            dict: Tournament and match analysis
        """
        # Enrich input data with additional information from multiple sources
        enriched_data = self._enrich_input_data(input_data)
        
        # Prepare conversation messages
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self._format_input(enriched_data)}
        ]
        
        # Generate completion
        response = self.generate_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        # Process and structure the response
        return self._process_response(response)
    
    def _enrich_input_data(self, input_data):
        """
        Enrich input data with additional information from multiple sources
        
        Args:
            input_data (dict): Original input data
            
        Returns:
            dict: Enriched input data
        """
        logger.info("Enriching input data with additional information from multiple sources")
        
        match_data = input_data.get("match_data", {})
        player_stats = input_data.get("player_stats", {})
        
        enriched_data = {
            "match_data": match_data,
            "player_stats": player_stats,
            "query": input_data.get("query", ""),
            "additional_data": {}
        }
        
        try:
            # Get match ID
            match_id = str(match_data.get("id", ""))
            if not match_id:
                return input_data
            
            # Get player names
            player1_name = match_data.get("player1", "")
            player2_name = match_data.get("player2", "")
            
            # Get tournament ID
            tournament_id = str(match_data.get("tournament_id", ""))
            
            # Get additional match information from SportRadar if available
            if "sportradar" in self.data_manager.sources:
                logger.info("Getting additional match information from SportRadar")
                
                # Get current live matches
                live_matches = self.data_manager.get_current_tournaments(source="sportradar")
                if live_matches and "error" not in live_matches:
                    enriched_data["additional_data"]["live_matches"] = live_matches
                
                # Try to find the match in SportRadar by searching for the players
                sportradar_matches = []
                if player1_name and player2_name:
                    # First try to find in live matches
                    if "sport_events" in live_matches:
                        for event in live_matches.get("sport_events", []):
                            competitors = event.get("competitors", [])
                            if len(competitors) == 2:
                                comp1_name = competitors[0].get("name", "").lower()
                                comp2_name = competitors[1].get("name", "").lower()
                                if ((player1_name.lower() in comp1_name and player2_name.lower() in comp2_name) or
                                    (player1_name.lower() in comp2_name and player2_name.lower() in comp1_name)):
                                    sportradar_matches.append(event)
                    
                    # If not found in live matches, search in seasons
                    if not sportradar_matches:
                        search_results = self.data_manager.search_tournaments(
                            match_data.get("tournament", ""), 
                            limit=5, 
                            source="sportradar"
                        )
                        
                        if search_results:
                            for season in search_results:
                                season_id = season.get("id", "")
                                if season_id:
                                    season_details = self.data_manager.get_tournament_info(
                                        season_id, 
                                        source="sportradar"
                                    )
                                    
                                    if "sport_events" in season_details:
                                        for event in season_details.get("sport_events", []):
                                            competitors = event.get("competitors", [])
                                            if len(competitors) == 2:
                                                comp1_name = competitors[0].get("name", "").lower()
                                                comp2_name = competitors[1].get("name", "").lower()
                                                if ((player1_name.lower() in comp1_name and player2_name.lower() in comp2_name) or
                                                    (player1_name.lower() in comp2_name and player2_name.lower() in comp1_name)):
                                                    sportradar_matches.append(event)
                
                if sportradar_matches:
                    # Use the first matching match
                    sportradar_match = sportradar_matches[0]
                    enriched_data["additional_data"]["sportradar_match"] = sportradar_match
                    
                    # Get match timeline if available
                    sport_event_id = sportradar_match.get("id", "")
                    if sport_event_id:
                        match_timeline = self.data_manager.get_match_timeline(sport_event_id, source="sportradar")
                        if match_timeline and "error" not in match_timeline:
                            enriched_data["additional_data"]["match_timeline"] = match_timeline
                    
                    # Get player statistics
                    competitors = sportradar_match.get("competitors", [])
                    if len(competitors) == 2:
                        player1_id = competitors[0].get("id", "")
                        player2_id = competitors[1].get("id", "")
                        
                        if player1_id and player2_id:
                            # Get head-to-head statistics
                            head_to_head = self.data_manager.get_head_to_head(player1_id, player2_id, source="sportradar")
                            if head_to_head and "error" not in head_to_head:
                                enriched_data["additional_data"]["head_to_head"] = head_to_head
                            
                            # Get player statistics
                            player1_stats = self.data_manager.get_player_statistics(player1_id, source="sportradar")
                            if player1_stats and "error" not in player1_stats:
                                enriched_data["additional_data"]["player1_statistics"] = player1_stats
                            
                            player2_stats = self.data_manager.get_player_statistics(player2_id, source="sportradar")
                            if player2_stats and "error" not in player2_stats:
                                enriched_data["additional_data"]["player2_statistics"] = player2_stats
                
                # Get daily summaries for today
                daily_summaries = self.data_manager.sources["sportradar"].get_daily_summaries()
                if daily_summaries and "error" not in daily_summaries:
                    enriched_data["additional_data"]["daily_summaries"] = daily_summaries
            
            # Get tournament information
            if tournament_id:
                tournament_info = self.data_manager.get_tournament_info(tournament_id)
                if tournament_info and "error" not in tournament_info:
                    enriched_data["additional_data"]["tournament_info"] = tournament_info
            
            logger.info("Successfully enriched input data with additional information")
            
        except Exception as e:
            logger.error(f"Error enriching input data: {e}")
        
        return enriched_data
    
    def _format_input(self, input_data):
        """Format input data for the agent prompt"""
        match_data = input_data.get("match_data", {})
        player_stats = input_data.get("player_stats", {})
        query = input_data.get("query", "")
        additional_data = input_data.get("additional_data", {})
        
        # Basic match information
        prompt = f"""
        Please analyze the following tennis match:
        
        MATCH INFORMATION:
        - Tournament: {match_data.get('tournament', 'Not specified')}
        - Round: {match_data.get('round', 'Not specified')}
        - Surface: {match_data.get('surface', 'Not specified')}
        - Player 1: {match_data.get('player1', 'Not specified')}
        - Player 2: {match_data.get('player2', 'Not specified')}
        - Score: {match_data.get('score', 'Not specified')}
        - Duration: {match_data.get('duration', 'Not specified')}
        
        PLAYER STATISTICS:
        Player 1 ({match_data.get('player1', 'Player 1')}):
        - Aces: {player_stats.get('player1', {}).get('aces', 'N/A')}
        - Double Faults: {player_stats.get('player1', {}).get('double_faults', 'N/A')}
        - First Serve %: {player_stats.get('player1', {}).get('first_serve_percentage', 'N/A')}
        - First Serve Points Won %: {player_stats.get('player1', {}).get('first_serve_points_won_percentage', 'N/A')}
        - Second Serve Points Won %: {player_stats.get('player1', {}).get('second_serve_points_won_percentage', 'N/A')}
        - Break Points Saved: {player_stats.get('player1', {}).get('break_points_saved', 'N/A')}
        - Total Points Won: {player_stats.get('player1', {}).get('total_points_won', 'N/A')}
        
        Player 2 ({match_data.get('player2', 'Player 2')}):
        - Aces: {player_stats.get('player2', {}).get('aces', 'N/A')}
        - Double Faults: {player_stats.get('player2', {}).get('double_faults', 'N/A')}
        - First Serve %: {player_stats.get('player2', {}).get('first_serve_percentage', 'N/A')}
        - First Serve Points Won %: {player_stats.get('player2', {}).get('first_serve_points_won_percentage', 'N/A')}
        - Second Serve Points Won %: {player_stats.get('player2', {}).get('second_serve_points_won_percentage', 'N/A')}
        - Break Points Saved: {player_stats.get('player2', {}).get('break_points_saved', 'N/A')}
        - Total Points Won: {player_stats.get('player2', {}).get('total_points_won', 'N/A')}
        
        KEY MOMENTS:
        {match_data.get('key_moments', 'No key moments specified')}
        """
        
        # Add SportRadar match information if available
        if "sportradar_match" in additional_data:
            sr_match = additional_data["sportradar_match"]
            prompt += "\nSPORTRADAR MATCH INFORMATION:\n"
            
            # Extract tournament info
            tournament = sr_match.get("tournament", {})
            if tournament:
                prompt += f"- Tournament: {tournament.get('name', 'N/A')}\n"
                prompt += f"- Category: {tournament.get('category', {}).get('name', 'N/A')}\n"
            
            # Extract venue info
            venue = sr_match.get("venue", {})
            if venue:
                prompt += f"- Venue: {venue.get('name', 'N/A')}, {venue.get('city', {}).get('name', 'N/A')}, {venue.get('country', {}).get('name', 'N/A')}\n"
                prompt += f"- Court: {venue.get('court_name', 'N/A')}\n"
                prompt += f"- Surface: {venue.get('surface', 'N/A')}\n"
            
            # Extract competitor info
            competitors = sr_match.get("competitors", [])
            if len(competitors) == 2:
                player1 = competitors[0]
                player2 = competitors[1]
                
                prompt += f"- Player 1: {player1.get('name', 'N/A')} ({player1.get('country', {}).get('name', 'N/A')})\n"
                prompt += f"- Player 2: {player2.get('name', 'N/A')} ({player2.get('country', {}).get('name', 'N/A')})\n"
            
            # Extract match status
            status = sr_match.get("status", "")
            if status:
                prompt += f"- Status: {status}\n"
            
            # Extract scheduled time
            scheduled = sr_match.get("scheduled", "")
            if scheduled:
                prompt += f"- Scheduled: {scheduled}\n"
        
        # Add head-to-head information if available
        if "head_to_head" in additional_data:
            h2h = additional_data["head_to_head"]
            prompt += "\nHEAD-TO-HEAD INFORMATION:\n"
            
            # Extract total matches and results
            sport_events = h2h.get("sport_events", [])
            if sport_events:
                total_matches = len(sport_events)
                player1_wins = 0
                player2_wins = 0
                
                # Count wins for each player
                for event in sport_events:
                    competitors = event.get("competitors", [])
                    if len(competitors) == 2:
                        if competitors[0].get("winner", False):
                            player1_wins += 1
                        elif competitors[1].get("winner", False):
                            player2_wins += 1
                
                prompt += f"- Total Matches: {total_matches}\n"
                prompt += f"- {match_data.get('player1', 'Player 1')} Wins: {player1_wins}\n"
                prompt += f"- {match_data.get('player2', 'Player 2')} Wins: {player2_wins}\n"
                
                # Add recent head-to-head matches
                prompt += "- Recent Matches:\n"
                for i, event in enumerate(sport_events[:3]):  # Show up to 3 recent matches
                    result = event.get("results", [{}])[0] if event.get("results") else {}
                    home_score = result.get("home_score", "N/A")
                    away_score = result.get("away_score", "N/A")
                    
                    # Determine winner
                    winner = "Unknown"
                    competitors = event.get("competitors", [])
                    if len(competitors) == 2:
                        if competitors[0].get("winner", False):
                            winner = competitors[0].get("name", "Unknown")
                        elif competitors[1].get("winner", False):
                            winner = competitors[1].get("name", "Unknown")
                    
                    scheduled = event.get("scheduled", "N/A")
                    prompt += f"  {i+1}. {scheduled}: Winner: {winner}, Score: {home_score}-{away_score}\n"
        
        # Add player statistics if available
        if "player1_statistics" in additional_data or "player2_statistics" in additional_data:
            prompt += "\nADDITIONAL PLAYER STATISTICS:\n"
            
            if "player1_statistics" in additional_data:
                p1_stats = additional_data["player1_statistics"]
                prompt += f"{match_data.get('player1', 'Player 1')}:\n"
                
                # Extract player info
                competitor = p1_stats.get("competitor", {})
                if competitor:
                    prompt += f"- Nationality: {competitor.get('country', {}).get('name', 'N/A')}\n"
                    prompt += f"- Handedness: {competitor.get('handedness', 'N/A')}\n"
                    prompt += f"- Date of Birth: {competitor.get('date_of_birth', 'N/A')}\n"
                
                # Extract rankings
                rankings = p1_stats.get("rankings", [])
                if rankings:
                    for ranking in rankings:
                        prompt += f"- {ranking.get('name', 'Ranking')}: {ranking.get('rank', 'N/A')}\n"
                
                # Extract tournaments played
                tournaments = p1_stats.get("tournaments", [])
                if tournaments:
                    prompt += f"- Tournaments Played: {len(tournaments)}\n"
                    
                    # Count wins and losses
                    wins = 0
                    losses = 0
                    for tournament in tournaments:
                        for event in tournament.get("sport_events", []):
                            competitors = event.get("competitors", [])
                            for comp in competitors:
                                if comp.get("id") == competitor.get("id") and comp.get("winner") is not None:
                                    if comp.get("winner"):
                                        wins += 1
                                    else:
                                        losses += 1
                    
                    prompt += f"- Recent Form: {wins} wins, {losses} losses\n"
            
            if "player2_statistics" in additional_data:
                p2_stats = additional_data["player2_statistics"]
                prompt += f"{match_data.get('player2', 'Player 2')}:\n"
                
                # Extract player info
                competitor = p2_stats.get("competitor", {})
                if competitor:
                    prompt += f"- Nationality: {competitor.get('country', {}).get('name', 'N/A')}\n"
                    prompt += f"- Handedness: {competitor.get('handedness', 'N/A')}\n"
                    prompt += f"- Date of Birth: {competitor.get('date_of_birth', 'N/A')}\n"
                
                # Extract rankings
                rankings = p2_stats.get("rankings", [])
                if rankings:
                    for ranking in rankings:
                        prompt += f"- {ranking.get('name', 'Ranking')}: {ranking.get('rank', 'N/A')}\n"
                
                # Extract tournaments played
                tournaments = p2_stats.get("tournaments", [])
                if tournaments:
                    prompt += f"- Tournaments Played: {len(tournaments)}\n"
                    
                    # Count wins and losses
                    wins = 0
                    losses = 0
                    for tournament in tournaments:
                        for event in tournament.get("sport_events", []):
                            competitors = event.get("competitors", [])
                            for comp in competitors:
                                if comp.get("id") == competitor.get("id") and comp.get("winner") is not None:
                                    if comp.get("winner"):
                                        wins += 1
                                    else:
                                        losses += 1
                    
                    prompt += f"- Recent Form: {wins} wins, {losses} losses\n"
        
        # Add tournament information if available
        if "tournament_info" in additional_data:
            t_info = additional_data["tournament_info"]
            prompt += "\nTOURNAMENT CONTEXT:\n"
            
            # Extract tournament info
            tournament = t_info.get("tournament", {})
            if tournament:
                prompt += f"- Name: {tournament.get('name', 'N/A')}\n"
                prompt += f"- Category: {tournament.get('category', {}).get('name', 'N/A')}\n"
            
            # Extract season info
            season = t_info.get("season", {})
            if season:
                prompt += f"- Season: {season.get('name', 'N/A')}\n"
                prompt += f"- Start Date: {season.get('start_date', 'N/A')}\n"
                prompt += f"- End Date: {season.get('end_date', 'N/A')}\n"
            
            # Extract sport events
            sport_events = t_info.get("sport_events", [])
            if sport_events:
                prompt += f"- Total Matches: {len(sport_events)}\n"
                
                # Extract completed matches
                completed_matches = [e for e in sport_events if e.get("status") == "closed"]
                prompt += f"- Completed Matches: {len(completed_matches)}\n"
        
        # Add match timeline highlights if available
        if "match_timeline" in additional_data:
            timeline = additional_data["match_timeline"]
            prompt += "\nMATCH TIMELINE HIGHLIGHTS:\n"
            
            # Extract timeline events
            timeline_events = timeline.get("timeline", [])
            if timeline_events:
                # Filter for important events
                important_events = [e for e in timeline_events if e.get("important", False) or "break_point" in e.get("type", "").lower()]
                
                for event in important_events[:10]:  # Show up to 10 important events
                    event_type = event.get("type", "")
                    match_time = event.get("match_time", "")
                    
                    prompt += f"- {match_time}: {event_type.replace('_', ' ').title()}"
                    
                    # Add additional event details
                    if "competitor" in event:
                        prompt += f" by {event.get('competitor', {}).get('name', 'Unknown')}"
                    
                    if "score" in event:
                        home_score = event.get("score", {}).get("home", "")
                        away_score = event.get("score", {}).get("away", "")
                        prompt += f", Score: {home_score}-{away_score}"
                    
                    prompt += "\n"
        
        # Add live matches information if available
        if "live_matches" in additional_data:
            live_matches = additional_data["live_matches"]
            prompt += "\nCURRENT LIVE MATCHES:\n"
            
            # Extract sport events
            sport_events = live_matches.get("sport_events", [])
            if sport_events:
                for i, event in enumerate(sport_events[:5]):  # Show up to 5 live matches
                    tournament = event.get("tournament", {})
                    competitors = event.get("competitors", [])
                    
                    if tournament and len(competitors) == 2:
                        tournament_name = tournament.get("name", "Unknown Tournament")
                        player1_name = competitors[0].get("name", "Unknown")
                        player2_name = competitors[1].get("name", "Unknown")
                        
                        prompt += f"- {tournament_name}: {player1_name} vs {player2_name}"
                        
                        # Add score if available
                        if "sport_event_status" in event:
                            status = event.get("sport_event_status", {})
                            home_score = status.get("home_score", "")
                            away_score = status.get("away_score", "")
                            
                            if home_score and away_score:
                                prompt += f", Score: {home_score}-{away_score}"
                        
                        prompt += "\n"
        
        # Add specific focus query
        if query:
            prompt += f"""
        SPECIFIC FOCUS:
        {query}
        """
        
        prompt += """
        Based on this information, please provide:
        1. An overview of the match dynamics and flow
        2. Analysis of key tactical patterns used by both players
        3. Identification of critical moments that influenced the outcome
        4. Statistical insights and their implications
        5. Technical observations about both players' performances
        6. Head-to-head analysis and historical context
        7. Comparison with similar matches in the tournament
        """
        
        return prompt
    
    def _process_response(self, response):
        """Process and structure the agent's response"""
        if not response:
            return {
                "status": "error",
                "message": "Failed to generate tournament info response",
                "data": None
            }
        
        return {
            "status": "success",
            "message": "Tournament analysis completed successfully",
            "data": {
                "analysis": response,
                "key_insights": self._extract_key_insights(response)
            }
        }
    
    def _extract_key_insights(self, response):
        """Extract key insights from the response text"""
        insights = []
        
        # Split by paragraphs and look for key insights
        paragraphs = response.split('\n\n')
        
        for paragraph in paragraphs:
            if paragraph.strip() and len(paragraph.strip()) > 50:
                # Look for paragraphs that contain key insights
                if any(keyword in paragraph.lower() for keyword in [
                    'key', 'critical', 'important', 'significant', 'notable',
                    'tactic', 'strategy', 'pattern', 'technique', 'statistic',
                    'head-to-head', 'historical', 'comparison'
                ]):
                    insights.append(paragraph.strip())
        
        # If no insights were found, take the first few paragraphs
        if not insights and len(paragraphs) > 2:
            insights = [p.strip() for p in paragraphs[1:3] if p.strip()]
        
        return insights
        
    def analyze_match(self, match_id):
        """
        Analyze a match using the Tournament Info Agent.
        
        Args:
            match_id: ID of the match to analyze
            
        Returns:
            dict: Analysis results
        """
        logger.info(f"Analyzing match {match_id} with Tournament Info Agent")
        
        try:
            # Get match data from the data source manager
            match_data = self.data_manager.get_match_info(str(match_id))
            
            if "error" in match_data:
                logger.error(f"Error retrieving match data: {match_data['error']}")
                return {
                    "status": "error",
                    "message": f"Failed to retrieve match data: {match_data['error']}",
                    "data": None
                }
            
            # Extract player statistics from match data
            player_stats = {
                "player1": {},
                "player2": {}
            }
            
            # Process points to extract statistics
            if "points" in match_data:
                points = match_data["points"]
                
                # Calculate basic statistics
                p1_aces = sum(1 for p in points if p.get("winning_shot") == "ace" and p.get("server") == match_data["player1"])
                p2_aces = sum(1 for p in points if p.get("winning_shot") == "ace" and p.get("server") == match_data["player2"])
                
                p1_double_faults = sum(1 for p in points if not p.get("first_serve_in") and p.get("server") == match_data["player1"] and p.get("winner") != match_data["player1"])
                p2_double_faults = sum(1 for p in points if not p.get("first_serve_in") and p.get("server") == match_data["player2"] and p.get("winner") != match_data["player2"])
                
                p1_first_serves = sum(1 for p in points if p.get("server") == match_data["player1"] and p.get("first_serve_in") is not None)
                p1_first_serves_in = sum(1 for p in points if p.get("server") == match_data["player1"] and p.get("first_serve_in") == True)
                
                p2_first_serves = sum(1 for p in points if p.get("server") == match_data["player2"] and p.get("first_serve_in") is not None)
                p2_first_serves_in = sum(1 for p in points if p.get("server") == match_data["player2"] and p.get("first_serve_in") == True)
                
                p1_first_serve_points = sum(1 for p in points if p.get("server") == match_data["player1"] and p.get("first_serve_in") == True)
                p1_first_serve_points_won = sum(1 for p in points if p.get("server") == match_data["player1"] and p.get("first_serve_in") == True and p.get("winner") == match_data["player1"])
                
                p2_first_serve_points = sum(1 for p in points if p.get("server") == match_data["player2"] and p.get("first_serve_in") == True)
                p2_first_serve_points_won = sum(1 for p in points if p.get("server") == match_data["player2"] and p.get("first_serve_in") == True and p.get("winner") == match_data["player2"])
                
                p1_second_serve_points = sum(1 for p in points if p.get("server") == match_data["player1"] and p.get("first_serve_in") == False)
                p1_second_serve_points_won = sum(1 for p in points if p.get("server") == match_data["player1"] and p.get("first_serve_in") == False and p.get("winner") == match_data["player1"])
                
                p2_second_serve_points = sum(1 for p in points if p.get("server") == match_data["player2"] and p.get("first_serve_in") == False)
                p2_second_serve_points_won = sum(1 for p in points if p.get("server") == match_data["player2"] and p.get("first_serve_in") == False and p.get("winner") == match_data["player2"])
                
                p1_break_points_faced = sum(1 for p in points if p.get("server") == match_data["player1"] and "break point" in p.get("point_score", "").lower())
                p1_break_points_saved = sum(1 for p in points if p.get("server") == match_data["player1"] and "break point" in p.get("point_score", "").lower() and p.get("winner") == match_data["player1"])
                
                p2_break_points_faced = sum(1 for p in points if p.get("server") == match_data["player2"] and "break point" in p.get("point_score", "").lower())
                p2_break_points_saved = sum(1 for p in points if p.get("server") == match_data["player2"] and "break point" in p.get("point_score", "").lower() and p.get("winner") == match_data["player2"])
                
                p1_total_points_won = sum(1 for p in points if p.get("winner") == match_data["player1"])
                p2_total_points_won = sum(1 for p in points if p.get("winner") == match_data["player2"])
                
                # Set player statistics
                player_stats["player1"] = {
                    "aces": p1_aces,
                    "double_faults": p1_double_faults,
                    "first_serve_percentage": round((p1_first_serves_in / p1_first_serves * 100) if p1_first_serves > 0 else 0, 1),
                    "first_serve_points_won_percentage": round((p1_first_serve_points_won / p1_first_serve_points * 100) if p1_first_serve_points > 0 else 0, 1),
                    "second_serve_points_won_percentage": round((p1_second_serve_points_won / p1_second_serve_points * 100) if p1_second_serve_points > 0 else 0, 1),
                    "break_points_saved": f"{p1_break_points_saved}/{p1_break_points_faced}",
                    "total_points_won": p1_total_points_won
                }
                
                player_stats["player2"] = {
                    "aces": p2_aces,
                    "double_faults": p2_double_faults,
                    "first_serve_percentage": round((p2_first_serves_in / p2_first_serves * 100) if p2_first_serves > 0 else 0, 1),
                    "first_serve_points_won_percentage": round((p2_first_serve_points_won / p2_first_serve_points * 100) if p2_first_serve_points > 0 else 0, 1),
                    "second_serve_points_won_percentage": round((p2_second_serve_points_won / p2_second_serve_points * 100) if p2_second_serve_points > 0 else 0, 1),
                    "break_points_saved": f"{p2_break_points_saved}/{p2_break_points_faced}",
                    "total_points_won": p2_total_points_won
                }
            
            # Identify key moments
            key_moments = self._identify_key_moments(match_data)
            
            # Prepare input data for the agent
            input_data = {
                "match_data": {
                    "id": match_data["id"],
                    "tournament_id": match_data["tournament"]["id"],
                    "tournament": match_data["tournament"]["name"],
                    "round": match_data["round"],
                    "surface": match_data["tournament"]["surface"],
                    "player1": match_data["player1"],
                    "player2": match_data["player2"],
                    "score": match_data["score"],
                    "date": match_data["date"],
                    "duration": match_data["duration"],
                    "key_moments": key_moments
                },
                "player_stats": player_stats
            }
            
            # Process the input data
            return self.process(input_data)
            
        except Exception as e:
            logger.error(f"Error analyzing match: {e}")
            return {
                "status": "error",
                "message": f"Failed to analyze match: {str(e)}",
                "data": None
            }
    
    def _identify_key_moments(self, match_data):
        """
        Identify key moments in a match.
        
        Args:
            match_data: Match data dictionary
            
        Returns:
            str: Description of key moments
        """
        key_moments = []
        
        # Check if points data is available
        if "points" not in match_data or not match_data["points"]:
            return "No point-by-point data available to identify key moments."
        
        points = match_data["points"]
        
        # Identify break points
        break_points = [p for p in points if "break point" in p.get("point_score", "").lower()]
        if break_points:
            break_point_conversions = [p for p in break_points if p.get("winner") != p.get("server")]
            key_moments.append(f"Break points: {len(break_point_conversions)}/{len(break_points)} converted")
        
        # Identify long rallies
        long_rallies = [p for p in points if p.get("rally_length", 0) > 9]  # Rallies with 10+ shots
        if long_rallies:
            p1_long_rally_wins = sum(1 for p in long_rallies if p.get("winner") == match_data["player1"])
            p2_long_rally_wins = sum(1 for p in long_rallies if p.get("winner") == match_data["player2"])
            key_moments.append(f"Long rallies (10+ shots): {match_data['player1']} won {p1_long_rally_wins}, {match_data['player2']} won {p2_long_rally_wins}")
        
        # Identify tiebreaks
        tiebreak_points = [p for p in points if "tiebreak" in p.get("game_score", "").lower()]
        if tiebreak_points:
            tiebreak_sets = set()
            for p in tiebreak_points:
                if "game_score" in p:
                    set_number = p["game_score"].split("-")[0].strip()[0]
                    tiebreak_sets.add(set_number)
            
            key_moments.append(f"Tiebreaks played in sets: {', '.join(sorted(tiebreak_sets))}")
        
        # Identify comebacks
        # This is a simplified approach - would need more sophisticated logic for a real implementation
        sets = {}
        for p in points:
            if "game_score" in p:
                set_number = p["game_score"].split("-")[0].strip()[0]
                if set_number not in sets:
                    sets[set_number] = []
                sets[set_number].append(p)
        
        for set_number, set_points in sets.items():
            # Check if a player was down by 2+ games and came back to win the set
            games_diff = []
            current_diff = 0
            
            for p in set_points:
                if "game_score" in p:
                    game_score = p["game_score"].split("-")
                    if len(game_score) >= 2:
                        p1_games = int(game_score[0].strip()[-1])
                        p2_games = int(game_score[1].strip()[0])
                        current_diff = p1_games - p2_games
                        games_diff.append(current_diff)
            
            if games_diff:
                min_diff = min(games_diff)
                max_diff = max(games_diff)
                
                if min_diff <= -2 and max_diff > 0:
                    key_moments.append(f"Comeback in Set {set_number}: {match_data['player1']} was down by {abs(min_diff)} games but won the set")
                elif max_diff >= 2 and min_diff < 0:
                    key_moments.append(f"Comeback in Set {set_number}: {match_data['player2']} was down by {max_diff} games but won the set")
        
        # Format the key moments
        if key_moments:
            return "\n".join(key_moments)
        else:
            return "No significant key moments identified."
