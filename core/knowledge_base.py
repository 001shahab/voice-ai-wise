"""
Knowledge Base Module

This module handles retrieving relevant information from the FAISS index
based on user queries.
"""

import os
import logging
import numpy as np
import faiss
import shutil
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """Class for knowledge base retrieval using FAISS."""
    
    def __init__(self, index_path: str = None, kb_path: str = None):
        """
        Initialize the knowledge base.
        
        Args:
            index_path: Path to the FAISS index file
            kb_path: Path to the knowledge base text file
        """
        # Set default paths if not provided
        self.index_path = index_path or os.path.join('data', 'faiss_index', 'index.faiss')
        self.kb_path = kb_path or os.path.join('data', 'knowledge_base.txt')
        
        # Check if we have the embeddings file in the root directory
        root_embeddings_path = "embeddings#cs200#co50.faiss"
        if os.path.exists(root_embeddings_path):
            logger.info(f"Found embeddings file in root directory: {root_embeddings_path}")
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            
            # Copy the embeddings file to the default location if it doesn't exist
            if not os.path.exists(self.index_path):
                try:
                    shutil.copy(root_embeddings_path, self.index_path)
                    logger.info(f"Copied embeddings from {root_embeddings_path} to {self.index_path}")
                except Exception as e:
                    logger.error(f"Error copying embeddings file: {e}")
        
        # Ensure the knowledge base file exists with sample data if not present
        self._ensure_knowledge_base_exists()
        
        # Load or create the FAISS index
        try:
            if os.path.exists(self.index_path):
                self.index = faiss.read_index(self.index_path)
                logger.info(f"FAISS index loaded from {self.index_path}")
            else:
                logger.warning(f"FAISS index not found at {self.index_path}, creating new index")
                self._create_faiss_index()
        except Exception as e:
            logger.error(f"Error with FAISS index, creating new one: {e}")
            self._create_faiss_index()
        
        # Load the embedding model
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence embedding model loaded")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            raise
        
        # Load text chunks
        try:
            self.chunks = self._load_text_chunks()
            logger.info(f"Loaded {len(self.chunks)} text chunks from knowledge base")
        except Exception as e:
            logger.error(f"Error loading text chunks: {e}")
            self._ensure_knowledge_base_exists()
            self.chunks = self._load_text_chunks()
            logger.info(f"Created and loaded {len(self.chunks)} sample text chunks")
    
    def _load_text_chunks(self) -> List[str]:
        """
        Load text chunks from the knowledge base file.
        
        Returns:
            List of text chunks
        """
        # Load and split the knowledge base into chunks
        with open(self.kb_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # More sophisticated chunk splitting for better retrieval
        # Split by sections based on headers and reasonable chunk sizes
        lines = content.split('\n')
        chunks = []
        current_chunk = []
        current_chunk_size = 0
        
        for line in lines:
            # If line is a potential header (short line with no ending punctuation)
            is_header = len(line.strip()) < 80 and not line.strip().endswith(('.', '?', '!', ',', ';', ':'))
            
            # If we have a large enough chunk and this is a header, start a new chunk
            if current_chunk_size > 300 and is_header:
                chunks.append('\n'.join(current_chunk).strip())
                current_chunk = []
                current_chunk_size = 0
            
            # Add the line to the current chunk
            current_chunk.append(line)
            current_chunk_size += len(line)
            
            # If current chunk is very large, split it
            if current_chunk_size > 1000:
                chunks.append('\n'.join(current_chunk).strip())
                current_chunk = []
                current_chunk_size = 0
        
        # Add the last chunk if not empty
        if current_chunk:
            chunks.append('\n'.join(current_chunk).strip())
        
        # Filter out empty chunks
        chunks = [chunk for chunk in chunks if chunk.strip()]
        
        logger.info(f"Split knowledge base into {len(chunks)} chunks")
        return chunks
        
    def _ensure_knowledge_base_exists(self):
        """
        Ensure the knowledge base file exists with sample data.
        If it doesn't exist, create it with sample Fort Wise data.
        """
        os.makedirs(os.path.dirname(self.kb_path), exist_ok=True)
        
        if not os.path.exists(self.kb_path) or os.path.getsize(self.kb_path) == 0:
            logger.warning(f"Knowledge base file not found or empty at {self.kb_path}, creating sample data")
            
            # Sample Fort Wise data
            sample_data = """
Fort Wise History
Fort Wise was established in 1847 as a military outpost to protect settlers moving west during the American expansion. Named after General Thomas Wise, the fort played a crucial role in maintaining peace between settlers and Native American tribes in the region.

Fort Wise Location
Fort Wise is located in the southwestern region of the United States, situated near the confluence of the Green and Blue Rivers. The fort is surrounded by picturesque mountains and sits at an elevation of 5,280 feet above sea level.

Fort Wise Architecture
The fort was originally constructed with a rectangular layout featuring wooden palisades and four corner bastions. By 1860, it was expanded to include stone buildings, barracks for 200 soldiers, officers' quarters, and a hospital. The central parade ground measures approximately 300 by 200 feet.

Fort Wise Today
Today, Fort Wise serves as a historical museum and national monument. Visitors can explore the restored buildings, view military artifacts, and learn about the fort's history through interactive exhibits. The fort attracts approximately 150,000 visitors annually.

Fort Wise Events
Fort Wise hosts several annual events including the Summer Heritage Festival in June, historical reenactments on Memorial Day and Independence Day, and the Fort Wise Candlelight Tour in December. Educational programs for schools run throughout the academic year.

Fort Wise Natural Environment
The fort is situated in a diverse ecological zone with pine forests, grasslands, and riparian areas along the nearby rivers. Wildlife in the area includes deer, elk, various bird species, and smaller mammals. The area experiences four distinct seasons with moderate snowfall in winter.

Fort Wise Visitor Information
Fort Wise is open to visitors daily from 9am to 5pm from April through October, and Thursday through Monday from 10am to 4pm from November through March. Admission is $10 for adults, $5 for children 6-12, and free for children under 6. Annual passes are available for $35.
            """
            
            with open(self.kb_path, 'w', encoding='utf-8') as file:
                file.write(sample_data)
                
    def _create_faiss_index(self):
        """
        Create a new FAISS index from the knowledge base text.
        """
        logger.info("Creating new FAISS index")
        
        # Load embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load text chunks
        self.chunks = self._load_text_chunks()
        
        # Create embeddings
        embeddings = self.model.encode(self.chunks)
        
        # Set dimensions
        dimension = embeddings.shape[1]
        
        # Create the index
        self.index = faiss.IndexFlatL2(dimension)
        
        # Add the embeddings to the index
        self.index.add(embeddings.astype('float32'))
        
        # Save the index
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        
        logger.info(f"Created and saved FAISS index with {len(self.chunks)} chunks at {self.index_path}")
    
    def search(self, query: str, n_results: int = 5, 
               conversation_history: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, Any]]:
        """
        Search for relevant information from the knowledge base.
        
        Args:
            query: The query text
            n_results: Number of results to return
            conversation_history: Optional conversation history for context
            
        Returns:
            List of relevant chunks with metadata
        """
        logger.info(f"Searching for: {query}")
        
        try:
            # Create enhanced query using conversation history
            if conversation_history and len(conversation_history) > 0:
                # Include recent conversation context in the query
                recent_exchanges = conversation_history[-2:]  # Last 2 exchanges
                enhanced_query = query + " " + " ".join([
                    f"{exchange['query']} {exchange['response']}" 
                    for exchange in recent_exchanges
                ])
            else:
                enhanced_query = query
            
            # Create vector embedding for the query
            query_vector = self.model.encode([enhanced_query])[0]
            query_vector = np.array([query_vector]).astype('float32')
            
            # Search the index - increase number of results for filtering
            distances, indices = self.index.search(query_vector, k=n_results * 2)
            
            # Collect results
            results = []
            for i, idx in enumerate(indices[0]):
                if idx != -1:  # Valid index
                    results.append({
                        "chunk": self.chunks[idx],
                        "score": float(distances[0][i]),
                        "index": int(idx)
                    })
            
            # Filter results by relevance score threshold
            threshold = 1.5  # Adjust based on your embedding model
            relevant_results = [r for r in results if r["score"] < threshold]
            
            # Sort by relevance score (lower is better)
            relevant_results.sort(key=lambda x: x["score"])
            
            # Limit to requested number
            relevant_results = relevant_results[:n_results]
            
            logger.info(f"Found {len(relevant_results)} relevant chunks out of {len(results)} total matches")
            
            return relevant_results
            
        except Exception as e:
            logger.error(f"Error during knowledge base search: {e}")
            raise