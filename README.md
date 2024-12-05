# PDF to Email Sender

This Python project automates the process of sending all PDF files from a specific folder as email attachments. It includes error handling, a graphical user interface (GUI), and ensures proper logging and file management.

## Features

- **SMTP Email Sending**: Sends all PDF files in the folder `C:\an-Drucker-senden` as attachments to the specified email address.
- **GUI Feedback**: Displays status messages in a simple GUI window:
  - 📨 `Sending…` when the process starts.
  - ✅ `Erfolgreich gesendet!` on successful email sending.
  - ❌ `ERROR: [message]` if an error occurs.
- **Error Logging**: Saves detailed error logs in the same folder as the PDF files, with filenames like `_error-log-YYYY-MM-DD-hh-mm-ss.log`.
- **File Management**:
  - Successfully sent PDF files are moved to the subfolder `_sent`.
  - Deletes files in `_sent` older than 30 days upon program start.
- **Environment Variable Usage**: Stores sensitive credentials securely using environment variables.

## Requirements

- **Python 3.7+**
- Required Python packages:
  - `tkinter` (usually included in Python installations)
  - `smtplib` (part of the standard library)
  - `os` (part of the standard library)
  - `shutil` (part of the standard library)
  - `datetime` (part of the standard library)

## Installation

1. Clone or download this repository.
2. Ensure Python is installed on your system.
3. Install any missing dependencies using `pip`.

## Setup

1. Create the following environment variables on your system:
   - `SMTP_USER`: Your email address (e.g., `rechnungern@panda-office.at`).
   - `SMTP_PASSWORD`: Your email password.
2. Replace the SMTP server and port placeholders in the code with the correct values for your email provider:
   - `SMTP_SERVER`: e.g., `smtp.gmail.com`
   - `SMTP_PORT`: e.g., `465` for SSL/TLS.
3. Ensure the folder structure is set up:
   - `C:\an-Drucker-senden`: Folder for PDF files to send.
   - `C:\an-Drucker-senden\_sent`: Subfolder for processed files (automatically created if missing).

## Usage

1. Run the script: `python script_name.py`.
2. The GUI will display the sending progress and any errors.
3. Upon success:
   - All PDF files in the folder are sent as attachments.
   - Files are moved to the `_sent` subfolder.

## Error Handling

- If any error occurs, it is logged in `_error-log-YYYY-MM-DD-hh-mm-ss.log`.
- The error message is also displayed in the GUI for quick feedback.

## Notes

- **Security**: Environment variables are used to avoid hardcoding sensitive credentials in the code.
- **Timeouts**: Email sending is set to timeout after 120 seconds to prevent hanging.

## Example Environment Variable Configuration

```bash
# Linux/macOS
export SMTP_USER="your_sender_email"
export SMTP_PASSWORD="your_password"

# Windows (Command Prompt)
set SMTP_USER=your_sender_email
set SMTP_PASSWORD=your_password
```
