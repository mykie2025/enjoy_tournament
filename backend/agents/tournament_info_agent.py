from .base_agent import BaseAgent
from backend.app.config import settings

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
        
        Provide detailed, objective analysis of tennis matches that can help players understand
        professional tactics and strategies.
        """
    
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
        # Prepare conversation messages
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self._format_input(input_data)}
        ]
        
        # Generate completion
        response = self.generate_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        # Process and structure the response
        return self._process_response(response)
    
    def _format_input(self, input_data):
        """Format input data for the agent prompt"""
        match_data = input_data.get("match_data", {})
        player_stats = input_data.get("player_stats", {})
        query = input_data.get("query", "")
        
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
        
        SPECIFIC FOCUS:
        {query}
        
        Based on this information, please provide:
        1. An overview of the match dynamics and flow
        2. Analysis of key tactical patterns used by both players
        3. Identification of critical moments that influenced the outcome
        4. Statistical insights and their implications
        5. Technical observations about both players' performances
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
                    'tactic', 'strategy', 'pattern', 'technique', 'statistic'
                ]):
                    insights.append(paragraph.strip())
        
        # If no insights were found, take the first few paragraphs
        if not insights and len(paragraphs) > 2:
            insights = [p.strip() for p in paragraphs[1:3] if p.strip()]
        
        return insights
