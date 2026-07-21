import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv('c:/games/t5/.env', override=True)
url = os.getenv('DATABASE_URL')
if not url:
    print("DATABASE_URL not found")
    exit(1)

clean_url = url.replace('DATABASE_URL=', '').replace('"', '')
parsed = urlparse(clean_url)

print(f"Loaded Host: {parsed.hostname}")
masked_url = f"{parsed.scheme}://{parsed.username}:****@{parsed.hostname}:{parsed.port}{parsed.path}"

if parsed.hostname != "aws-0-ap-southeast-1.pooler.supabase.com":
    print(f"Loaded DATABASE_URL (masked): {masked_url}")
    print("Stopping because the loaded host is not the pooler host.")
    exit(0)
