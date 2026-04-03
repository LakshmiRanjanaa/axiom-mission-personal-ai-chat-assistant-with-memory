# Personal AI Chat Assistant with Memory

A conversational AI assistant that remembers past conversations and learns user preferences using OpenAI's API and vector embeddings.

## Features

- 💬 **Smart Conversations**: Powered by OpenAI GPT-3.5
- 🧠 **Memory System**: Remembers past conversations using FAISS vector search
- 🎯 **Preference Learning**: Automatically detects and remembers user preferences
- 📊 **Memory Stats**: Track stored memories and learned preferences
- 🔄 **Persistent Storage**: Conversations saved between sessions

## Quick Start

1. **Install Dependencies**:
   bash
   pip install -r requirements.txt
   

2. **Set OpenAI API Key**:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     
     OPENAI_API_KEY=your_api_key_here
     
   - Get your API key from: https://platform.openai.com/api-keys

3. **Run the Application**:
   bash
   streamlit run app.py
   

4. **Start Chatting**:
   - Open your browser to the provided URL (usually http://localhost:8501)
   - Start having conversations with your AI assistant
   - Watch as it remembers your preferences and past discussions!

## How It Works

### Memory System
- **FAISS Vector Store**: Efficiently searches through past conversations
- **Sentence Embeddings**: Converts conversations to vector representations
- **Contextual Retrieval**: Finds relevant past conversations for each new message

### Preference Learning
- Automatically detects preference keywords (like, love, prefer, etc.)
- Stores and displays learned preferences in the sidebar
- Uses preferences to provide more personalized responses

## Project Structure


├── app.py              # Main Streamlit application
├── memory_manager.py   # FAISS vector memory management
├── config.py          # Configuration and API key handling
├── requirements.txt   # Python dependencies
├── README.md         # This file
├── .env              # Your API keys (create this)
└── memories.json     # Stored conversations (auto-generated)


## Customization Ideas

- **Different AI Models**: Change the OpenAI model in `app.py`
- **Memory Capacity**: Adjust `MAX_MEMORIES` in `config.py`
- **Embedding Models**: Try different sentence transformer models
- **UI Themes**: Customize the Streamlit interface
- **Export Features**: Add conversation export functionality

## Learning Objectives

- ✅ AI API Integration (OpenAI)
- ✅ Vector Embeddings & Similarity Search (FAISS)
- ✅ Web App Development (Streamlit)
- ✅ Data Persistence (JSON)
- ✅ Environment Configuration
- ✅ User Experience Design

This project demonstrates key skills for building personalized AI systems that modern companies need!