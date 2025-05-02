from .base_agent import BaseAgent
from backend.app.config import settings

class OrchestratorAgent(BaseAgent):
    """
    Orchestrator Agent - Central coordinator for tennis analysis workflow
    
    Responsibilities:
    - Manage analysis workflow between agents
    - Synthesize insights from tournament and skill analysis
    - Generate comprehensive tennis development reports
    - Track implementation of recommendations
    """
    
    def __init__(self):
        """Initialize the Orchestrator Agent with the appropriate model"""
        super().__init__(model_name=settings.ORCHESTRATOR_MODEL)
        
        # System prompt for the orchestrator agent
        self.system_prompt = """
        You are the Orchestrator Agent in a Tennis Tournament Analysis System.
        Your role is to coordinate the analysis workflow between the Tournament Info Agent and Tennis Skill Coach Agent.
        You synthesize insights from both agents to generate comprehensive tennis development recommendations.
        
        Your responsibilities include:
        1. Managing the analysis workflow between agents
        2. Synthesizing insights from tournament and skill analysis
        3. Generating comprehensive tennis development reports
        4. Tracking implementation of recommendations
        
        Provide clear, actionable insights that help tennis players improve their skills based on professional match analysis.
        """
    
    def process(self, input_data):
        """
        Process input data and coordinate analysis between agents
        
        Args:
            input_data (dict): Input data containing:
                - user_preferences: User preferences and skill level
                - tournament_info: Output from Tournament Info Agent
                - skill_coach: Output from Tennis Skill Coach Agent
                - query: User's specific query (optional)
                
        Returns:
            dict: Synthesized analysis and recommendations
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
            max_tokens=2000
        )
        
        # Process and structure the response
        return self._process_response(response)
    
    def _format_input(self, input_data):
        """Format input data for the agent prompt"""
        user_preferences = input_data.get("user_preferences", {})
        tournament_info = input_data.get("tournament_info", {})
        skill_coach = input_data.get("skill_coach", {})
        query = input_data.get("query", "")
        
        prompt = f"""
        Please analyze the following tennis match information and provide comprehensive recommendations:
        
        USER PREFERENCES:
        - Skill Level: {user_preferences.get('skill_level', 'Not specified')}
        - Preferred Surface: {user_preferences.get('preferred_surface', 'Not specified')}
        - Playing Style: {user_preferences.get('playing_style', 'Not specified')}
        - Focus Areas: {', '.join(user_preferences.get('focus_areas', ['Not specified']))}
        
        TOURNAMENT INFO AGENT ANALYSIS:
        {tournament_info.get('analysis', 'No tournament analysis available')}
        
        TENNIS SKILL COACH ANALYSIS:
        {skill_coach.get('analysis', 'No skill coach analysis available')}
        
        USER QUERY:
        {query}
        
        Based on this information, please provide:
        1. A synthesis of the key insights from both analyses
        2. Specific, actionable recommendations for improvement
        3. A prioritized list of drills or exercises
        4. Suggestions for implementing these recommendations
        """
        
        return prompt
    
    def _process_response(self, response):
        """Process and structure the agent's response"""
        if not response:
            return {
                "status": "error",
                "message": "Failed to generate orchestrator response",
                "data": None
            }
        
        return {
            "status": "success",
            "message": "Orchestrator analysis completed successfully",
            "data": {
                "analysis": response,
                "recommendations": self._extract_recommendations(response)
            }
        }
    
    def _extract_recommendations(self, response):
        """Extract structured recommendations from the response text"""
        # This is a simple implementation that could be enhanced with more sophisticated parsing
        recommendations = []
        
        # Split by numbered items and look for recommendation patterns
        lines = response.split('\n')
        current_rec = None
        
        for line in lines:
            # Look for numbered recommendations or bullet points
            if (line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '•', '-')) and 
                any(keyword in line.lower() for keyword in ['recommend', 'drill', 'exercise', 'practice', 'improve'])):
                
                if current_rec:
                    recommendations.append(current_rec)
                
                current_rec = {
                    'title': line.strip(),
                    'description': '',
                    'category': self._determine_category(line),
                    'priority': len(recommendations) + 1
                }
            elif current_rec and line.strip():
                current_rec['description'] += line.strip() + ' '
        
        # Add the last recommendation if exists
        if current_rec:
            recommendations.append(current_rec)
        
        return recommendations
    
    def _determine_category(self, text):
        """Determine the category of a recommendation based on its text"""
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in ['forehand', 'backhand', 'serve', 'volley', 'technique', 'stroke']):
            return 'Technical'
        elif any(keyword in text_lower for keyword in ['strategy', 'tactic', 'position', 'pattern', 'game plan']):
            return 'Tactical'
        elif any(keyword in text_lower for keyword in ['mental', 'focus', 'confidence', 'pressure', 'psychology']):
            return 'Mental'
        elif any(keyword in text_lower for keyword in ['fitness', 'strength', 'conditioning', 'endurance', 'agility']):
            return 'Physical'
        else:
            return 'General'
