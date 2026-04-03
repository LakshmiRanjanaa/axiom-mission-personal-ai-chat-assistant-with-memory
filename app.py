import streamlit as st
import openai
import json
import os
from datetime import datetime
from memory_manager import MemoryManager
from config import OPENAI_API_KEY

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Initialize session state
if 'memory_manager' not in st.session_state:
    st.session_state.memory_manager = MemoryManager()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {}

def get_ai_response(user_message):
    """Get response from OpenAI with context from memory"""
    try:
        # Retrieve relevant memories
        relevant_memories = st.session_state.memory_manager.search_memories(user_message, k=3)
        
        # Build context from memories
        context = "Previous conversations and preferences:\n"
        for memory in relevant_memories:
            context += f"- {memory}\n"
        
        # Create system prompt with context
        system_prompt = f"""
        You are a helpful AI assistant with memory of past conversations.
        Use the following context to provide personalized responses:
        
        {context}
        
        Be conversational, helpful, and reference past interactions when relevant.
        """
        
        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

def save_conversation(user_message, ai_response):
    """Save conversation to memory and update preferences"""
    # Create conversation entry
    conversation = f"User: {user_message} | AI: {ai_response} | Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    # Add to memory
    st.session_state.memory_manager.add_memory(conversation)
    
    # Extract and update preferences (simple keyword-based)
    preference_keywords = ['like', 'love', 'prefer', 'favorite', 'enjoy', 'hate', 'dislike']
    for keyword in preference_keywords:
        if keyword in user_message.lower():
            if 'preferences' not in st.session_state.user_preferences:
                st.session_state.user_preferences['preferences'] = []
            st.session_state.user_preferences['preferences'].append({
                'text': user_message,
                'timestamp': datetime.now().isoformat()
            })
            break

# Streamlit UI
st.title("🤖 Personal AI Chat Assistant")
st.caption("Your AI assistant that remembers our conversations!")

# Sidebar for memory stats
with st.sidebar:
    st.header("Memory Stats")
    memory_count = len(st.session_state.memory_manager.memories)
    st.metric("Stored Memories", memory_count)
    
    preference_count = len(st.session_state.user_preferences.get('preferences', []))
    st.metric("Learned Preferences", preference_count)
    
    if st.button("Clear Memory"):
        st.session_state.memory_manager.clear_memory()
        st.session_state.user_preferences = {}
        st.session_state.messages = []
        st.success("Memory cleared!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to talk about?"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt)
            st.write(response)
    
    # Add AI response to chat
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Save conversation to memory
    save_conversation(prompt, response)

# Show recent preferences
if st.session_state.user_preferences.get('preferences'):
    with st.expander("🧠 What I've Learned About You"):
        recent_prefs = st.session_state.user_preferences['preferences'][-3:]  # Show last 3
        for pref in recent_prefs:
            st.write(f"• {pref['text']}")