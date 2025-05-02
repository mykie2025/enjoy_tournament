from abc import ABC, abstractmethod
import openai
from backend.app.config import settings

class BaseAgent(ABC):
    """
    Base class for all agents in the Tennis Tournament Analysis System.
    Provides common functionality and interface for agent implementations.
    """
    
    def __init__(self, model_name=None):
        """
        Initialize the agent with OpenAI configuration.
        
        Args:
            model_name (str): The name of the OpenAI model to use
        """
        self.model_name = model_name
        self.client = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )
    
    @abstractmethod
    def process(self, input_data):
        """
        Process input data and return agent response.
        
        Args:
            input_data (dict): Input data for the agent to process
            
        Returns:
            dict: Processed output from the agent
        """
        pass
    
    def generate_completion(self, messages, temperature=0.7, max_tokens=1000):
        """
        Generate a completion using the OpenAI API.
        
        Args:
            messages (list): List of message dictionaries for the conversation
            temperature (float): Sampling temperature
            max_tokens (int): Maximum number of tokens to generate
            
        Returns:
            str: Generated text from the model
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating completion: {e}")
            return None
