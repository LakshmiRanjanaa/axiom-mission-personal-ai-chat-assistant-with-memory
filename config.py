import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("""
    OpenAI API key not found!
    
    Please set your OpenAI API key in one of these ways:
    1. Create a .env file with: OPENAI_API_KEY=your_key_here
    2. Set environment variable: export OPENAI_API_KEY=your_key_here
    
    Get your API key from: https://platform.openai.com/api-keys
    """)

# Memory Configuration
MAX_MEMORIES = 1000  # Maximum number of memories to store
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'  # Sentence transformer model for embeddings