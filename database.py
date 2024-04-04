import os
from supabase import Client, create_client

# Database class
class Database:
    # Initialize the database
    def __init__(self):
        self.supabase: Client = create_client("https://wzzpouxkytdjsiopcifw.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6enBvdXhreXRkanNpb3BjaWZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MjQ1ODEsImV4cCI6MjAyMzAwMDU4MX0.bnjccPpvQNTm8RVOXM_Hpd4IVnZnMrbDqJHskKCH30M")
        self.supabase.auth.sign_in_with_password(credentials={"email": "team_19@software.engineering.org", "password": "D1seng@ge"})
        self.table = "players"

    def close(self):
        self.supabase.auth.sign_out()

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
            print(readable_id + "\t" + str(row['player_id']) + "\t\t" + row['name'] + "\t" + str(row['equip_id']) + "\t\t" + str(row['team']))

    # Insert a new row into the table
    def insert(self, player_id: int, name: str) -> bool:
        # Insert the new row
        ret = self.supabase.table(self.table).insert({"player_id": int(player_id), "name": name}).execute()
        # Return whether the insert was successful
        return len(ret.data) > 0

    # Update a row in the table
    def update(self, player_id: int, name: str) -> bool:
        # Create a dictionary to store the data to update
        data = {}
        # If the name is not empty, add it to the dictionary
        if name != "":
            data["name"] = name
        # Update the row
        ret = self.supabase.table(self.table).update(data).eq('player_id', player_id).execute()
        # Return whether the update was successful
        return len(ret.data) > 0

    # Delete a row from the table
    def delete(self, player_id: int) -> bool:
        # Delete the row
        ret = self.supabase.table(self.table).delete().eq('player_id', player_id).execute()
        # Return whether the delete was successful
        return len(ret.data) > 0

    # Check if the player_id exists in the table
    def check_id(self, player_id: int) -> bool:
        # Check if the player_id exists
        if str(player_id) == "":
            return False
        ret = self.supabase.table(self.table).select("*").eq('player_id', player_id).execute()
        # Return whether the player_id exists
        return len(ret.data) > 0

    # Select a row from the table
    def select(self, player_id: int):
        # Select the row
        ret = self.supabase.table(self.table).select("*").eq('player_id', player_id).single().execute()
        # Return the selected row
        return ret.data