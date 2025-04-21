"""
Context Manager Module

This module manages conversation context for follow-up questions.
"""

import logging
from typing import List, Dict, Any

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
        logger.info(f"Context Manager initialized with max_history={max_history}")
    
    def add_exchange(self, query: str, response: str) -> None:
        """
        Add a query-response exchange to the history.
        
        Args:
            query: User query
            response: System response
        """
        exchange = {
            "query": query,
            "response": response
        }
        
        self.history.append(exchange)
        
        # Trim history if it exceeds max_history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        logger.debug(f"Added exchange to history. Current history size: {len(self.history)}")
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Returns:
            List of query-response exchanges
        """
        return self.history
    
    def reset(self) -> None:
        """Reset the conversation history."""
        self.history = []
        logger.info("Conversation history reset")
    
    def get_last_exchange(self) -> Dict[str, str]:
        """
        Get the last exchange in the history.
        
        Returns:
            Last query-response exchange or empty dict if no history
        """
        if self.history:
            return self.history[-1]
        return {"query": "", "response": ""}