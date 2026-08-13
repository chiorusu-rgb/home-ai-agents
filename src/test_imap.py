from tools.email_tools import fetch_unread_emails

print("Attempting to connect to the IMAP server...")
result = fetch_unread_emails(limit=2) 
print("\n--- Result ---")
print(result)
