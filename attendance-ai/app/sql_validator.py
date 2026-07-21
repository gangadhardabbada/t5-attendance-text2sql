import sqlparse
from fastapi import HTTPException

def validate_sql(generated_sql: str) -> bool:
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
            raise HTTPException(status_code=403, detail=f"Forbidden destructive keyword '{kw}' detected.")
            
    return True
