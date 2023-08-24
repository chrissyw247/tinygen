from supabase_py import create_client, Client
import os

SUPABASE_URL = "https://ubgdcfrgidlczshndpmj.supabase.co"
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
GENERATION_DATA_TABLE_NAME = "generation_data"
SUPABASE_CLIENT = None

# NOTE: only initialize client if key is present
if SUPABASE_API_KEY:
    SUPABASE_CLIENT = create_client(SUPABASE_URL, SUPABASE_API_KEY)
