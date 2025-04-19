import imaplib
import email
import json
import re
from datetime import datetime

EMAIL = "abhishekbanshiwal2005@gmail.com"
PASSWORD = "efne vixb oryp axfr"
IMAP_SERVER = "imap.gmail.com"

def save_payment(entry):
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

def check_payments():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, '(UNSEEN SUBJECT "Payment received")')
    for num in messages[0].split():
        status, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body += part.get_payload(decode=True).decode()
                else:
                    body = msg.get_payload(decode=True).decode()

                match = re.search(r"₹(\d+\.?\d*) received from (.+?) via UPI", body)
                if match:
                    amount = match.group(1)
                    name = match.group(2)
                    entry = {
                        "name": name,
                        "upi": "Auto Detected",
                        "amount": amount,
                        "utr": "Auto",
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "Auto Verified"
                    }
                    save_payment(entry)

    mail.logout()

if __name__ == "__main__":
    check_payments()
  
