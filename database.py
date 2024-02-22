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

# Create loop to perform operations
choice = ''
while choice.upper() != 'Q':
    # Ask what the user wants to do
    choice = input("\nSelect Operation: (C)hange_Table, (I)nsert, (U)pdate, (D)elete, (Q)uit\n")
    while choice.upper() not in ['C', 'I', 'U', 'D', 'Q']:
        choice = input("Invalid choice. Select Operation: (C)hange_Table, (I)nsert, (U)pdate, (D)elete, (Q)uit\n")

    # Perform the selected operation
    # Change table
    if choice.upper() == 'C':
        table = input("Enter the table name: ")
        # Check if the table exists in the database
        #ret = supabase.table(table).select("*").execute()
        #if ret.json['status_code'] == 404:
            #print("Table changed to " + table)
        #else:
            #print("Table does not exist")
    elif choice.upper() == 'I':
        name = input("Enter the name of the player to insert: ")
        equip_id = input("Enter the equipment id of the player: ")
        if equip_id == "":
            equip_id = None
        else:
            equip_id = int(equip_id)
        ret = supabase.table(table).insert({"name": name, "equip_id": equip_id}).execute()
        print("Insert successful")
    elif choice.upper() == 'U':
        player_id = int(input("Enter the id of the player to update: "))
        name = input("Enter the new name of the player (Leave blank for no change): ")
        equip_id = input("Enter the new equipment id of the player (Leave blank for no change): ")
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
