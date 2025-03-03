# evaluation/metrics.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
import sys
import os

# Add the project root to sys.path to make imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation.ragas_evaluator import RagasEvaluator
from chatbot.utils.api_client import APIClient

def run_metrics_dashboard():
    st.set_page_config(page_title="RAG Evaluation Dashboard", layout="wide")
    
    st.title("RAG Evaluation Dashboard")
    
    # Initialize API client if not already in session state
    if "api_client" not in st.session_state:
        st.session_state.api_client = APIClient(api_url=st.secrets.get("API_URL", "http://localhost:8000"))
    
    # Initialize evaluator
    evaluator = RagasEvaluator()
    
    # Sidebar for controls
    with st.sidebar:
        st.title("Controls")
        
        # Get available flows
        try:
            flows_response = st.session_state.api_client.get_flows()
            flows = flows_response.get("flows", [])
            
            if not flows:
                st.warning("No flows available. Please create flows in LangFlow first.")
                return
            
            # Flow selection for evaluation
            flow_options = [(flow["id"], flow["name"]) for flow in flows]
            flow_names = [f"{name} (ID: {id})" for id, name in flow_options]
            selected_flow_name = st.selectbox("Select a flow to evaluate:", flow_names)
            
            selected_flow_id = selected_flow_name.split("(ID: ")[1].split(")")[0]
            
            # Button to run evaluation
            if st.button("Run Evaluation"):
                with st.spinner("Running evaluation..."):
                    results = evaluator.evaluate_flow(selected_flow_id, st.session_state.api_client)
                st.success("Evaluation complete!")
                
            # Toggle for historical view
            show_historical = st.checkbox("Show Historical Data", value=True)
            
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")
            st.warning("Make sure the API server is running.")
            return
    
    # Main content area
    # Get results for the selected flow
    results = evaluator.get_historical_results(selected_flow_id if "selected_flow_id" in locals() else None)
    
    if not results:
        st.info("No evaluation results found. Run an evaluation using the sidebar controls.")
        return
    
    # Display the latest result
    latest_result = results[0]
    
    st.header(f"Latest Evaluation: {latest_result.get('timestamp', 'Unknown date')}")
    
    # Create metrics display
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Faithfulness", f"{latest_result['metrics']['faithfulness']:.2f}")
    
    with col2:
        st.metric("Answer Relevancy", f"{latest_result['metrics']['answer_relevancy']:.2f}")
    
    with col3:
        st.metric("Context Relevancy", f"{latest_result['metrics']['context_relevancy']:.2f}")
    
    with col4:
        st.metric("Context Recall", f"{latest_result['metrics']['context_recall']:.2f}")
    
    with col5:
        st.metric("Safety Score", f"{1 - latest_result['metrics']['harmfulness']:.2f}")
    
    # Display radar chart of metrics
    metrics_df = pd.DataFrame({
        "Metric": ["Faithfulness", "Answer Relevancy", "Context Relevancy", "Context Recall", "Safety"],
        "Value": [
            latest_result['metrics']['faithfulness'],
            latest_result['metrics']['answer_relevancy'],
            latest_result['metrics']['context_relevancy'],
            latest_result['metrics']['context_recall'],
            1 - latest_result['metrics']['harmfulness']
        ]
    })
    
    fig = px.line_polar(
        metrics_df, 
        r="Value", 
        theta="Metric", 
        line_close=True,
        range_r=[0, 1],
        title="Metrics Radar Chart"
    )
    fig.update_traces(fill='toself')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Historical data (if available and selected)
    if show_historical and len(results) > 1:
        st.header("Historical Performance")
        
        # Prepare historical data
        historical_data = []
        for result in results:
            historical_data.append({
                "timestamp": result.get("timestamp", "Unknown"),
                "faithfulness": result['metrics']['faithfulness'],
                "answer_relevancy": result['metrics']['answer_relevancy'],
                "context_relevancy": result['metrics']['context_relevancy'],
                "context_recall": result['metrics']['context_recall'],
                "safety": 1 - result['metrics']['harmfulness']
            })
        
        hist_df = pd.DataFrame(historical_data)
        
        # Line chart for historical metrics
        fig = go.Figure()
        
        for metric in ["faithfulness", "answer_relevancy", "context_relevancy", "context_recall", "safety"]:
            fig.add_trace(go.Scatter(
                x=hist_df["timestamp"],
                y=hist_df[metric],
                mode='lines+markers',
                name=metric.replace("_", " ").title()
            ))
        
        fig.update_layout(
            title="Historical Metrics Performance",
            xaxis_title="Evaluation Date",
            yaxis_title="Score",
            yaxis=dict(range=[0, 1]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Display evaluation details
    with st.expander("View Raw Evaluation Data"):
        st.json(latest_result)

if __name__ == "__main__":
    run_metrics_dashboard()