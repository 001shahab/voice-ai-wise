"""
Language Model Module

This module handles generating responses using OpenAI's GPT models.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import openai

logger = logging.getLogger(__name__)

class LanguageModel:
    """Class for generating responses using OpenAI's GPT models."""
    
    def __init__(self):
        """Initialize the LLM module."""
        # Get API key from environment
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        openai.api_key = self.api_key
        
        # Set the model to use
        self.model = "gpt-4o-mini"  # As specified in requirements
        
        # System prompt template
        self.system_prompt = """
        You are the Fort Wise Voice AI Assistant, a helpful and knowledgeable assistant.
        Your answers should be based ONLY on the provided context from the Fort Wise knowledge base.
        If you don't know the answer based on the provided context, say so politely.
        Keep your responses concise and clear, as they will be spoken to the user.
        """
        
        logger.info(f"Language Model initialized with model: {self.model}")
    
    def generate_response(self, query: str, context: List[Dict[str, Any]], 
                          conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Generate a response using the language model.
        
        Args:
            query: User query
            context: Retrieved context chunks
            conversation_history: Optional conversation history
            
        Returns:
            Generated response text
        """
        logger.info(f"Generating response for query: {query}")
        
        try:
            # Format context for prompt
            formatted_context = "\n\n".join([item["chunk"] for item in context])
            
            # Create messages for OpenAI API
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history for context
            if conversation_history:
                # Only include the last few exchanges to keep context manageable
                recent_history = conversation_history[-3:]  # Last 3 exchanges
                for exchange in recent_history:
                    messages.append({"role": "user", "content": exchange["query"]})
                    messages.append({"role": "assistant", "content": exchange["response"]})
            
            # Add current query with context
            user_message = f"Query: {query}\n\nContext from Fort Wise Knowledge Base:\n{formatted_context}"
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            response_text = response.choices[0].message.content
            
            logger.info(f"Generated response: {response_text[:50]}...")
            return response_text
            
        except Exception as e:
            logger.error(f"Error during response generation: {e}")
            
            # Fallback response in case of API failure
            fallback_response = "I'm sorry, I encountered an error while processing your request. Please try again."
            return fallback_response