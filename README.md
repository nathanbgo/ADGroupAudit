Active Directory Group Membership Tracker
This Python script queries Active Directory (AD) for members of a and tracks changes in group membership over time. It stores the results of each query to a CSV file and compares the current members with the previous query, highlighting any differences. This is useful for monitoring and auditing changes in group membership.

Features:
LDAP Query: Connects to an Active Directory server and retrieves the members of a specific group.
CSV Storage: Saves the list of group members to a CSV file for future comparisons.
Change Detection: Compares the current group membership with previous results and outputs any additions or removals.
Error Handling: Includes error handling for Active Directory connection issues and missing CSV files.
Requirements:
Python 3.x
ldap3 library for querying Active Directory
csv for file handling
difflib for comparing changes

Usage:
Configure your AD server, username, password, and group name in the script.
Run the script to query group members and save the results to previous_members.csv.
Run the script again later to compare the current membership with the previous state and detect changes.
