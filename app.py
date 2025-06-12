import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from io import BytesIO
from PIL import Image
import json
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components
import os
import branca.colormap as cm
import json
from datetime import datetime
import time
import random
import google.generativeai as genai
from dotenv import load_dotenv

# Set page configuration
st.set_page_config(
    page_title="Indian Cultural Heritage Explorer",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def add_indian_culture_footer():
    """
    Add Indian culture footer section to your Streamlit app
    """
    
    # Add some spacing
    st.markdown("---")
    
    # Sustainability quote section
    st.markdown("""
        <div style='text-align: center; margin: 1rem 0; padding: 1rem; background-color: #F0F8F0; border-radius: 8px;'>
            <p style='font-size: 1.1rem; color: #2E7D32; font-weight: bold; margin-bottom: 0.5rem;'>
                "वसुधैव कुटुम्बकम्" - The World is One Family
            </p>
            <p style='font-size: 0.95rem; color: #388E3C; font-style: italic;'>
                Embracing sustainability through ancient wisdom and modern innovation
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Create columns for buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🏛️ Indian Culture Portal", use_container_width=True):
            st.markdown('[🌐 Visit Indian Culture Portal](https://indianculture.gov.in/)')
    
    with col2:
        if st.button("🏺 Archaeological Survey", use_container_width=True):
            st.markdown('[🌐 Visit ASI Portal](https://asi.nic.in/)')
    
    with col3:
        st.write("")  # Empty column for spacing


def bharat_explorer():
    """
    A beautiful, modern Streamlit chatbot for exploring Indian culture, art, and tourism.
    Features enhanced UI, streaming responses, and comprehensive chat management.
    """
    
    # Custom CSS for modern styling
    st.markdown("""
    <style>
    /* Main styling */
    .main-header {
        background: linear-gradient(135deg, #FF9933, #FFFFFF, #138808);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: #000;
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        border: 3px solid rgba(255,255,255,0.3);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .user-message {
        background: linear-gradient(135deg, #FF9933, #FF6B35);
        color: white;
        padding: 1.2rem 1.8rem;
        border-radius: 25px 25px 8px 25px;
        margin: 0.8rem 0;
        margin-left: 15%;
        box-shadow: 0 6px 20px rgba(255, 153, 51, 0.4);
        font-size: 1rem;
        line-height: 1.5;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #138808, #2E8B57);
        color: white;
        padding: 1.2rem 1.8rem;
        border-radius: 25px 25px 25px 8px;
        margin: 0.8rem 0;
        margin-right: 15%;
        box-shadow: 0 6px 20px rgba(19, 136, 8, 0.4);
        font-size: 1rem;
        line-height: 1.5;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .input-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: linear-gradient(180deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    /* Animation for typing effect */
    .typing-indicator {
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load environment variables
    load_dotenv()
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🇮🇳 भारत Explorer</h1>
        <h3>Discover the Rich Heritage of India</h3>
        <p>Your AI companion for Indian culture, art, festivals, and tourism</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("### 🎯 Features")
        st.markdown("""
        - 🏛️ **Cultural Heritage** - Ancient traditions & customs
        - 🎨 **Art & Crafts** - Classical & folk art forms  
        - 🎭 **Festivals** - Celebrations across India
        - 🏰 **Tourism** - Historical sites & destinations
        - 🍛 **Cuisine** - Regional delicacies
        - 💃 **Dance & Music** - Classical & folk performances
        """)
        
        # Chat statistics
        if 'chat_history' in st.session_state:
            total_messages = len(st.session_state['chat_history'])
            st.markdown(f"""
            <div class="stats-card">
                <h4>📊 Chat Stats</h4>
                <p><strong>{total_messages}</strong> messages exchanged</p>
                <p><strong>{total_messages // 2}</strong> questions asked</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Clear chat button moved to main interface
        st.markdown("---")
        if st.button("🔄 Start New Conversation", use_container_width=True, type="secondary"):
            st.session_state['chat_history'] = []
            if 'gemini_chat' in st.session_state:
                del st.session_state['gemini_chat']
            st.success("✅ Ready for a new conversation!")
            time.sleep(1)
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # API Configuration
    if not api_key:
        st.error("🔑 API key not found. Please set GOOGLE_API_KEY in your .env file.")
        st.info("💡 Get your API key from Google AI Studio and add it to your .env file")
        return
    
    # Configure Gemini API
    genai.configure(api_key=api_key)
    
    system_instruction = """
    You are Bharat Explorer, an enthusiastic and knowledgeable AI assistant specializing in Indian culture, art, and tourism. 
    
    Your expertise includes:
    - Indian cultural traditions, customs, and heritage
    - Classical and folk art forms, dance, and music
    - Festivals and celebrations across different regions
    - Historical monuments, temples, and tourist destinations
    - Regional cuisines and culinary traditions
    - Traditional crafts and handicrafts
    - Ancient philosophies and spiritual practices
    
    Always provide:
    - Detailed, accurate, and engaging responses
    - Cultural context and historical background
    - Practical travel tips when relevant
    - Respectful and culturally sensitive information
    - Regional variations and diversity within India
    
    Use emojis appropriately to make responses more engaging and maintain a warm, conversational tone.
    """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )

    # Initialize chat session and history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'gemini_chat' not in st.session_state:
        st.session_state['gemini_chat'] = model.start_chat(history=[])
    
    # Suggested questions
    st.markdown("### 💡 Popular Topics")
    col1, col2, col3, col4 = st.columns(4)
    
    suggestions = [
        "Tell me about Diwali celebrations",
        "Famous temples in South India", 
        "Traditional Indian art forms",
        "Best time to visit Rajasthan"
    ]
    
    for i, (col, suggestion) in enumerate(zip([col1, col2, col3, col4], suggestions)):
        with col:
            if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                st.session_state['selected_suggestion'] = suggestion
    
    # Input section with integrated clear button
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Use suggested question if selected
    default_input = st.session_state.get('selected_suggestion', '')
    if default_input:
        st.session_state['selected_suggestion'] = ''  # Clear after use
    
    user_input = st.text_input(
        "🤔 What would you like to know about Indian culture?",
        value=default_input,
        placeholder="e.g., Tell me about classical Indian dance forms...",
        key="culture_input"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        submit = st.button("🚀 Explore", use_container_width=True, type="primary")
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
            st.session_state['chat_history'] = []
            if 'gemini_chat' in st.session_state:
                del st.session_state['gemini_chat']
            st.success("✅ Chat cleared!")
            time.sleep(0.5)
            st.rerun()
    with col3:
        # Chat stats in a compact format
        if st.session_state.get('chat_history'):
            msg_count = len(st.session_state['chat_history'])
            st.metric("Messages", msg_count)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process user input
    if submit and user_input:
        # Add user message to history
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state['chat_history'].append({
            "role": "user", 
            "content": user_input, 
            "timestamp": timestamp
        })
        
        # Show typing indicator
        with st.spinner("🤖 Bharat Explorer is thinking..."):
            try:
                # Get response from Gemini with streaming
                response = st.session_state['gemini_chat'].send_message(user_input, stream=True)
                
                # Collect response text
                response_text = ""
                for chunk in response:
                    response_text += chunk.text
                
                # Add bot response to history
                st.session_state['chat_history'].append({
                    "role": "assistant", 
                    "content": response_text, 
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Please check your API key and try again.")
    
    # Display chat history (newest messages first)
    if st.session_state['chat_history']:
        st.markdown("### 💬 Conversation")
        
        # Create chat container
        chat_container = st.container()
        
        with chat_container:
            # Reverse the chat history to show newest messages first
            for message in reversed(st.session_state['chat_history']):
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You</strong> <small>({message['timestamp']})</small><br><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Clean the bot response to avoid HTML rendering issues
                    clean_content = message['content'].replace('<', '&lt;').replace('>', '&gt;')
                    st.markdown(f"""
                    <div class="bot-message">
                        <strong>🇮🇳 Bharat Explorer</strong> <small>({message['timestamp']})</small><br><br>
                        {clean_content}
                    
                    """, unsafe_allow_html=True)
    
    else:
        # Welcome message using Streamlit components
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown("### 🙏 Namaste! Welcome to Bharat Explorer")
        st.write("I'm here to help you discover the incredible diversity of Indian culture, art, and tourism. Ask me about anything from ancient temples to modern festivals, traditional crafts to regional cuisines!")
        
        st.markdown("**Try asking about:**")
        st.write("🎭 Classical dance forms like Bharatanatyam or Kathak")
        st.write("🏛️ UNESCO World Heritage sites in India") 
        st.write("🎨 Traditional art forms and handicrafts")
        st.write("🎪 Regional festivals and their significance")
        st.write("🍛 Famous dishes from different states")
        #st.markdown('</div>', unsafe_allow_html=True)


# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6347;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Georgia', serif;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #FF8C00;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-family: 'Georgia', serif;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2E8B57;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-family: 'Georgia', serif;
    }
    .highlight-text {
        background-color: #F0F8FF;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #4682B4;
        font-style: italic;
    }
    .container {
        background-color: #FAFAFA;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .img-container {
        text-align: center;
        margin: 20px 0;
    }
    .caption {
        font-size: 0.9rem;
        font-style: italic;
        color: #555;
        text-align: center;
        margin-top: 5px;
    }
    /* Simple Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #F5F5F5;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
    }
    .sidebar-title {
        font-size: 1.6rem;
        color: #D81B60;
        text-align: center;
        margin-bottom: 15px;
        font-family: 'Georgia', serif;
    }
    .stRadio > label {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        background-color: #FFFFFF;
        border: 1px solid #B0BEC5;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stRadio > label:hover {
        background-color: #E1F5FE;
    }
    .stRadio > label > div > input:checked + div {
        background-color: #0288D1;
        color: white;
        border-radius: 5px;
        padding: 10px;
    }
    .folium-map {
        width: 100%;
        height: 600px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)




# Function to load and cache data
@st.cache_data(ttl=3600)
def load_tourism_data():
    data = {
        'State/UT': ['Tamil Nadu', 'Maharashtra', 'Uttar Pradesh', 'Delhi', 'Rajasthan', 
                    'West Bengal', 'Punjab', 'Kerala', 'Bihar', 'Karnataka', 
                    'Goa', 'Haryana', 'Gujarat', 'Uttarakhand', 'Madhya Pradesh',
                    'Himachal Pradesh', 'Assam', 'Odisha', 'Telangana', 'Andhra Pradesh'],
        'FTV_2022': [436362, 360403, 227277, 203694, 188245, 
                    156382, 117588, 103104, 93065, 84031, 
                    59300, 41230, 35914, 28772, 27291,
                    21391, 16964, 16785, 12045, 5847],
        'Percentage_Share_2022': [18.25, 15.07, 9.51, 8.52, 7.87, 
                                6.54, 4.92, 4.31, 3.89, 3.52, 
                                2.48, 1.72, 1.5, 1.2, 1.14,
                                0.89, 0.71, 0.7, 0.5, 0.24]
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_domestic_tourism_data():
    data = {
        'State/UT': ['Uttar Pradesh', 'Tamil Nadu', 'Karnataka', 'Andhra Pradesh', 'Telangana', 
                    'Maharashtra', 'Uttarakhand', 'Gujarat', 'Rajasthan', 'Madhya Pradesh', 
                    'West Bengal', 'Kerala', 'Bihar', 'Himachal Pradesh', 'Odisha',
                    'Punjab', 'Jharkhand', 'Goa', 'Haryana', 'Delhi'],
        'DTV_2022_millions': [318.58, 240.43, 135.34, 121.95, 113.33, 
                            103.56, 70.35, 55.42, 54.56, 51.93, 
                            38.48, 38.06, 37.24, 15.23, 12.56,
                            11.35, 8.50, 6.99, 6.65, 5.32],
        'Percentage_Share_2022': [20.77, 15.67, 8.82, 7.95, 7.39, 
                                6.75, 4.59, 3.61, 3.56, 3.38, 
                                2.51, 2.48, 2.43, 0.99, 0.82,
                                0.74, 0.55, 0.46, 0.43, 0.35]
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_monuments_data():
    data = {
        'State/UT': ['Uttar Pradesh', 'Karnataka', 'Tamil Nadu', 'Maharashtra', 'Madhya Pradesh', 
                    'Delhi', 'Gujarat', 'Rajasthan', 'Bihar', 'Andhra Pradesh', 
                    'Punjab', 'Haryana', 'West Bengal', 'Odisha', 'Telangana',
                    'Kerala', 'Assam', 'Jammu & Kashmir', 'Uttarakhand', 'Himachal Pradesh'],
        'No_of_Monuments': [743, 506, 413, 285, 292, 
                           174, 202, 163, 70, 134, 
                           36, 91, 134, 80, 27,
                           29, 55, 59, 41, 43]
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_cultural_funding_data():
    data = {
        'Scheme': ['Archaeological Survey of India', 'Museums', 'Archives and Records', 
                  'Anthropological Survey', 'National Library', 'Public Libraries', 
                  'IGNCA', 'Akademies', 'Centenaries & Anniversaries', 'Financial Assistance to Cultural Organizations'],
        'Expenditure_2019_20': [974.56, 362.8, 102.3, 51.4, 82.7, 138.6, 110.5, 155.8, 91.2, 285.7],
        'Expenditure_2020_21': [843.2, 310.5, 85.6, 47.8, 75.4, 120.3, 95.6, 140.2, 82.5, 240.8],
        'Expenditure_2021_22': [1085.7, 395.4, 112.5, 55.9, 88.1, 150.7, 124.8, 172.3, 97.5, 310.8],
        'Expenditure_2022_23': [1200.3, 425.2, 125.6, 62.4, 94.3, 165.8, 135.2, 184.5, 102.6, 345.9]
    }
    return pd.DataFrame(data)


@st.cache_data(ttl=3600)
def load_arts_data():
    data = {
        'Art_Form': [
            'Madhubani', 'Warli', 'Kalamkari', 'Tanjore', 'Pattachitra', 
            'Kathakali', 'Bharatanatyam', 'Kathak', 'Odissi', 'Kuchipudi',
            'Carnatic', 'Hindustani', 'Gond', 'Phad', 'Miniature',
            'Bihu', 'Ghoomar', 'Chhau', 'Garba', 'Lavani',
            'Bodo Dance', 'Sattriya', 'Yakshagana', 'Thang-Ta', 'Kalaripayattu',
            'Bhangra', 'Giddha', 'Cheraw', 'Fugdi', 'Dalkhai',
            'Theyyam', 'Tharu Folk', 'Santhali Dance', 'Rabindra Sangeet', 'Pahari Painting',
            'Koli Dance', 'Tusu Parab',
        ],
        'Category': [
            'Painting', 'Painting', 'Painting', 'Painting', 'Painting',
            'Dance', 'Dance', 'Dance', 'Dance', 'Dance',
            'Music', 'Music', 'Painting', 'Painting', 'Painting',
            'Dance', 'Dance', 'Dance', 'Dance', 'Dance',
            'Dance', 'Dance', 'Dance', 'Dance', 'Martial Art',
            'Dance', 'Dance', 'Dance', 'Dance', 'Dance',
            'Ritual Dance', 'Dance', 'Dance', 'Music', 'Painting',
            'Dance', 'Dance',
        ],
        'Region': [
            'Bihar', 'Maharashtra', 'Andhra Pradesh', 'Tamil Nadu', 'Odisha',
            'Kerala', 'Tamil Nadu', 'Uttar Pradesh', 'Odisha', 'Andhra Pradesh',
            'Tamil Nadu', 'Uttar Pradesh', 'Madhya Pradesh', 'Rajasthan', 'Rajasthan',
            'Assam', 'Rajasthan', 'Jharkhand', 'Gujarat', 'Maharashtra',
            'Tripura', 'Assam', 'Karnataka', 'Manipur', 'Kerala',
            'Punjab', 'Punjab', 'Mizoram', 'Goa', 'Odisha',
            'Kerala', 'Uttarakhand', 'Jharkhand', 'West Bengal', 'Himachal Pradesh',
            'Dadra and Nagar Haveli', 'Jharkhand',
        ],
        'Popularity_Score': [
            85, 78, 82, 80, 72, 88, 92, 89, 83, 79,
            91, 90, 70, 68, 76, 75, 80, 73, 85, 77,
            70, 82, 78, 74, 76, 85, 80, 72, 70, 73,
            84, 71, 74, 88, 75, 70, 68,
        ],
        'lat': [
            25.0961, 19.7515, 15.9129, 11.1271, 20.9517,
            10.8505, 11.1271, 26.8467, 20.9517, 15.9129,
            11.1271, 26.8467, 23.4735, 27.0238, 27.0238,
            26.2006, 27.0238, 23.3441, 22.2587, 19.7515,
            23.8315, 26.2006, 15.3173, 24.8170, 10.8505,
            31.1048, 31.1048, 23.6145, 15.4989, 20.9517,
            10.8505, 30.3165, 23.3441, 22.9868, 31.6360,
            20.1809, 23.3441,
        ],
        'lon': [
            85.3131, 75.7139, 79.7400, 78.6569, 85.0985,
            76.2711, 78.6569, 80.9462, 85.0985, 79.7400,
            78.6569, 80.9462, 77.9471, 74.2179, 74.2179,
            92.9376, 74.2179, 85.2799, 71.1924, 75.7139,
            91.6192, 92.9376, 75.7139, 93.9442, 76.2711,
            75.7139, 75.7139, 91.8933, 73.6918, 85.0985,
            76.2711, 78.1624, 85.2799, 87.8546, 77.1025,
            73.0169, 85.2799,
        ]
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_crafts_data():
    data = {
        'Craft': [
            'Pashmina', 'Chikankari', 'Blue Pottery', 'Brass Work', 'Bidriware',
            'Kanjivaram Silk', 'Bandhani', 'Phulkari', 'Terracotta', 'Dokra',
            'Chanderi', 'Zardozi', 'Meenakari', 'Aari Work', 'Kasuti',
            'Bamboo Craft', 'Assam Silk', 'Stone Carving', 'Kalamkari', 'Puppetry',
            'Applique Work', 'Muga Silk', 'Wood Carving', 'Thangka Painting', 'Kani Shawl',
            'Dhokra', 'Bagh Print', 'Kashida', 'Sujani', 'Marble Inlay',
            'Kullu Shawl', 'Pithora Painting', 'Jute Craft', 'Shell Craft', 'Sohrai Painting',
            'Leather Craft',
        ],
        'State': [
            'Jammu & Kashmir', 'Uttar Pradesh', 'Rajasthan', 'Uttar Pradesh', 'Karnataka',
            'Tamil Nadu', 'Gujarat', 'Punjab', 'West Bengal', 'Chhattisgarh',
            'Madhya Pradesh', 'Uttar Pradesh', 'Rajasthan', 'Jammu & Kashmir', 'Karnataka',
            'Assam', 'Assam', 'Odisha', 'Telangana', 'Rajasthan',
            'Gujarat', 'Assam', 'Kerala', 'Sikkim', 'Jammu & Kashmir',
            'Odisha', 'Madhya Pradesh', 'Jammu & Kashmir', 'Bihar', 'Rajasthan',
            'Himachal Pradesh', 'Gujarat', 'West Bengal', 'Goa', 'Jharkhand',
            'Andhra Pradesh',
        ],
        'Artisans_Count': [
            12500, 35000, 7800, 15600, 5200,
            18900, 28700, 9500, 22000, 6300,
            8700, 17500, 4900, 10800, 3500,
            15000, 12000, 8000, 10000, 4500,
            7000, 9000, 6000, 2000, 11000,
            7500, 8200, 9500, 4000, 5000,
            6500, 3000, 18000, 2500, 3500,
            7000,
        ],
        'Annual_Revenue_Cr': [
            185, 240, 95, 120, 78,
            350, 210, 65, 130, 45,
            110, 195, 85, 75, 40,
            90, 100, 80, 95, 50,
            60, 85, 70, 30, 120,
            55, 75, 65, 35, 90,
            80, 40, 110, 25, 30,
            50,
        ]
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_heritage_site_data():
    data = {
        'Site': ['Cellular Jail', 'Tirupati Temple', 'Tawang Monastery', 'Kamakhya Temple', 'Mahabodhi Temple',
                 'Rock Garden', 'Chitrakoot Falls', 'Diu Fort', 'Qutub Minar', 'Basilica of Bom Jesus',
                 'Somnath Temple', 'Kurukshetra', 'Kullu Valley', 'Vaishno Devi Temple', 'Betla National Park',
                 'Hampi', 'Periyar National Park', 'Leh Palace', 'Agatti Island', 'Khajuraho Temples',
                 'Ajanta Caves', 'Loktak Lake', 'Living Root Bridges', 'Vantawng Falls', 'Kohima War Cemetery',
                 'Konark Sun Temple', 'Auroville', 'Golden Temple', 'Amber Fort', 'Rumtek Monastery',
                 'Meenakshi Temple', 'Charminar', 'Ujjayanta Palace', 'Taj Mahal', 'Valley of Flowers',
                 'Victoria Memorial'],
        'State': ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
                  'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                  'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand',
                  'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh',
                  'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
                  'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim',
                  'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand',
                  'West Bengal'],
        'Year_Inscribed': [2004, 1987, 2009, 1985, 2002,
                           2011, 2010, 2006, 1993, 1987,
                           1983, 2008, 2010, 1985, 2009,
                           1986, 2012, 2009, 2014, 1986,
                           1983, 2010, 2014, 2010, 2009,
                           1987, 2006, 1983, 1986, 2009,
                           1984, 2008, 2010, 1983, 2005,
                           2007],
        'Visitors_Annual': [100000, 5000000, 150000, 2000000, 1000000,
                            300000, 200000, 150000, 3000000, 500000,
                            600000, 400000, 250000, 2000000, 150000,
                            550000, 800000, 100000, 50000, 600000,
                            400000, 100000, 200000, 50000, 100000,
                            400000, 300000, 2500000, 700000, 100000,
                            450000, 600000, 150000, 7000000, 200000,
                            2000000],
        'Type': ['Historical', 'Religious', 'Religious', 'Religious', 'Religious',
                 'Cultural', 'Natural', 'Historical', 'Cultural', 'Religious',
                 'Religious', 'Historical', 'Natural', 'Religious', 'Natural',
                 'Cultural', 'Natural', 'Historical', 'Natural', 'Cultural',
                 'Cultural', 'Natural', 'Cultural', 'Natural', 'Historical',
                 'Cultural', 'Cultural', 'Religious', 'Historical', 'Religious',
                 'Religious', 'Historical', 'Historical', 'Cultural', 'Natural',
                 'Cultural'],
        'lat': [11.6744, 13.6833, 27.5860, 26.1664, 24.6959,
                30.7524, 19.2049, 20.7151, 28.6562, 15.5009,
                20.8880, 29.9695, 31.9579, 33.0299, 23.9240,
                15.3419, 9.5824, 34.1650, 10.8571, 24.8318,
                20.5519, 24.5599, 25.2478, 23.2535, 25.6651,
                19.8874, 12.0054, 31.6200, 26.9855, 27.2980,
                9.9195, 17.3616, 23.8361, 27.1751, 30.7280,
                22.5448],
        'lon': [92.7384, 79.3470, 91.8592, 91.7054, 84.9913,
                76.8053, 81.7107, 70.9962, 77.1855, 73.9116,
                70.4011, 76.8783, 77.1095, 74.9481, 84.2270,
                76.4746, 77.1780, 77.5848, 72.1964, 79.9214,
                75.7033, 93.9240, 91.6807, 92.7638, 94.1003,
                86.0945, 79.8106, 74.8765, 75.8513, 88.5903,
                78.1193, 78.4747, 91.2794, 78.0421, 79.6050,
                88.3426]
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def load_seasonal_tourism_data():
    data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'North India': [65, 75, 85, 70, 55, 40, 55, 60, 75, 90, 95, 85],
        'South India': [80, 85, 75, 60, 50, 65, 75, 80, 85, 90, 95, 90],
        'East India': [70, 80, 85, 70, 50, 40, 30, 25, 45, 75, 90, 80],
        'West India': [75, 80, 70, 65, 60, 50, 45, 50, 60, 85, 90, 85]
    }
    df = pd.DataFrame(data)
    df = df.melt(id_vars=['Month'], var_name='Region', value_name='Tourism_Index')
    return df

@st.cache_data(ttl=3600)
def load_cultural_events_data():
    data = {
        'Event': [
            'Kumbh Mela', 'Pushkar Camel Fair', 'Rann Utsav', 'Hornbill Festival', 'Onam',
            'Durga Puja', 'Diwali in Varanasi', 'Hemis Festival', 'Holi in Mathura', 'Pongal',
            'Bihu', 'Ganesh Chaturthi', 'Navratri', 'Jaipur Literature Festival', 'Khajuraho Dance Festival',
            'Thrissur Pooram', 'Baisakhi', 'Chhath Puja', 'Teej', 'Losar',
            'Goa Carnival', 'Torgya Festival', 'Sangai Festival', 'Konark Dance Festival', 'Makar Sankranti',
            'Vishu', 'Bathukamma', 'Wangala Festival', 'Chapchar Kut', 'Gudi Padwa',
            'Ambubachi Mela', 'Sankranti', 'Lohri', 'Modhera Dance Festival', 'Ladakh Festival',
            'Tansen Samaroh', 'Lakshadweep Cultural Fest',
        ],
        'State': [
            'Uttar Pradesh', 'Rajasthan', 'Gujarat', 'Nagaland', 'Kerala',
            'West Bengal', 'Uttar Pradesh', 'Ladakh', 'Uttar Pradesh', 'Tamil Nadu',
            'Assam', 'Maharashtra', 'Gujarat', 'Rajasthan', 'Madhya Pradesh',
            'Kerala', 'Punjab', 'Bihar', 'Rajasthan', 'Sikkim',
            'Goa', 'Arunachal Pradesh', 'Manipur', 'Odisha', 'Gujarat',
            'Kerala', 'Telangana', 'Meghalaya', 'Mizoram', 'Maharashtra',
            'Assam', 'Karnataka', 'Punjab', 'Gujarat', 'Ladakh',
            'Madhya Pradesh', 'Lakshadweep',
        ],
        'Month': [
            'Rotational', 'November', 'Dec-Feb', 'December', 'Aug-Sep',
            'Sep-Oct', 'Oct-Nov', 'June-July', 'March', 'January',
            'April', 'Aug-Sep', 'Sep-Oct', 'January', 'February',
            'April', 'April', 'Nov-Dec', 'August', 'Feb-Mar',
            'February', 'January', 'November', 'December', 'January',
            'April', 'Sep-Oct', 'January', 'March', 'March-April',
            'June-July', 'January', 'January', 'January', 'September',
            'December', 'January',
        ],
        'Visitors_Estimate': [
            50000000, 250000, 500000, 100000, 1000000,
            5000000, 300000, 20000, 200000, 3000000,
            500000, 1000000, 3000000, 400000, 30000,
            500000, 1000000, 2000000, 150000, 10000,
            200000, 15000, 50000, 30000, 1000000,
            500000, 400000, 20000, 15000, 300000,
            100000, 200000, 500000, 25000, 20000,
            30000, 5000,
        ],
        'Cultural_Significance': [
            10, 8, 7, 9, 8,
            9, 8, 7, 9, 8,
            8, 9, 9, 7, 8,
            8, 8, 9, 7, 7,
            7, 6, 8, 8, 8,
            7, 7, 7, 7, 8,
            8, 7, 8, 7, 7,
            8, 6,
        ]
    }
    return pd.DataFrame(data)


@st.cache_data(ttl=3600)
def load_handicraft_export_data():
    data = {
        'Year': [2017, 2018, 2019, 2020, 2021, 2022, 2023],
        'Handmade_Carpets': [9000, 9300, 9700, 6800, 8200, 11500, 12800],
        'Art_Metalwares': [6700, 7100, 7400, 5200, 6100, 8700, 9500],
        'Embroidered_Textiles': [5500, 5800, 6200, 4300, 5400, 7800, 8600],
        'Shawls_Artifacts': [2200, 2400, 2600, 1800, 2200, 3200, 3600],
        'Woodwares': [3800, 4000, 4200, 2900, 3600, 5100, 5700],
        'Zari_Products': [1900, 2000, 2100, 1500, 1800, 2600, 2900],
        'Imitation_Jewelry': [3200, 3400, 3600, 2500, 3000, 4300, 4800],
        'Miscellaneous': [4700, 4900, 5200, 3600, 4400, 6300, 7000]
    }
    df = pd.DataFrame(data)
    df['Total'] = df.iloc[:, 1:].sum(axis=1)
    return df

@st.cache_data(ttl=3600)
def load_responsible_tourism_data():
    data = {
        'State': ['Kerala', 'Rajasthan', 'Himachal Pradesh', 'Uttarakhand', 'Karnataka', 
                 'Madhya Pradesh', 'Sikkim', 'Goa', 'Tamil Nadu', 'Gujarat'],
        'Eco_Tourism_Score': [92, 85, 90, 88, 82, 78, 94, 76, 80, 79],
        'Community_Involvement': [95, 82, 84, 87, 80, 85, 90, 75, 84, 78],
        'Sustainable_Practices': [90, 78, 85, 86, 81, 82, 92, 70, 79, 80],
        'Cultural_Preservation': [88, 95, 82, 84, 86, 89, 85, 78, 90, 85],
        'Overall_RT_Score': [91.25, 85, 85.25, 86.25, 82.25, 83.5, 90.25, 74.75, 83.25, 80.5]
    }
    return pd.DataFrame(data)



@st.cache_data(ttl=3600)
def load_csv_data():
    try:
        # Connect to Snowflake using secrets.toml
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        
        cursor = conn.cursor()

        # Query for RS_Session_258_AU_1095_1 (Tourism Visitors Data)
        query_visitors = """
        SELECT SL_NO, STATE_UT, "DTVS_2019", "FTVS_2019", "DTVS_2020", "FTVS_2020", "DTVS_2021", "FTVS_2021"
        FROM TOURIST_VISITS
        """
        cursor.execute(query_visitors)
        visitors_df = pd.DataFrame.from_records(
            cursor.fetchall(),
            columns=[desc[0] for desc in cursor.description]
        ).rename(columns={
            'STATE_UT': 'State/UT',
            'DTVS_2019': '2019 - DTVs',
            'FTVS_2019': '2019 - FTVs',
            'DTVS_2020': '2020 - DTVs',
            'FTVS_2020': '2020 - FTVs',
            'DTVS_2021': '2021 - DTVs',
            'FTVS_2021': '2021 - FTVs'
        })

        # Query for RS_Session_258_AU_1773_1 (Monuments Data)
        query_monuments = """
        SELECT SL_NO, STATE_UT, NOS_OF_MONUMENTS
        FROM MONUMENTS
        """
        cursor.execute(query_monuments)
        monuments_df = pd.DataFrame.from_records(
            cursor.fetchall(),
            columns=[desc[0] for desc in cursor.description]
        ).rename(columns={'STATE_UT': 'State/UT', 'NOS_OF_MONUMENTS': 'No_of_Monuments'})

        # Query for RS_Session_259_AU_2079_1 (GI State Data)
        query_gi_state = """
        SELECT SL_NO, STATE_UT, "YEAR_2014_2015", "YEAR_2015_2016", "YEAR_2016_2017", "YEAR_2017_2018", 
               "YEAR_2018_2019", "YEAR_2019_2020", "YEAR_2020_2021", "YEAR_2021_2022", "YEAR_2022_2023", TOTAL
        FROM HERITAGE_SITES
        """
        cursor.execute(query_gi_state)
        gi_state_df = pd.DataFrame.from_records(
            cursor.fetchall(),
            columns=[desc[0] for desc in cursor.description]
        ).rename(columns={'STATE_UT': 'State/UT',
                            'TOTAL': 'Total'})

        # Query for RS_Session_259_AU_1971_A (GI Year Data)
        query_gi_year = """
        SELECT YEAR, NO_OF_GI_APPLICATIONS NUMBER
        FROM GI_APPLICATIONS
        """
        cursor.execute(query_gi_year)
        gi_year_df = pd.DataFrame.from_records(
            cursor.fetchall(),
            columns=[desc[0] for desc in cursor.description]
        )

        # Query for RS_Session_256_AU_173_A_and_B (Budget Data)
        query_budget = """
        SELECT SL_NO, YEAR, ALLOCATION, EXPENDITURE
        FROM BUDGET
        """
        cursor.execute(query_budget)
        budget_df = pd.DataFrame.from_records(
            cursor.fetchall(),
            columns=[desc[0] for desc in cursor.description]
        ).rename(columns={
            'YEAR': 'Year',
            'ALLOCATION': 'Allocation',
            'EXPENDITURE': 'Expenditure'
        })

        # Query for asi_monuments_visitors (ASI Visitors Data)
        query_asi_visitors = """
        SELECT YEAR,NO_OF_TICKETED_MONUMENTS,DOMESTIC_VISITORS,
                FOREIGN_VISITORS,TOTAL_VISITORS,GROWTH_RATE_DOMESTIC,
                GROWTH_RATE_FOREIGN,GROWTH_RATE_TOTAL
        FROM ASI_VISITORS
        """
        cursor.execute(query_asi_visitors)
        asi_visitors_df = pd.DataFrame.from_records(
            cursor.fetchall(),
            columns=[desc[0] for desc in cursor.description]
        )

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Normalize column names for asi_visitors_df
        asi_visitors_df.columns = asi_visitors_df.columns.str.strip().str.replace('\s+', ' ', regex=True)
        
        # Check for 'Year' column and map possible variations
        possible_year_columns = [col for col in asi_visitors_df.columns if col.lower() in ['year', 'fiscal year', 'period']]
        if possible_year_columns:
            asi_visitors_df = asi_visitors_df.rename(columns={possible_year_columns[0]: 'Year'})
        else:
            st.warning("No 'Year' column found in asi_monuments_visitors.csv. Skipping ASI visitors plot.")
            asi_visitors_df['Year'] = pd.Series(dtype='object')  # Empty column to prevent errors
        
        # Check for visitor columns
        possible_domestic_cols = [col for col in asi_visitors_df.columns if 'domestic' in col.lower()]
        possible_foreign_cols = [col for col in asi_visitors_df.columns if 'foreign' in col.lower()]
        
        if possible_domestic_cols:
            asi_visitors_df = asi_visitors_df.rename(columns={possible_domestic_cols[0]: 'Number of Visitors - Domestic'})
        if possible_foreign_cols:
            asi_visitors_df = asi_visitors_df.rename(columns={possible_foreign_cols[0]: 'Number of Visitors - Foreign'})
        
        return visitors_df, monuments_df, gi_state_df, gi_year_df, budget_df, asi_visitors_df
    except Exception as e:
        st.error(f"Error loading CSV data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()


def create_animated_header():
    """Create an animated header component for Streamlit"""
    
    animated_header_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cultural Heritage Animation</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                overflow-x: hidden;
                min-height: 100vh;
                position: relative;
            }
            
            /* Background Pattern */
            body::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: 
                    radial-gradient(circle at 25% 25%, rgba(255,255,255,0.1) 1px, transparent 1px),
                    radial-gradient(circle at 75% 75%, rgba(255,255,255,0.05) 1px, transparent 1px);
                background-size: 50px 50px;
                animation: float 20s ease-in-out infinite;
                pointer-events: none;
            }
            
            @keyframes float {
                0%, 100% { transform: translate(0, 0) rotate(0deg); }
                33% { transform: translate(10px, -10px) rotate(1deg); }
                66% { transform: translate(-5px, 5px) rotate(-1deg); }
            }
            
            /* Header */
            .header {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                padding: 2rem;
                z-index: 100;
                color: white;
                opacity: 0;
                animation: fadeInDown 1s ease-out 2s forwards;
            }
            
            .header-inner {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .header-left {
                font-size: 1.2rem;
                font-weight: 600;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            
            .header-middle {
                display: flex;
                gap: 2rem;
            }
            
            .nav-link {
                color: white;
                text-decoration: none;
                font-weight: 500;
                font-size: 0.9rem;
                letter-spacing: 1px;
                text-transform: uppercase;
                transition: all 0.3s ease;
                position: relative;
                cursor: default; /* Remove pointer cursor */
            }
            
            .nav-link::after {
                content: '';
                position: absolute;
                bottom: -5px;
                left: 0;
                width: 0;
                height: 2px;
                background: white;
                transition: width 0.3s ease;
            }
            
            .nav-link:hover::after {
                width: 100%;
            }
            
            .social-links {
                display: flex;
                gap: 1rem;
            }
            
            .social-links a {
                color: white;
                text-decoration: none;
                font-weight: 500;
                font-size: 0.9rem;
                padding: 0.5rem;
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 50%;
                width: 35px;
                height: 35px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                cursor: default; /* Remove pointer cursor */
            }
            
            .social-links a:hover {
                background: rgba(255,255,255,0.2);
                transform: translateY(-2px);
            }
            
            /* Main Container */
            .main-container {
                position: relative;
                width: 100%;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }
            
            /* Side Text Elements */
            .text-element {
                position: absolute;
                font-family: 'Playfair Display', serif;
                font-size: 4rem;
                font-weight: 900;
                color: rgba(255,255,255,0.8);
                z-index: 50;
                letter-spacing: -2px;
                opacity: 0;
                animation: slideInSide 1s ease-out 1.5s forwards;
            }
            
            #text-ve {
                left: 5%;
                animation-name: slideInLeft;
            }
            
            #text-la {
                right: 5%;
                animation-name: slideInRight;
            }
            
            /* Image Container */
            .image-container {
                position: relative;
                width: 600px;
                height: 400px;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 30px 60px rgba(0,0,0,0.3);
                transform: scale(0.8);
                opacity: 0;
                animation: imageReveal 1.2s cubic-bezier(0.4, 0, 0.2, 1) 0.5s forwards;
            }
            
            .image-container img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                transition: transform 0.8s ease;
            }
            
            .image-container:hover img {
                transform: scale(1.05);
            }
            
            /* Image Overlay */
            .image-overlay {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                background: linear-gradient(transparent, rgba(0,0,0,0.8));
                color: white;
                padding: 2rem;
                transform: translateY(100%);
                animation: overlaySlideUp 0.8s ease-out 2.5s forwards;
            }
            
            .overlay-title {
                font-family: 'Playfair Display', serif;
                font-size: 1.8rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                letter-spacing: 1px;
            }
            
            .overlay-subtitle {
                font-size: 1rem;
                opacity: 0.9;
                font-weight: 300;
            }
            
            /* Big Title */
            .big-title {
                position: absolute;
                bottom: 8%;
                left: 5%;
                color: white;
                z-index: 75;
                font-family: 'Playfair Display', serif;
                font-weight: 900;
                font-size: clamp(2.5rem, 8vw, 6rem);
                line-height: 0.9;
                letter-spacing: -2px;
                text-shadow: 2px 2px 20px rgba(0,0,0,0.3);
            }
            
            .title-line {
                overflow: hidden;
                height: auto;
                margin-bottom: 0.2rem;
            }
            
            .title-line span {
                display: block;
                transform: translateY(100%);
                opacity: 0;
            }
            
            .title-line:nth-child(1) span {
                animation: titleSlideUp 0.8s cubic-bezier(0.4, 0, 0.2, 1) 3s forwards;
            }
            
            .title-line:nth-child(2) span {
                animation: titleSlideUp 0.8s cubic-bezier(0.4, 0, 0.2, 1) 3.2s forwards;
            }
            
            .title-line:nth-child(3) span {
                animation: titleSlideUp 0.8s cubic-bezier(0.4, 0, 0.2, 1) 3.4s forwards;
            }
            
            /* Footer */
            .footer {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 2rem;
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 100;
                color: white;
                transform: translateY(100%);
                animation: fadeInUp 1s ease-out 2.2s forwards;
            }
            
            .coordinates {
                font-size: 0.9rem;
                font-weight: 300;
                letter-spacing: 1px;
                opacity: 0.8;
            }
            
            /* Animations */
            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translateY(-30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(100%);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideInLeft {
                from {
                    opacity: 0;
                    transform: translateX(-50px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(50px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes imageReveal {
                from {
                    opacity: 0;
                    transform: scale(0.8);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            @keyframes overlaySlideUp {
                from {
                    transform: translateY(100%);
                }
                to {
                    transform: translateY(0);
                }
            }
            
            @keyframes titleSlideUp {
                from {
                    opacity: 0;
                    transform: translateY(100%);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .header-middle {
                    display: none;
                }
                
                .image-container {
                    width: 90vw;
                    height: 60vh;
                    max-width: 500px;
                }
                
                .text-element {
                    font-size: 2.5rem;
                }
                
                #text-ve {
                    left: 2%;
                }
                
                #text-la {
                    right: 2%;
                }
                
                .big-title {
                    left: 2%;
                    bottom: 5%;
                    font-size: clamp(2rem, 12vw, 4rem);
                }
                
                .header-inner {
                    padding: 0 1rem;
                }
                
                .social-links {
                    gap: 0.5rem;
                }
            }
        </style>
    </head>
    <body>
        <!-- Header -->
        <header class="header">
            <div class="header-inner">
                <div class="header-left">CULTURAL HERITAGE</div>
                <div class="header-middle">
                    <span class="nav-link">EXPLORE</span>
                    <span class="nav-link">DISCOVER</span>
                </div>
                <div class="header-right">
                    <div class="social-links">
                        <span>📍</span>
                        <span>🔍</span>
                    </div>
                </div>
            </div>
        </header>

        <!-- Side Text Elements -->
        <div class="text-element" id="text-ve">IN</div>
        <div class="text-element" id="text-la">DIA</div>

        <!-- Main Container -->
        <div class="main-container">
            <!-- Image Container -->
            <div class="image-container">
                <img src="https://studyinindia.gov.in/V3/images/blogs/single-blog/what-its-like-to-study-in-the-multicultural-land-of-india.webp" alt="Multicultural India">
                <div class="image-overlay">
                    <div class="overlay-title">Multicultural Heritage</div>
                    <div class="overlay-subtitle">Discover the rich tapestry of Indian culture and traditions</div>
                </div>
            </div>
        </div>

        <!-- Big Title -->
        <div class="big-title">
            <div class="title-line"><span>INCREDIBLE</span></div>
            <div class="title-line"><span>CULTURAL</span></div>
            <div class="title-line"><span>JOURNEY</span></div>
        </div>

        <!-- Footer -->
        <footer class="footer">
            <div class="coordinates">28.6139° N, 77.2090° E - New Delhi, India</div>
        </footer>
    </body>
    </html>
    """
    
    return animated_header_html
    
# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
    
    .main-header {
        font-size: 2.5rem;
        color: #FF6347;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Playfair Display', serif;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #FF8C00;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-family: 'Playfair Display', serif;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2E8B57;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-family: 'Playfair Display', serif;
    }
    .highlight-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .container {
        background-color: #FAFAFA;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .img-container {
        text-align: center;
        margin: 20px 0;
    }
    .caption {
        font-size: 0.9rem;
        font-style: italic;
        color: #555;
        text-align: center;
        margin-top: 5px;
    }
    
    /* Modern Sidebar Navigation */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .sidebar-title {
        font-size: 1.6rem;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        font-family: 'Playfair Display', serif;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Modern Radio Buttons */
    .stRadio > div {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    .stRadio > div:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .stRadio > div > label {
        color: white !important;
        font-weight: 500;
        cursor: pointer;
    }
    .stRadio > div > label > div[data-testid="stMarkdownContainer"] > p {
        color: white !important;
        font-size: 1rem;
        margin: 0;
    }
    
    /* Radio button selected state */
    .stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
        background-color: white !important;
        border-color: white !important;
    }
    
    .folium-map {
        width: 100%;
        height: 600px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Enhanced Cards */
    .heritage-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border: none;
        transition: transform 0.3s ease;
    }
    .heritage-card:hover {
        transform: translateY(-5px);
    }
    
    /* Modern Metrics */
    .metric-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .metric-container:hover {
        transform: translateY(-3px);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Animated Welcome Banner */
    .welcome-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    .welcome-banner::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    /* Style all selectbox containers with a gradient */
    .stSelectbox [data-baseweb="select"] {
        background: linear-gradient(45deg, #ADD8E6, #87CEEB); /* Gradient from light blue to darker light blue */
        border-radius: 5px;
        padding: 5px;
        border: 2px solid #87CEEB !important; /* Slightly darker light blue border */
    }
    /* Ensure inner elements of selectbox are filled with the gradient */
    .stSelectbox [data-baseweb="select"] > div {
        background: linear-gradient(45deg, #ADD8E6, #87CEEB) ; /* Gradient for inner div */
        color: #333333; /* Dark text for contrast */
        font-weight: 500;
    }
    /* Style all dropdown menu containers with the gradient */
    .stSelectbox [data-baseweb="popover"] {
        background: linear-gradient(45deg, #ADD8E6, #87CEEB) ; /* Gradient for dropdown container */
        border-radius: 5px;
        border: 1px solid #87CEEB !important; /* Light blue border for dropdown */
    }
    /* Style all dropdown lists with the gradient */
    .stSelectbox [data-baseweb="popover"] ul {
        background: linear-gradient(45deg, #ADD8E6, #87CEEB) ; /* Gradient for dropdown list */
        padding: 0;
        margin: 0;
    }
    /* Style all dropdown options with the gradient */
    .stSelectbox [data-baseweb="popover"] li {
        background: linear-gradient(45deg, #ADD8E6, #87CEEB) ; /* Gradient for each option */
        color: #333333; /* Dark text for readability */
        padding: 8px 12px;
        font-weight: 400;
    }
    /* Ensure no inherited styles override the dropdown option background */
    .stSelectbox [data-baseweb="popover"] li[data-testid="option"] {
        background: linear-gradient(45deg, #ADD8E6, #87CEEB) ; /* Gradient for specific option elements */
    }
    /* Hover effect for all dropdown options */
    .stSelectbox [data-baseweb="popover"] li:hover {
        background: #87CEEB !important; /* Solid darker light blue on hover */
        color: #FFFFFF; /* White text on hover for contrast */
    }
    /* Style for all selected dropdown options */
    .stSelectbox [data-baseweb="popover"] li[aria-selected="true"] {
        background: #87CEEB !important; /* Solid darker light blue for selected option */
        color: #FFFFFF; /* White text for selected option */
    }
    /* Style all dropdown arrows */
    .stSelectbox [data-baseweb="select"] .icon {
        color: #333333; /* Dark arrow for contrast */
    }
</style>
""", unsafe_allow_html=True)

# Function to display a placeholder image
def display_placeholder_image(width=600):
    st.image("https://img.freepik.com/free-vector/gradient-abstract-wireframe-background_23-2149009903.jpg?semt=ais_hybrid&w=740", width=width, caption="Image Not Available")

# Function to fetch and display an image from URL
def display_image_from_url(url, caption="", width=600):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            st.image(img, width=width, caption=caption)
        else:
            display_placeholder_image(width)
    except Exception:
        display_placeholder_image(width)



# Load CSV data
visitors_df, monuments_df, gi_state_df, gi_year_df, budget_df, asi_visitors_df = load_csv_data()

def create_responsible_tourism_swiper():
    # List of Indian states and Union Territories with 5 major tourist places each
    tourism_data = [
        {
            'state': 'Andaman and Nicobar Islands',
            'places': ['Radhanagar Beach', 'Cellular Jail', 'Neil Island', 'Ross Island', 'Baratang Limestone Caves']
        },
        {
            'state': 'Andhra Pradesh',
            'places': ['Tirupati Temple', 'Visakhapatnam Beach', 'Amaravati Stupa', 'Araku Valley', 'Lepakshi']
        },
        {
            'state': 'Arunachal Pradesh',
            'places': ['Tawang Monastery', 'Ziro Valley', 'Sela Pass', 'Namdapha National Park', 'Bomdila']
        },
        {
            'state': 'Assam',
            'places': ['Kaziranga National Park', 'Majuli Island', 'Kamakhya Temple', 'Umananda Temple', 'Hoollongapar Gibbon Sanctuary']
        },
        {
            'state': 'Bihar',
            'places': ['Mahabodhi Temple', 'Nalanda Ruins', 'Patna Sahib', 'Vishnupad Temple', 'Bodh Gaya']
        },
        {
            'state': 'Chandigarh',
            'places': ['Rock Garden', 'Sukhna Lake', 'Rose Garden', 'Capitol Complex', 'Elante Mall']
        },
        {
            'state': 'Dadra and Nagar Haveli and Daman and Diu',
            'places': ['Diu Fort', 'Naida Caves', 'Jampore Beach', 'Silvassa Tribal Museum', 'Devka Beach']
        },
        {
            'state': 'Chhattisgarh',
            'places': ['Chitrakoot Falls', 'Bastar Dussehra', 'Sirpur Heritage Site', 'Bhoramdeo Temple', 'Kanger Valley National Park']
        },
        {
            'state': 'Delhi',
            'places': ['Red Fort', 'Qutub Minar', 'India Gate', 'Lotus Temple', 'Humayun’s Tomb']
        },
        {
            'state': 'Goa',
            'places': ['Baga Beach', 'Basilica of Bom Jesus', 'Dudhsagar Falls', 'Fort Aguada', 'Anjuna Beach']
        },
        {
            'state': 'Gujarat',
            'places': ['Somnath Temple', 'Rann of Kutch', 'Gir National Park', 'Sabarmati Ashram', 'Dwarka']
        },
        {
            'state': 'Haryana',
            'places': ['Kurukshetra', 'Sultanpur Bird Sanctuary', 'Pinjore Gardens', 'Morni Hills', 'Badkhal Lake']
        },
        {
            'state': 'Himachal Pradesh',
            'places': ['Shimla Mall Road', 'Manali', 'Dharamshala', 'Kullu Valley', 'Spiti Valley']
        },
        {
            'state': 'Jammu and Kashmir',
            'places': ['Dal Lake', 'Gulmarg', 'Vaishno Devi Temple', 'Amarnath Cave', 'Pangong Lake']
        },
        {
            'state': 'Jharkhand',
            'places': ['Betla National Park', 'Jubilee Park', 'Dassam Falls', 'Ranchi Lake', 'Hundru Falls']
        },
        {
            'state': 'Karnataka',
            'places': ['Hampi Ruins', 'Mysore Palace', 'Coorg', 'Gokarna Beach', 'Badami Caves']
        },
        {
            'state': 'Kerala',
            'places': ['Munnar', 'Alleppey Backwaters', 'Kochi Fort', 'Periyar National Park', 'Varkala Beach']
        },
        {
            'state': 'Ladakh',
            'places': ['Leh Palace', 'Pangong Lake', 'Nubra Valley', 'Hemis Monastery', 'Tso Moriri']
        },
        {
            'state': 'Lakshadweep',
            'places': ['Agatti Island', 'Bangaram Atoll', 'Kavaratti Island', 'Minicoy Island', 'Kalpeni Island']
        },
        {
            'state': 'Madhya Pradesh',
            'places': ['Khajuraho Temples', 'Sanchi Stupa', 'Bandhavgarh National Park', 'Gwalior Fort', 'Orchha']
        },
        {
            'state': 'Maharashtra',
            'places': ['Ajanta & Ellora Caves', 'Gateway of India', 'Marine Drive', 'Shirdi Sai Baba Temple', 'Lonavala']
        },
        {
            'state': 'Manipur',
            'places': ['Loktak Lake', 'Keibul Lamjao National Park', 'Imphal War Cemetery', 'Shirui Lily', 'Kangla Fort']
        },
        {
            'state': 'Meghalaya',
            'places': ['Shillong', 'Cherrapunji', 'Living Root Bridges', 'Mawlynnong Village', 'Nohkalikai Falls']
        },
        {
            'state': 'Mizoram',
            'places': ['Aizawl', 'Vantawng Falls', 'Reiek Tlang', 'Dampa Tiger Reserve', 'Tam Dil Lake']
        },
        {
            'state': 'Nagaland',
            'places': ['Kohima War Cemetery', 'Hornbill Festival', 'Dzukou Valley', 'Kisama Heritage Village', 'Mokokchung']
        },
        {
            'state': 'Odisha',
            'places': ['Konark Sun Temple', 'Puri Jagannath Temple', 'Chilika Lake', 'Bhubaneswar Lingaraj Temple', 'Simlipal National Park']
        },
        {
            'state': 'Puducherry',
            'places': ['Auroville', 'Promenade Beach', 'Sri Aurobindo Ashram', 'Paradise Beach', 'French Quarter']
        },
        {
            'state': 'Punjab',
            'places': ['Golden Temple', 'Jallianwala Bagh', 'Wagah Border', 'Anandpur Sahib', 'Patiala Palace']
        },
        {
            'state': 'Rajasthan',
            'places': ['Jaipur Amber Fort', 'Udaipur City Palace', 'Jaisalmer Fort', 'Pushkar Lake', 'Ranthambore National Park']
        },
        {
            'state': 'Sikkim',
            'places': ['Gangtok', 'Tsomgo Lake', 'Nathula Pass', 'Rumtek Monastery', 'Pelling']
        },
        {
            'state': 'Tamil Nadu',
            'places': ['Madurai Meenakshi Temple', 'Chennai Marina Beach', 'Ooty', 'Kanyakumari', 'Mahabalipuram']
        },
        {
            'state': 'Telangana',
            'places': ['Charminar', 'Golconda Fort', 'Ramoji Film City', 'Warangal Fort', 'Salar Jung Museum']
        },
        {
            'state': 'Tripura',
            'places': ['Ujjayanta Palace', 'Neermahal', 'Unakoti Rock Carvings', 'Tripura Sundari Temple', 'Jampui Hills']
        },
        {
            'state': 'Uttar Pradesh',
            'places': ['Taj Mahal', 'Varanasi Ghats', 'Agra Fort', 'Fatehpur Sikri', 'Sarnath']
        },
        {
            'state': 'Uttarakhand',
            'places': ['Rishikesh', 'Haridwar', 'Kedarnath Temple', 'Valley of Flowers', 'Nainital']
        },
        {
            'state': 'West Bengal',
            'places': ['Kolkata Victoria Memorial', 'Darjeeling', 'Sundarbans', 'Howrah Bridge', 'Kalimpong']
        },
    ]
      
    swiper_html = f"""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <style>
      .tourism-swiper {{
        width: 100%;
        height: 450px;
        margin: 20px 0;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        overflow: hidden;
      }}
      .tourism-swiper .swiper-wrapper {{
        align-items: center;
      }}
      .tourism-swiper .swiper-slide {{
        text-align: center;
        font-size: 18px;
        background: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 10px;
        overflow: hidden;
        position: relative;
        transition: all 0.3s ease;
        transform: scale(0.8);
        opacity: 0.6;
      }}
      .tourism-swiper .swiper-slide-active {{
        transform: scale(1);
        opacity: 1;
        z-index: 10;
      }}
      .tourism-swiper .swiper-slide-prev,
      .tourism-swiper .swiper-slide-next {{
        transform: scale(0.9);
        opacity: 0.8;
        z-index: 5;
      }}
      .tourism-swiper .swiper-slide img {{
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
        opacity: 0.7; /* Slight opacity to emphasize text */
      }}
      .tourism-swiper .swiper-slide:hover img {{
        transform: scale(1.05);
      }}
      .slide-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5); /* Semi-transparent background for text readability */
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 20px;
      }}
      .slide-title {{
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 15px;
        font-family: 'Georgia', serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5); /* Shadow for readability */
      }}
      .slide-places {{
        font-size: 1.2rem;
        line-height: 1.8;
        opacity: 0.9;
        font-family: 'Arial', sans-serif;
        max-width: 80%; /* Prevent text from touching edges */
      }}
      .slide-places ul {{
        list-style-type: none;
        padding: 0;
      }}
      .slide-places li {{
        margin: 5px 0;
      }}
      .tourism-swiper .swiper-button-next,
      .tourism-swiper .swiper-button-prev {{
        color: #FF6347;
        background: rgba(255, 255, 255, 0.9);
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-top: 0;
        top: 50%;
        transform: translateY(-50%);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
      }}
      .tourism-swiper .swiper-button-next:hover,
      .tourism-swiper .swiper-button-prev:hover {{
        background: rgba(255, 255, 255, 1);
        transform: translateY(-50%) scale(1.1);
        box-shadow: 0 6px 16px rgba(0,0,0,0.3);
      }}
      .tourism-swiper .swiper-button-next:after,
      .tourism-swiper .swiper-button-prev:after {{
        font-size: 18px;
        font-weight: bold;
      }}
      .tourism-swiper .swiper-pagination-bullet {{
        width: 12px;
        height: 12px;
        background: #FF6347;
        opacity: 0.5;
      }}
      .tourism-swiper .swiper-pagination-bullet-active {{
        opacity: 1;
        transform: scale(1.2);
      }}
    </style>
    <div class="swiper tourism-swiper">
      <div class="swiper-wrapper">
        {''.join([f'''
        <div class="swiper-slide">
          <img src="https://img.freepik.com/free-vector/gradient-abstract-wireframe-background_23-2149009903.jpg?semt=ais_hybrid&w=740" alt="{data['state']}" />
          <div class="slide-overlay">
            <div class="slide-title">{data['state']}</div>
            <div class="slide-places">
              <ul>
                {''.join([f'<li>{place}</li>' for place in data['places']])}
              </ul>
            </div>
          </div>
        </div>
        ''' for data in tourism_data])}
      </div>
      <div class="swiper-button-next"></div>
      <div class="swiper-button-prev"></div>
      <div class="swiper-pagination"></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
      const swiper = new Swiper(".tourism-swiper", {{
        slidesPerView: 3,
        spaceBetween: 30,
        centeredSlides: true,
        loop: true,
        autoplay: {{
          delay: 4000,
          disableOnInteraction: false,
        }},
        pagination: {{
          el: ".swiper-pagination",
          clickable: true,
        }},
        navigation: {{
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        }},
        breakpoints: {{
          320: {{
            slidesPerView: 1,
            spaceBetween: 10,
          }},
          768: {{
            slidesPerView: 2,
            spaceBetween: 20,
          }},
          1024: {{
            slidesPerView: 3,
            spaceBetween: 30,
          }},
        }},
        effect: 'coverflow',
        coverflowEffect: {{
          rotate: 50,
          stretch: 0,
          depth: 100,
          modifier: 1,
          slideShadows: true,
        }},
      }});
    </script>
    """
    return swiper_html


# Enhanced Swiper component with web-accessible images
def create_enhanced_swiper():
    # Use placeholder images that represent Indian cultural heritage
    heritage_images = [
        {
            'url': 'https://static.toiimg.com/photo/62022874.cms',
            'title': 'Taj Mahal',
            'description': 'Symbol of eternal love in Agra'
        },
        {
            'url': 'https://images.unsplash.com/photo-1691075209051-00bf980a8a05?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8a2F0aGFrYWxpfGVufDB8fDB8fHww',
            'title': 'Kathakali Dance',
            'description': 'Traditional dance form from Kerala'
        },
        {
            'url': 'https://media.istockphoto.com/id/479431428/photo/puppets-many-hanging-on-string-rajasthan-india.jpg?s=612x612&w=0&k=20&c=bjuK7YrOc1Tx41CSU2lkkivibTDg46g6BYXj7FTky7U=', 
            'title': 'Rajasthani Crafts',
            'description': 'Intricate handicrafts from Rajasthan'
        },
        {
            'url': 'https://images.theconversation.com/files/642200/original/file-20250114-15-oucsvl.jpg?ixlib=rb-4.1.0&rect=0%2C85%2C4063%2C2031&q=45&auto=format&w=1356&h=668&fit=crop',
            'title': 'Kumbh Mela',
            'description': 'World\'s largest religious gathering'
        },
        {
            'url': 'https://images.moneycontrol.com/static-mcnews/2025/05/20250509124804_6-offbeat-hill-stations-in-south-india.jpg',
            'title': 'Hill Stations',
            'description': 'Scenic beauty of Indian mountains'
        },
        {
            'url': 'https://www.solitarytraveller.com/wp-content/uploads/2023/03/package_hampi_banner.jpg',
            'title': 'Hampi Ruins',
            'description': 'Ancient Vijayanagara Empire remains'
        },
        {
            'url': 'https://static.toiimg.com/img/107570872/Master.jpg',
            'title': 'Varanasi Ghats',
            'description': 'Sacred steps along the Ganges'
        },
        {
            'url': 'https://t3.ftcdn.net/jpg/09/49/56/84/360_F_949568481_ZVT2qxC7FmtZwOyDoBndGiVbV6ha5ZQF.jpg',
            'title': 'Bandhani Textiles',
            'description': 'Traditional tie-dye from Gujarat'
        },
        {
            'url': 'https://theindosphere.com/wp-content/uploads/2024/08/image-4.jpg',
            'title': 'Khajuraho Temples',
            'description': 'Medieval architectural marvels'
        },
         {
            'url': 'https://i.pinimg.com/736x/4a/66/10/4a66104772d3ba817af1ec89d4f3a242.jpg',
            'title': 'Kedharnath Temple',
            'description': 'Lord of the field'
        }
        
    ]
    
    swiper_html = f"""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <style>
      .heritage-swiper {{
        width: 100%;
        height: 450px;
        margin: 20px 0;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        overflow: hidden;
      }}
      
      .heritage-swiper .swiper-wrapper {{
        align-items: center;
      }}
      
      .heritage-swiper .swiper-slide {{
        text-align: center;
        font-size: 18px;
        background: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 10px;
        overflow: hidden;
        position: relative;
        transition: all 0.3s ease;
        transform: scale(0.8);
        opacity: 0.6;
      }}
      
      .heritage-swiper .swiper-slide-active {{
        transform: scale(1);
        opacity: 1;
        z-index: 10;
      }}
      
      .heritage-swiper .swiper-slide-prev,
      .heritage-swiper .swiper-slide-next {{
        transform: scale(0.9);
        opacity: 0.8;
        z-index: 5;
      }}
      
      .heritage-swiper .swiper-slide img {{
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
      }}
      
      .heritage-swiper .swiper-slide:hover img {{
        transform: scale(1.05);
      }}
      
      .slide-overlay {{
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(transparent, rgba(0,0,0,0.8));
        color: white;
        padding: 30px 20px 20px;
        text-align: left;
      }}
      
      .slide-title {{
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 5px;
        font-family: 'Georgia', serif;
      }}
      
      .slide-description {{
        font-size: 1rem;
        opacity: 0.9;
      }}
      
      .heritage-swiper .swiper-button-next,
      .heritage-swiper .swiper-button-prev {{
        color: #FF6347;
        background: rgba(255, 255, 255, 0.9);
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-top: 0;
        top: 50%;
        transform: translateY(-50%);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
      }}
      
      .heritage-swiper .swiper-button-next:hover,
      .heritage-swiper .swiper-button-prev:hover {{
        background: rgba(255, 255, 255, 1);
        transform: translateY(-50%) scale(1.1);
        box-shadow: 0 6px 16px rgba(0,0,0,0.3);
      }}
      
      .heritage-swiper .swiper-button-next:after,
      .heritage-swiper .swiper-button-prev:after {{
        font-size: 18px;
        font-weight: bold;
      }}
      
      .heritage-swiper .swiper-pagination-bullet {{
        width: 12px;
        height: 12px;
        background: #FF6347;
        opacity: 0.5;
      }}
      
      .heritage-swiper .swiper-pagination-bullet-active {{
        opacity: 1;
        transform: scale(1.2);
      }}
    </style>
    
    <div class="swiper heritage-swiper">
      <div class="swiper-wrapper">
        {''.join([f'''
        <div class="swiper-slide">
          <img src="{img['url']}" alt="{img['title']}" />
          <div class="slide-overlay">
            <div class="slide-title">{img['title']}</div>
            <div class="slide-description">{img['description']}</div>
          </div>
        </div>
        ''' for img in heritage_images])}
      </div>
      <div class="swiper-button-next"></div>
      <div class="swiper-button-prev"></div>
      <div class="swiper-pagination"></div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
      const swiper = new Swiper(".heritage-swiper", {{
        slidesPerView: 3,
        spaceBetween: 30,
        centeredSlides: true,
        loop: true,
        autoplay: {{
          delay: 4000,
          disableOnInteraction: false,
        }},
        pagination: {{
          el: ".swiper-pagination",
          clickable: true,
        }},
        navigation: {{
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        }},
        breakpoints: {{
          320: {{
            slidesPerView: 1,
            spaceBetween: 10,
          }},
          768: {{
            slidesPerView: 2,
            spaceBetween: 20,
          }},
          1024: {{
            slidesPerView: 3,
            spaceBetween: 30,
          }},
        }},
        effect: 'coverflow',
        coverflowEffect: {{
          rotate: 50,
          stretch: 0,
          depth: 100,
          modifier: 1,
          slideShadows: true,
        }},
      }});
    </script>
    """
    return swiper_html

# Custom CSS for modern navigation styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-right: none !important;
    }
    
    /* Sidebar content */
    .css-17eq0hr {
        background: transparent !important;
        color: white !important;
    }
    
    /* Modern sidebar title */
    .sidebar-title {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        padding: 1rem 0 !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Navigation container */
    .nav-container {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Navigation items */
    .nav-item {
        display: flex !important;
        align-items: center !important;
        padding: 0.75rem 1rem !important;
        margin: 0.5rem 0 !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: rgba(255, 255, 255, 0.9) !important;
        text-decoration: none !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        transform: translateX(5px) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52) !important;
        color: white !important;
        border-color: #ff6b6b !important;
        box-shadow: 0 8px 30px rgba(255, 107, 107, 0.4) !important;
    }
    
    .nav-icon {
        margin-right: 12px !important;
        font-size: 1.2rem !important;
        min-width: 24px !important;
    }
    
    /* Radio button styling override */
    .stRadio > div {
        background: transparent !important;
    }
    
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 0.75rem 1rem !important;
        margin: 0.5rem 0 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        transform: translateX(5px) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stRadio > div > label > div:first-child {
        display: none !important;
    }
    
    /* Hide default radio button */
    .stRadio input[type="radio"] {
        display: none !important;
    }
    
    /* Selected state */
    .stRadio > div > label[data-checked="true"] {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52) !important;
        border-color: #ff6b6b !important;
        box-shadow: 0 8px 30px rgba(255, 107, 107, 0.4) !important;
        color: white !important;
    }
    
    /* Navigation arrows/chevrons */
    .nav-arrow {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(79, 172, 254, 0.3) !important;
        margin: 0 0.5rem !important;
    }
    
    .nav-arrow:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 25px rgba(79, 172, 254, 0.5) !important;
    }
    
    .nav-arrow svg {
        color: white !important;
        font-size: 1.2rem !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .sidebar-title {
            font-size: 1.5rem !important;
        }
        
        .nav-item {
            padding: 0.6rem 0.8rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Alternative: Custom clickable navigation (if you want more control)
def create_custom_navigation():
    load_custom_css()
    
    #st.sidebar.markdown("""
     #   <div class='sidebar-title' style="color: black; backgroung-color : #FFFFFF">
      #      🛕 Cultural Explorer
       # </div>
    #""", unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style="
            background-color: #FFFFFF !important;
            padding: 10px;
            border-radius: 8px;
            display: flex;
            align-items: center;">
            <span style="font-size: 30px;">🛕</span>
            <span style="
                color: black !important;
                font-size: 0.6cm ;
                font-weight: bold;
                font-family: 'Arial Black', Arial, sans-serif;
                margin-left: 10px;">
                Cultural Explorer
            </span>
        </div>
    """, unsafe_allow_html=True)


    
    nav_items = [
        ("🏠", "Home"),
        ("🤖", "Bharat Bot"),
        ("🎨", "Traditional Art Forms"), 
        ("🏛️", "Cultural Heritage Sites"),
        ("📊", "Tourism Analytics"),
        ("🌱", "Responsible Tourism"),
        ("📅", "Cultural Events Calendar"),
        ("💰", "Cultural Economy"),
        ("🗺️", "Interactive Explorer")
    ]
    
    #st.sidebar.markdown("<div class='nav-container'>", unsafe_allow_html=True)
    
    current_page = st.session_state.get('page', 'Home')
    
    for icon, page_name in nav_items:
        active_class = "active" if page_name == current_page else ""
        
        # Create clickable navigation item
        if st.sidebar.button(f"{icon} {page_name}", key=f"nav_{page_name}"):
            st.session_state.page = page_name
            st.rerun()
    
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    return st.session_state.get('page', 'Home')

# Modern arrow navigation component
def create_navigation_arrows():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("◀", key="nav_prev", help="Previous"):
            # Add your previous page logic here
            pass
    
    with col3:
        if st.button("▶", key="nav_next", help="Next"):
            # Add your next page logic here
            pass

# Integration with your existing app structure:
def integrate_with_existing_app():
    """
    Replace your existing navigation code with this integration
    """
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'
    
    # Create the modern navigation (replaces your old sidebar code)
    page = create_custom_navigation()
    
    if page == "Bharat Bot":
        bharat_explorer()

    elif page == "Home":
        st.markdown("<h1 class='main-header'>🏛️ Indian Cultural Heritage Explorer</h1>", unsafe_allow_html=True)
    
        # Enhanced Swiper Carousel
        components.html(create_animated_header(), height=600, scrolling=False)
        components.html(create_enhanced_swiper(), height=500)
    
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            <div class='highlight-text'>
            <h3>🌟 Welcome to India's Cultural Tapestry</h3>
            Embark on a data-driven journey through India's magnificent cultural heritage. Discover traditional art forms, 
            explore UNESCO World Heritage sites, and learn about sustainable tourism practices that preserve our rich legacy for future generations.
            </div>
            """, unsafe_allow_html=True)
        
            st.markdown("""
            ### 🎭 What You'll Discover
        
            India's cultural heritage spans millennia, encompassing diverse traditions, architectural marvels, 
            and artistic expressions. This interactive platform combines data analytics with cultural exploration to offer:
        
            - **📊 Data-Driven Insights**: Tourism trends, visitor statistics, and economic impact analysis
            - **🎨 Art & Craft Traditions**: Geographic distribution and popularity of traditional art forms  
            - **🏛️ Heritage Sites**: Comprehensive information about UNESCO sites and protected monuments
            - **🌱 Sustainable Tourism**: Responsible travel practices and their positive impact
            - **🎪 Cultural Events**: Festival calendar and cultural celebration insights
            - **💰 Economic Impact**: Understanding the cultural economy and its significance
            """)
    
        with col2:
            st.markdown("""
            <div class='heritage-card'>
                <h3>🏛️ Quick Stats</h3>
                <p><strong>UNESCO Sites:</strong> 40</p>
                <p><strong>Protected Monuments:</strong> 3,691</p>
                <p><strong>Traditional Art Forms:</strong> 150+</p>
                <p><strong>Cultural Diversity Index:</strong> 95/100</p>
            </div>
            """, unsafe_allow_html=True)
        
            st.markdown("""
            <div class='heritage-card'>
                <h3>🎯 Featured Insights</h3>
                <p>• Tamil Nadu leads in foreign tourist arrivals</p>
                <p>• Uttar Pradesh has the most protected monuments</p>
                <p>• Kerala excels in responsible tourism practices</p>
                <p>• Rajasthan dominates cultural craft exports</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<h2 class='sub-header'>India's Cultural Diversity at a Glance</h2>", unsafe_allow_html=True)
    
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("UNESCO World Heritage Sites", "40", "+3 in last 5 years")
        with col2:
            st.metric("Protected Monuments", "3,691", "Maintained by ASI")
        with col3:
            st.metric("Traditional Art Forms", "150+", "Across different regions")
    
        st.markdown("<h2 class='sub-header'>Geographical Distribution of Cultural Heritage</h2>", unsafe_allow_html=True)
    
        monuments_data = load_monuments_data()
        monuments_data = monuments_data.sort_values(by='No_of_Monuments', ascending=False).head(10)
    
        fig = px.bar(monuments_data, x='State/UT', y='No_of_Monuments', 
                     title='Top 10 States by Number of Protected Monuments/Sites',
                     color='No_of_Monuments',
                     color_continuous_scale=px.colors.sequential.Viridis)
        fig.update_layout(xaxis_title='State/UT', yaxis_title='Number of Monuments')
        st.plotly_chart(fig, use_container_width=True)
    
        # Additional Visual: ASI Visitors Trend from CSV
        st.markdown("<h2 class='sub-header'>ASI Monuments Visitor Trends</h2>", unsafe_allow_html=True)
        if not asi_visitors_df.empty and 'Year' in asi_visitors_df.columns:
                fig_asi = go.Figure()
                if 'Number of Visitors - Domestic' in asi_visitors_df.columns:
                    fig_asi.add_trace(go.Scatter(
                        x=asi_visitors_df['Year'], 
                        y=asi_visitors_df['Number of Visitors - Domestic'].fillna(0),
                        mode='lines+markers', 
                        name='Domestic Visitors', 
                            line=dict(color='#FF5722')
                    ))
                if 'Number of Visitors - Foreign' in asi_visitors_df.columns:
                    fig_asi.add_trace(go.Scatter(
                        x=asi_visitors_df['Year'], 
                        y=asi_visitors_df['Number of Visitors - Foreign'].fillna(0),
                        mode='lines+markers', 
                        name='Foreign Visitors', 
                        line=dict(color='#4CAF50')
                    ))
                fig_asi.update_layout(
                    title="ASI Monument Visitors (1996-2020)", 
                    xaxis_title="Year", 
                    yaxis_title="Visitors"
                )
                st.plotly_chart(fig_asi, use_container_width=True)
        else:
                st.warning("ASI visitor data unavailable or missing required columns.")
    
        st.markdown("""
        <div class='caption'>
        Source: Archaeological Survey of India (ASI) data accessed from data.gov.in
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h2 class='sub-header'>Latest Tourism Trends</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
    
        with col1:
            # Placeholder data for Foreign Tourist Arrivals by Purpose (2023)
            fta_purpose = pd.DataFrame({
                'Purpose': ['Leisure', 'Business', 'Religious', 'Others'],
                'Share': [60, 20, 15, 5]
            })
            fig_fta = px.pie(fta_purpose, values='Share', names='Purpose', 
                             title='Foreign Tourist Arrivals by Purpose (2023)',
                             color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig_fta, use_container_width=True)
    
        with col2:
            # Placeholder data for Domestic Tourism by Region (2023)
            domestic_region = pd.DataFrame({
                'Region': ['North', 'South', 'East', 'West', 'Northeast'],
                'Share': [30, 25, 20, 18, 7]
            })
            fig_domestic = px.pie(domestic_region, values='Share', names='Region', 
                                  title='Domestic Tourism by Region (2023)',
                                  color_discrete_sequence=px.colors.qualitative.Set1)
            st.plotly_chart(fig_domestic, use_container_width=True)
    
        st.markdown("""
        <div class='caption'>
        The above charts illustrate the diversity of tourism in India, with foreign visitors primarily 
        arriving for leisure and religious purposes, while domestic tourism is spread across regions, 
        with the North and South leading.
        </div>
        """, unsafe_allow_html=True)

    # Traditional Art Forms Page
    elif page == "Traditional Art Forms":
        st.markdown("<h1 class='main-header'>Traditional Art Forms of India</h1>", unsafe_allow_html=True)
    
        st.markdown("""
        <div class='highlight-text'>
        India's artistic heritage includes a diverse array of painting styles, dance forms, music traditions, 
        and crafts that are deeply rooted in the country's cultural history and regional diversity.
        </div>
        """, unsafe_allow_html=True)
    
        art_category = st.tabs(["Visual Arts", "Performing Arts", "Crafts"])
    
        with art_category[0]:
            st.markdown("<h2 class='sub-header'>Traditional Painting Styles</h2>", unsafe_allow_html=True)
        
            arts_data = load_arts_data()
            painting_data = arts_data[arts_data['Category'] == 'Painting']
        
            col1, col2 = st.columns([3, 2])
        
            with col1:
                fig = px.bar(painting_data.sort_values(by='Popularity_Score', ascending=False), 
                             x='Art_Form', y='Popularity_Score', color='Region',
                             title='Traditional Painting Styles by Region and Popularity')
                fig.update_layout(xaxis_title='Art Form', yaxis_title='Popularity Score')
                st.plotly_chart(fig, use_container_width=True)
       
            with col2:
                selected_art = st.selectbox(
                    "Select a painting style to learn more:",
                    painting_data['Art_Form'].tolist()
                )
            
                art_info = {
                    'Madhubani': {
                        'description': 'Madhubani painting, also known as Mithila painting, originates from Bihar’s Mithila region. It uses geometric patterns, natural dyes, and vibrant colors to depict mythological themes and daily life.',
                        'image_url': 'https://media-cdn.tripadvisor.com/media/photo-s/1b/39/bf/a2/madhubani-painting-is.jpg'
                    },
                    'Warli': {
                        'description': 'Warli painting is a tribal art form from Maharashtra, using simple geometric shapes like circles, triangles, and squares. Painted with white pigment on a mud base, it illustrates social events and nature.',
                        'image_url': 'https://cdn.magicdecor.in/com/2024/01/17124731/Village-Life-Ancient-Indian-Warli-Art-Wallpaper-for-Wall-710x488.jpg'
                    },
                    'Kalamkari': {
                        'description': 'Kalamkari, from Andhra Pradesh, is an ancient hand-painting style on cotton or silk using a bamboo pen. Its 23-step process creates intricate designs, often depicting mythological narratives.',
                        'image_url': 'https://i.pinimg.com/736x/ad/35/65/ad35659c094db9a255bd57255da7d3a3.jpg'
                    },
                    'Tanjore': {
                        'description': 'Tanjore painting, from Thanjavur, Tamil Nadu, is a classical art form known for vibrant colors, gold foil, and inlaid gems. It typically portrays Hindu deities and religious themes.',
                        'image_url': 'https://img1.wsimg.com/isteam/ip/bd95d888-15fd-4e22-9514-3b3e7856faa7/d1fc0d4d-12eb-4019-a7aa-f00566d84891.jpg'
                    },
                    'Pattachitra': {
                        'description': 'Pattachitra, a cloth-based scroll painting from Odisha and West Bengal, features intricate details and vibrant colors, depicting Hindu mythological stories and folktales.',
                        'image_url': 'https://i0.wp.com/www.craftsodisha.com/wp-content/uploads/2019/03/p00628-141323-radha-krishna-dancing-monochrome-pattachitra-art.jpg'
                    },
                    'Gond': {
                        'description': 'Gond painting, a tribal art from Madhya Pradesh, uses intricate patterns of dots, dashes, and lines to represent nature, folklore, and tribal life in vibrant colors.',
                        'image_url': 'https://m.media-amazon.com/images/I/61Kv77ptK1L._AC_UF1000,1000_QL80_.jpg'
                    },
                    'Phad': {
                        'description': 'Phad painting is a religious scroll painting from Rajasthan, depicting folk epics and local deities on long cloth pieces, using bold colors and narrative storytelling.',
                        'image_url': 'https://www.bridgebharat.com/cdn/shop/files/BBP0002RPHD00023_533x.jpg?v=1720843220'
                    },
                    'Miniature': {
                        'description': 'Miniature painting, prominent in Rajasthan, features intricate details and delicate brushwork. Rajput and Mughal styles depict royal life, mythology, and nature.',
                        'image_url': 'https://m.media-amazon.com/images/I/61tUr+HkaoL._AC_UF1000,1000_QL80_.jpg'
                    },
                    "Pahari Painting": {
                        "description": "Pahari painting, originating from the hill states of Himachal Pradesh and Jammu, is known for its delicate, lyrical style, vibrant colors, and themes of love, mythology, and nature, often depicting Krishna and Radha.",
                        "image_url": "https://hpgeneralstudies.com/wp-content/uploads/2016/11/Pahari-Styles-of-Painting-Kangra-painting-himachal-pradesh-general-knowledge.jpg"
                    }
                }
            
                if selected_art in art_info:
                    st.markdown(f"### {selected_art} Painting")
                    st.markdown(art_info[selected_art]['description'])
                    display_image_from_url(art_info[selected_art]['image_url'], f"{selected_art} Style", width=400)
                else:
                    st.write(f"Information about {selected_art} is not available.")
                
            st.markdown("<h2 class='sub-header'>Art Form Distribution by Region</h2>", unsafe_allow_html=True)
        
            # Assuming this is within an elif block in a Streamlit app
            # Load both datasets
            arts_data = load_arts_data()
            crafts_data = load_crafts_data()

            # Combine datasets, prioritizing arts_data and adding crafts_data where coordinates match
            combined_data = arts_data.copy()
            crafts_data['source'] = 'craft'
            arts_data['source'] = 'art'
            combined_data = pd.concat([arts_data, crafts_data], ignore_index=True)

            # Check for NaN values in lat and lon
            if combined_data[['lat', 'lon']].isna().any().any():
                #st.warning("Some entries contain missing latitude or longitude values and will be excluded from the map.")
                combined_data = combined_data.dropna(subset=['lat', 'lon'])

            # Verify if any data remains after dropping NaNs
            if combined_data.empty:
                st.error("No valid data with latitude and longitude available to display on the map.")
            else:
                # Create the Folium map
                m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles='cartodbpositron')
                marker_cluster = MarkerCluster().add_to(m)

                # Iterate through combined data to create markers
                for _, row in combined_data.iterrows():
                    # Initialize popup content
                    popup_content = ""
                    
                    if row['source'] == 'art':
                        # Art-related information
                        popup_content = f"""
                        <b>{row['Art_Form']}</b><br>
                        Region: {row['Region']}<br>
                        Popularity: {row['Popularity_Score']}<br>
                        Category: {row['Category']}
                        """
                        tooltip = row['Art_Form']
                    elif row['source'] == 'craft':
                        # Craft-related information
                        popup_content = f"""
                        <b>{row['Craft']}</b><br>
                        State: {row['State']}<br>
                        Artisans Count: {row['Artisans_Count']}<br>
                        Annual Revenue (Cr): {row['Annual_Revenue_Cr']}
                        """
                        tooltip = row['Craft']

                    # Add marker to the map
                    folium.Marker(
                        location=[row['lat'], row['lon']],
                        popup=folium.Popup(popup_content, max_width=300),
                        tooltip=tooltip,
                        icon=folium.Icon(color='orange' if row['source'] == 'art' else 'blue', icon='paint-brush' if row['source'] == 'art' else 'scissors', prefix='fa')
                    ).add_to(marker_cluster)

                # Render the map in Streamlit
                map_html = m._repr_html_()
                components.html(map_html, height=600)
                
    
        with art_category[1]:
            st.markdown("<h2 class='sub-header'>Classical Dance and Music Traditions</h2>", unsafe_allow_html=True)
        
            arts_data = load_arts_data()
            performing_arts = arts_data[(arts_data['Category'] == 'Dance') | (arts_data['Category'] == 'Music')]
        
            col1, col2 = st.columns([3, 2])
        
            with col1:
                fig = px.bar(performing_arts.sort_values(by='Popularity_Score', ascending=False), 
                             x='Art_Form', y='Popularity_Score', color='Category',
                             title='Traditional Performing Arts by Type and Popularity')
                fig.update_layout(xaxis_title='Art Form', yaxis_title='Popularity Score')
                st.plotly_chart(fig, use_container_width=True)
        
            with col2:
                selected_art = st.selectbox(
                    "Select a performing art to learn more:",
                    performing_arts['Art_Form'].tolist()
                )
            
                art_info = {
                    'Carnatic': {
                        'description': 'Carnatic music is a system of music commonly associated with South India, including the modern states of Karnataka, Andhra Pradesh, Telangana, Kerala and Tamil Nadu.',
                        'image_url': 'https://centerforworldmusic.org/wp-content/uploads/2021/02/Subbulakshmi-Concert.jpg'
                    },
                    'Kathakali': {
                        'description': 'Kathakali is a classical dance form from Kerala that combines dance, music, and acting. Performers use elaborate costumes, makeup, and face masks to portray characters from Hindu epics.',
                        'image_url': 'https://miro.medium.com/v2/resize:fit:1024/1*lhWHQ6Oq1gowqn_uOtlfbg.jpeg'
                    },
                    'Bharatanatyam': {
                        'description': 'Bharatanatyam is one of the oldest classical dance forms of India, originating in Tamil Nadu. It is known for its grace, purity, tenderness, and sculpturesque poses.',
                        'image_url': 'https://5.imimg.com/data5/BM/CE/WE/SELLER-92722583/bharatanatyam-arangetram-photoshoot.jpg'
                    },
                    'Kathak': {
                        'description': 'Kathak is one of the eight major forms of Indian classical dance that originated from North India. It is characterized by rhythmic footwork, rapid spins, and expressive storytelling.',
                        'image_url': 'https://i.pinimg.com/564x/8b/94/fc/8b94fc84c81c6acddddf1644db60990f.jpg'
                    },
                    'Odissi': {
                        'description': 'Odissi is a classical dance form from Odisha that emphasizes fluid movements, emotional expressions, and intricate footwork. It primarily portrays themes related to Lord Jagannath and other regional deities.',
                        'image_url': 'https://lotusarise.com/wp-content/uploads/2024/03/Odissi_Performance-632x1024.jpeg'
                    },
                    'Kuchipudi': {
                        'description': 'Kuchipudi is a classical dance form from Andhra Pradesh that involves rituals, invocations, rhythm, and expressive communication of spiritual ideas.',
                        'image_url': 'https://i.pinimg.com/1200x/6a/44/d2/6a44d248445f651f482248f39119bf78.jpg'
                    },
                    'Hindustani': {
                        'description': 'Hindustani classical music is a North Indian classical music tradition that evolved from ancient Hindu musical traditions, Vedic philosophy, and Persian influences.',
                        'image_url': 'https://blogs.lawrence.edu/news/files/2017/04/Zahir-Hussain_newsblog.jpg'
                    },
                    "Bihu": {
                        "description": "Bihu is a folk dance from Assam, performed during the Bihu festival. It is characterized by brisk steps, rapid hand movements, and vibrant costumes, celebrating the Assamese New Year and agricultural cycles.",
                        "image_url": "https://i.pinimg.com/736x/4c/88/94/4c8894faf7b15fc026f98f646436c6b2.jpg"
                    },
                    "Ghoomar": {
                        "description": "Ghoomar is a traditional folk dance from Rajasthan, performed by women in swirling skirts. It is known for its graceful movements and vibrant attire, often performed during festivals and celebrations.",
                        "image_url": "https://i.pinimg.com/736x/d9/83/4a/d9834af8475da9aa305f679dcbb6f3e5.jpg"
                    },
                    "Chhau": {
                        "description": "Chhau is a semi-classical dance form from eastern India, particularly Jharkhand, Odisha, and West Bengal. It combines martial arts, acrobatics, and storytelling, often depicting scenes from Hindu epics.",
                        "image_url": "https://photos.smugmug.com/Photography-still-life-culture/Photography-Dances-of-India-Chhau-Dance/i-qxgH7fs/0/NNnxW5vFTFPQrbZDdZfVsPTxt4dqSpH2nPc7B77Wm/XL/Kartik%201-XL.jpg"
                    },
                    "Garba": {
                        "description": "Garba is a folk dance from Gujarat, performed during the Navratri festival. It involves circular movements and rhythmic clapping, symbolizing devotion to Goddess Durga.",
                        "image_url": "https://www.livemint.com/lm-img/img/2024/10/03/600x338/2-0-305167323--ABH0216-men-0_1680607324691_1727968179214.jpg"
                    },
                    "Lavani": {
                        "description": "Lavani is a traditional folk dance from Maharashtra, known for its energetic and sensuous movements. It is often performed to the beats of the dholki and combines dance with storytelling.",
                        "image_url": "https://static.toiimg.com/photo/51616060.cms?imgsize=111336"
                    },
                    "Bodo Dance": {
                        "description": "Bodo dance is a folk dance performed by the Bodo community of Assam. It is characterized by vibrant costumes and rhythmic movements, often celebrating agricultural and cultural festivals.",
                        "image_url": "https://www.contentgarden.in/PICTURES/270123/WATERMARK/20230127002L.jpg"
                    },
                    "Sattriya": {
                        "description": "Sattriya is a classical dance form from Assam, originating in the Vaishnavite monasteries. It combines grace, spirituality, and storytelling, depicting themes from Hindu mythology.",
                        "image_url": "https://i0.wp.com/rotarynewsonline.org/wp-content/uploads/2019/07/545px-Satriya_dance_performance_at_Guwahati_Rabindra_Bhawan.jpg?ssl=1"
                    },
                    "Yakshagana": {
                        "description": "Yakshagana is a traditional theatre form from Karnataka, combining dance, music, and drama. Performers wear elaborate costumes and makeup to enact stories from Indian epics.",
                        "image_url": "https://orunewculture.com/wp-content/uploads/2025/01/yaksh.webp"
                    },
                    "Thang-Ta": {
                        "description": "Thang-Ta is a martial art dance form from Manipur, combining graceful movements with combat techniques. It is performed with swords and spears, showcasing strength and agility.",
                        "image_url": "https://cdn-images.prepp.in/public/image/5fa7ca05557ad47e2753cde27c4431ef.png?tr=w-512,h-327,c-force"
                    },
                    "Bhangra": {
                        "description": "Bhangra is a lively folk dance from Punjab, traditionally performed by men during harvest festivals. It is characterized by energetic movements, vibrant costumes, and the beat of the dhol.",
                        "image_url": "https://cdn.britannica.com/04/60404-050-77D978DF/Bhangra-folk-dance-region-Punjab-India-Pakistan.jpg"
                    },
                    "Giddha": {
                        "description": "Giddha is a folk dance performed by women in Punjab, known for its lively and expressive movements. It often involves singing traditional songs and storytelling through dance.",
                        "image_url": "https://indianetzone.wordpress.com/wp-content/uploads/2023/06/1541273538_giddha-dance1.jpg?w=1024"
                    },
                    "Cheraw": {
                        "description": "Cheraw is a traditional bamboo dance from Mizoram, performed by women. It involves rhythmic stepping between moving bamboo sticks, showcasing coordination and grace.",
                        "image_url": "https://pbs.twimg.com/media/FCnyH-YVQAQ3kOz?format=jpg&name=large"
                    },
                    "Fugdi": {
                        "description": "Fugdi is a folk dance from Goa, performed by women during festivals like Ganesh Chaturthi. It involves circular movements and singing, reflecting joy and community spirit.",
                        "image_url": "https://media.assettype.com/gomantaktimes%2F2022-11%2F69306823-68e1-4166-8eb3-698d0d1e473f%2F1.png"
                    },
                    "Dalkhai": {
                        "description": "Dalkhai is a folk dance from Odisha, performed by women during festivals. It is known for its vibrant movements and songs that narrate stories of love and nature.",
                        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Sambalpuri_Dance.JPG/1200px-Sambalpuri_Dance.JPG"
                    },
                    "Tharu Folk": {
                        "description": "Tharu folk dance is performed by the Tharu community in Uttar Pradesh and Uttarakhand. It reflects their cultural heritage, with rhythmic movements celebrating agricultural life.",
                        "image_url": "https://staticimg.amarujala.com/assets/images/gaonjunction.com/2023/11/16/jhamara-lkanataya-ka-parasatata-thata-vavasha-lkashhama-va-anaya-thanpr-janajata-ka-lga_1700144716.jpeg?w=414&dpr=1.0&q=50"
                    },
                    "Santhali Dance": {
                        "description": "Santhali dance is a tribal folk dance performed by the Santhal community in Jharkhand, Odisha, and West Bengal. It is characterized by vibrant group movements and traditional music.",
                        "image_url": "https://live.staticflickr.com/7606/16147402643_4586ed4b6f_c.jpg"
                    },
                    "Rabindra Sangeet": {
                        "description": "Rabindra Sangeet refers to songs composed by Rabindranath Tagore, often accompanied by dance in West Bengal. The dance complements the soulful music, expressing poetic themes.",
                        "image_url": "https://assets.thehansindia.com/hansindia-bucket/7460_Rabindra_Sangeet.jpg"
                    },
                    "Koli Dance": {
                        "description": "Koli dance is a folk dance performed by the Koli fishing community in Maharashtra. It reflects their coastal culture with lively steps and songs about the sea.",
                        "image_url": "https://i.pinimg.com/736x/e2/08/18/e20818253fc1a887292f163b6882b904.jpg"
                    },
                    "Tusu Parab": {
                        "description": "Tusu Parab is a folk dance performed during the Tusu festival in Jharkhand and West Bengal. It involves singing and dancing to celebrate the harvest season.",
                        "image_url": "https://utsav.gov.in/public/uploads/event_picture_image/event_686/16607352252119234166.jpg"
                    }
                }
                            
                if selected_art in art_info:
                    st.markdown(f"### {selected_art}")
                    st.markdown(art_info[selected_art]['description'])
                    display_image_from_url(art_info[selected_art]['image_url'], f"{selected_art}", width=400)
                else:
                    st.write(f"Information about {selected_art} is not available.")
        
            st.markdown("<h2 class='sub-header'>Performing Arts Schools and Academies</h2>", unsafe_allow_html=True)
        
            institutions_data = {
                'Institution': ['Kalakshetra Foundation', 'Kathak Kendra', 'Sangeet Natak Akademi', 
                               'Nrityagram', 'Manipuri Dance Academy', 'Utkal Sangeet Mahavidyalaya',
                               'ITC Sangeet Research Academy', 'Kerala Kalamandalam', 'Jaipur Gharana',
                               'Bharatiya Vidya Bhavan'],
                'Location': ['Chennai', 'New Delhi', 'New Delhi', 'Bangalore', 'Imphal', 'Bhubaneswar',
                            'Kolkata', 'Thrissur', 'Jaipur', 'Multiple Locations'],
                'Art_Form': ['Bharatanatyam', 'Kathak', 'Multiple', 'Multiple', 'Manipuri', 'Odissi',
                            'Hindustani', 'Kathakali', 'Kathak', 'Multiple'],
                'Established': [1936, 1964, 1952, 1990, 1954, 1964, 1977, 1930, 1750, 1938],
                'Students_Annual': [300, 250, 150, 80, 120, 200, 90, 220, 150, 500]
            }
        
            institutions_df = pd.DataFrame(institutions_data)
        
            fig = px.scatter(institutions_df, x='Established', y='Students_Annual', 
                            color='Art_Form', size='Students_Annual',
                            hover_name='Institution', hover_data=['Location'],
                            title='Major Performing Arts Institutions in India')
            fig.update_layout(xaxis_title='Year Established', yaxis_title='Annual Student Intake')
            st.plotly_chart(fig, use_container_width=True)
    
        with art_category[2]:
            st.markdown("<h2 class='sub-header'>Traditional Handicrafts</h2>", unsafe_allow_html=True)
        
            crafts_data = load_crafts_data()
        
            col1, col2 = st.columns([3, 2])
        
            with col1:
                fig = px.bar(crafts_data.sort_values(by='Annual_Revenue_Cr', ascending=False).head(10), 
                             x='Craft', y='Annual_Revenue_Cr', color='State',
                             title='Top 10 Handicrafts by Annual Revenue (₹ in Crores)')
                fig.update_layout(xaxis_title='Craft', yaxis_title='Annual Revenue (₹ Crores)')
                st.plotly_chart(fig, use_container_width=True)
        
            with col2:
                selected_craft = st.selectbox(
                    "Select a craft to learn more:",
                    crafts_data['Craft'].tolist()
                )
            
                craft_info = {
                    'Kanjivaram Silk': {
                        'description': 'Kanjivaram silk sarees are woven from pure mulberry silk and are known for their heavy body, vibrant colors, wide contrast borders, and rich pallu adorned with intricate zari work.',
                        'image_url': 'https://www.singhanias.in/cdn/shop/articles/1e31d5353b95970dd2d9f4c8a4abc755.jpg?v=1646740243'
                    },
                    'Pashmina': {
                        'description': 'Pashmina refers to a fine type of Kashmir wool and the textiles made from it. Known for its exceptional warmth, softness, and lightweight quality, it is derived from the fine undercoat fibers of the Changthangi goat.',
                        'image_url': 'https://media.istockphoto.com/id/1429359526/photo/lao-silk-scarf-at-night-market-at-lunag-prabang-with-wat-may-souvannapoumaram-in-the.jpg?s=612x612&w=0&k=20&c=ITcJxlyoupDZznv-X3qOxwBB74FASOXm5oPDSjfFyzc='
                    },
                    'Chikankari': {
                        'description': 'Chikankari is a traditional embroidery style from Lucknow, Uttar Pradesh. It involves white thread embroidery on fine white cotton fabric, creating a shadow work effect.',
                        'image_url': 'https://t3.ftcdn.net/jpg/12/14/79/94/360_F_1214799416_Jqnavj8Hc866yW3JZS1z1icxcOWs4l8B.jpg'
                    },
                    'Blue Pottery': {
                        'description': 'Blue Pottery is a traditional craft of Jaipur, Rajasthan. It is made from quartz stone powder, not clay, and is known for its vibrant blue dye and distinctive Persian patterns.',
                        'image_url': 'https://media.istockphoto.com/id/497537972/photo/chinese-style-porcelain-pottery.jpg?s=612x612&w=0&k=20&c=hr702O-4YrezRL6L4ZyotCNSMdM9jT5cwPf0EVsK2xU='
                    },
                    'Brass Work': {
                        'description': 'Brass work is a significant craft tradition in Uttar Pradesh, particularly in Moradabad, which is known as the "Brass City." Artisans create intricately designed utensils, decorative items, and religious artifacts.',
                        'image_url': 'https://www.gitagged.com/wp-content/uploads/2022/10/MBC-002-RAM-DARBHAR-BIG-2.jpg'
                    },
                    'Bidriware': {
                        'description': 'Bidriware is a metal handicraft from Bidar, Karnataka. It involves inlaying silver or gold on a blackened metal alloy of zinc and copper, creating striking contrast designs.',
                        'image_url': 'https://www.ibef.org/experienceindia/images/bidriware/bidri-image-1.png'
                    },
                    'Bandhani': {
                        'description': 'Bandhani is a tie-dye textile technique from Gujarat and Rajasthan. It involves tying portions of cloth before dyeing, resulting in intricate patterns of dots.',
                        'image_url': 'https://t3.ftcdn.net/jpg/09/49/56/84/360_F_949568481_ZVT2qxC7FmtZwOyDoBndGiVbV6ha5ZQF.jpg'
                    },
                    'Phulkari': {
                        'description': 'Phulkari is an embroidery technique from Punjab, where colorful threads are used to create floral patterns on shawls and other garments. The term means "flower work" in Punjabi.',
                        'image_url': 'https://static.fibre2fashion.com//articleresources/images/57/5630/AdobeStock_968996166-s_Small.jpg'
                    },
                    'Terracotta': {
                        'description': 'Terracotta crafts involve creating objects from baked clay. In West Bengal, particularly in Bankura district, artisans are famous for creating the Bankura horse and other figurines.',
                        'image_url': 'https://cdn.shopify.com/s/files/1/0486/7712/6297/files/Add-a-subheading_2_600x600.webp?v=1687850806'
                    },
                    'Dokra': {
                        'description': 'Dokra is a non-ferrous metal casting technique using the lost-wax casting method. It is practiced in tribal areas of Chhattisgarh, West Bengal, and Odisha, creating distinctive figurines.',
                        'image_url': 'https://www.gitagged.com/wp-content/uploads/2020/10/Bastar-Dhokra-Swan-Art-GiTAGGED-4.jpg'
                    },
                    'Chanderi': {
                        'description': 'Chanderi is a traditional handwoven fabric made in Chanderi, Madhya Pradesh. Known for its sheer texture and lightweight, it often features gold and silver zari work.',
                        'image_url': 'https://www.shutterstock.com/image-photo/hand-weaving-silk-handloom-sarees-600nw-2552045721.jpg'
                    },
                    'Zardozi': {
                        'description': 'Zardozi is a form of heavy and elaborate metal embroidery on fabric. It originated in Persia and was brought to India during the Mughal era. It uses gold and silver threads to create intricate designs.',
                        'image_url': 'https://5.imimg.com/data5/WW/TR/YB/ANDROID-49526605/imtemp1573397807473-png-500x500.png'
                    },
                    'Meenakari': {
                        'description': 'Meenakari is the art of coloring and ornamenting the surface of metals by fusing brilliant colors in an intricate design. Rajasthan, particularly Jaipur, is famous for this craft.',
                        'image_url': 'https://i.pinimg.com/736x/5d/75/5e/5d755e1d31fd4dbe44fe3827c869c0e7.jpg'
                    },
                    'Aari Work': {
                        'description': 'Aari work is a type of embroidery done using a hooked needle (aari) from Kashmir. It produces a chain stitch on the fabric surface and is characterized by minute detailing and elaborate patterns.',
                        'image_url': 'https://i.ytimg.com/vi/HXkfSlhzb0A/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLDyDZqGgBth1bQP_4-_7BS_zjtBUg'
                    },
                    'Kasuti': {
                        'description': 'Kasuti is a traditional form of folk embroidery from Karnataka. It involves intricate stitches to create geometric patterns on clothing, particularly sarees.',
                        'image_url': 'https://www.hunarcourses.com/blog/wp-content/uploads/2022/08/Image-1-13.jpg'
                    },
                    'Bamboo Craft': {
                        'description': 'Bamboo Craft is a traditional art form widely practiced in Assam and other northeastern states of India. Artisans create intricate baskets, mats, furniture, and decorative items using sustainable bamboo, known for its flexibility and strength.',
                        'image_url': 'https://5.imimg.com/data5/IH/OU/MY-12266299/bamboo-work-handicraft-500x500.jpg'
                    },
                    'Assam Silk': {
                        'description': 'Assam Silk, particularly Eri, Muga, and Pat silk, is renowned for its rich texture and natural sheen. Woven in Assam, these silks are used for traditional garments like Mekhela Chador, celebrated for their durability and elegance.',
                        'image_url': 'https://media.assettype.com/outlooktraveller%2Fimport%2Foutlooktraveller%2Fpublic%2Fuploads%2Farticles%2Ftravelnews%2F2018%2F06%2Fassamese-traditional-assam-silk-featured.jpg'
                    },
                    'Stone Carving': {
                        'description': 'Stone Carving is a traditional craft practiced across India, especially in Odisha and Rajasthan. Artisans sculpt intricate designs on marble, sandstone, and other stones to create statues, temple architecture, and decorative pieces.',
                        'image_url': 'https://i.pinimg.com/564x/0b/41/26/0b4126948b738c40103e957585eb05b3.jpg'
                    },
                    'Kalamkari': {
                        'description': 'Kalamkari is a traditional hand-painting or block-printing technique from Andhra Pradesh and Telangana, using natural dyes to create intricate narrative designs on cotton or silk, often depicting mythological themes.',
                        'image_url': 'https://curatorscart.com/cdn/shop/files/hand-painted-blue-orange-red-kalamkari-wall-plate.jpg?v=1695364899'
                    },
                    'Puppetry': {
                        'description': 'Puppetry, particularly Kathputli from Rajasthan, is a traditional performing art using wooden puppets adorned with colorful costumes. These puppets are used to narrate folktales and historical stories through performances.',
                        'image_url': 'https://media.licdn.com/dms/image/v2/D5612AQH7Wryn-xzTog/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1726808503325?e=2147483647&v=beta&t=TO0eLlFZljF5niQfbkn5APvpMp9Ou4EXh4krCPu8kPg'
                    },
                    'Applique Work': {
                        'description': 'Applique Work, prominent in Gujarat and Odisha, involves stitching colorful fabric patches onto a base cloth to create vibrant patterns, often used for wall hangings, canopies, and traditional garments like Pipli applique.',
                        'image_url': 'https://www.utsavpedia.com/wp-content/uploads/2013/05/3429d5d3507b40c594d235c73e13a5c7.jpg'
                    },
                    'Muga Silk': {
                        'description': 'Muga Silk, exclusive to Assam, is a golden-yellow silk known for its natural luster and durability. Used in traditional Assamese attire, it is one of the costliest silks, prized for its cultural significance.',
                        'image_url': 'https://www.utsavpedia.com/wp-content/uploads/2013/06/Muga-Silk-Fabric3.jpg'
                    },
                    'Wood Carving': {
                        'description': 'Wood Carving is a traditional craft in states like Kerala and Karnataka, where artisans create detailed sculptures, furniture, and decorative panels, often featuring mythological figures and intricate floral patterns.',
                        'image_url': 'https://www.shutterstock.com/image-photo/wood-carving-tools-carpenters-hands-600nw-2403216529.jpg'
                    },
                    'Kani Shawl': {
                        'description': 'Kani Shawls from Jammu & Kashmir are woven with fine Pashmina wool using the twill-tapestry technique, featuring intricate multicolored patterns that reflect the region’s rich textile heritage.',
                        'image_url': 'https://www.pashwrap.com/cdn/shop/articles/Pashmina_Kani_Shawl.jpg?v=1697614181'
                    },
                    'Dhokra': {
                        'description': 'Dhokra is an ancient metal casting craft from Chhattisgarh and Odisha, using the lost-wax technique to create intricate brass figurines, jewelry, and decorative items with a rustic aesthetic.',
                        'image_url': 'https://i0.wp.com/utkalikaodisha.com/wp-content/uploads/2024/07/11.jpg?resize=600%2C600&ssl=1'
                    },
                    'Bagh Print': {
                        'description': 'Bagh Print is a traditional block-printing technique from Madhya Pradesh, using natural dyes and hand-carved wooden blocks to create vibrant geometric and floral patterns on cotton and silk fabrics.',
                        'image_url': 'https://s7ap1.scene7.com/is/image/incredibleindia/bagh-prints-of-madhya-pradesh-1-craft-body?qlt=82&ts=1726641261156'
                    },
                    'Kashida': {
                        'description': 'Kashida is an embroidery style from Jammu & Kashmir, featuring intricate thread work with floral and paisley motifs, often used to embellish shawls, sarees, and home furnishings.',
                        'image_url': 'https://i.pinimg.com/736x/03/3e/96/033e96a5f80ac0b85abf69de11346b02.jpg'
                    },
                    'Sujani': {
                        'description': 'Sujani is a traditional quilt-making craft from Bihar, where layers of old cloth are stitched together with colorful threads to create vibrant quilts and bedspreads, often depicting social themes.',
                        'image_url': 'https://akm-img-a-in.tosshub.com/indiatoday/images/story/202404/sujani-084407387-16x9_0.jpg?VersionId=LeAtqhxQCWQthiG.ezumwiO0IRl2rY3V'
                    },
                    'Marble Inlay': {
                        'description': 'Marble Inlay, practiced in Rajasthan, involves embedding semi-precious stones into marble to create intricate floral and geometric designs, commonly seen in tabletops and decorative items.',
                        'image_url': 'https://themarbleartstudio.com/wp-content/uploads/2022/08/Patten-Inlay-Work3.jpg'
                    },
                    'Kullu Shawl': {
                        'description': 'Kullu Shawls from Himachal Pradesh are handwoven woolen shawls known for their vibrant geometric patterns and bright colors, often used for warmth and cultural expression.',
                        'image_url': 'https://5.imimg.com/data5/SELLER/Default/2020/11/GW/DK/NO/117116792/kullu-shawls-500x500.jpg'
                    },
                    'Pithora Painting': {
                        'description': 'Pithora Painting is a ritualistic tribal art form from Gujarat, created by the Rathwa and Bhil tribes. These vibrant wall paintings depict mythological stories and are considered sacred.',
                        'image_url': 'https://www.memeraki.com/cdn/shop/articles/the-ritual-art-of-pithora-wall-paintings-420449_1200x1200.jpg?v=1661329608'
                    },
                    'Jute Craft': {
                        'description': 'Jute Craft, popular in West Bengal, involves creating eco-friendly products like bags, mats, and home decor using durable jute fibers, known for their sustainability and rustic appeal.',
                        'image_url': 'https://images-na.ssl-images-amazon.com/images/I/616PjMqbBpL.jpg'
                    },
                    'Shell Craft': {
                        'description': 'Shell Craft, practiced in coastal regions like Goa, uses seashells to create decorative items, jewelry, and home furnishings, showcasing intricate designs inspired by marine life.',
                        'image_url': 'https://i.pinimg.com/474x/62/93/1b/62931bb9db2d7ed6d20a355586896c04.jpg'
                    },
                    'Sohrai Painting': {
                        'description': 'Sohrai Painting is a tribal art form from Jharkhand, traditionally painted on mud walls during festivals. It features natural motifs like animals and plants, using earth-based colors.',
                        'image_url': 'https://dirumsbucket.blob.core.windows.net/dirumsbucket/download-2022.1.23_19.7.26-dirums-(dirums.com)/media/sohrai-painting-peacock-natural-color-on-handmade-paper-painting-for-living-room-office-worspace-dirums-frame-1.jpg'
                    },
                    'Leather Craft': {
                        'description': 'Leather Craft, prevalent in Andhra Pradesh and Rajasthan, involves creating durable goods like footwear, bags, and decorative items using embossed and dyed leather, often with intricate patterns.',
                        'image_url': 'https://www.truetridentleather.com/wp-content/uploads/2020/04/custom-leather-working.jpg'
                    }
                }
            
                if selected_craft in craft_info:
                    st.markdown(f"### {selected_craft}")
                    st.markdown(craft_info[selected_craft]['description'])
                    display_image_from_url(craft_info[selected_craft]['image_url'], f"{selected_craft}", width=400)
                else:
                    st.write(f"Information about {selected_craft} is not available.")
        
            st.markdown("<h2 class='sub-header'>Handicraft Distribution and Artisan Communities</h2>", unsafe_allow_html=True)
        
            fig = px.scatter(crafts_data, x='Annual_Revenue_Cr', y='Artisans_Count', 
                            color='State', size='Annual_Revenue_Cr', hover_name='Craft',
                            log_y=True, title='Handicrafts: Revenue vs Artisan Community Size')
            fig.update_layout(xaxis_title='Annual Revenue (₹ Crores)', yaxis_title='Number of Artisans')
            st.plotly_chart(fig, use_container_width=True)
        
            # Additional Visual: GI Registrations from CSV
            st.markdown("<h2 class='sub-header'>Geographical Indications (GI) for Crafts</h2>", unsafe_allow_html=True)
            if not gi_state_df.empty:
                fig_gi = px.bar(gi_state_df, x='State/UT', y='Total', color='State/UT',
                                title='GI Registrations by State (2014-2023)',
                                color_discrete_sequence=px.colors.qualitative.Set2)
                st.plotly_chart(fig_gi, use_container_width=True)
        
            st.markdown("""
            <div class='caption'>
            Source: Ministry of Textiles, Handicrafts Census data compiled from data.gov.in
            </div>
            """, unsafe_allow_html=True)
        
            st.markdown("<h3 class='section-header'>Crafts Marketing Initiatives</h3>", unsafe_allow_html=True)
        
            st.markdown("""
            Several government initiatives support the marketing and promotion of traditional handicrafts:
        
            1. **Dastkar Haat Samiti**: Organizing craft bazaars across India to provide direct market access to artisans
            2. **Crafts Council of India**: Promoting craft awareness and supporting artisans through workshops and exhibitions
            3. **Handicrafts Development Commissioner**: Implementing various marketing support schemes
            4. **Geographical Indication (GI) Tags**: Protecting traditional crafts and ensuring authenticity
            5. **e-Commerce Platforms**: Special initiatives to bring traditional handicrafts to online marketplaces
            """)

    # Cultural Heritage Sites
    elif page == "Cultural Heritage Sites":
        st.markdown("<h1 class='main-header'>Cultural Heritage Sites of India</h1>", unsafe_allow_html=True)
    
        st.markdown("""
        <div class='highlight-text'>
        India's rich history has bestowed upon it a wealth of cultural and historical sites, 
        from ancient temples and forts to colonial architecture and modern monuments.
        </div>
        """, unsafe_allow_html=True)
    
        site_category = st.tabs(["UNESCO World Heritage Sites", "Archaeological Monuments", "Living Heritage"])
    
        with site_category[0]:
            st.markdown("<h2 class='sub-header'>UNESCO World Heritage Sites in India</h2>", unsafe_allow_html=True)
        
            heritage_data = load_heritage_site_data()
        
            col1, col2 = st.columns([2, 1])
        
            with col1:
                heritage_types = heritage_data.groupby('Type').size().reset_index(name='Count')
            
                fig = px.bar(heritage_data.sort_values(by='Visitors_Annual', ascending=False).head(10), 
                             x='Site', y='Visitors_Annual', color='State',
                             title='Top 10 UNESCO World Heritage Sites by Annual Visitors')
                fig.update_layout(xaxis_title='Heritage Site', yaxis_title='Annual Visitors')
                st.plotly_chart(fig, use_container_width=True)
            
                fig = px.pie(heritage_types, names='Type', values='Count',
                           title='Distribution of UNESCO World Heritage Sites by Type')
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        
            with col2:
                selected_site = st.selectbox(
                    "Select a UNESCO World Heritage Site to learn more:",
                    heritage_data['Site'].tolist()
                )
            
                site_info = {
                    'Taj Mahal': {
                        'description': 'Built by Emperor Shah Jahan in memory of his beloved wife Mumtaz Mahal, the Taj Mahal is a masterpiece of Mughal architecture, combining elements from Persian, Ottoman Turkish, and Indian architectural styles.',
                        'image_url': 'https://static.toiimg.com/photo/62022874.cms',
                        'year': '1983',
                        'fact': 'The Taj Mahal changes its color subtly throughout the day, appearing pinkish in the morning, white during the day, and golden at night under moonlight.'
                    },
                    'Ajanta Caves': {
                        'description': 'The Ajanta Caves are 30 rock-cut Buddhist cave monuments dating from the 2nd century BCE to about 480 CE. The caves include paintings and sculptures considered to be masterpieces of Buddhist religious art.',
                        'image_url': 'https://cdn.getyourguide.com/img/tour/5b881032cf989.jpeg/146.jpg',
                        'year': '1983',
                        'fact': 'The Ajanta Caves were forgotten until 1819 when a British officer accidentally discovered them while hunting tigers.'
                    },
                    'Ellora Caves': {
                        'description': 'The Ellora Caves are a UNESCO World Heritage Site featuring Buddhist, Hindu and Jain cave temples and monasteries, built between the 6th and 10th century CE. The most remarkable is the Kailasa Temple, a huge monolithic structure carved out of a single rock.',
                        'image_url': 'https://www.worldhistory.org/img/c/p/1200x900/4565.jpg',
                        'year': '1983',
                        'fact': 'The Kailasa Temple at Ellora is carved out of a single rock, making it one of the largest monolithic structures in the world.'
                    },
                    'Agra Fort': {
                        'description': 'Agra Fort is a historical fort built by Akbar in 1565. It was the main residence of the emperors of the Mughal Dynasty until 1638 when the capital was shifted from Agra to Delhi.',
                        'image_url': 'https://www.holidify.com/images/cmsuploads/compressed/6799416268_822e8d98f5_b_20180814155943.jpg',
                        'year': '1983',
                        'fact': 'Shah Jahan, who built the Taj Mahal, was imprisoned by his son Aurangzeb in Agra Fort. He spent his last years gazing at the Taj Mahal from a window in the fort.'
                    },
                    'Khajuraho': {
                        'description': 'The Khajuraho Group of Monuments are a group of Hindu and Jain temples known for their nagara-style architectural symbolism and erotic sculptures. Built between 950 and 1050 by the Chandela dynasty, only about 20 temples remain from the original 85.',
                        'image_url': 'https://theindosphere.com/wp-content/uploads/2024/08/image-4.jpg',
                        'year': '1986',
                        'fact': 'Only about 10% of the sculptures at Khajuraho are erotic in nature, while the rest depict various aspects of everyday life and mythological narratives.'
                    },
                    'Fatehpur Sikri': {
                        'description': 'Fatehpur Sikri, built by Emperor Akbar in the late 16th century, served as the capital of the Mughal Empire for a short time. The city is an architectural masterpiece blending Persian, Indian, and Islamic influences.',
                        'image_url': 'https://www.raffaeleferrari.com/wp-content/uploads/2020/03/Fateh.jpg',
                        'year': '1986',
                        'fact': 'Fatehpur Sikri was abandoned shortly after its completion due to water scarcity in the region.'
                    },
                    'Mahabalipuram': {
                        'description': 'Mahabalipuram, also known as Mamallapuram, is famous for its rock-cut temples and sculptures created by the Pallava dynasty in the 7th and 8th centuries. The site features the Shore Temple and remarkable bas-relief carvings.',
                        'image_url': 'https://live.staticflickr.com/5654/23173189005_86a20afdf6_b.jpg',
                        'year': '1984',
                        'fact': 'The “Descent of the Ganges” sculpture at Mahabalipuram is one of the largest open-air rock reliefs in the world.'
                        },
                    'Kaziranga National Park': {
                        'description': 'Kaziranga National Park, located in Assam, is home to the largest population of the Indian one-horned rhinoceros. The park is a biodiversity hotspot and also shelters tigers, elephants, and a variety of bird species.',
                        'image_url': 'https://kaziranganationalparkassam.in/wp-content/uploads/2024/09/IMG_20240719_074806_954-2.jpg',
                        'year': '1985',
                        'fact': 'Kaziranga hosts over two-thirds of the world’s population of the Indian one-horned rhinoceros.'
                    },
                    'Qutub Minar': {
                        'description': 'Qutub Minar in Delhi is a 73-meter tall tower built in the early 13th century by Qutb-ud-din Aibak and his successors. It is a UNESCO World Heritage Site known for its intricate carvings and towering presence.',
                        'image_url': 'https://imgmediagumlet.lbb.in/media/2019/10/5d99cb588780ab0635aed883_1570360152711.jpg',
                        'year': '1993',
                        'fact': 'Qutub Minar is the tallest brick minaret in the world and has survived several earthquakes.'
                    },
                    'Jantar Mantar': {
                        'description': 'Jantar Mantar in Jaipur is an astronomical observatory built in the 18th century by Maharaja Jai Singh II. It features the world’s largest stone sundial and numerous instruments for measuring time, predicting eclipses, and tracking stars.',
                        'image_url': 'https://media.istockphoto.com/id/486396268/photo/historic-observatory.jpg?s=612x612&w=0&k=20&c=3D6GNFqEba-wnA4oLgelezGKSfl1FxOEYf_pU90B8qI=',
                        'year': '2010',
                        'fact': 'The instruments at Jantar Mantar are so large and precise that they can be used with the naked eye for accurate astronomical measurements.'
                    },
                    'Red Fort': {
                        'description': 'The Red Fort in Delhi was the main residence of the Mughal emperors for nearly 200 years. Built in 1648 by Shah Jahan, it is an outstanding example of Mughal architecture, combining Persian, Timurid, and Indian elements.',
                        'image_url': 'https://rukminim2.flixcart.com/image/850/1000/xif0q/poster/y/b/k/small-red-fort-poster-437-red-fort-poster-multicolor-photo-paper-original-imaghwgpmybwuu8e.jpeg?q=90&crop=false',
                        'year': '2007',
                        'fact': 'The Indian Prime Minister hoists the national flag at the Red Fort every Independence Day since 1947.'
                    },
                    'Humayun\'s Tomb': {
                        'description': 'Humayun’s Tomb in Delhi, built in 1572, is the first garden-tomb in the Indian subcontinent. It inspired several major architectural innovations, including the Taj Mahal.',
                        'image_url': 'https://cdn.britannica.com/57/91457-050-CEC85B47/Humayun-tomb-Delhi-India.jpg',
                        'year': '1993',
                        'fact': 'Humayun’s Tomb was the first structure in India to use red sandstone on such a grand scale.'
                    },
                    'Konark Sun Temple': {
                        'description': 'The Konark Sun Temple, built in the 13th century by King Narasimhadeva I of the Eastern Ganga dynasty, is designed in the shape of a colossal chariot with intricately carved stone wheels, pillars, and walls. It is dedicated to the Sun God, Surya.',
                        'image_url': 'https://media.istockphoto.com/id/96668487/photo/ancient-hindu-sun-temple-at-konark.jpg?s=612x612&w=0&k=20&c=tfjyAU_J1jmhxXTIu31E-6WcH3vcedUOhN-a2Z-YtCY=',
                        'year': '1984',
                        'fact': 'The temple’s 24 carved wheels are not just decorative — they also function as sundials.'
                    },
                    'Western Ghats': {
                        'description': 'The Western Ghats, also known as the Sahyadri Hills, is a mountain range along the western coast of India. It is one of the world’s eight “hottest hotspots” of biological diversity and includes numerous protected areas and endemic species.',
                        'image_url': 'https://plus.unsplash.com/premium_photo-1697730334419-fba83fe143b7?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8d2VzdGVybiUyMGdoYXRzfGVufDB8fDB8fHww',
                        'year': '2012',
                        'fact': 'The Western Ghats influence the Indian monsoon weather pattern and are older than the Himalayas.'
                    },
                    'Hampi': {
                        'description': 'Hampi, located in Karnataka, was the capital of the Vijayanagara Empire in the 14th century. The site is known for its well-preserved ruins, majestic temples like the Virupaksha Temple, and unique architecture blending Hindu and Islamic styles.',
                        'image_url': 'https://www.solitarytraveller.com/wp-content/uploads/2023/03/package_hampi_banner.jpg',
                        'year': '1986',
                        'fact': 'Hampi was once one of the richest cities in the world, attracting traders from Persia and Portugal.'
                    },
                    "Cellular Jail": {
                        "description": "Located in Port Blair, Andaman and Nicobar Islands, the Cellular Jail, also known as Kala Pani, was a colonial prison used by the British to exile political prisoners. It is now a national memorial showcasing India’s freedom struggle.",
                        "image_url": "https://s7ap1.scene7.com/is/image/incredibleindia/cellular-jail-port-blair-andaman-and-nicobar-islands-1-attr-hero?qlt=82&ts=1726816912863",
                        "year": "1998",
                        "fact": "The Cellular Jail had 698 cells designed to prevent communication between prisoners, symbolizing its role in isolating freedom fighters."
                    },
                    "Tirupati Temple": {
                        "description": "Sri Venkateswara Temple in Tirupati, Andhra Pradesh, is one of the most revered Hindu pilgrimage sites, dedicated to Lord Vishnu. It is renowned for its Dravidian architecture and massive devotee footfall.",
                        "image_url": "https://thefederal.com/file/2023/01/Tirupatitemple.jpg",
                        "year": "Not a UNESCO site",
                        "fact": "The temple is one of the richest religious institutions in the world, receiving millions of devotees and donations annually."
                    },
                    "Tawang Monastery": {
                        "description": "Located in Arunachal Pradesh, Tawang Monastery is the largest Buddhist monastery in India, founded in the 17th century. It is a significant spiritual center for Tibetan Buddhism.",
                        "image_url": "https://i.cdn.newsbytesapp.com/images/l33420241024094000.jpeg",
                        "year": "Not a UNESCO site",
                        "fact": "The monastery houses a 28-foot-high golden statue of Lord Buddha, making it a focal point for Buddhist pilgrims."
                    },
                    "Kamakhya Temple": {
                        "description": "Situated in Guwahati, Assam, the Kamakhya Temple is a major Shakti Peetha dedicated to Goddess Kamakhya. It is known for its unique tantric worship practices.",
                        "image_url": "https://s7ap1.scene7.com/is/image/incredibleindia/kamakhya-temple-dispur-assam-2-attr-hero?qlt=82&ts=1726741392778",
                        "year": "Not a UNESCO site",
                        "fact": "The temple hosts the annual Ambubachi Mela, attracting thousands to celebrate the goddess’s menstruation cycle."
                    },
                    "Mahabodhi Temple": {
                        "description": "Located in Bodh Gaya, Bihar, the Mahabodhi Temple marks the spot where Gautama Buddha attained enlightenment. It is a UNESCO World Heritage Site and a major Buddhist pilgrimage destination.",
                        "image_url": "https://s7ap1.scene7.com/is/image/incredibleindia/mahabodhi-temple-gaya-bihar-4-attr-hero?qlt=82&ts=1726740645749",
                        "year": "2002",
                        "fact": "The temple’s Bodhi Tree is a direct descendant of the original tree under which Buddha meditated."
                    },
                    "Rock Garden": {
                        "description": "The Rock Garden in Chandigarh, created by Nek Chand, is a unique sculpture garden made from recycled materials like ceramics, stones, and industrial waste, showcasing artistic ingenuity.",
                        "image_url": "https://www.gardendesign.com/pictures/images/650x490Exact_48x0/site_3/asian-style-rock-garden-rock-garden-with-blue-screen-garden-design_15639.jpg",
                        "year": "Not a UNESCO site",
                        "fact": "The garden spans 40 acres and was secretly built by Nek Chand over decades before being officially recognized."
                    },
                    "Chitrakoot Falls": {
                        "description": "Located in Chhattisgarh, Chitrakoot Falls is one of India’s widest waterfalls, often called the 'Niagara Falls of India,' surrounded by lush greenery.",
                        "image_url": "https://static.toiimg.com/photo/38796013.cms",
                        "year": "Not a UNESCO site",
                        "fact": "The falls are named after the nearby Chitrakoot, associated with Lord Rama’s exile in the Ramayana."
                    },
                    "Diu Fort": {
                        "description": "Built by the Portuguese in 1535, Diu Fort in Diu is a well-preserved coastal fortress, reflecting colonial architecture and strategic maritime history.",
                        "image_url": "https://makeithappen.co.in/wp-content/uploads/2021/12/Diu-Fort-G1-4.jpg",
                        "year": "Not a UNESCO site",
                        "fact": "The fort houses a lighthouse and cannons, offering panoramic views of the Arabian Sea."
                    },
                    "Basilica of Bom Jesus": {
                        "description": "Located in Goa, the Basilica of Bom Jesus is a UNESCO World Heritage Site famous for housing the mortal remains of St. Francis Xavier, showcasing Baroque architecture.",
                        "image_url": "https://cdn-iladmib.nitrocdn.com/htBCYuNetSQrkeDEiUPoyTCbyIlIyAQV/assets/images/optimized/rev-0efd0da/www.soultravelling.in/blog/wp-content/uploads/2024/12/4-6-1024x685.jpg",
                        "year": "1986",
                        "fact": "The body of St. Francis Xavier, preserved in the basilica, is displayed every 10 years during a public exposition."
                    },
                    "Somnath Temple": {
                        "description": "Located in Gujarat, the Somnath Temple is one of the twelve Jyotirlinga shrines of Lord Shiva, known for its historical significance and coastal location.",
                        "image_url": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0e/61/81/52/il-tempio.jpg?w=900&h=500&s=1",
                        "year": "Not a UNESCO site",
                        "fact": "The temple has been rebuilt multiple times after being destroyed by invaders, symbolizing resilience."
                    },
                    "Kurukshetra": {
                        "description": "Kurukshetra in Haryana is a historic city associated with the Mahabharata, known for its sacred sites like Jyotisar, where the Bhagavad Gita was delivered.",
                        "image_url": "https://static.toiimg.com/thumb/50366039,width-96,height-65.cms",
                        "year": "Not a UNESCO site",
                        "fact": "The city is believed to be the battlefield of the epic Mahabharata war between the Pandavas and Kauravas."
                    },
                    "Kullu Valley": {
                        "description": "Nestled in Himachal Pradesh, Kullu Valley is known for its scenic beauty, adventure sports, and vibrant Dussehra festival, surrounded by the Himalayas.",
                        "image_url": "https://i0.wp.com/traveltoyournature.com/wp-content/uploads/2023/10/nature-activities-with-views-in-Kullu-Valley-1024x768.jpg?resize=1024%2C768",
                        "year": "Not a UNESCO site",
                        "fact": "Kullu’s Dussehra festival is unique, celebrating Lord Raghunath with grand processions."
                    },
                    "Vaishno Devi Temple": {
                        "description": "Located in Katra, Jammu and Kashmir, the Vaishno Devi Temple is a major Hindu pilgrimage site dedicated to Goddess Vaishno Devi, situated in the Trikuta Mountains.",
                        "image_url": "https://thetempleguru.com/wp-content/uploads/2024/08/Vaishno-Devi-Temple-katra-jk-3.jpg",
                        "year": "Not a UNESCO site",
                        "fact": "Devotees trek 12 km to reach the cave shrine, which is one of India’s most visited pilgrimage sites."
                    },
                    "Betla National Park": {
                        "description": "Located in Jharkhand, Betla National Park is a tiger reserve known for its biodiversity, waterfalls, and historic forts amidst dense forests.",
                        "image_url": "https://site.outlookindia.com/traveller/wp-content/uploads/2017/06/jharkhand1_Betla-NP_FI.jpg",
                        "year": "Not a UNESCO site",
                        "fact": "The park is home to the 16th-century Betla Fort, adding historical significance to its natural beauty."
                    },
                    "Periyar National Park": {
                        "description": "Situated in Kerala, Periyar National Park is a biodiversity hotspot and tiger reserve, famous for its elephant and tiger populations and scenic Periyar Lake.",
                        "image_url": "https://www.periyarnationalparkonline.in/images/wildlife-wonders-periyar.jpg",
                        "year": "2010",
                        "fact": "The park’s lake, formed by the Mullaperiyar Dam, offers unique boat safaris for wildlife viewing."
                    },
                    "Leh Palace": {
                        "description": "Located in Ladakh, Leh Palace is a 17th-century royal palace built in Tibetan architectural style, offering panoramic views of the Himalayas.",
                        "image_url": "https://www.go2ladakh.in/img/shared/gallery/28a3d6951d94be8c08426de8da80e78b.jpg",
                        "year": "Not a UNESCO site",
                        "fact": "The palace, resembling a smaller Potala Palace, was once home to the Namgyal dynasty."
                    },
                    "Agatti Island": {
                        "description": "Part of Lakshadweep, Agatti Island is known for its coral reefs, turquoise lagoons, and pristine beaches, making it a paradise for water sports and marine life enthusiasts.",
                        "image_url": "https://static.tripzilla.in/media/51542/conversions/df4b93dd-5f80-4e21-a4fa-e7d530506ed1-w768.webp",
                        "year": "Not a UNESCO site",
                        "fact": "Agatti has one of the few airports in Lakshadweep, serving as a gateway to the islands."
                    },
                    "Khajuraho Temples": {
                        "description": "The Khajuraho Temples in Madhya Pradesh, a UNESCO World Heritage Site, are renowned for their intricate erotic carvings and Nagara-style architecture, built between 950-1050 CE.",
                        "image_url": "https://www.holidify.com/images/cmsuploads/compressed/shutterstock_1032564361_20200219140048.jpg",
                        "year": "1986",
                        "fact": "Only about 20 of the original 85 temples remain, showcasing exquisite medieval Indian art."
                    },
                    "Loktak Lake": {
                        "description": "Located in Manipur, Loktak Lake is the largest freshwater lake in Northeast India, famous for its floating phumdis (vegetation islands) and Keibul Lamjao National Park.",
                        "image_url": "https://www.savaari.com/blog/wp-content/uploads/2022/12/loktak-lake-in-india.jpg",
                        "year": "Not a UNESCO site",
                        "fact": "Keibul Lamjao, on the lake, is the world’s only floating national park, home to the endangered Sangai deer."
                    },
                    "Living Root Bridges": {
                        "description": "Found in Meghalaya, the Living Root Bridges are hand-crafted by the Khasi and Jaintia tribes using the roots of rubber trees, creating sustainable natural bridges.",
                        "image_url": "https://faw-marketing.transforms.svdcdn.com/production/images/A-living-root-bridge.jpg?w=600&h=400&q=80&auto=format&fit=crop&crop=focalpoint&fp-x=0.5&fp-y=0.5&dm=1542707094&s=a6f7365df9bdffff06bce06f32310013",
                        "year": "Not a UNESCO site",
                        "fact": "The double-decker root bridge in Nongriat is one of the most iconic, taking decades to grow."
                    },
                    "Vantawng Falls": {
                        "description": "Located in Mizoram, Vantawng Falls is the state’s highest waterfall, cascading through lush forests and offering breathtaking views.",
                        "image_url": "https://cdn.tripuntold.com/media/photos/location/2018/08/14/fbd0dbd7-7cdc-4f46-8394-e97485dab7dc.jpg",
                        "year": "Not a UNESCO site",
                        "fact": "The falls are named after Vantawnga, a legendary Mizo hunter who discovered them."
                    },
                    "Kohima War Cemetery": {
                        "description": "In Kohima, Nagaland, this cemetery commemorates Allied soldiers who died in the 1944 Battle of Kohima, a turning point in World War II.",
                        "image_url": "https://travelsetu.com/apps/uploads/new_destinations_photos/destination/2024/01/18/e6b0b1fd4bb207ec797bc528045e21b2_1000x1000.jpg",
                        "year": "Not a UNESCO site",
                        "fact": "The cemetery’s epitaph reads, ‘When you go home, tell them of us and say, for your tomorrow, we gave our today.’"
                    },
                    "Auroville": {
                        "description": "Located in Puducherry, Auroville is an experimental township founded in 1968, aiming to be a universal community based on peace and human unity, centered around the Matrimandir.",
                        "image_url": "https://static.toiimg.com/thumb/99391984/Matrimandir-in-Puducherry.jpg?width=1200&height=900",
                        "year": "Not a UNESCO site",
                        "fact": "The Matrimandir, a golden spherical meditation center, is Auroville’s spiritual and architectural highlight."
                    },
                    "Golden Temple": {
                        "description": "Located in Amritsar, Punjab, the Golden Temple (Harmandir Sahib) is the holiest Sikh shrine, known for its stunning golden architecture and communal kitchen serving free meals.",
                        "image_url": "https://www.whyweseek.com/wp-content/uploads/2020/01/facebook-amritsar.jpg",
                        "year": "Not a UNESCO site",
                        "fact": "The temple’s langar serves up to 100,000 meals daily, open to all regardless of faith or status."
                    },
                    "Amber Fort": {
                        "description": "Situated in Jaipur, Rajasthan, Amber Fort is a majestic hilltop fortress known for its Rajput architecture, intricate mirror work, and stunning views.",
                        "image_url": "https://www.rajasthanbhumitours.com/blog/wp-content/uploads/2024/08/Amber-Fort-and-Palace-The-Guardian-of-Rajput-Glory.jpg",
                        "year": "2013",
                        "fact": "The fort’s Sheesh Mahal features thousands of tiny mirrors, creating a dazzling effect when lit."
                    },
                    "Rumtek Monastery": {
                        "description": "Located in Sikkim, Rumtek Monastery is a key center for Tibetan Buddhism, known for its traditional architecture and as the seat of the Karmapa.",
                        "image_url": "https://www.elginhotels.com/wp-content/uploads/2020/03/rumtek-monastery-01.jpg.webp",
                        "year": "Not a UNESCO site",
                        "fact": "The monastery houses rare Buddhist relics, including a golden stupa containing the remains of the 16th Karmapa."
                    },
                    "Meenakshi Temple": {
                        "description": "Located in Madurai, Tamil Nadu, the Meenakshi Temple is a historic Dravidian temple dedicated to Goddess Meenakshi and Lord Sundareswarar, famous for its towering gopurams.",
                        "image_url": "https://thrillingtravel.in/wp-content/uploads/2018/02/Golden-Lotus-Pond-at-Meenakshi-Temple.jpg",
                        "year": "Not a UNESCO site",
                        "fact": "The temple’s 14 gopurams are adorned with over 33,000 sculptures, showcasing intricate craftsmanship."
                    },
                    "Charminar": {
                        "description": "Built in 1591 in Hyderabad, Telangana, the Charminar is an iconic monument and mosque, known for its four minarets and vibrant surrounding markets.",
                        "image_url": "https://media1.thrillophilia.com/filestore/3g77vc5tt9qxuuorsmeudjjscqtu_Charminar.jpg?w=400&dpr=2",
                        "year": "Not a UNESCO site",
                        "fact": "The Charminar was built to commemorate the end of a deadly plague in Hyderabad."
                    },
                    "Ujjayantha Palace": {
                        "description": "Located in Agartala, Tripura, Ujjayantha Palace is a 19th-century royal palace, now a museum, showcasing the history and culture of Tripura.",
                        "image_url": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/17/9f/9b/ef/img-20190308-132059-largejpg.jpg?w=900&h=500&s=1",
                        "year": "Not a UNESCO site",
                        "fact": "The palace was named by Rabindranath Tagore, who was a frequent visitor."
                    },
                    "Valley of Flowers": {
                        "description": "Located in Uttarakhand, the Valley of Flowers is a UNESCO World Heritage Site known for its vibrant alpine meadows and rare flora, nestled in the Himalayas.",
                        "image_url": "https://www.holidify.com/images/bgImages/VALLEY-OF-FLOWERS.jpg",
                        "year": "2005",
                        "fact": "The valley is home to over 500 species of wildflowers, blooming vividly during the monsoon season."
                    },
                    "Victoria Memorial": {
                        "description": "Located in Kolkata, West Bengal, the Victoria Memorial is a grand marble monument built in memory of Queen Victoria, now a museum showcasing colonial history.",
                        "image_url": "https://images.unsplash.com/photo-1558431382-9b06d0507edc?ixid=MnwzODM4MzZ8MHwxfGFsbHx8fHx8fHx8fDE2NzAxNjMwNTg&ixlib=rb-4.0.3&fm=jpg&q=85&fit=crop&w=2560&h=1920",
                        "year": "Not a UNESCO site",
                        "fact": "The memorial houses a vast collection of artifacts, including paintings and manuscripts from the British Raj era."
                    }
                }
            
                if selected_site in site_info:
                    st.markdown(f"### {selected_site}")
                    site_data = heritage_data[heritage_data['Site'] == selected_site].iloc[0]
                    st.markdown(f"**Location:** {site_data['State']}")
                    st.markdown(f"**Year Inscribed:** {site_data['Year_Inscribed']}")
                    st.markdown(f"**Annual Visitors:** {site_data['Visitors_Annual']:,}")
                
                    st.markdown(site_info[selected_site]['description'])
                    st.markdown(f"**Interesting Fact:** {site_info[selected_site]['fact']}")
                
                    display_image_from_url(site_info[selected_site]['image_url'], f"{selected_site}", width=400)
                else:
                    site_data = heritage_data[heritage_data['Site'] == selected_site].iloc[0]
                    st.markdown(f"### {selected_site}")
                    st.markdown(f"**Location:** {site_data['State']}")
                    st.markdown(f"**Year Inscribed:** {site_data['Year_Inscribed']}")
                    st.markdown(f"**Annual Visitors:** {site_data['Visitors_Annual']:,}")
                    st.write(f"Detailed information about {selected_site} is not available.")
        
            st.markdown("<h2 class='sub-header'>Geographical Distribution of UNESCO Heritage Sites</h2>", unsafe_allow_html=True)
        
            m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles='cartodbpositron')
            marker_cluster = MarkerCluster().add_to(m)
        
            for _, row in heritage_data.iterrows():
                popup_content = f"""
                <b>{row['Site']}</b><br>
                State: {row['State']}<br>
                Year Inscribed: {row['Year_Inscribed']}<br>
                Visitors: {row['Visitors_Annual']:,}<br>
                Type: {row['Type']}
                """
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=folium.Popup(popup_content, max_width=300),
                    tooltip=row['Site'],
                    icon=folium.Icon(color='blue', icon='landmark', prefix='fa')
                ).add_to(marker_cluster)
        
            map_html = m._repr_html_()
            components.html(map_html, height=600)
    
        with site_category[1]:
            st.markdown("<h2 class='sub-header'>Archaeological Monuments and Sites</h2>", unsafe_allow_html=True)
        
            monuments_data = load_monuments_data()
        
            col1, col2 = st.columns([2, 1])
        
            with col1:
                fig = px.bar(monuments_data.sort_values(by='No_of_Monuments', ascending=False).head(10), 
                             x='State/UT', y='No_of_Monuments', color='State/UT',
                             title='Top 10 States by Number of ASI-Protected Monuments')
                fig.update_layout(xaxis_title='State/UT', yaxis_title='Number of Monuments')
                st.plotly_chart(fig, use_container_width=True)
        
            with col2:
                st.markdown("""
                <div class='container'>
                The Archaeological Survey of India (ASI) maintains 3,691 protected monuments and sites across the country. 
                These include temples, mosques, forts, tombs, and other historical structures, showcasing India's architectural diversity.
                </div>
                """, unsafe_allow_html=True)
            
                selected_state = st.selectbox(
                    "Select a State/UT to view monument count:",
                    monuments_data['State/UT'].tolist()
                )
            
                state_data = monuments_data[monuments_data['State/UT'] == selected_state].iloc[0]
                st.markdown(f"**{selected_state}** has **{state_data['No_of_Monuments']}** ASI-protected monuments.")
            
            # Additional Visual: Monument Distribution from CSV
            st.markdown("<h2 class='sub-header'>Monument Distribution from ASI Data</h2>", unsafe_allow_html=True)
            if not monuments_df.empty:
                fig_treemap = px.treemap(monuments_df, path=['State/UT'], values='No_of_Monuments',
                                         title="State-wise Monument Distribution (ASI Data)",
                                         color='No_of_Monuments', color_continuous_scale='Oranges')
                st.plotly_chart(fig_treemap, use_container_width=True)
    
        with site_category[2]:
            st.markdown("<h2 class='sub-header'>Living Heritage and Cultural Practices</h2>", unsafe_allow_html=True)
        
            st.markdown("""
            <div class='container'>
            India's living heritage includes vibrant traditions such as festivals, rituals, and community practices 
            that continue to thrive. These intangible cultural heritages are preserved through generations and celebrated widely.
            </div>
            """, unsafe_allow_html=True)
        
            living_heritage = {
                'Practice': ['Yoga', 'Ayurveda', 'Vedic Chanting', 'Kumbh Mela', 'Navratri'],
                'Region': ['Nationwide', 'Nationwide', 'Nationwide', 'Uttar Pradesh/Uttarakhand', 'Gujarat'],
                'UNESCO_Inscribed': ['2016', 'Not Inscribed', '2008', '2017', 'Not Inscribed'],
                'Practitioners_Estimate': [50000000, 2000000, 100000, 50000000, 10000000]
            }
        
            living_df = pd.DataFrame(living_heritage)
        
            fig = px.bar(living_df, x='Practice', y='Practitioners_Estimate', color='Region',
                         title='Major Living Heritage Practices by Practitioners')
            fig.update_layout(xaxis_title='Cultural Practice', yaxis_title='Estimated Practitioners')
            st.plotly_chart(fig, use_container_width=True)
        
            st.markdown("""
            <div class='caption'>
            Source: UNESCO Intangible Cultural Heritage List and Cultural Reports
            </div>
            """, unsafe_allow_html=True)

    # Tourism Analytics Page
    elif page == "Tourism Analytics":
        st.markdown("<h1 class='main-header'>Tourism Analytics</h1>", unsafe_allow_html=True)
    
        st.markdown("""
        <div class='highlight-text'>
        Explore domestic and foreign tourism trends across India, including seasonal patterns and 
        the impact of tourism on local economies.
        </div>
        """, unsafe_allow_html=True)
    
        tourism_tabs = st.tabs(["Foreign Tourism", "Domestic Tourism", "Seasonal Patterns"])
    
        with tourism_tabs[0]:
            st.markdown("<h2 class='sub-header'>Foreign Tourist Visits (2022)</h2>", unsafe_allow_html=True)
        
            foreign_tourism = load_tourism_data()
        
            col1, col2 = st.columns([2, 1])
        
            with col1:
                fig = px.bar(foreign_tourism.sort_values(by='FTV_2022', ascending=False).head(10), 
                             x='State/UT', y='FTV_2022', color='Percentage_Share_2022',
                             title='Top 10 States by Foreign Tourist Visits (2022)')
                fig.update_layout(xaxis_title='State/UT', yaxis_title='Foreign Tourist Visits')
                st.plotly_chart(fig, use_container_width=True)
        
            with col2:
                st.markdown("""
                <div class='container'>
                Foreign tourism is a significant contributor to India's economy, with states like Tamil Nadu, 
                Maharashtra, and Uttar Pradesh attracting the most visitors due to their rich cultural heritage.
                </div>
                """, unsafe_allow_html=True)
            
                selected_state = st.selectbox(
                    "Select a State/UT to view details:",
                    foreign_tourism['State/UT'].tolist()
                )
            
                state_data = foreign_tourism[foreign_tourism['State/UT'] == selected_state].iloc[0]
                st.markdown(f"**{selected_state}**")
                st.markdown(f"- Foreign Tourist Visits (2022): **{state_data['FTV_2022']:,}**")
                st.markdown(f"- Percentage Share: **{state_data['Percentage_Share_2022']}%**")
        
            # Additional Visual: Visitor Trends from CSV
            st.markdown("<h2 class='sub-header'>Foreign Visitor Trends (2019-2021)</h2>", unsafe_allow_html=True)
            if not visitors_df.empty:
                fig_visitors = px.bar(visitors_df, x='State/UT', y='2021 - FTVs', color='State/UT',
                                      title='Foreign Tourist Visits by State (2021)',
                                      color_discrete_sequence=px.colors.qualitative.Set2)
                st.plotly_chart(fig_visitors, use_container_width=True)
    
        with tourism_tabs[1]:
            st.markdown("<h2 class='sub-header'>Domestic Tourist Visits (2022)</h2>", unsafe_allow_html=True)
        
            domestic_tourism = load_domestic_tourism_data()
        
            col1, col2 = st.columns([2, 1])
        
            with col1:
                fig = px.bar(domestic_tourism.sort_values(by='DTV_2022_millions', ascending=False).head(10), 
                             x='State/UT', y='DTV_2022_millions', color='Percentage_Share_2022',
                             title='Top 10 States by Domestic Tourist Visits (2022, millions)')
                fig.update_layout(xaxis_title='State/UT', yaxis_title='Domestic Tourist Visits (millions)')
                st.plotly_chart(fig, use_container_width=True)
        
            with col2:
                st.markdown("""
                <div class='container'>
                Domestic tourism reflects India's cultural vibrancy, with millions visiting religious, historical, 
                and natural sites annually.
                </div>
                """, unsafe_allow_html=True)
            
                selected_state = st.selectbox(
                    "Select a State/UT to view details:",
                    domestic_tourism['State/UT'].tolist()
                )
            
                state_data = domestic_tourism[domestic_tourism['State/UT'] == selected_state].iloc[0]
                st.markdown(f"**{selected_state}**")
                st.markdown(f"- Domestic Tourist Visits (2022): **{state_data['DTV_2022_millions']:.2f} million**")
                st.markdown(f"- Percentage Share: **{state_data['Percentage_Share_2022']}%**")
        
            # Additional Visual: Domestic Visitor Trends from CSV
            st.markdown("<h2 class='sub-header'>Domestic Visitor Trends (2019-2021)</h2>", unsafe_allow_html=True)
            if not visitors_df.empty:
                fig_visitors = px.bar(visitors_df, x='State/UT', y='2021 - DTVs', color='State/UT',
                                      title='Domestic Tourist Visits by State (2021)',
                                      color_discrete_sequence=px.colors.qualitative.Set2)
                st.plotly_chart(fig_visitors, use_container_width=True)
    
        with tourism_tabs[2]:
            st.markdown("<h2 class='sub-header'>Seasonal Tourism Patterns</h2>", unsafe_allow_html=True)
        
            seasonal_data = load_seasonal_tourism_data()
        
            fig = px.line(seasonal_data, x='Month', y='Tourism_Index', color='Region',
                          title='Seasonal Tourism Index by Region (2022)')
            fig.update_layout(xaxis_title='Month', yaxis_title='Tourism Index')
            st.plotly_chart(fig, use_container_width=True)
        
            st.markdown("""
            <div class='container'>
            The tourism index reflects the relative popularity of different regions throughout the year. 
            North and West India see peak tourism in winter months (Oct-Dec), while South India remains 
            a consistent destination year-round.
            </div>
            """, unsafe_allow_html=True)
        
            selected_region = st.selectbox(
                "Select a region to view peak months:",
                seasonal_data['Region'].unique()
            )
        
            region_data = seasonal_data[seasonal_data['Region'] == selected_region]
            peak_month = region_data.loc[region_data['Tourism_Index'].idxmax(), 'Month']
            st.markdown(f"**Peak Tourism Month for {selected_region}: {peak_month}**")

    # Responsible Tourism Page
    elif page == "Responsible Tourism":
        st.markdown("<h1 class='main-header'>Responsible Tourism in India</h1>", unsafe_allow_html=True)
    
        st.markdown("""
        <div class='highlight-text'>
        Responsible tourism aims to preserve cultural heritage, support local communities, and promote sustainable practices. 
        Explore how Indian states are leading in this area.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<h3> Major Tourist Places </h3>" , unsafe_allow_html = True)
        components.html(create_responsible_tourism_swiper(), height=500)
    
        rt_data = load_responsible_tourism_data()
    
        col1, col2 = st.columns([2, 1])
    
        with col1:
            fig = px.bar(rt_data.sort_values(by='Overall_RT_Score', ascending=False), 
                         x='State', y='Overall_RT_Score', color='State',
                         title='Top States by Responsible Tourism Score')
            fig.update_layout(xaxis_title='State', yaxis_title='Overall Responsible Tourism Score')
            st.plotly_chart(fig, use_container_width=True)
        
            fig = px.scatter(rt_data, 
                             x='Eco_Tourism_Score', 
                             y='Community_Involvement', 
                             size='Sustainable_Practices', 
                             color='State',
                             hover_name='State',
                             title='Responsible Tourism Metrics by State')
            fig.update_layout(xaxis_title='Eco-Tourism Score', yaxis_title='Community Involvement Score')
            st.plotly_chart(fig, use_container_width=True)
    
        with col2:
            selected_state = st.selectbox(
                "Select a State to view details:",
                rt_data['State'].tolist()
            )
        
            state_data = rt_data[rt_data['State'] == selected_state].iloc[0]
            st.markdown(f"**{selected_state}**")
            st.markdown(f"- Eco-Tourism Score: **{state_data['Eco_Tourism_Score']}**")
            st.markdown(f"- Community Involvement: **{state_data['Community_Involvement']}**")
            st.markdown(f"- Sustainable Practices: **{state_data['Sustainable_Practices']}**")
            st.markdown(f"- Cultural Preservation: **{state_data['Cultural_Preservation']}**")
            st.markdown(f"- Overall Score: **{state_data['Overall_RT_Score']}**")
        
            st.markdown("""
            <div class='container'>
            Responsible tourism in India emphasizes eco-friendly practices, community engagement, and cultural preservation. 
            States like Kerala and Sikkim lead due to their focus on sustainable tourism models.
            </div>
            """, unsafe_allow_html=True)

    # Cultural Events Calendar Page
    elif page == "Cultural Events Calendar":
        st.markdown("<h1 class='main-header'>Cultural Events Calendar</h1>", unsafe_allow_html=True)
    
        st.markdown("""
        <div class='highlight-text'>
        India's cultural calendar is filled with vibrant festivals and events that attract millions of visitors. 
        Explore major cultural events and plan your visit.
        </div>
        """, unsafe_allow_html=True)
    
        events_data = load_cultural_events_data()
    
        col1, col2 = st.columns([2, 1])
    
        with col1:
            fig = px.bar(events_data.sort_values(by='Visitors_Estimate', ascending=False).head(10), 
                         x='Event', y='Visitors_Estimate', color='State',
                         title='Top 10 Cultural Events by Estimated Visitors')
            fig.update_layout(xaxis_title='Event', yaxis_title='Estimated Visitors')
            st.plotly_chart(fig, use_container_width=True)
        
            fig = px.scatter(events_data, x='Cultural_Significance', y='Visitors_Estimate', 
                            color='State', size='Visitors_Estimate', hover_name='Event',
                            title='Cultural Events: Significance vs Visitors')
            fig.update_layout(xaxis_title='Cultural Significance', yaxis_title='Estimated Visitors')
            st.plotly_chart(fig, use_container_width=True)
    
        with col2:
            selected_event = st.selectbox(
                "Select an event to learn more:",
                events_data['Event'].tolist()
            )

            event_info = {
				'Kumbh Mela': {
						'description': 'The Kumbh Mela is a major Hindu pilgrimage and festival held every 12 years at four sacred river-bank locations. It is the world’s largest religious gathering, attracting millions of devotees.',
						'image_url': 'https://images.theconversation.com/files/642200/original/file-20250114-15-oucsvl.jpg?ixlib=rb-4.1.0&rect=0%2C85%2C4063%2C2031&q=45&auto=format&w=1356&h=668&fit=crop'
				},
				'Pushkar Camel Fair': {
						'description': 'The Pushkar Camel Fair is an annual livestock fair held in Pushkar, Rajasthan, featuring camel trading, cultural performances, and religious ceremonies.',
						'image_url': 'https://blog.dookinternational.com/wp-content/uploads/2017/06/a24.jpg'
				},
				'Rann Utsav': {
						'description': 'Rann Utsav is a cultural festival held in the Great Rann of Kutch, Gujarat, showcasing traditional crafts, folk music, and dance under the full moon in the white salt desert.',
						'image_url': 'https://c.ndtvimg.com/2024-10/beukk88_rann-utsav_625x300_23_October_24.jpg?im=FaceCrop,algorithm=dnn,width=545,height=307'
				},
				'Hornbill Festival': {
						'description': 'The Hornbill Festival in Nagaland is a vibrant celebration of Naga culture, featuring traditional dances, indigenous games, and tribal crafts, uniting all Naga tribes.',
						'image_url': 'https://img.theweek.in/content/dam/week/week/news/tourism/images/2024/11/30/hornbill-file-photo.jpg'
				},
				'Onam': {
						'description': 'Onam is a harvest festival in Kerala, marked by floral decorations, traditional feasts, snake boat races, and the mythical return of King Mahabali.',
						'image_url': 'https://currentaffairs.adda247.com/wp-content/uploads/multisite/sites/5/2021/08/23081756/Onam-Celebration-in-Kerala-1024x660-1.jpg'
				},
				'Durga Puja': {
						'description': 'Durga Puja is a major Hindu festival in West Bengal, celebrating the victory of Goddess Durga over Mahishasura, with elaborate pandals, idol immersions, and cultural performances.',
						'image_url': 'https://surojitpalmal.com/wp-content/uploads/2023/10/Best-Durga-Puja-in-Hyderabad.webp'
				},
				'Diwali in Varanasi': {
						'description': 'Diwali in Varanasi is a spectacular celebration with thousands of oil lamps lighting up the ghats, fireworks, and devotional music, symbolizing the victory of light over darkness.',
						'image_url': 'https://www.nativeplanet.com/img/2023/09/illuminated-city-of-varanasi-during-the-divine-festival-of-dev-diwali_1695797197486-1200x675-20230927122601.jpg'
				},
				'Hemis Festival': {
						'description': 'The Hemis Festival in Ladakh commemorates the birth of Guru Padmasambhava with vibrant masked dances, traditional music, and Buddhist rituals at the Hemis Monastery.',
						'image_url': 'https://images.indianexpress.com/2023/06/hemis-new.png'
				},
				'Holi in Mathura': {
						'description': 'Holi in Mathura, the birthplace of Lord Krishna, is a vibrant festival of colors with temple rituals, folk songs, and playful throwing of colored powders.',
						'image_url': 'https://clubmahindra.gumlet.io/blog/media/section_images/holifestiv-a5b10b7c01f70d2.jpg?w=376&dpr=2.6'
				},
				'Pongal': {
						'description': 'Pongal is a Tamil harvest festival dedicated to the Sun God, marked by cooking a special rice dish, traditional dances, and cattle worship over four days.',
						'image_url': 'https://cdn.shopify.com/s/files/1/0525/5285/9819/files/4_2_1024x1024.jpg?v=1734523615'
				},
				'Bihu': {
						'description': 'Bihu is Assam’s harvest festival, celebrated with vigorous Bihu dances, traditional music, and feasts, marking the Assamese New Year and agricultural cycles.',
						'image_url': 'https://media.istockphoto.com/id/1482254684/photo/rongali-bihu-festival.jpg?s=612x612&w=0&k=20&c=OKRcAAc6HMqMluMBQFQmPypo5uZZ_AO6xIVkI-TV6Pw='
				},
				'Ganesh Chaturthi': {
						'description': 'Ganesh Chaturthi in Maharashtra celebrates Lord Ganesha’s birth with grand idol installations, prayers, and processions, culminating in idol immersions.',
						'image_url': 'https://images.mid-day.com/images/images/2022/aug/Ganesh-Chaturthi-Mumbai.jpg'
				},
				'Navratri': {
						'description': 'Navratri is a nine-night Hindu festival celebrating Goddess Durga, with Garba and Dandiya dances in Gujarat, fasting, and vibrant worship across India.',
						'image_url': 'https://www.travelandtourworld.com/wp-content/uploads/2024/09/pikaso_texttoimage_Navratri-Fest.jpg'
				},
				'Jaipur Literature Festival': {
						'description': 'The Jaipur Literature Festival in Rajasthan is the world’s largest free literary festival, attracting global authors, poets, and intellectuals for discussions and cultural events.',
						'image_url': 'https://akm-img-a-in.tosshub.com/indiatoday/images/story/201601/jaipur-lit-fest_647_012016104450.jpg?VersionId=smUFj19HBJPNugmvaxtHMaTxb_1tVQeh'
				},
				'Khajuraho Dance Festival': {
						'description': 'The Khajuraho Dance Festival in Madhya Pradesh showcases classical Indian dance forms against the backdrop of the Khajuraho temples, celebrating India’s performing arts heritage.',
						'image_url': 'https://www.theweek.in/content/dam/week/news/entertainment/images/2023/2/19/khajuraho-dance-fest.jpg.transform/schema-1x1/image.jpg'
				},
				'Thrissur Pooram': {
						'description': 'Thrissur Pooram is a vibrant Hindu temple festival in Kerala, known for its spectacular elephant processions, traditional music, and fireworks, held at the Vadakkunnathan Temple.',
						'image_url': 'https://thrissurpooramfestival.com/engine1/bnr_img/bnr01.jpg'
				},
				'Baisakhi': {
						'description': 'Baisakhi is a harvest festival celebrated in Punjab, marking the Sikh New Year with vibrant processions, traditional dances like Bhangra, and communal feasts.',
						'image_url': 'https://static.toiimg.com/thumb/msid-90802194,width-1280,height-720,imgsize-178800,resizemode-6,overlay-toi_sw,pt-32,y_pad-40/photo.jpg'
				},
				'Chhath Puja': {
						'description': 'Chhath Pooja is a Hindu festival primarily in Bihar, dedicated to the Sun God, involving rituals, fasting, and offerings at riverbanks over four days.',
						'image_url': 'https://121clicks.com/wp-content/uploads/2017/11/chhath_puja_mass_prayer_to_the_sun_photo_story_121_clicks_arup_biswas_27.jpg'
				},
				'Teej': {
						'description': 'Teej is a women-centric festival celebrated in Rajasthan and other northern states, marked by fasting, colorful attire, and traditional dances to honor Goddess Parvati.',
						'image_url': 'https://s7ap1.scene7.com/is/image/incredibleindia/teej%20festival-1-regional-fes-hero?qlt=82&ts=1726639479648'
				},
				'Losar': {
						'description': 'Losar is the Tibetan New Year celebrated in Ladakh with Buddhist rituals, vibrant dances, and feasts, marking the beginning of the lunar calendar.',
						'image_url': 'https://i0.wp.com/www.tusktravel.com/blog/wp-content/uploads/2021/02/Losar-Festival-Ladakh.jpg?fit=1024%2C683&ssl=1'
				},
				'Goa Carnival': {
						'description': 'Goa Carnival is a lively pre-Lenten festival in Goa, featuring colorful parades, street dancing, and vibrant costumes, reflecting Portuguese cultural influences.',
						'image_url': 'https://static.toiimg.com/photo/62649959.cms'
				},
				'Torgya Festival': {
						'description': 'Torgya Festival in Arunachal Pradesh is a monastic festival at Tawang Monastery, featuring ritualistic dances to ward off evil spirits and promote prosperity.',
						'image_url': 'https://currentaffairs.adda247.com/wp-content/uploads/multisite/sites/5/2022/02/03080344/arunachal-festival-01.jpg'
				},
				'Sangai Festival': {
						'description': 'Sangai Festival in Manipur showcases the state’s cultural heritage with traditional dances, indigenous sports, and crafts, named after the endangered Sangai deer.',
						'image_url': 'https://static2.tripoto.com/media/filter/tst/img/172710/TripDocument/1542010952_sangai_41.jpg'
				},
				'Konark Dance Festival': {
						'description': 'Konark Dance Festival in Odisha celebrates classical Indian dance forms like Odissi and Bharatanatyam, set against the backdrop of the historic Konark Sun Temple.',
						'image_url': 'https://odishatourism.gov.in/content/dam/tourism/home/upcoming-events/konark_dance_festival/stb/img1.jpg'
				},
				'Makar Sankranti': {
						'description': 'Makar Sankranti is a harvest festival celebrated across India, marking the sun’s transition into Capricorn with kite flying, bonfires, and traditional sweets.',
						'image_url': 'https://www.stmarys-school.in/wp-content/uploads/2023/01/1-1.jpg'
				},
				'Vishu': {
						'description': 'Vishu is the Malayalam New Year in Kerala, celebrated with traditional rituals, Vishukkani arrangements, and feasts to mark prosperity and new beginnings.',
						'image_url': 'https://cdn.pixabay.com/photo/2022/01/27/06/35/happy-vishu-6971252_960_720.jpg'
				},
				'Bathukamma': {
						'description': 'Bathukamma is a floral festival in Telangana, where women create vibrant flower arrangements and sing folk songs to honor Goddess Gauri.',
						'image_url': 'https://www.sakshi.com/gallery_images/2023/10/13/bathukamma%20celebrations%20in%20hyderabad-1.jpg'
				},
				'Wangala Festival': {
						'description': 'Wangala Festival in Meghalaya is a harvest celebration of the Garo tribe, featuring traditional drum beating, dances, and offerings to the Sun God.',
						'image_url': 'https://i0.wp.com/www.tusktravel.com/blog/wp-content/uploads/2023/11/100-Drums-Festival-of-Meghalay.jpg?fit=1024%2C768&ssl=1'
				},
				'Chapchar Kut': {
						'description': 'Chapchar Kut is a spring festival in Mizoram, celebrating the sowing season with traditional Mizo dances, music, and feasts, showcasing tribal unity.',
						'image_url': 'https://assamtribune.com/h-upload/2025/03/08/1694809-chapchar-kut-mizo-fest.jpg'
				},
				'Gudi Padwa': {
						'description': 'Gudi Padwa marks the Marathi New Year in Maharashtra, celebrated with colorful rangolis, hoisting of Gudi flags, and traditional feasts.',
						'image_url': 'https://cdn.cdnparenting.com/articles/2018/09/19150407/Gudi-Padwa-1.webp'
				},
				'Ambubachi Mela': {
						'description': 'Ambubachi Mela in Assam is a tantric festival at Kamakhya Temple, celebrating the menstruation of Goddess Kamakhya with rituals and pilgrimages.',
						'image_url': 'https://thehillstimes.in/wp-content/uploads/2024/06/image_editor_output_image1737499973-1652978579963.jpg'
				},
				'Sankranti': {
						'description': 'Sankranti, celebrated in Andhra Pradesh, is a harvest festival with traditional rituals, kite flying, and offerings to mark the sun’s northward journey.',
						'image_url': 'https://assets.thehansindia.com/h-upload/2025/01/07/1512814-haridasu.webp'
				},
				'Lohri': {
						'description': 'Lohri is a Punjabi festival marking the winter solstice, celebrated with bonfires, folk songs, and dances like Bhangra, symbolizing harvest and prosperity.',
						'image_url': 'https://i.pinimg.com/736x/e7/07/c5/e707c568aa174eae63e3fd677a81bb05.jpg'
				},
				'Modhera Dance Festival': {
						'description': 'Modhera Dance Festival in Gujarat showcases classical dance forms like Garba and Dandiya, performed at the historic Sun Temple in Modhera.',
						'image_url': 'https://creativeyatra.com/wp-content/uploads/2017/02/RDSC01292-1-bw.jpg'
                        
				},
				'Ladakh Festival': {
						'description': 'Ladakh Festival celebrates the region’s Buddhist heritage with traditional dances, polo matches, and cultural exhibitions in Leh and surrounding areas.',
						'image_url': 'https://lifeontheplanetladakh.com/wp-content/uploads/2024/07/IMG_5991.jpeg'
				},
				'Tansen Samaroh': {
						'description': 'Tansen Samaroh in Madhya Pradesh is a classical music festival honoring Tansen, featuring performances by renowned musicians near his tomb in Gwalior.',
						'image_url': 'https://www.festivalsofindia.in/images/tansen.jpg'
				},
				'Lakshadweep Cultural Fest': {
						'description': 'Lakshadweep Cultural Festival showcases the islands’ unique traditions with folk dances, music, and local crafts, celebrating the vibrant island culture.',
						'image_url': 'https://tripxl.com/blog/wp-content/uploads/2024/10/Milad-un-Nabi.jpg'
				}
		    }
           
        
            if selected_event in event_info:
                st.markdown(f"### {selected_event}")
                event_data = events_data[events_data['Event'] == selected_event].iloc[0]
                st.markdown(f"**Location:** {event_data['State']}")
                st.markdown(f"**Month:** {event_data['Month']}")
                st.markdown(f"**Estimated Visitors:** {event_data['Visitors_Estimate']:,}")
                st.markdown(f"**Cultural Significance:** {event_data['Cultural_Significance']}/10")
            
                st.markdown(event_info[selected_event]['description'])
                display_image_from_url(event_info[selected_event]['image_url'], f"{selected_event}", width=400)
            else:
                event_data = events_data[events_data['Event'] == selected_event].iloc[0]
                st.markdown(f"### {selected_event}")
                st.markdown(f"**Location:** {event_data['State']}")
                st.markdown(f"**Month:** {event_data['Month']}")
                st.markdown(f"**Estimated Visitors:** {event_data['Visitors_Estimate']:,}")
                st.markdown(f"**Cultural Significance:** {event_data['Cultural_Significance']}/10")
                st.write(f"Detailed information about {selected_event} is not available.")

        st.markdown("<h2 class='sub-header'>Events by Month</h2>", unsafe_allow_html=True)
    
        selected_month = st.selectbox("Filter events by month:", 
                                      ['All'] + events_data['Month'].unique().tolist())
    
        if selected_month != 'All':
            filtered_events = events_data[events_data['Month'].str.contains(selected_month, case=False, na=False)]
        else:
            filtered_events = events_data

        st.dataframe(filtered_events[['Event', 'State', 'Month', 'Visitors_Estimate', 'Cultural_Significance']],
                     use_container_width=True)

        st.markdown("<h2 class='sub-header'>Geographical Distribution of Major Events</h2>", unsafe_allow_html=True)

        # Assuming this is within an elif block in a Streamlit app
        # Load cultural events data
        events_data = load_cultural_events_data()

        # Add coordinates to events data
        event_coords = {
            'Uttar Pradesh/Uttarakhand': [26.8467, 80.9462],
            'Rajasthan': [26.9124, 75.7873],
            'Gujarat': [23.0225, 72.5714],
            'Nagaland': [25.6747, 94.1106],
            'Kerala': [10.8505, 76.2711],
            'West Bengal': [22.5726, 88.3639],
            'Uttar Pradesh': [25.3176, 82.9739],
            'Ladakh': [34.1526, 77.5770],
            'Tamil Nadu': [11.1271, 78.6569],
            'Assam': [26.2006, 92.9376],
            'Maharashtra': [19.0760, 72.8777],
            'Madhya Pradesh': [23.2599, 77.4126],
            'Bihar': [25.0961, 85.3131],
            'Sikkim': [27.5330, 88.5122],
            'Arunachal Pradesh': [27.1004, 93.6166],
            'Manipur': [24.8170, 93.9442],
            'Odisha': [20.9517, 85.0985],
            'Telangana': [17.1232, 79.2089],
            'Meghalaya': [25.4670, 91.3662],
            'Mizoram': [23.1645, 92.9376],
            'Karnataka': [15.3173, 75.7139],
            'Punjab': [31.1048, 75.7139],
            'Goa': [15.4989, 73.6918],
            'Lakshadweep': [10.5593, 72.6358]
        }
        events_data['lat'] = events_data['State'].map(lambda x: event_coords.get(x, [None, None])[0])
        events_data['lon'] = events_data['State'].map(lambda x: event_coords.get(x, [None, None])[1])

        # Check for NaN values in events data
        if events_data[['lat', 'lon']].isna().any().any():
            #st.warning("Some events entries contain missing latitude or longitude values and will be excluded from the map.")
            events_data = events_data.dropna(subset=['lat', 'lon'])

        # Verify if any data remains after dropping NaNs
        if events_data.empty:
            st.error("No valid data with latitude and longitude available to display on the map.")
        else:
            # Create the Folium map (unchanged)
            m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles='cartodbpositron')
            marker_cluster = MarkerCluster().add_to(m)

            # Iterate through events data to create markers (unchanged)
            for _, row in events_data.iterrows():
                state = row['State']
                if state in event_coords:  # This check is retained from the original code
                    lat, lon = event_coords[state]
                    popup_content = f"""
                    <b>{row['Event']}</b><br>
                    State: {row['State']}<br>
                    Month: {row['Month']}<br>
                    Visitors: {row['Visitors_Estimate']:,}<br>
                    Significance: {row['Cultural_Significance']}/10
                    """
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_content, max_width=300),
                        tooltip=row['Event'],
                        icon=folium.Icon(color='green', icon='calendar', prefix='fa')
                    ).add_to(marker_cluster)

            # Render the map in Streamlit
            map_html = m._repr_html_()
            components.html(map_html, height=600)

    # Cultural Economy Page
    elif page == "Cultural Economy":
        st.markdown("<h1 class='main-header'>Cultural Economy of India</h1>", unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-text'>
        India's cultural sector contributes significantly to the economy through tourism, handicrafts exports, 
        and cultural institutions. Explore the economic impact of cultural heritage.
        </div>
        """, unsafe_allow_html=True)

        economy_tabs = st.tabs(["Cultural Funding", "Handicrafts Exports", "Tourism Revenue"])

        with economy_tabs[0]:
            st.markdown("<h2 class='sub-header'>Government Funding for Cultural Preservation</h2>", unsafe_allow_html=True)

            funding_data = load_cultural_funding_data()

            col1, col2 = st.columns([2, 1])

            with col1:
                funding_melted = funding_data.melt(id_vars=['Scheme'], 
                                                   value_vars=['Expenditure_2019_20', 'Expenditure_2020_21', 
                                                               'Expenditure_2021_22', 'Expenditure_2022_23'],
                                                   var_name='Year', value_name='Expenditure')
                funding_melted['Year'] = funding_melted['Year'].str.extract(r'(\d{4}_\d{2})')[0].str.replace('_', '-')

                fig = px.line(funding_melted, x='Year', y='Expenditure', color='Scheme',
                              title='Cultural Funding Expenditure (2019-2023, ₹ in Crores)')
                fig.update_layout(xaxis_title='Year', yaxis_title='Expenditure (₹ Crores)')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                selected_scheme = st.selectbox(
                    "Select a funding scheme to view details:",
                    funding_data['Scheme'].tolist()
                )

                scheme_data = funding_data[funding_data['Scheme'] == selected_scheme].iloc[0]
                st.markdown(f"**{selected_scheme}**")
                st.markdown(f"- 2019-20: ₹ **{scheme_data['Expenditure_2019_20']}** Cr")
                st.markdown(f"- 2020-21: ₹ **{scheme_data['Expenditure_2020_21']}** Cr")
                st.markdown(f"- 2021-22: ₹ **{scheme_data['Expenditure_2021_22']}** Cr")
                st.markdown(f"- 2022-23: ₹ **{scheme_data['Expenditure_2022_23']}** Cr")

                st.markdown("""
                <div class='container'>
                Government funding supports cultural preservation through institutions like ASI, museums, 
                and cultural academies, ensuring the maintenance of heritage sites and promotion of arts.
                </div>
                """, unsafe_allow_html=True)

            # Additional Visual: Budget Trends from CSV
            st.markdown("<h2 class='sub-header'>Cultural Budget Trends</h2>", unsafe_allow_html=True)
            if not budget_df.empty:
                #change
                #fig_budget = px.bar(budget_df, x='Year', y='Budget', color='Scheme',
                                #title='Cultural Budget Allocation (2017-2022)',
                                #color_discrete_sequence=px.colors.qualitative.Set2)
                fig_budget = px.bar(budget_df, x='Year', y='Allocation',
                                title='Cultural Budget Allocation (2017-2022)',
                                color_discrete_sequence=px.colors.qualitative.Set2)
                st.plotly_chart(fig_budget, use_container_width=True)

        with economy_tabs[1]:
            st.markdown("<h2 class='sub-header'>Handicrafts Exports (2017-2023)</h2>", unsafe_allow_html=True)

            export_data = load_handicraft_export_data()

            col1, col2 = st.columns([2, 1])

            with col1:
                fig = px.line(export_data, x='Year', y='Total', 
                              title='Total Handicrafts Exports (2017-2023, ₹ in Crores)')
                fig.update_layout(xaxis_title='Year', yaxis_title='Export Value (₹ Crores)')
                st.plotly_chart(fig, use_container_width=True)

                export_melted = export_data.drop(columns=['Total']).melt(id_vars=['Year'], 
                                                                         var_name='Category', value_name='Export_Value')
                fig = px.area(export_melted, x='Year', y='Export_Value', color='Category',
                              title='Handicrafts Export Categories (2017-2023, ₹ in Crores)')
                fig.update_layout(xaxis_title='Year', yaxis_title='Export Value (₹ Crores)')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                selected_year = st.selectbox(
                    "Select a year to view export details:",
                    export_data['Year'].tolist()
                )

                year_data = export_data[export_data['Year'] == selected_year].iloc[0]
                st.markdown(f"**Exports in {selected_year}**")
                for category in export_data.columns[1:-1]:
                    st.markdown(f"- {category}: ₹ **{year_data[category]}** Cr")
                st.markdown(f"- Total: ₹ **{year_data['Total']}** Cr")
            
                st.markdown("""
                <div class='container'>
                Handicrafts exports are a vital part of India's cultural economy, supporting millions of artisans 
                and showcasing traditional craftsmanship globally.
                </div>
                """, unsafe_allow_html=True)

        with economy_tabs[2]:
            st.markdown("<h2 class='sub-header'>Tourism Revenue Contribution</h2>", unsafe_allow_html=True)
        
            # Placeholder data for tourism revenue
            tourism_revenue = {
                'Year': [2019, 2020, 2021, 2022, 2023],
                'Revenue_Cr': [211000, 50000, 65000, 134000, 195000]
            }
            revenue_df = pd.DataFrame(tourism_revenue)

            fig = px.bar(revenue_df, x='Year', y='Revenue_Cr', 
                         title='Tourism Revenue Contribution (2019-2023, ₹ in Crores)')
            fig.update_layout(xaxis_title='Year', yaxis_title='Revenue (₹ Crores)')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            <div class='container'>
            Tourism, driven by cultural heritage, is a major economic contributor. The dip in 2020-2021 reflects 
            the impact of the pandemic, with a strong recovery in 2022-2023.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<h3 class='section-header'>Key Economic Impacts</h3>", unsafe_allow_html=True)
            st.markdown("""
            - **Employment**: Cultural tourism supports millions of jobs in hospitality, guiding, and artisan sectors.
            - **Foreign Exchange**: Foreign tourists contribute significantly to India's forex earnings.
            - **Regional Development**: Heritage sites boost local economies through visitor spending.
            """)

    # Interactive Explorer Page
    elif page == "Interactive Explorer":
        st.markdown("<h1 class='main-header'>Interactive Cultural Explorer</h1>", unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-text'>
        Plan your cultural journey across India with this interactive tool. Filter by state, category, 
        or time of year to discover heritage sites, art forms, crafts, and events.
        </div>
        """, unsafe_allow_html=True)

# Remove the content_col, video_col line since it's creating unnecessary space
        
        st.markdown("<h2 class='sub-header'>Explore by Filters</h2>", unsafe_allow_html=True)

        # State options for both the video dropdown and the filter dropdown
        state_options = ['All'] + sorted(set(load_heritage_site_data()['State'].tolist() + 
                                            load_arts_data()['Region'].tolist() + 
                                            load_crafts_data()['State'].tolist() + 
                                            load_cultural_events_data()['State'].tolist()))

        # Dictionary mapping states to YouTube video embed URLs and watch URLs for fallback
        state_videos = {
            'All':{
                'embed':'https://www.youtube.com/embed/rTDaZoDDW5g?si=jXTEyrijaRy2tTAJ',
                'watch':'https://youtu.be/rTDaZoDDW5g?si=rhqh69hbMZuWF8_i'
            },
            'West Bengal': {
                'embed': 'https://www.youtube.com/embed/QqJU_YpGeNs?si=BImaGc2qZfEMNGEC',
                'watch': 'https://youtu.be/QqJU_YpGeNs?si=75dwkHUMB1zfyPkp'
            },
            'Uttarakhand': {
                'embed': 'https://www.youtube.com/embed/Rl7iBeqGSjE?si=ur493o3yRB5s27q-',
                'watch': 'https://youtu.be/Rl7iBeqGSjE?si=wSUXpqlNd-TfkBs7'
            },
            'Ladakh': {
                'embed': 'https://www.youtube.com/embed/C1x1Vix17Y8?si=8LurlAWAqLwRHexv',
                'watch': 'https://youtu.be/C1x1Vix17Y8?si=1rfCfOEtafG-DBTI'
            },
            'Lakshadweep': {
                'embed': 'https://www.youtube.com/embed/SckmeqUExS8?si=-6yxOBfDCUNacUC3',
                'watch': 'https://youtu.be/SckmeqUExS8?si=IHo6zcH0-X14nYl9'
            },
            'Dadra and Nagar Haveli': {
                'embed': 'https://www.youtube.com/embed/FlBNzZHzBwo?si=VVUKAnSgy9xA9XUv',
                'watch': 'https://youtu.be/FlBNzZHzBwo?si=PLWfLm4S5LILQO80'
            },
            'Dadra and Nagar Haveli and Daman and Diu': {
                'embed': 'https://www.youtube.com/embed/FlBNzZHzBwo?si=VVUKAnSgy9xA9XUv',
                'watch': 'https://youtu.be/FlBNzZHzBwo?si=PLWfLm4S5LILQO80'
            },
            'Nagaland': {
                'embed': 'https://www.youtube.com/embed/HNATfahjQk0?si=TqYhVZn3VFwCFeb0',
                'watch': 'https://youtu.be/HNATfahjQk0?si=WTqdnOJAxJlogzNL'
            },
            'Mizoram': {
                'embed': 'https://www.youtube.com/embed/TtMMsdd2IjM?si=40wJvNY9XQXqm_6z',
                'watch': 'https://youtu.be/TtMMsdd2IjM?si=HgVNoWt95O8TPRgq'
            },
            'Meghalaya': {
                'embed': 'https://www.youtube.com/embed/mGSXsie7ag4?si=AOwfhfyqwXKQhoX3',
                'watch': 'https://youtu.be/mGSXsie7ag4?si=a6cIvMpfv9HucT6o'
            },
            'Sikkim': {
                'embed': 'https://www.youtube.com/embed/K7IYGNxwzQA?si=71ICx0Fzx1fyzHk2',
                'watch': 'https://youtu.be/K7IYGNxwzQA?si=Z1xEl3D0yr2CU680'
            },
            'Gujarat': {
                'embed': 'https://www.youtube.com/embed/5YlBFEbbz8M?si=crEs2dQMDnvzIlkj',
                'watch': 'https://youtu.be/5YlBFEbbz8M?si=szB186JDwtOI8Ntx'
            },
            'Madhya Pradesh': {
                'embed': 'https://www.youtube.com/embed/TWOGgt1IP0Q?si=PuUH3BfTftC4UxpU',
                'watch': 'https://youtu.be/TWOGgt1IP0Q?si=KYahjY3f5xHvWei_'
            },
            'Uttar Pradesh': {
                'embed': 'https://www.youtube.com/embed/CBeEGq6x1YU?si=_mtDsLlxzvg2rvP5',
                'watch': 'https://youtu.be/CBeEGq6x1YU?si=_WjshCoDFaFnrWgO'
            },
            'Andhra Pradesh': {
                'embed': 'https://www.youtube.com/embed/LJLnd0EE9Cg?si=RcS5Go_xRSc_HWq0',
                'watch': 'https://youtu.be/LJLnd0EE9Cg?si=PYlsWIj48yj0rRQg'
            },
            'Arunachal Pradesh': {
                'embed': 'https://www.youtube.com/embed/GJ9wUxjxUsw?si=JTxBMNm1Ws8DOnOT',
                'watch': 'https://youtu.be/GJ9wUxjxUsw?si=xoNNIsNogujTMUV_'
            },
            'Kolkata': {
                'embed': 'https://www.youtube.com/embed/avMu7oylX7E?si=SdftfgyDgRKI6G5_',
                'watch': 'https://youtu.be/avMu7oylX7E?si=BVRNXUaeKdHOO1gp'
            },
            'Karnataka': {
                'embed': 'https://www.youtube.com/embed/sWevKpEwSEg?si=kT-LJIKZ1u-ETN4C',
                'watch': 'https://youtu.be/sWevKpEwSEg?si=34qj0NHTchkrPS1H'
            },
            'Maharashtra': {
                'embed': 'https://www.youtube.com/embed/Kh4MU4EonkI?si=x89v8xV9Rxu4sU4D',
                'watch': 'https://youtu.be/Kh4MU4EonkI?si=sDOAnA7clScjcN8O'
            },
            'Chhattisgarh': {
                'embed': 'https://www.youtube.com/embed/RsqaKLWKfBQ?si=F1ZOfbfcJN6BJHWl',
                'watch': 'https://youtu.be/RsqaKLWKfBQ?si=GM95qelT39frIrGN'
            },
            'Chandigarh': {
                'embed': 'https://www.youtube.com/embed/RsqaKLWKfBQ?si=F1ZOfbfcJN6BJHWl',
                'watch': 'https://youtu.be/RsqaKLWKfBQ?si=GM95qelT39frIrGN'
            },
            'Telangana': {
                'embed': 'https://www.youtube.com/embed/Zv8uHQ157oA?si=nMgNA4L0y6Trjgde',
                'watch': 'https://youtu.be/Zv8uHQ157oA?si=5TQky5LqPaGEFXHY'
            },
            'Delhi': {
                'embed': 'https://www.youtube.com/embed/AoLiXe05-Z8?si=FTH0wxC-Eg559fhg',
                'watch': 'https://youtu.be/AoLiXe05-Z8?si=0CGFIARLnZ00rQr2'
            },
            'Punjab': {
                'embed': 'https://www.youtube.com/embed/vGWNr1dRFeA?si=mqC4OUH9C97PZE_c',
                'watch': 'https://youtu.be/vGWNr1dRFeA?si=G4TMhs24CDYB3YmA'
            },
            'Rajasthan': {
                'embed': 'https://www.youtube.com/embed/vQq6AwZo6Ok?si=6pQZoRxPQmrTOwVT',
                'watch': 'https://youtu.be/vQq6AwZo6Ok?si=KNhc--K0qzDsAp6g'
            },
            'Assam': {
                'embed': 'https://www.youtube.com/embed/4buWapbwT0E?si=HqHOUJJICbr-PMVH',
                'watch': 'https://youtu.be/4buWapbwT0E?si=XHpI__5zxDb5vh7U'
            },
            'Goa': {
                'embed': 'https://www.youtube.com/embed/uRvZWUx5V8I?si=gis4fZMElFkN5ZbN',
                'watch': 'https://youtu.be/uRvZWUx5V8I?si=ypXv22VJ3nCQGCWi'
            },
            'Odisha': {
                'embed': 'https://www.youtube.com/embed/ph_QTWWNHoA?si=p5hIzmCF4i7Y7SxF',
                'watch': 'https://www.youtube.com/live/ph_QTWWNHoA?si=RkcC3CrteDPSa4K9'
            },
            'Haryana': {
                'embed': 'https://www.youtube.com/embed/EX8O1cNbcZY?si=tHkTM0mHofDM-gqM',
                'watch': 'https://youtu.be/EX8O1cNbcZY?si=0LEhPXdk4qjwHE7j'
            },
            'Himachal Pradesh': {
                'embed': 'https://www.youtube.com/embed/GZfXk5QeuEs?si=-sswQV3_O0beXMJQ',
                'watch': 'https://youtu.be/GZfXk5QeuEs?si=PFLfm7X-ONVxpweR'
            },
            'Jharkhand': {
                'embed': 'https://www.youtube.com/embed/eDIJv93S_tQ?si=6ADv_xDSQTsYfmpz',
                'watch': 'https://youtu.be/eDIJv93S_tQ?si=_pIQtZzLv8ARfvAg'
            },
            'Manipur': {
                'embed': 'https://www.youtube.com/embed/8lHJpuXKttg?si=Fsb9vnKuev0JIrH0',
                'watch': 'https://youtu.be/8lHJpuXKttg?si=mbIg0vlZd8zaxfE6'
            },
            'Tamil Nadu': {
                'embed': 'https://www.youtube.com/embed/Ru1xj3LE_WM?si=q6LCQ9qaeUdIzzMC',
                'watch': 'https://youtu.be/Ru1xj3LE_WM?si=yvfeOItRvAxKbJzX'
            },
            'Tripura': {
                'embed': 'https://www.youtube.com/embed/NAZ67u41tNk?si=YOEP4yagfAPkSoUy',
                'watch': 'https://youtu.be/NAZ67u41tNk?si=AMGqiLe9zVgRTuzE'
            },
            'Bihar' : {
                'embed': 'https://www.youtube.com/embed/XxGytwfWBSQ?si=j-50K8l0HpZcEPWy',
                'watch': 'https://youtu.be/XxGytwfWBSQ?si=Q6ceFmy2_F6D_B-o'
            },
            'Jammu & Kashmir' : {
                'embed' : 'https://www.youtube.com/embed/D_bgCyM1nRY?si=kFQlWEW9IRNP4ftb',
                'watch' :'https://www.youtube.com/watch?v=D_bgCyM1nRY'
            },
            'Jammu and Kashmir' : {
                'embed' : 'https://www.youtube.com/embed/D_bgCyM1nRY?si=kFQlWEW9IRNP4ftb',
                'watch' :'https://www.youtube.com/watch?v=D_bgCyM1nRY'
            },
            'Kerala': {
                'embed' : 'https://www.youtube.com/embed/R83BlU5nnbs?si=owfMCYZG0hCNNamB',
                'watch' :'https://www.youtube.com/watch?v=R83BlU5nnbs'
            },
            'Andaman and Nicobar Islands' : {
                'embed' : 'https://www.youtube.com/embed/q43hYTqNFXc?si=xspc4AKPZLJGTBWG',
                'watch' :'https://www.youtube.com/watch?v=q43hYTqNFXc&t=61s'
            },
            'Puducherry': {
                'embed': 'https://www.youtube.com/embed/XRrerLnkO-I?si=I4lS-kKboUbM5CtP',
                'watch': 'https://www.youtube.com/watch?v=XRrerLnkO-I'
            },
        }

        st.markdown("<h3 class='section-header'>Cultural Video by State</h3>", unsafe_allow_html=True)
        
        # Create two columns with better ratios: dropdown takes more space, video takes remaining
        dropdown_col, video_display_col = st.columns([1, 3])  # Much better ratio
    
        with dropdown_col:
            video_state = st.selectbox(
                "Select a State for Video:", 
                state_options, 
                key="video_state_selectbox"
            )

        with video_display_col:
            if video_state :
                video_data = state_videos.get(video_state, {
                    'embed': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Fallback if state video not found
                    'watch': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
                })
                # Embed the video with proper sizing
                st.markdown(
                    f"""
                    <div style='width: 100%; height: 400px;'>
                        <iframe 
                            width="100%" 
                            height="100%" 
                            src="{video_data['embed']}" 
                            frameborder="0" 
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                            allowfullscreen
                            style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                        </iframe>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # Provide a fallback link in case embedding fails
                st.markdown(
                    f"""
                    <div style='margin-top: 10px; text-align: center;'>
                        <p style='font-size: 0.9rem; color: #666;'>
                            If the video doesn't load, 
                            <a href='{video_data['watch']}' target='_blank' style='color: #1f77b4; text-decoration: none;'>
                                click here to watch it on YouTube
                            </a>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Show placeholder when no state is selected
                st.markdown(
                    """
                    <div style='width: 100%; height: 400px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 8px; border: 2px dashed #ccc;'>
                        <div style='text-align: center; color: #666;'>
                            <i class='fas fa-video' style='font-size: 48px; margin-bottom: 15px; opacity: 0.5;'></i>
                            <h4 style='margin: 0; font-weight: 300;'>Select a state to view cultural video</h4>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        col1, col2, col3 = st.columns(3)

        with col1:
            state_options = ['All'] + sorted(set(load_heritage_site_data()['State'].tolist() + 
                                                load_arts_data()['Region'].tolist() + 
                                                load_crafts_data()['State'].tolist() + 
                                                load_cultural_events_data()['State'].tolist()))
            selected_state = st.selectbox("Select State/Region:", state_options)
    
        with col2:
            category_options = ['All', 'Heritage Sites', 'Art Forms', 'Crafts', 'Events']
            selected_category = st.selectbox("Select Category:", category_options)

        with col3:
            month_options = ['All'] + ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            selected_month = st.selectbox("Select Month:", month_options)

        # Combine all datasets for filtering
        heritage_data = load_heritage_site_data()[['Site', 'State', 'Type', 'lat', 'lon']].rename(
            columns={'Site': 'Name', 'Type': 'Category'})
        heritage_data['Category'] = 'Heritage Sites'

        arts_data = load_arts_data()[['Art_Form', 'Region', 'Category', 'lat', 'lon']].rename(
            columns={'Art_Form': 'Name', 'Region': 'State'})
        arts_data['Category'] = 'Art Forms'

        crafts_data = load_crafts_data()[['Craft', 'State']].rename(columns={'Craft': 'Name'})
        # Assign approximate coordinates for crafts (using state centroids)
        state_coords = {
            'Jammu & Kashmir': [34.0837, 74.7973],
            'Uttar Pradesh': [26.8467, 80.9462],
            'Rajasthan': [26.9124, 75.7873],
            'Karnataka': [15.3173, 75.7139],
            'Tamil Nadu': [11.1271, 78.6569],
            'Gujarat': [23.0225, 72.5714],
            'Punjab': [31.1471, 75.3412],
            'West Bengal': [22.5726, 88.3639],
            'Chhattisgarh': [21.2787, 81.8661],
            'Madhya Pradesh': [23.2599, 77.4126]
        }
        crafts_data['lat'] = crafts_data['State'].map(lambda x: state_coords.get(x, [20.5937, 78.9629])[0])
        crafts_data['lon'] = crafts_data['State'].map(lambda x: state_coords.get(x, [20.5937, 78.9629])[1])
        crafts_data['Category'] = 'Crafts'

        events_data = load_cultural_events_data()[['Event', 'State', 'Month']].rename(columns={'Event': 'Name'})
        events_data['Category'] = 'Events'
        # Define event_coords for mapping event locations
        event_coords = {
            'Uttar Pradesh/Uttarakhand': [26.8467, 80.9462],
            'Rajasthan': [26.9124, 75.7873],
            'Gujarat': [23.0225, 72.5714],
            'Nagaland': [25.6747, 94.1106],
            'Kerala': [10.8505, 76.2711],
            'West Bengal': [22.5726, 88.3639],
            'Uttar Pradesh': [25.3176, 82.9739],
            'Ladakh': [34.1526, 77.5770],
            'Tamil Nadu': [11.1271, 78.6569],
            'Assam': [26.2006, 92.9376],
            'Maharashtra': [19.0760, 72.8777],
            'Madhya Pradesh': [23.2599, 77.4126]
        }
        events_data['lat'] = events_data['State'].map(lambda x: event_coords.get(x, [20.5937, 78.9629])[0])
        events_data['lon'] = events_data['State'].map(lambda x: event_coords.get(x, [20.5937, 78.9629])[1])

        combined_data = pd.concat([heritage_data, arts_data, crafts_data, events_data], ignore_index=True)

        # Apply filters
        filtered_data = combined_data.copy()
        if selected_state != 'All':
            filtered_data = filtered_data[filtered_data['State'] == selected_state]
        if selected_category != 'All':
            filtered_data = filtered_data[filtered_data['Category'] == selected_category]
        if selected_month != 'All' and selected_category in ['All', 'Events']:
            filtered_data = filtered_data[filtered_data['Month'].str.contains(selected_month, case=False, na=False)]

        st.markdown("<h2 class='sub-header'>Explore on Map</h2>", unsafe_allow_html=True)

        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles='cartodbpositron')
        marker_cluster = MarkerCluster().add_to(m)

        category_icons = {
            'Heritage Sites': {'color': 'blue', 'icon': 'landmark'},
            'Art Forms': {'color': 'orange', 'icon': 'paint-brush'},
            'Crafts': {'color': 'purple', 'icon': 'tools'},
            'Events': {'color': 'green', 'icon': 'calendar'}
        }

        for _, row in filtered_data.iterrows():
            popup_content = f"""
            <b>{row['Name']}</b><br>
            State: {row['State']}<br>
            Category: {row['Category']}<br>
            """
            if 'Month' in row and pd.notna(row['Month']):
                popup_content += f"Month: {row['Month']}<br>"

            icon_info = category_icons.get(row['Category'], {'color': 'gray', 'icon': 'info'})
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=row['Name'],
                icon=folium.Icon(color=icon_info['color'], icon=icon_info['icon'], prefix='fa')
            ).add_to(marker_cluster)
        
        # Load custom CSS for modern styling
        st.markdown("""
        <style>
        .sub-header {
            color: #2c3e50;
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 20px;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .section-header {
            color: #34495e;
            font-size: 22px;
            font-weight: 500;
            margin-bottom: 15px;
        }
        /* Style all selectbox containers with a gradient */
        .stSelectbox [data-baseweb="select"] {
            background: linear-gradient(45deg, #ADD8E6, #87CEEB) !important; /* Gradient for selectbox */
            border-radius: 5px;
            padding: 5px;
            border: 2px solid #87CEEB !important; /* Slightly darker light blue border */
        }
        /* Ensure inner elements of selectbox are filled with the gradient */
        .stSelectbox [data-baseweb="select"] > div {
            background: linear-gradient(45deg, #ADD8E6, #87CEEB) !important; /* Gradient for inner div */
            color: #333333; /* Dark text for contrast */
            font-weight: 500;
        }
        /* Style all dropdown menu containers with the gradient */
        .stSelectbox [data-baseweb="popover"] {
            background: linear-gradient(45deg, #ADD8E6, #87CEEB)  /* Gradient for dropdown container */
            border-radius: 5px;
            border: 1px solid #87CEEB  /* Light blue border for dropdown */
        }
        /* Style all dropdown lists with the gradient */
        .stSelectbox [data-baseweb="popover"] ul {
            background: linear-gradient(45deg, #ADD8E6, #87CEEB)  /* Gradient for dropdown list */
            padding: 0;
            margin: 0;
        }
        /* Style all dropdown options with the gradient */
        .stSelectbox [data-baseweb="popover"] li {
            background: linear-gradient(45deg, #ADD8E6, #87CEEB) /* Gradient for each option */
            color: #333333; /* Dark text for readability */
            padding: 8px 12px;
            font-weight: 400;
        }
        /* Ensure no inherited styles override the dropdown option background */
        .stSelectbox [data-baseweb="popover"] li[data-testid="option"] {
            background: linear-gradient(45deg, #ADD8E6, #87CEEB) !important; /* Gradient for specific option elements */
        }
        /* Hover effect for all dropdown options */
        .stSelectbox [data-baseweb="popover"] li:hover {
            background: #87CEEB !important; /* Solid darker light blue on hover */
            color: #FFFFFF; /* White text on hover for contrast */
        }
        /* Style for all selected dropdown options */
        .stSelectbox [data-baseweb="popover"] li[aria-selected="true"] {
            background: #87CEEB !important; /* Solid darker light blue for selected option */
            color: #FFFFFF; /* White text for selected option */
        }
        /* Style all dropdown arrows */
        .stSelectbox [data-baseweb="select"] .icon {
            color: #333333; /* Dark arrow for contrast */
        }
        </style>
        """, unsafe_allow_html=True)
        map_html = m._repr_html_()
        components.html(map_html, height=600)

        st.markdown("<h2 class='sub-header'>Filtered Results</h2>", unsafe_allow_html=True)
        st.dataframe(filtered_data[['Name', 'State', 'Category']], use_container_width=True)

        st.markdown("<h3 class='section-header'>Plan Your Visit</h3>", unsafe_allow_html=True)
        st.markdown("""
        Use the filters above to customize your cultural exploration. Click on map markers to learn more about each site, 
        art form, craft, or event. Combine state and month filters to plan a trip aligned with major festivals!
        """)
        # Footer for all pages
        add_indian_culture_footer()
    st.markdown("""
    <div style='text-align: center; margin-top: 2rem; padding: 1rem; background-color: #F5F5F5; border-radius: 8px;'>
        <p style='font-size: 0.9rem; color: #555;'>
            Indian Cultural Heritage Explorer | Powered by Streamlit | Data sourced from data.gov.in and UNESCO
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Error handling for unexpected issues
try:
    if __name__ == "__main__":
        integrate_with_existing_app()
        st.session_state.setdefault('page', 'Home')
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
    st.markdown("""
    Please try refreshing the page or contact support if the issue persists.
    """)
