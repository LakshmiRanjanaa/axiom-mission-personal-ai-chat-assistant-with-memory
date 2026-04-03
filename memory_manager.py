import faiss
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer

class MemoryManager:
    """Manages conversation memory using FAISS vector embeddings"""
    
    def __init__(self, embedding_model='all-MiniLM-L6-v2'):
        # Initialize sentence transformer for embeddings
        self.encoder = SentenceTransformer(embedding_model)
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        
        # Store memories as text
        self.memories = []
        
        # Load existing memories if available
        self.load_memories()
    
    def add_memory(self, text):
        """Add a new memory to the vector store"""
        # Generate embedding
        embedding = self.encoder.encode([text])
        
        # Add to FAISS index
        self.index.add(embedding.astype('float32'))
        
        # Store the text
        self.memories.append(text)
        
        # Save to disk
        self.save_memories()
    
    def search_memories(self, query, k=3):
        """Search for relevant memories based on query"""
        if len(self.memories) == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.encoder.encode([query])
        
        # Search FAISS index
        k = min(k, len(self.memories))  # Don't search for more than we have
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Return relevant memories
        relevant_memories = []
        for i in indices[0]:
            if i < len(self.memories):  # Safety check
                relevant_memories.append(self.memories[i])
        
        return relevant_memories
    
    def save_memories(self):
        """Save memories to JSON file"""
        try:
            data = {
                'memories': self.memories
            }
            with open('memories.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving memories: {e}")
    
    def load_memories(self):
        """Load memories from JSON file"""
        try:
            if os.path.exists('memories.json'):
                with open('memories.json', 'r') as f:
                    data = json.load(f)
                    self.memories = data.get('memories', [])
                    
                    # Rebuild FAISS index
                    if self.memories:
                        embeddings = self.encoder.encode(self.memories)
                        self.index.add(embeddings.astype('float32'))
        except Exception as e:
            print(f"Error loading memories: {e}")
            self.memories = []
    
    def clear_memory(self):
        """Clear all memories"""
        self.memories = []
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        
        # Remove saved file
        if os.path.exists('memories.json'):
            os.remove('memories.json')