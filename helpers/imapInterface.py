import imaplib
import os


def openConnection():
    try:
        print("Opening connection")

        username = os.environ.get("INBOX_1_USER")
        password = os.environ.get("INBOX_1_PASSWORD")
        imap_server = os.environ.get("INBOX_1_IMAP_SERVER")
        imap_port = os.environ.get("INBOX_1_IMAP_PORT", "993")

        print("Open IMAP Connection")
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(username, password)

        print("Open Mailbox")
        mail.select("INBOX", readonly=True)

        return mail
    except Exception as e:
        print(e)
        print("Connection error. Terminating..")


def closeConnection(mail):
    try:
        print("Closing connection")
        mail.close()
        mail.logout()

        print("Connection closed")
    except Exception as e:
        print(e)
        print("Connection error. Terminating..")
