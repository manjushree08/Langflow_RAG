# chatbot/components/sidebar.py
import streamlit as st

def setup_sidebar():
    """Set up the sidebar with flow selection and other controls"""
    with st.sidebar:
        st.title("LangFlow Chatbot")
        
        # Get available flows
        try:
            flows_response = st.session_state.api_client.get_flows()
            flows = flows_response.get("flows", [])
            
            if not flows:
                st.warning("No flows available. Please create flows in LangFlow first.")
                return
            
            # Create a dropdown for flow selection
            flow_names = [f"{flow['name']} (ID: {flow['id']})" for flow in flows]
            selected_flow_name = st.selectbox("Select a flow:", flow_names, index=0 if flow_names else None)
            
            if selected_flow_name:
                selected_flow_id = selected_flow_name.split("(ID: ")[1].split(")")[0]
                # Find the selected flow
                for flow in flows:
                    if flow["id"] == selected_flow_id:
                        st.session_state.selected_flow = flow
                        break
            
            # Add option to clear chat history
            if st.button("Clear Chat History"):
                st.session_state.messages = []
                st.session_state.session_id = None
                st.success("Chat history cleared")
            
            # Add link to evaluation dashboard
            st.markdown("---")
            st.markdown("[View Evaluation Dashboard](/evaluation)")
            
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")
            st.warning("Make sure the API server is running.")