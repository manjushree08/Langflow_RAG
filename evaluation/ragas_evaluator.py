# evaluation/ragas_evaluator.py
import json
import pandas as pd
import datetime
import os
from typing import Dict, List, Any
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_relevancy,
    context_recall
)
from ragas.metrics.critique import harmfulness
from ragas import evaluate
from .data_generator import EvaluationDataGenerator

class RagasEvaluator:
    def __init__(self, results_dir: str = "data/evaluation_results"):
        self.results_dir = results_dir
        os.makedirs(self.results_dir, exist_ok=True)
    
    def evaluate_flow(self, flow_id: str, api_client):
        """
        Evaluate a specific LangFlow flow using RAGAS metrics
        
        Args:
            flow_id: The ID of the flow to evaluate
            api_client: API client instance to communicate with the flow
        """
        # Generate evaluation data
        data_generator = EvaluationDataGenerator()
        eval_data = data_generator.generate_evaluation_data()
        
        # Process each question and collect responses
        questions = []
        contexts = []
        responses = []
        ground_truths = []
        
        for item in eval_data:
            question = item["question"]
            ground_truth = item["ground_truth"]
            
            # Get response from the flow
            response_data = api_client.send_query(
                query=question,
                flow_id=flow_id
            )
            
            response = response_data["response"]
            
            # Extract context if available in metadata
            context = ""
            if "metadata" in response_data and "raw_output" in response_data["metadata"]:
                raw_output = response_data["metadata"]["raw_output"]
                if "context" in raw_output:
                    context = raw_output["context"]
                elif "sources" in raw_output:
                    context = " ".join(raw_output["sources"])
            
            questions.append(question)
            responses.append(response)
            contexts.append(context)
            ground_truths.append(ground_truth)
        
        # Create evaluation dataframe
        eval_df = pd.DataFrame({
            "question": questions,
            "answer": responses,
            "contexts": [[ctx] for ctx in contexts],
            "ground_truth": ground_truths
        })
        
        # Run RAGAS evaluation
        result = evaluate(
            eval_df,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_relevancy,
                context_recall,
                harmfulness
            ]
        )
        
        # Save results
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"{self.results_dir}/evaluation_{flow_id}_{timestamp}.json"
        
        # Convert result to a serializable format
        result_dict = {
            "flow_id": flow_id,
            "timestamp": timestamp,
            "metrics": {
                "faithfulness": result["faithfulness"].mean(),
                "answer_relevancy": result["answer_relevancy"].mean(),
                "context_relevancy": result["context_relevancy"].mean(),
                "context_recall": result["context_recall"].mean(),
                "harmfulness": result["harmfulness"].mean()
            },
            "detailed_results": result.to_dict(),
            "sample_size": len(eval_data)
        }
        
        with open(result_file, "w") as f:
            json.dump(result_dict, f, indent=2)
        
        return result_dict
    
    def get_historical_results(self, flow_id: str = None) -> List[Dict[str, Any]]:
        """Get historical evaluation results, optionally filtered by flow ID"""
        results = []
        
        for filename in os.listdir(self.results_dir):
            if filename.endswith(".json") and filename.startswith("evaluation_"):
                file_path = os.path.join(self.results_dir, filename)
                
                with open(file_path, "r") as f:
                    result = json.load(f)
                
                if flow_id is None or result.get("flow_id") == flow_id:
                    results.append(result)
        
        # Sort by timestamp
        results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return results