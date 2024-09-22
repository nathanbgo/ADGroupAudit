import csv
import difflib
from ldap3 import Server, Connection, ALL
import os
from dotenv import load_dotenv

# Sets LDAP information from .env file, rather than hardcoding credentials into script

path_for_creds = ('Creds.env')
load_dotenv(path_for_creds)
username = os.getenv("LDAP_USER")
password = os.getenv("LDAP_PASS")
ad_server = os.getenv("DOMAIN")
group_name = os.getenv("GROUP")

# Function to query Active Directory group members

def query_group_members(group_name, ad_server, user, password):
    server = Server(ad_server, get_info=ALL)
    conn = Connection(server, user=user, password=password, auto_bind=True)
    
    # Search for the group and its members
    
    search_filter = f'(memberOf=CN={group_name},CN=Users,DC=example,DC=com)'
    conn.search('DC=example,DC=com', search_filter, attributes=['sAMAccountName'])

    members = [entry['attributes']['sAMAccountName'][0] for entry in conn.entries]
    
    return members

# Function to save group members to a CSV file

def save_to_csv(filename, members):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['sAMAccountName'])
        for member in members:
            writer.writerow([member])

# Function to load group members from a CSV file

def load_members_from_csv(filename):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return [row[0] for row in reader]

# Function to compare the old and new members

def compare_members(old_members, new_members):
    diff = list(difflib.unified_diff(old_members, new_members, lineterm=''))
    return diff

def main():
    
    # File to store the previous members list
    
    filename = 'previous_members.csv'
    
    # Query the current group members from Active Directory
    
    new_members = query_group_members(group_name, ad_server, username, password)

    try:
        # Load previous members from file
        
        old_members = load_members_from_csv(filename)
    except FileNotFoundError:
        print("No previous data found, creating a new record.")
        old_members = []
    
    # Compare old and new members
    
    diff = compare_members(old_members, new_members)
    
    if diff:
        print("Changes found:")
        for line in diff:
            print(line)
    else:
        print("No changes found.")
    
    # Save the current group members for future comparisons
    save_to_csv(filename, new_members)

if __name__ == "__main__":
    main()
