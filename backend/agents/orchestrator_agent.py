from .base_agent import BaseAgent
from backend.app.config import settings
import json
from datetime import datetime

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
        1. Managing the analysis workflow between agents with advanced task coordination
        2. Synthesizing insights from tournament and skill analysis using improved recommendation logic
        3. Generating comprehensive tennis development reports with actionable insights
        4. Tracking implementation of recommendations with progress metrics
        5. Prioritizing recommendations based on player needs and potential impact
        
        Provide clear, actionable insights that help tennis players improve their skills based on professional match analysis.
        Consider short-term and long-term development goals when making recommendations.
        """
        
        # Task coordination state
        self.task_state = {
            "current_tasks": [],
            "completed_tasks": [],
            "pending_tasks": [],
            "task_dependencies": {}
        }
        
        # Progress tracking
        self.progress_tracker = {
            "recommendations": {},
            "last_updated": None,
            "implementation_metrics": {}
        }
    
    def process(self, input_data):
        """
        Process input data and coordinate analysis between agents
        
        Args:
            input_data (dict): Input data containing:
                - user_preferences: User preferences and skill level
                - tournament_info: Output from Tournament Info Agent
                - skill_coach: Output from Tennis Skill Coach Agent
                - query: User's specific query (optional)
                - previous_recommendations: Previous recommendations (optional)
                - implementation_progress: Progress on previous recommendations (optional)
                
        Returns:
            dict: Synthesized analysis and recommendations with progress tracking
        """
        # Update task coordination state
        self._update_task_state(input_data)
        
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
        processed_response = self._process_response(response)
        
        # Update progress tracking
        self._update_progress_tracking(processed_response, input_data)
        
        return processed_response
    
    def _update_task_state(self, input_data):
        """Update the task coordination state based on input data"""
        # Extract relevant information from input data
        query = input_data.get("query", "")
        previous_recommendations = input_data.get("previous_recommendations", [])
        
        # Clear current tasks
        self.task_state["current_tasks"] = []
        
        # Determine tasks based on query and available data
        if "tournament_info" in input_data and "skill_coach" not in input_data:
            self.task_state["current_tasks"].append({
                "id": f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "type": "request_skill_analysis",
                "description": "Request skill analysis based on tournament information",
                "priority": "high"
            })
        
        if "skill_coach" in input_data and "tournament_info" not in input_data:
            self.task_state["current_tasks"].append({
                "id": f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "type": "request_tournament_analysis",
                "description": "Request tournament analysis to complement skill coaching",
                "priority": "high"
            })
        
        # Add synthesis task if we have both analyses
        if "tournament_info" in input_data and "skill_coach" in input_data:
            self.task_state["current_tasks"].append({
                "id": f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "type": "synthesize_analyses",
                "description": "Synthesize tournament and skill analyses",
                "priority": "highest"
            })
        
        # Add progress tracking task if we have previous recommendations
        if previous_recommendations:
            self.task_state["current_tasks"].append({
                "id": f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "type": "track_recommendation_progress",
                "description": "Track progress on previous recommendations",
                "priority": "medium"
            })
    
    def _format_input(self, input_data):
        """Format input data for the agent prompt"""
        user_preferences = input_data.get("user_preferences", {})
        tournament_info = input_data.get("tournament_info", {})
        skill_coach = input_data.get("skill_coach", {})
        query = input_data.get("query", "")
        previous_recommendations = input_data.get("previous_recommendations", [])
        implementation_progress = input_data.get("implementation_progress", {})
        
        # Format previous recommendations and progress if available
        previous_recs_text = ""
        if previous_recommendations:
            previous_recs_text = "\nPREVIOUS RECOMMENDATIONS:\n"
            for i, rec in enumerate(previous_recommendations):
                progress = implementation_progress.get(rec.get("id", ""), "Not started")
                previous_recs_text += f"{i+1}. {rec.get('title', 'Recommendation')}: {progress}\n"
        
        prompt = f"""
        Please analyze the following tennis match information and provide comprehensive recommendations:
        
        USER PREFERENCES:
        - Skill Level: {user_preferences.get('skill_level', 'Not specified')}
        - Preferred Surface: {user_preferences.get('preferred_surface', 'Not specified')}
        - Playing Style: {user_preferences.get('playing_style', 'Not specified')}
        - Focus Areas: {', '.join(user_preferences.get('focus_areas', ['Not specified']))}
        - Development Goals: {', '.join(user_preferences.get('development_goals', ['Not specified']))}
        
        TOURNAMENT INFO AGENT ANALYSIS:
        {tournament_info.get('analysis', 'No tournament analysis available')}
        
        TENNIS SKILL COACH ANALYSIS:
        {skill_coach.get('analysis', 'No skill coach analysis available')}
        {previous_recs_text}
        USER QUERY:
        {query}
        
        Based on this information, please provide:
        1. A synthesis of the key insights from both analyses, highlighting patterns and connections
        2. Specific, actionable recommendations for improvement with clear implementation steps
        3. A prioritized list of drills or exercises with expected outcomes
        4. Suggestions for implementing these recommendations with measurable progress indicators
        5. A timeline for implementation with short-term and long-term goals
        
        For each recommendation, include:
        - Priority level (High/Medium/Low)
        - Expected timeframe for results
        - Difficulty level
        - Prerequisites (if any)
        - Success metrics
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
        
        recommendations = self._extract_recommendations(response)
        
        # Generate recommendation IDs if they don't exist
        for rec in recommendations:
            if "id" not in rec:
                rec["id"] = f"rec_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(recommendations)}"
        
        return {
            "status": "success",
            "message": "Orchestrator analysis completed successfully",
            "data": {
                "analysis": response,
                "recommendations": recommendations,
                "task_state": self.task_state,
                "progress_metrics": self._calculate_progress_metrics(recommendations)
            }
        }
    
    def _extract_recommendations(self, response):
        """Extract structured recommendations from the response text with enhanced parsing"""
        recommendations = []
        
        # Split by numbered items and look for recommendation patterns
        lines = response.split('\n')
        current_rec = None
        in_recommendation_section = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Detect recommendation sections
            if any(section in line_lower for section in ["recommendation", "recommendations:", "recommended", "suggest"]):
                in_recommendation_section = True
                continue
                
            # Look for numbered recommendations or bullet points
            if in_recommendation_section and (
                line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '•', '-')) or
                any(keyword in line_lower for keyword in ['recommend', 'drill', 'exercise', 'practice', 'improve'])
            ):
                if current_rec:
                    # Process the current recommendation before starting a new one
                    self._process_recommendation_details(current_rec, lines[i-5:i-1])
                    recommendations.append(current_rec)
                
                # Start a new recommendation
                current_rec = {
                    'id': f"rec_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(recommendations)}",
                    'title': line.strip(),
                    'description': '',
                    'category': self._determine_category(line),
                    'priority': self._extract_priority(line),
                    'difficulty': 'Medium',  # Default value
                    'timeframe': 'Medium-term',  # Default value
                    'prerequisites': [],
                    'success_metrics': []
                }
            elif current_rec and line.strip():
                # Add to description of current recommendation
                current_rec['description'] += line.strip() + ' '
                
                # Look for specific details in the line
                self._extract_recommendation_details(current_rec, line)
        
        # Add the last recommendation if exists
        if current_rec:
            self._process_recommendation_details(current_rec, lines[-5:])
            recommendations.append(current_rec)
        
        return recommendations
    
    def _process_recommendation_details(self, recommendation, context_lines):
        """Process additional details for a recommendation from surrounding context"""
        context_text = '\n'.join(line.strip() for line in context_lines if line.strip())
        context_lower = context_text.lower()
        
        # Extract difficulty if not already set
        if recommendation['difficulty'] == 'Medium':
            if 'easy' in context_lower or 'beginner' in context_lower or 'simple' in context_lower:
                recommendation['difficulty'] = 'Easy'
            elif 'hard' in context_lower or 'advanced' in context_lower or 'challenging' in context_lower:
                recommendation['difficulty'] = 'Hard'
        
        # Extract timeframe if not already set
        if recommendation['timeframe'] == 'Medium-term':
            if 'immediate' in context_lower or 'short-term' in context_lower or 'quick' in context_lower:
                recommendation['timeframe'] = 'Short-term'
            elif 'long-term' in context_lower or 'extended' in context_lower or 'over time' in context_lower:
                recommendation['timeframe'] = 'Long-term'
        
        # Extract success metrics if not already set
        if not recommendation['success_metrics']:
            metric_indicators = ['measure', 'success', 'improvement', 'progress', 'indicator', 'metric']
            for line in context_lines:
                if any(indicator in line.lower() for indicator in metric_indicators):
                    recommendation['success_metrics'].append(line.strip())
    
    def _extract_recommendation_details(self, recommendation, line):
        """Extract specific details from a line for a recommendation"""
        line_lower = line.lower()
        
        # Extract priority
        if 'priority' in line_lower:
            if 'high' in line_lower:
                recommendation['priority'] = 'High'
            elif 'medium' in line_lower:
                recommendation['priority'] = 'Medium'
            elif 'low' in line_lower:
                recommendation['priority'] = 'Low'
        
        # Extract difficulty
        if 'difficulty' in line_lower or 'level' in line_lower:
            if 'easy' in line_lower or 'beginner' in line_lower:
                recommendation['difficulty'] = 'Easy'
            elif 'medium' in line_lower or 'intermediate' in line_lower:
                recommendation['difficulty'] = 'Medium'
            elif 'hard' in line_lower or 'advanced' in line_lower or 'difficult' in line_lower:
                recommendation['difficulty'] = 'Hard'
        
        # Extract timeframe
        if 'timeframe' in line_lower or 'time' in line_lower or 'period' in line_lower:
            if 'immediate' in line_lower or 'short' in line_lower or 'quick' in line_lower:
                recommendation['timeframe'] = 'Short-term'
            elif 'medium' in line_lower:
                recommendation['timeframe'] = 'Medium-term'
            elif 'long' in line_lower or 'extended' in line_lower:
                recommendation['timeframe'] = 'Long-term'
        
        # Extract prerequisites
        if 'prerequisite' in line_lower or 'require' in line_lower or 'need' in line_lower:
            recommendation['prerequisites'].append(line.strip())
        
        # Extract success metrics
        if 'metric' in line_lower or 'measure' in line_lower or 'success' in line_lower or 'indicator' in line_lower:
            recommendation['success_metrics'].append(line.strip())
    
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
    
    def _extract_priority(self, text):
        """Extract priority from recommendation text"""
        text_lower = text.lower()
        
        if 'high priority' in text_lower or 'priority: high' in text_lower or 'critical' in text_lower:
            return 'High'
        elif 'low priority' in text_lower or 'priority: low' in text_lower or 'optional' in text_lower:
            return 'Low'
        else:
            return 'Medium'
    
    def _update_progress_tracking(self, processed_response, input_data):
        """Update progress tracking for recommendations"""
        # Get current recommendations
        current_recommendations = processed_response.get("data", {}).get("recommendations", [])
        
        # Get previous implementation progress
        implementation_progress = input_data.get("implementation_progress", {})
        
        # Update progress tracker
        for rec in current_recommendations:
            rec_id = rec.get("id")
            if rec_id:
                # If this is a new recommendation, initialize progress
                if rec_id not in self.progress_tracker["recommendations"]:
                    self.progress_tracker["recommendations"][rec_id] = {
                        "status": "Not started",
                        "progress_percentage": 0,
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "history": []
                    }
                
                # If we have implementation progress data, update it
                if rec_id in implementation_progress:
                    self.progress_tracker["recommendations"][rec_id]["status"] = implementation_progress[rec_id]
                    
                    # Calculate progress percentage based on status
                    if implementation_progress[rec_id] == "Completed":
                        progress_percentage = 100
                    elif implementation_progress[rec_id] == "In progress":
                        progress_percentage = 50
                    elif implementation_progress[rec_id] == "Not started":
                        progress_percentage = 0
                    else:
                        try:
                            progress_percentage = int(implementation_progress[rec_id].replace("%", ""))
                        except:
                            progress_percentage = 0
                    
                    self.progress_tracker["recommendations"][rec_id]["progress_percentage"] = progress_percentage
                    
                    # Add to history
                    self.progress_tracker["recommendations"][rec_id]["history"].append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": implementation_progress[rec_id],
                        "progress_percentage": progress_percentage
                    })
        
        # Update last updated timestamp
        self.progress_tracker["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _calculate_progress_metrics(self, recommendations):
        """Calculate progress metrics for recommendations"""
        total_recommendations = len(recommendations)
        completed = 0
        in_progress = 0
        not_started = 0
        
        # Count recommendations by status
        for rec in recommendations:
            rec_id = rec.get("id")
            if rec_id in self.progress_tracker["recommendations"]:
                status = self.progress_tracker["recommendations"][rec_id]["status"]
                if status == "Completed":
                    completed += 1
                elif status == "In progress":
                    in_progress += 1
                else:
                    not_started += 1
            else:
                not_started += 1
        
        # Calculate overall progress percentage
        overall_progress = 0
        if total_recommendations > 0:
            overall_progress = int((completed + (in_progress * 0.5)) / total_recommendations * 100)
        
        return {
            "total_recommendations": total_recommendations,
            "completed": completed,
            "in_progress": in_progress,
            "not_started": not_started,
            "overall_progress": overall_progress,
            "last_updated": self.progress_tracker.get("last_updated")
        }
