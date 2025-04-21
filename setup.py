"""
Setup script for Fort Wise Voice AI Assistant

This script creates the necessary directory structure and sample files
for the Fort Wise Voice AI Assistant to run properly.
"""

import os
import logging
from dotenv import load_dotenv
import shutil

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Set up the project environment.
    """
    logger.info("Setting up Fort Wise Voice AI Assistant environment...")
    
    # Load environment variables
    load_dotenv()
    
    # Create directory structure
    directories = [
        'data',
        'data/recordings',
        'data/faiss_index',
        'logs',
        'static/img',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    # Create sample knowledge base if it doesn't exist
    kb_path = os.path.join('data', 'knowledge_base.txt')
    if not os.path.exists(kb_path) or os.path.getsize(kb_path) == 0:
        logger.info("Creating sample knowledge base...")
        
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
        
        with open(kb_path, 'w', encoding='utf-8') as file:
            file.write(sample_data)
            
        logger.info(f"Created sample knowledge base at {kb_path}")
        
    # Check .env file exists
    env_path = '.env'
    if not os.path.exists(env_path):
        logger.info("Creating sample .env file...")
        
        sample_env = """# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Flask Settings
FLASK_ENV=development
PORT=5000

# Audio Settings
MAX_AUDIO_DURATION=30

# Model Settings
LLM_MODEL=gpt-4o-mini
TTS_VOICE=alloy
"""
        
        with open(env_path, 'w', encoding='utf-8') as file:
            file.write(sample_env)
            
        logger.info(f"Created sample .env file at {env_path}")
        logger.warning("Please update the .env file with your OpenAI API key")
    
    logger.info("Setup completed successfully!")
    logger.info("To run the application:")
    logger.info("1. Ensure you have installed the required packages: pip install -r requirements.txt")
    logger.info("2. Update the .env file with your OpenAI API key")
    logger.info("3. Run the application: python app.py")

if __name__ == "__main__":
    main()