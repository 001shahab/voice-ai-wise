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
        self.model = "o4-mini-2025-04-16"  # As specified in requirements
        
        # System prompt template
        self.system_prompt = """
        You are the Fort Wise Voice AI Assistant, a helpful and knowledgeable assistant for Fort Wise AI agency.
        
        Fort Wise AI is an agency which focuses on AI solutions for businesses, with their flagship product being Alara, an AI-powered sales assistant.
        
        Prioritize being helpful and engaging in natural conversation. Remember personal information shared by the user and incorporate it in your responses when appropriate.
        
        When answering questions:
        1. If the knowledge base has relevant information, use that as your primary source
        2. If the knowledge base doesn't have relevant information, use your general knowledge to provide a helpful response
        3. For personal questions or conversation, engage naturally without disclaimers
        4. Remember and use the user's name if they've shared it
        
        Keep your responses concise and clear, as they will be spoken to the user.
        
        IMPORTANT: Always respond in English regardless of the language of the query.
        If you receive a query in a language other than English, still respond in English only.
        """
        
        logger.info(f"Language Model initialized with model: {self.model}")
    
    def generate_response(self, query: str, context: List[Dict[str, Any]], 
                          conversation_history: Optional[List[Dict[str, str]]] = None,
                          user_info: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a response using the language model.
        
        Args:
            query: User query
            context: Retrieved context chunks
            conversation_history: Optional conversation history
            user_info: Optional user information
            
        Returns:
            Generated response text
        """
        logger.info(f"Generating response for query: {query}")
        
        try:
            # Format context for prompt
            formatted_context = "\n\n".join([item["chunk"] for item in context])
            
            # Check if any relevant context was found
            context_found = len(context) > 0 and any(item["score"] < 1.0 for item in context)
            
            # Create messages for OpenAI API
            system_prompt = self.system_prompt
            
            # Add user information to system prompt if available
            if user_info and len(user_info) > 0:
                user_info_str = "User Information:\n"
                for key, value in user_info.items():
                    user_info_str += f"- {key.capitalize()}: {value}\n"
                system_prompt += f"\n\n{user_info_str}"
                system_prompt += "\nUse the user's name when appropriate to make the conversation more personalized."
            
            # Modify system prompt if no relevant context found
            if not context_found:
                system_prompt += "\n\nIf no relevant information is found in the context, provide a helpful answer based on your general knowledge. Remember that you should engage in natural conversation and acknowledge personal information the user has shared."
            
            messages = [
                {"role": "system", "content": system_prompt}
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
            logger.info(f"Sending request to OpenAI API with {len(messages)} messages")
            for idx, msg in enumerate(messages):
                logger.debug(f"Message {idx}: {msg['role']} - {msg['content'][:50]}...")
                
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                max_completion_tokens=500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Log the full response for debugging
            logger.debug(f"OpenAI API response: {response}")
            
            response_text = response.choices[0].message.content
            logger.debug(f"Raw response text: '{response_text}'")
            
            # Check for empty response
            if not response_text or response_text.strip() == "":
                logger.warning("Empty response from OpenAI API, using fallback")
                if user_info and "name" in user_info:
                    response_text = f"I'm sorry {user_info['name']}, I couldn't generate a proper response to your question. Could you please try asking in a different way?"
                else:
                    response_text = "I'm sorry, I couldn't generate a proper response to your question. Could you please try asking in a different way?"
            
            # If we have user info but the response ignores the user's name,
            # and the query is conversational, add a personalized touch
            if user_info and "name" in user_info and "what's my name" in query.lower():
                if user_info["name"].lower() not in response_text.lower():
                    response_text = f"Your name is {user_info['name']}. {response_text}"
            
            logger.info(f"Generated response: {response_text[:50]}...")
            return response_text
            
        except Exception as e:
            logger.error(f"Error during response generation: {e}")
            
            # Fallback response in case of API failure
            fallback_response = "I'm sorry, I encountered an error while processing your request. Please try again."
            return fallback_response