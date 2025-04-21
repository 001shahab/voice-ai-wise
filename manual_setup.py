"""
Fort Wise Manual Setup Script

This script sets up the knowledge base and FAISS index for the Fort Wise Voice AI Assistant
using the provided Agent's manual.txt file.
"""

import os
import logging
import shutil
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def setup_knowledge_base():
    """Set up the knowledge base using the Agent's manual."""
    # File paths
    agents_manual_path = "Agent's manual.txt"
    kb_path = os.path.join('data', 'knowledge_base.txt')
    faiss_dir = os.path.join('data', 'faiss_index')
    faiss_path = os.path.join(faiss_dir, 'index.faiss')
    root_embeddings_path = "embeddings#cs200#co50.faiss"
    
    # Create directories
    os.makedirs(os.path.dirname(kb_path), exist_ok=True)
    os.makedirs(faiss_dir, exist_ok=True)
    
    # Check if Agent's manual exists
    if not os.path.exists(agents_manual_path):
        logger.error(f"Agent's manual not found at {agents_manual_path}")
        return False
    
    # Copy Agent's manual to knowledge base location
    logger.info(f"Copying Agent's manual to {kb_path}")
    try:
        shutil.copy(agents_manual_path, kb_path)
    except Exception as e:
        logger.error(f"Error copying Agent's manual: {e}")
        return False
    
    # Check if root embeddings file exists
    if os.path.exists(root_embeddings_path):
        logger.info(f"Found embeddings file in root directory: {root_embeddings_path}")
        try:
            # Copy the embeddings file to the data directory
            shutil.copy(root_embeddings_path, faiss_path)
            logger.info(f"Copied embeddings to {faiss_path}")
            return True
        except Exception as e:
            logger.error(f"Error copying embeddings file: {e}")
            # Continue to generate new embeddings
    
    # Create new FAISS index with text chunks from the manual
    logger.info("Creating new FAISS index from the manual")
    
    # Load the manual
    with open(kb_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Create chunks for better retrieval
    chunks = create_chunks(content)
    logger.info(f"Created {len(chunks)} chunks from the manual")
    
    # Create embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))
    
    # Save the index
    faiss.write_index(index, faiss_path)
    logger.info(f"Created and saved FAISS index at {faiss_path}")
    
    return True

def create_chunks(text, max_chunk_size=1000, overlap=200):
    """Create overlapping chunks from text."""
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    current_chunk_size = 0
    
    for line in lines:
        # If line is a potential header (short line with no ending punctuation)
        is_header = len(line.strip()) < 80 and not line.strip().endswith(('.', '?', '!', ',', ';', ':'))
        
        # If we have a large enough chunk and this is a header, start a new chunk
        if current_chunk_size > max_chunk_size and is_header:
            chunks.append('\n'.join(current_chunk).strip())
            
            # Keep some context for overlap
            overlap_lines = current_chunk[-5:] if len(current_chunk) > 5 else current_chunk
            current_chunk = overlap_lines
            current_chunk_size = sum(len(line) for line in current_chunk)
        
        # Add the line to the current chunk
        current_chunk.append(line)
        current_chunk_size += len(line)
        
        # If current chunk is very large, force split it
        if current_chunk_size > max_chunk_size*1.5:
            chunks.append('\n'.join(current_chunk).strip())
            
            # Keep some context for overlap
            overlap_lines = current_chunk[-5:] if len(current_chunk) > 5 else current_chunk
            current_chunk = overlap_lines
            current_chunk_size = sum(len(line) for line in current_chunk)
    
    # Add the last chunk if not empty
    if current_chunk:
        chunks.append('\n'.join(current_chunk).strip())
    
    # Filter out empty chunks
    chunks = [chunk for chunk in chunks if chunk.strip()]
    
    return chunks

if __name__ == "__main__":
    logger.info("Starting Fort Wise manual setup")
    
    try:
        success = setup_knowledge_base()
        if success:
            logger.info("Fort Wise manual setup completed successfully")
        else:
            logger.error("Fort Wise manual setup failed")
    except Exception as e:
        logger.error(f"Error during setup: {e}")
    
    logger.info("Setup process finished")