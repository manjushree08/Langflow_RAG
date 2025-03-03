# evaluation/data_generator.py
import json
import os
from typing import List, Dict, Any

class EvaluationDataGenerator:
    def __init__(self, data_file: str = "data/questions.json"):
        self.data_file = data_file
        
    def generate_evaluation_data(self) -> List[Dict[str, Any]]:
        """
        Generate or load evaluation data for RAGAS
        
        Returns:
            List of dictionaries containing question and ground truth
        """
        # Check if evaluation data already exists
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                return json.load(f)
        
        # Create sample evaluation data
        # In a real application, this would be more comprehensive
        sample_data = [
            {
                "question": "What are the key components of a RAG system?",
                "ground_truth": "The key components of a RAG (Retrieval-Augmented Generation) system include a document store/vector database, an embedding model, a retrieval mechanism, and a large language model (LLM) for generation. The system retrieves relevant context from the document store and augments the LLM's generation with this context."
            },
            {
                "question": "How does context relevancy affect RAG performance?",
                "ground_truth": "Context relevancy directly impacts RAG performance by determining the quality of information the LLM uses for generation. Relevant context leads to more accurate, factual responses. Poor context relevancy can cause hallucinations or irrelevant information in responses, reducing the system's reliability and usefulness."
            },
            {
                "question": "What is the difference between sparse and dense retrieval?",
                "ground_truth": "Sparse retrieval uses keyword-based methods like BM25 or TF-IDF to match documents based on term overlap, while dense retrieval uses neural embeddings to capture semantic similarity. Sparse methods excel at lexical matching but miss semantic relationships, while dense methods capture meaning but may miss exact term matches. Hybrid approaches often combine both methods."
            },
            {
                "question": "How can I improve faithfulness in my RAG application?",
                "ground_truth": "To improve faithfulness in RAG applications: ensure high-quality data sources, implement proper context filtering, use appropriate prompt engineering techniques, consider reranking retrieved documents, implement attribution tracking, apply post-generation verification, employ self-consistency techniques, and regularly evaluate using metrics like RAGAS faithfulness score."
            },
            {
                "question": "What are common evaluation metrics for RAG systems?",
                "ground_truth": "Common RAG evaluation metrics include: context relevancy (measuring retrieval quality), answer relevancy (response relevance to question), faithfulness (factual accuracy), context recall (coverage of necessary information), harmfulness (safety assessment), answer correctness (accuracy compared to ground truth), and latency/throughput (performance metrics)."
            }
        ]
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        # Save the sample data
        with open(self.data_file, "w") as f:
            json.dump(sample_data, f, indent=2)
        
        return sample_data