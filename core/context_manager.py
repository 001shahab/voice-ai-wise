"""
Context Manager Module

This module manages conversation context for follow-up questions and remembers user information.
"""

import logging
import re
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class ContextManager:
    """Class for managing conversation context."""
    
    def __init__(self, max_history: int = 10):
        """
        Initialize the context manager.
        
        Args:
            max_history: Maximum number of exchanges to keep in history
        """
        self.history = []
        self.max_history = max_history
        self.user_info = {}  # Dictionary to store user information
        logger.info(f"Context Manager initialized with max_history={max_history}")
    
    def add_exchange(self, query: str, response: str) -> None:
        """
        Add a query-response exchange to the history and extract user information.
        
        Args:
            query: User query
            response: System response
        """
        # Extract user information from the query
        self._extract_user_info(query)
        
        exchange = {
            "query": query,
            "response": response
        }
        
        self.history.append(exchange)
        
        # Trim history if it exceeds max_history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        logger.debug(f"Added exchange to history. Current history size: {len(self.history)}")
        logger.debug(f"Current user info: {self.user_info}")
    
    def _extract_user_info(self, query: str) -> None:
        """
        Extract user information from the query.
        
        Args:
            query: User query text
        """
        # Extract name using pattern matching
        name_patterns = [
            r"my name is (\w+)",
            r"I am (\w+)",
            r"I'm (\w+)",
            r"call me (\w+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                self.user_info["name"] = match.group(1)
                logger.info(f"Extracted user name: {self.user_info['name']}")
                break
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Returns:
            List of query-response exchanges
        """
        return self.history
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get the stored user information.
        
        Returns:
            Dictionary with user information
        """
        return self.user_info
    
    def reset(self) -> None:
        """Reset the conversation history but keep user information."""
        self.history = []
        logger.info("Conversation history reset, user information retained")
    
    def reset_all(self) -> None:
        """Reset both conversation history and user information."""
        self.history = []
        self.user_info = {}
        logger.info("Conversation history and user information reset")
    
    def get_last_exchange(self) -> Dict[str, str]:
        """
        Get the last exchange in the history.
        
        Returns:
            Last query-response exchange or empty dict if no history
        """
        if self.history:
            return self.history[-1]
        return {"query": "", "response": ""}
    
    def get_conversation_summary(self) -> str:
        """
        Get a summary of the conversation context for the LLM.
        
        Returns:
            String containing user information and recent exchanges
        """
        summary = ""
        
        # Add user information if available
        if self.user_info:
            summary += "User Information:\n"
            for key, value in self.user_info.items():
                summary += f"- {key.capitalize()}: {value}\n"
        
        # Add recent conversation history (last 3 exchanges)
        if self.history:
            recent_history = self.history[-3:]
            summary += "\nRecent Conversation:\n"
            for i, exchange in enumerate(recent_history):
                summary += f"User: {exchange['query']}\n"
                summary += f"Assistant: {exchange['response']}\n"
        
        return summary.strip()