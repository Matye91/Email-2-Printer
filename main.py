import os
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tkinter import Tk, Label
from datetime import datetime, timedelta

# Constants
PDF_FOLDER = r"C:\an-Drucker-senden"
SENT_FOLDER = os.path.join(PDF_FOLDER, "_sent")
LOG_FILE_TEMPLATE = os.path.join(PDF_FOLDER, "_error-log-{timestamp}.log")
SMTP_SERVER = "imap.easyname.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER_RECHNUNGEN")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD_RECHNUNGEN")
RECIPIENT_EMAIL = "01762476800@print.brother.com"

# GUI Setup
def update_gui(message):
    label.config(text=message)
    root.update()

root = Tk()
root.title("PDF Sender")
label = Label(root, text="Startet... ", font=("Arial", 14))
label.pack(padx=20, pady=20)

def log_error(message):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    log_file = LOG_FILE_TEMPLATE.format(timestamp=timestamp)
    with open(log_file, "w") as f:
        f.write(message)

def send_email_with_attachments():
    update_gui("📨 Sending... ")
    try:
        # Check and clean old files in SENT_FOLDER
        if not os.path.exists(SENT_FOLDER):
            os.makedirs(SENT_FOLDER)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        for file in os.listdir(SENT_FOLDER):
            file_path = os.path.join(SENT_FOLDER, file)
            if os.path.isfile(file_path) and datetime.fromtimestamp(os.path.getmtime(file_path)) < thirty_days_ago:
                os.remove(file_path)
        
        # Collect PDF files
        pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
        if not pdf_files:
            update_gui("❌ ERROR: Keine PDF-Dateien gefunden.")
            log_error("No PDF files found.")
            return
        
        # Prepare email
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = "zu Drucken"

        for pdf_file in pdf_files:
            file_path = os.path.join(PDF_FOLDER, pdf_file)
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={pdf_file}")
            msg.attach(part)
        
        # Send email using SMTP over TLS
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=120) as server:
            try:
                server.ehlo()  # Identify with the server
                server.starttls()  # Start TLS encryption
                server.ehlo()  # Re-identify after starting TLS
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(SMTP_USER, RECIPIENT_EMAIL, msg.as_string())
            except smtplib.SMTPException as e:
                log_error(f"SMTP error: {e}")
                update_gui(f"❌ SMTP ERROR: {e}")
                return
        
        # Move files to SENT_FOLDER
        for pdf_file in pdf_files:
            shutil.move(os.path.join(PDF_FOLDER, pdf_file), os.path.join(SENT_FOLDER, pdf_file))

        # Delete old error logs
        delete_error_logs()

        update_gui("✅ Erfolgreich gesendet!")

    except smtplib.SMTPConnectError as e:
        log_error(f"Connection error: {e}")
        update_gui(f"❌ ERROR: Connection error.")
    except smtplib.SMTPException as e:
        log_error(f"SMTP error: {e}")
        update_gui(f"❌ ERROR: {e}")
    except Exception as e:
        log_error(f"General error: {e}")
        update_gui(f"❌ ERROR: {e}")


def delete_error_logs():
    """Delete old error-log files in the PDF folder."""
    for file in os.listdir(PDF_FOLDER):
        if file.startswith("_error-log-") and file.endswith(".log"):
            file_path = os.path.join(PDF_FOLDER, file)
            try:
                os.remove(file_path)
            except Exception as e:
                # Log if there's an issue deleting a log file (optional)
                log_error(f"Failed to delete error log {file}: {e}")



# Start sending process
root.after(100, send_email_with_attachments)
root.mainloop()
