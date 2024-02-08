import os
from supabase import create_client, create_client

# Create a new client
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

# Read the data from the table
data = supabase.table('countries').select().execute()
