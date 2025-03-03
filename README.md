# LangFlow Streamlit Integration with RAGAS Evaluation

This project integrates LangFlow as a backend API with a Streamlit frontend for a chatbot interface. It also includes RAGAS evaluation for measuring the performance of RAG (Retrieval-Augmented Generation) pipelines.

<img src="data\Langflow.png" alt="Langflow" width="500" height="400">

Below is the chatbot for the application
<img src="data\Animation.gif" alt="this slowpoke moves"  width="250" />

## Project Structure

```
project/
├── api/                  # FastAPI server that connects to LangFlow
├── chatbot/              # Streamlit application
├── evaluation/           # RAGAS evaluation tools
├── data/                 # Data storage for evaluation
├── .env                  # Environment variables
├── requirements.txt      # Project dependencies
├── docker-compose.yml    # Docker configuration
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.10+

### Installation

1. Clone this repository
2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following content:
   ```
   LANGFLOW_API_URL=http://localhost:7860
   API_PORT=8000
   DEBUG=True
   ```

### Running the Application

#### Using Docker

The easiest way to run the entire stack is with Docker Compose:

```bash
docker-compose up -d
```

This will start:

- LangFlow on port 7860
- The API server on port 8000
- The Streamlit UI on port 8501

#### Running Locally

1. Start LangFlow:

   ```bash
   docker run -p 7860:7860 logspace/langflow:latest
   ```

2. Start the API server:

   ```bash
   uvicorn api.app:app --reload
   ```

   ```

   ```

3. Start the Streamlit application:

   ```bash
   streamlit run chatbot/app.py
   ```

4. Start the evaluation dashboard:
   ```bash
   streamlit run evaluation/metrics.py
   ```

## Using the Application

### Setting Up LangFlow

1. Access LangFlow at http://localhost:7860
2. Create a new flow using the drag-and-drop interface
3. Set up your RAG pipeline with appropriate components:
   - Document loaders
   - Vector stores
   - LLM models
   - Chain components
4. Deploy your flow

### Using the Chatbot

1. Access the Streamlit UI at http://localhost:8501
2. Select your flow from the dropdown in the sidebar
3. Start chatting with your LangFlow-powered application

### Running Evaluations

1. Access the evaluation dashboard at http://localhost:8501/evaluation
2. Select the flow you want to evaluate
3. Click "Run Evaluation" to test your flow with RAGAS metrics
4. Review the results and optimize your flow accordingly

## RAGAS Evaluation

This project uses RAGAS to evaluate the performance of your RAG pipelines with the following metrics:

1. **Faithfulness**: Measures how factually consistent the generated answer is with the retrieved context
2. **Answer Relevancy**: Evaluates whether the answer addresses the question
3. **Context Relevancy**: Assesses the quality of retrieval - how relevant the retrieved context is to the question
4. **Context Recall**: Measures how well the retrieved context covers the information needed to answer the question
5. **Harmfulness**: Evaluates the safety of the generated response

## Customizing the Application

### Adding Custom Evaluation Questions

Edit or replace the `data/questions.json` file with your domain-specific questions and ground truth answers.

### Extending the API

The API is built with FastAPI, making it easy to add new endpoints:

1. Open `api/app.py`
2. Add new route functions using the FastAPI decorator syntax
3. Implement your endpoint logic

### Customizing the UI

The Streamlit UI can be customized:

1. Edit `chatbot/app.py` to adjust the main application flow
2. Modify components in the `chatbot/components/` directory
3. Add new utility functions as needed

## Evaluation Insights

The evaluation dashboard provides valuable insights into your RAG pipeline performance:

- Metric comparison across different flows
- Historical performance tracking
- Detailed view of evaluation results
- Areas for improvement identification

Use these insights to iteratively improve your LangFlow pipelines:

1. Identify metrics with lower scores
2. Adjust relevant components in your flow
3. Re-run evaluations to measure improvement
4. Repeat until satisfactory performance is achieved
