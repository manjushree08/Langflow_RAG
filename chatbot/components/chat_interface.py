# chatbot/components/chat_interface.py
import json
import streamlit as st
import time

class ChatInterface:
    def __init__(self):
        pass
    
    def display_chat_history(self):
        """Display the chat history"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def display_chat_input(self):
        """Display the chat input field and handle user messages"""
        if prompt := st.chat_input("What would you like to know?"):
            if not st.session_state.selected_flow:
                st.error("Please select a flow first")
                return
                
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Thinking...")
                
                try:
                    # Call API to get response
                    response = st.session_state.api_client.send_query(
                        query=prompt,
                        flow_id=st.session_state.selected_flow["id"],
                        session_id=st.session_state.session_id
                    )
                    
                    # Update session ID if it was created
                    if response.get("session_id"):
                        st.session_state.session_id = response["session_id"]
                    
                    # Display response with a typing effect
                    full_response = response['response']['message']
                    response_placeholder = ""
                    
                    # Simple typing effect
                    for chunk in full_response['message'].split():
                        response_placeholder += chunk + " "
                        time.sleep(0.01)  # Adjust speed as needed
                        message_placeholder.markdown(response_placeholder)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    message_placeholder.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})