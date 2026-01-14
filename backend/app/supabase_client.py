import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env to ensure SUPABASE_* and WEBHOOK_URL are available when running locally
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

class SupabaseClient:
    def __init__(self):
        self.url = SUPABASE_URL
        self.key = SUPABASE_KEY
        if not self.url or not self.key:
            # Client not configured; remain None and log (print for demo)
            self.client = None
            print("[supabase] SUPABASE_URL or SUPABASE_KEY not found in environment; supabase inserts disabled.")
        else:
            self.client: Client = create_client(self.url, self.key)

    async def insert_record(self, table: str, record: dict):
        if not self.client:
            # In dev, do nothing or log
            print(f"[supabase] Skipping insert (no client): {record}")
            return
        # Supabase client is synchronous; run in thread
        loop = asyncio.get_running_loop()
        def _insert():
            res = self.client.table(table).insert(record).execute()
            return res
        try:
            result = await loop.run_in_executor(None, _insert)
            print(f"[supabase] Inserted record into {table}: {record}")
            return result
        except Exception as e:
            # If the error indicates a missing column (e.g., 'confidence'), try dropping it and retrying once
            err_str = str(e).lower()
            print(f"[supabase] Insert failed: {e}")
            if 'could not find' in err_str or 'column' in err_str:
                # Attempt to remove unknown keys commonly added (like 'confidence') and retry
                rec2 = record.copy()
                if 'confidence' in rec2:
                    rec2.pop('confidence', None)
                    def _insert_retry():
                        return self.client.table(table).insert(rec2).execute()
                    try:
                        result = await loop.run_in_executor(None, _insert_retry)
                        print(f"[supabase] Inserted record into {table} after dropping confidence: {rec2}")
                        return result
                    except Exception as e2:
                        print(f"[supabase] Insert retry failed: {e2}")
            return None
