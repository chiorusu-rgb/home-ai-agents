import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

# Load credentials from the .env file
load_dotenv()

def fetch_unread_emails(limit=5):
    """Connects to the IMAP server and fetches the latest unread emails."""
    imap_server = os.getenv("IMAP_SERVER")
    email_account = os.getenv("EMAIL_ACCOUNT")
    email_password = os.getenv("EMAIL_PASSWORD")

    try:
        # Securely connect to the email server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_account, email_password)
        
        # Select the main inbox
        mail.select("inbox")
        
        # Search for unread (UNSEEN) emails
        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        
        results = []
        
        # Fetch the latest emails up to the specified limit
        for e_id in email_ids[-limit:]:
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    # Decode the email subject properly
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # Default to utf-8 if encoding is unknown
                        subject = subject.decode(encoding if encoding else "utf-8")
                        
                    sender = msg.get("From")
                    
                    results.append(f"From: {sender}\nSubject: {subject}\n---")
                    
        mail.logout()
        return "\n".join(results) if results else "No unread emails found."
        
    except Exception as e:
        return f"Error connecting to email: {str(e)}"
