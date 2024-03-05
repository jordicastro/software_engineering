import os
from supabase import Client, create_client

# Create a new client
supabase: Client = create_client("https://wzzpouxkytdjsiopcifw.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6enBvdXhreXRkanNpb3BjaWZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MjQ1ODEsImV4cCI6MjAyMzAwMDU4MX0.bnjccPpvQNTm8RVOXM_Hpd4IVnZnMrbDqJHskKCH30M")
# Sign in as the sever account
supabase.auth.sign_in_with_password(credentials={"email": "team_19@software.engineering.org", "password": "D1seng@ge"})

# Ask the user for the table name
table = input("Enter the table name (players): ")
if table == "":
    table = "players"

# Read the data from the table
ret = supabase.table(table).select("*").execute()

# Format and print the data
print("\nCurrent data in the table:")
print("id\tplayer_id\tname\tequip_id\tteam")
for row in ret.data:
    readable_id = str(row['id']).split("-")[1]
    print(readable_id + "\t" + str(row['player_id']) + "\t\t" + row['name'] + "\t" + str(row['equip_id']) + "\t\t" + str(row['team']))

    # Insert a new row into the table
    def insert(self, player_id, name):
        # Insert the new row
        ret = self.supabase.table(self.table).insert({"player_id": int(player_id), "name": name}).execute()
        # Return whether the insert was successful
        return True

    # Update a row in the table
    def update(self, player_id, name, equip_id):
        # Create a dictionary to store the data to update
        data = {}
        if name != "":
            data["name"] = name
        if equip_id != "" and equip_id != "NULL":
            data["equip_id"] = int(equip_id)
        elif equip_id == "NULL":
            data["equip_id"] = None
        ret = supabase.table(table).update(data).eq('player_id', player_id).execute()
        print("Update successful")
    elif choice.upper() == 'D':
        id = int(input("Enter the id of the player to delete: "))
        ret = supabase.table(table).delete().eq('player_id', id).execute()
        #if ret.json['status_code'] == 200:
            #print("Delete successful")
        #else:
            #print("Delete failed with ")
    elif choice.upper() == 'Q':
        print("Goodbye")

    # Read the data from the table
    ret = supabase.table(table).select("*").execute()

    # Format and print the data
    print("\nUpdated data in table:")
    print("id\tplayer_id\tname\tequip_id\tteam")
    for row in ret.data:
        readable_id = str(row['id']).split("-")[1]
        print(readable_id + "\t" + str(row['player_id']) + "\t\t" + row['name'] + "\t" + str(row['equip_id']) + "\t\t" + str(row['team']))

# Sign out of the server account
supabase.auth.sign_out()
