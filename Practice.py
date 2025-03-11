import imaplib
import email
from email.header import decode_header

# List of email accounts and their credentials
email_accounts = [
    {"email": "email1@example.com", "password": "password1", "imap_server": "imap.example.com"},
    {"email": "email2@example.com", "password": "password2", "imap_server": "imap.example.com"},
    # Add more accounts as needed
]

def get_unread_emails(account):
    try:
        # Connect to the email server
        mail = imaplib.IMAP4_SSL(account["imap_server"])
        mail.login(account["email"], account["password"])
        mail.select("inbox")

        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()

        unread_emails = []
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From")
                    unread_emails.append({"subject": subject, "from": from_})

        mail.logout()
        return unread_emails
    except Exception as e:
        print(f"Failed to retrieve emails for {account['email']}: {e}")
        return []

all_unread_emails = []
for account in email_accounts:
    unread_emails = get_unread_emails(account)
    all_unread_emails.extend(unread_emails)

# Print all unread emails
for email in all_unread_emails:
    print(f"From: {email['from']}, Subject: {email['subject']}")