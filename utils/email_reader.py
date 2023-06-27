import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import base64
from bs4 import BeautifulSoup

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_code():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("config/token.pickle"):
        with open("config/token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "config/credentials.json", SCOPES
            )  # Change this line
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("config/token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)

    # Call the Gmail API
    results = (
        service.users().messages().list(userId="me", q="subject:amazon.com").execute()
    )
    messages = results.get("messages", [])

    if not messages:
        print("No new messages.")
    else:
        message = messages[0]
        msg = service.users().messages().get(userId="me", id=message["id"]).execute()
        payload = msg["payload"]
        headers = payload["headers"]

        for d in headers:
            if d["name"] == "Subject":
                subject = d["value"]
                print("Subject: ", subject)
            if d["name"] == "From":
                from_ = d["value"]
                print("From: ", from_)

        try:
            # Get the email body
            if "parts" in payload:
                parts = payload["parts"]
                data = parts[0]["body"]["data"]
            else:
                data = payload["body"]["data"]
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)
            soup = BeautifulSoup(decoded_data, "lxml")

            # Get all the <p> tags with numeric contents
            numeric_p_tag = soup.find(
                lambda tag: tag.name == "p" and tag.text.strip().isdigit()
            )

            if numeric_p_tag:
                numeric_text = numeric_p_tag.text.strip()
                print("Numeric text: ", numeric_text)
                return numeric_text
            else:
                print("No numeric <p> tag found.")

        except HttpError as error:
            print(f"An error occurred: {error}")
