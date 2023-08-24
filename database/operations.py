from supabase_py import create_client, Client
from database.constants import SUPABASE_CLIENT, GENERATION_DATA_TABLE_NAME
import json

def write_to_db(prompt, generated_diff):
    if not SUPABASE_CLIENT:
        print(f"Supabase client not initialized, skipping write to DB.")
        return

    row = {
        "prompt": prompt,
        "generated_diff": generated_diff
    }

    # Insert the row into generation_data table
    data = SUPABASE_CLIENT.table(GENERATION_DATA_TABLE_NAME).insert(row).execute()
    status_code = data["status_code"]

    if status_code == 201:
        print(f"Successfully stored data in {GENERATION_DATA_TABLE_NAME}!")
    else:
        print(f"Failed to insert data to {GENERATION_DATA_TABLE_NAME}")
