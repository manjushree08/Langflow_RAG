# api/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
from langflow_handler import LangFlowHandler
from config import settings

app = FastAPI(title="LangFlow API", description="API for LangFlow integration")
langflow_handler = LangFlowHandler(settings.LANGFLOW_API_URL)

class QueryRequest(BaseModel):
    query: str
    flow_id: str
    session_id: Optional[str] = None

class ResponseModel(BaseModel):
    message: str

class QueryResponse(BaseModel):
    response: Dict[Any, Any] = {}
    session_id: str
    metadata: Dict[Any, Any] = {}

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    try:
        response = langflow_handler.process_query(
            query=request.query,
            flow_id=request.flow_id,
            session_id=request.session_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/flows")
async def get_flows():
    try:
        flows = langflow_handler.get_flows()
        return {"flows": flows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)