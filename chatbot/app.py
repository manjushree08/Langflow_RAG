# chatbot/app.py
import streamlit as st
from components.chat_interface import *
from components.sidebar import *
from utils.api_client import *

def main():
    st.set_page_config(page_title="LangFlow Chatbot", layout="wide")
    
    # Initialize session state variables if they don't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
        
    if "selected_flow" not in st.session_state:
        st.session_state.selected_flow = None
    
    if "api_client" not in st.session_state:
        st.session_state.api_client = APIClient(api_url="http://localhost:8000")
    
    # Set up the sidebar
    setup_sidebar()
    
    # Main chat interface
    st.title("LangFlow Chatbot")
    
    # Display selected flow information
    if st.session_state.selected_flow:
        st.info(f"Using flow: {st.session_state.selected_flow['name']}")
    else:
        st.warning("Please select a flow from the sidebar to begin chatting.")
        return
    
    # Initialize the chat interface
    chat_interface = ChatInterface()
    chat_interface.display_chat_history()
    chat_interface.display_chat_input()

if __name__ == "__main__":
    main()