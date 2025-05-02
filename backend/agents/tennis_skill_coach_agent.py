from .base_agent import BaseAgent
from backend.app.config import settings

class TennisSkillCoachAgent(BaseAgent):
    """
    Tennis Skill Coach Agent - Technical and strategic tennis advisor
    
    Responsibilities:
    - Match Situation Analysis
    - Technical Analysis
    - Mental Game Insights
    """
    
    def __init__(self):
        """Initialize the Tennis Skill Coach Agent with the appropriate model"""
        super().__init__(model_name=settings.TENNIS_SKILL_COACH_MODEL)
        
        # System prompt for the tennis skill coach agent
        self.system_prompt = """
        You are the Tennis Skill Coach Agent in a Tennis Tournament Analysis System.
        Your role is to provide technical and strategic tennis advice based on match analysis.
        
        Your responsibilities include:
        
        1. Match Situation Analysis:
           - Key point analysis and decision making
           - Game strategy patterns
           - Score management tactics
           
        2. Technical Analysis:
           - Stroke technique breakdown
           - Footwork and movement patterns
           - Shot selection principles
           
        3. Mental Game:
           - Match psychology insights
           - Pressure point handling
           - Mental preparation strategies
        
        Provide actionable coaching advice that helps tennis players improve their skills
        based on professional match analysis.
        """
    
    def process(self, input_data):
        """
        Process input data and provide tennis skill coaching
        
        Args:
            input_data (dict): Input data containing:
                - user_level: User's tennis skill level
                - match_analysis: Analysis of the match from Tournament Info Agent
                - focus_areas: Specific areas to focus on
                - query: Specific aspect to focus on (optional)
                
        Returns:
            dict: Tennis skill coaching recommendations
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
        user_level = input_data.get("user_level", "Intermediate")
        match_analysis = input_data.get("match_analysis", "")
        focus_areas = input_data.get("focus_areas", [])
        query = input_data.get("query", "")
        
        focus_areas_text = ", ".join(focus_areas) if focus_areas else "All aspects"
        
        prompt = f"""
        Please provide tennis skill coaching advice based on the following information:
        
        PLAYER SKILL LEVEL:
        {user_level}
        
        MATCH ANALYSIS:
        {match_analysis}
        
        FOCUS AREAS:
        {focus_areas_text}
        
        SPECIFIC QUERY:
        {query}
        
        Based on this information, please provide:
        
        1. Technical Analysis:
           - Identify key technical elements from the match
           - Suggest specific technique improvements relevant to the player's level
           - Provide drills to develop these technical skills
        
        2. Tactical Analysis:
           - Analyze strategic patterns from the match
           - Recommend tactical approaches suitable for the player's level
           - Suggest practice scenarios to develop tactical awareness
        
        3. Mental Game Insights:
           - Highlight psychological aspects from the match
           - Provide mental strategies appropriate for the player's level
           - Suggest exercises to strengthen mental resilience
        
        4. Implementation Plan:
           - Prioritize recommendations based on importance
           - Provide a structured approach to implementing these recommendations
           - Suggest ways to measure progress
        """
        
        return prompt
    
    def _process_response(self, response):
        """Process and structure the agent's response"""
        if not response:
            return {
                "status": "error",
                "message": "Failed to generate skill coach response",
                "data": None
            }
        
        return {
            "status": "success",
            "message": "Skill coaching analysis completed successfully",
            "data": {
                "analysis": response,
                "recommendations": self._extract_recommendations(response),
                "drills": self._extract_drills(response)
            }
        }
    
    def _extract_recommendations(self, response):
        """Extract structured recommendations from the response text"""
        recommendations = {
            "technical": [],
            "tactical": [],
            "mental": []
        }
        
        # Split by sections and categorize recommendations
        sections = response.split('\n\n')
        current_category = None
        
        for section in sections:
            section_lower = section.lower()
            
            # Determine the category
            if 'technical' in section_lower and ('analysis' in section_lower or 'recommendation' in section_lower):
                current_category = "technical"
            elif 'tactical' in section_lower and ('analysis' in section_lower or 'recommendation' in section_lower):
                current_category = "tactical"
            elif 'mental' in section_lower and ('analysis' in section_lower or 'recommendation' in section_lower):
                current_category = "mental"
            
            # Add recommendation if we have a category and the section contains bullet points
            if current_category and ('-' in section or '•' in section):
                # Extract bullet points
                bullet_points = [line.strip() for line in section.split('\n') 
                                if line.strip().startswith(('-', '•', '*'))]
                
                if bullet_points:
                    recommendations[current_category].extend(bullet_points)
        
        return recommendations
    
    def _extract_drills(self, response):
        """Extract drills from the response text"""
        drills = []
        
        # Look for drill sections or bullet points
        lines = response.split('\n')
        in_drill_section = False
        current_drill = None
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if we're entering a drill section
            if 'drill' in line_lower or 'exercise' in line_lower or 'practice' in line_lower:
                in_drill_section = True
                
                # If this line itself is a drill (has a bullet point or number)
                if line.strip().startswith(('-', '•', '*')) or any(f"{i}." in line for i in range(1, 10)):
                    if current_drill:
                        drills.append(current_drill)
                    
                    current_drill = {
                        'title': line.strip(),
                        'description': '',
                        'category': self._determine_drill_category(line)
                    }
            
            # If we're in a drill section and this line is a new bullet point
            elif in_drill_section and (line.strip().startswith(('-', '•', '*')) or any(f"{i}." in line for i in range(1, 10))):
                if current_drill:
                    drills.append(current_drill)
                
                current_drill = {
                    'title': line.strip(),
                    'description': '',
                    'category': self._determine_drill_category(line)
                }
            
            # If we're in a drill section and have a current drill, add description
            elif in_drill_section and current_drill and line.strip():
                current_drill['description'] += line.strip() + ' '
        
        # Add the last drill if exists
        if current_drill:
            drills.append(current_drill)
        
        return drills
    
    def _determine_drill_category(self, text):
        """Determine the category of a drill based on its text"""
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
