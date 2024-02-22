import os
from supabase import Client, create_client

# Database class
class Database:
    # Initialize the database
    def __init__(self):
        self.supabase: Client = create_client("https://wzzpouxkytdjsiopcifw.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6enBvdXhreXRkanNpb3BjaWZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MjQ1ODEsImV4cCI6MjAyMzAwMDU4MX0.bnjccPpvQNTm8RVOXM_Hpd4IVnZnMrbDqJHskKCH30M")
        self.supabase.auth.sign_in_with_password(credentials={"email": "team_19@software.engineering.org", "password": "D1seng@ge"})
        self.table = "players"

    # Read the data from the table
    def read(self):
        ret = self.supabase.table(self.table).select("*").execute()
        return ret

    # Print the data from the table
    def print(self):
        ret = self.read()
        print("\nCurrent data in the table:")
        print("id\tplayer_id\tname\tequip_id\tteam")
        for row in ret.data:
            readable_id = str(row['id']).split("-")[1]
            print(readable_id + "\t" + str(row['player_id']) + "\t\t" + row['name'] + "\t" + str(row['equip_id']) + "\t\t" + str(row['team'])

    # Insert a new row into the table
    def insert(self, name, equip_id):
        # If the equip_id is empty, set it to None (NULL)
        if equip_id == "":
            equip_id = None
        else:
            equip_id = int(equip_id)
        # Insert the new row
        ret = supabase.table(table).insert({"name": name, "equip_id": equip_id}).execute()
        # Return whether the insert was successful
        return ret.json['status_code'] == 200

    # Update a row in the table
    def update(self, player_id, name, equip_id):
        # Create a dictionary to store the data to update
        data = {}
        # If the name is not empty, add it to the dictionary
        if name != "":
            data["name"] = name
        # If the equip_id is not empty and not "NULL", add it to the dictionary
        if equip_id != "" and equip_id != "NULL":
            data["equip_id"] = int(equip_id)
        # If the equip_id is "NULL", set it to None (NULL)
        elif equip_id == "NULL":
            data["equip_id"] = None
        # Update the row
        ret = supabase.table(table).update(data).eq('player_id', player_id).execute()
        # Return whether the update was successful
        return ret.json['status_code'] == 200

    # Delete a row from the table
    def delete(self, player_id):
        # Delete the row
        ret = supabase.table(table).delete().eq('player_id', id).execute()
        # Return whether the delete was successful
        return ret.json['status_code'] == 200

    # Read the data from the table
    ret = supabase.table(table).select("*").execute()
