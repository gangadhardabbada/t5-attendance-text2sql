import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('C:/games/t5/.env', override=True)
db_url = os.getenv('DATABASE_URL')

def execute_query(sql: str):
    conn = psycopg2.connect(db_url, sslmode='require')
    cur = conn.cursor()
    cur.execute(sql)
    
    rows = []
    if cur.description:
        columns = [desc[0] for desc in cur.description]
        for row in cur.fetchall():
            rows.append(dict(zip(columns, row)))
            
    cur.close()
    conn.close()
    return rows
