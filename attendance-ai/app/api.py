from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
from app.predict import T5SQLPredictor
from app.sql_validator import validate_sql
from app.database import execute_query

app = FastAPI(title="Attendance AI API")
predictor = T5SQLPredictor()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql: str
    confidence: float
    result: list = None
    execution_time_ms: float = 0.0

@app.post("/predict", response_model=QueryResponse)
def predict_sql(req: QueryRequest):
    start_time = time.time()
    try:
        # 1. Generate SQL
        generated_sql = predictor.predict(req.question)
        
        # 2. Validate SQL
        validate_sql(generated_sql)
        
        # 3. Execute
        rows = execute_query(generated_sql)
        
        # 4. Return
        exec_time = (time.time() - start_time) * 1000
        return QueryResponse(
            sql=generated_sql,
            confidence=0.95,
            result=rows,
            execution_time_ms=exec_time
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
