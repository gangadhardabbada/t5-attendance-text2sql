from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
import sqlparse
from reals.predict import T5SQLPredictor
from dotenv import load_dotenv

load_dotenv('C:/games/t5/.env', override=True)
db_url = os.getenv('DATABASE_URL')

app = FastAPI(title="T5 Text-to-SQL API")
predictor = T5SQLPredictor()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql: str
    confidence: float
    result: list = None

@app.post("/predict", response_model=QueryResponse)
def predict_sql(req: QueryRequest):
    try:
        # 1. Generate SQL
        generated_sql = predictor.predict(req.question)
        
        # 2. Validate SQL & Reject non-SELECT
        parsed = sqlparse.parse(generated_sql)
        if not parsed:
            raise HTTPException(status_code=400, detail="Could not parse generated SQL")
            
        stmt_type = parsed[0].get_type().upper()
        if stmt_type != 'SELECT':
            raise HTTPException(status_code=403, detail=f"Operation {stmt_type} is forbidden. Only SELECT is allowed.")
            
        forbidden_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE', 'CREATE']
        upper_sql = generated_sql.upper()
        for kw in forbidden_keywords:
            if kw in upper_sql:
                raise HTTPException(status_code=403, detail="Forbidden destructive keyword detected.")
        
        # 3. Execute validated SQL
        conn = psycopg2.connect(db_url, sslmode='require')
        cur = conn.cursor()
        cur.execute(generated_sql)
        
        rows = []
        if cur.description:
            columns = [desc[0] for desc in cur.description]
            for row in cur.fetchall():
                rows.append(dict(zip(columns, row)))
                
        cur.close()
        conn.close()
        
        # 4. Return JSON
        return QueryResponse(
            sql=generated_sql,
            confidence=0.95, # Mock confidence for now
            result=rows
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
