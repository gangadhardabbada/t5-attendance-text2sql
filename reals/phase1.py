import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('C:/games/t5/.env', override=True)
db_url = os.getenv('DATABASE_URL')

try:
    conn = psycopg2.connect(db_url, sslmode='require')
    cur = conn.cursor()
    
    print("Connection succeeded!")
    
    cur.execute("SELECT version();")
    print("Version:", cur.fetchone()[0])
    
    cur.execute("SELECT current_database();")
    print("Database:", cur.fetchone()[0])
    
    cur.execute("SELECT current_user;")
    print("User:", cur.fetchone()[0])
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)
