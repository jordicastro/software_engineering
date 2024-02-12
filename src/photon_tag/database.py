import os
from supabase import create_client, Client

# Create a new client
supabase: Client = create_client("https://wzzpouxkytdjsiopcifw.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6enBvdXhreXRkanNpb3BjaWZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MjQ1ODEsImV4cCI6MjAyMzAwMDU4MX0.bnjccPpvQNTm8RVOXM_Hpd4IVnZnMrbDqJHskKCH30M")

# Read the data from the table
ret = supabase.table('countries').select("*").execute()

# Format and print the data
print("\nCurrent data in the table:")
print("id\tname")
for row in ret.data:
    readable_id = str(row['id']).split("-")[1]
    print(readable_id + "\t" + row['name'])

# Ask what the user wants to do
choice = input("\nSelect Operation: (I)nsert, (U)pdate, (D)elete\n")
while choice.upper() not in ['I', 'U', 'D']:
    choice = input("Invalid choice. Select Operation: (I)nsert, (U)pdate, (D)elete\n")

# Perform the operation
if choice.upper() == 'I':
    name = input("Enter the name of the country to insert: ")
    ret = supabase.table('countries').insert({"name": name}).execute()
    print("Insert successful")
elif choice.upper() == 'U':
    old_name = input("Enter the name of the country to update: ")
    new_name = input("Enter the new name of the country: ")
    ret = supabase.table('countries').update({"name": new_name}).eq('name', old_name).execute()
    print("Update successful")
elif choice.upper() == 'D':
    name = input("Enter the name of the country to delete: ")
    ret = supabase.table('countries').delete().eq('name', name).execute()
    print("Delete successful")

# Read the data from the table
ret = supabase.table('countries').select("*").execute()

# Format and print the data
print("\nNew data in the table:")
print("id\tname")
for row in ret.data:
    readable_id = str(row['id']).split("-")[1]
    print(readable_id + "\t" + row['name'])