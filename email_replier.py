import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yaml
import logging
import time
import google.generativeai as genai

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

logging.basicConfig(filename='email_replier.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    try:
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        raise

def load_society_info(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error loading society info: {e}")
        return ""

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def check_for_new_emails(service):
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        return results.get('messages', [])
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return []

def get_email_content(service, message_id):
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        payload = message['payload']
        headers = payload['headers']
        subject = next(header['value'] for header in headers if header['name'] == 'Subject')
        sender = next(header['value'] for header in headers if header['name'] == 'From')
        
        if 'parts' in payload:
            parts = payload['parts']
            data = parts[0]['body']['data']
        else:
            data = payload['body']['data']
        
        body = base64.urlsafe_b64decode(data).decode()
        
        return {
            'id': message_id,
            'subject': subject,
            'from': sender,
            'body': body
        }
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return None

def generate_ai_response(prompt, email_content, society_info, config):
    try:
        genai.configure(api_key=config['google_api_key'])
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"{prompt}\n\nSociety Information:\n{society_info}\n\nEmail content:\nFrom: {email_content['from']}\nSubject: {email_content['subject']}\nBody: {email_content['body']}\n\nReply:",
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=500,
                temperature=0.7,
            ),
        )
        return response.text
    except Exception as e:
        logging.error(f"Error generating AI response: {e}")
        return f"Thank you for your email regarding '{email_content['subject']}'. We'll get back to you soon."

def create_draft(service, sender_email, recipient_email, subject, body):
    try:
        message = MIMEText(body)
        message['to'] = recipient_email
        message['from'] = sender_email
        message['subject'] = f"Re: {subject}"
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        draft = service.users().drafts().create(userId='me', body={'message': {'raw': raw_message}}).execute()
        logging.info(f"Draft created with ID: {draft['id']}")
        return draft
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return None

def mark_as_read(service, message_id):
    try:
        service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
        logging.info(f"Marked email {message_id} as read")
    except HttpError as error:
        logging.error(f'An error occurred: {error}')

def main():
    config = load_config()
    society_info = load_society_info(config['society_info_file'])
    service = get_gmail_service()
    
    while True:
        try:
            new_emails = check_for_new_emails(service)
            
            for email in new_emails[:config.get('max_emails_per_cycle', 5)]:
                email_content = get_email_content(service, email['id'])
                if email_content:
                    ai_response = generate_ai_response(config['ai_prompt'], email_content, society_info, config)
                    if ai_response:
                        create_draft(
                            service,
                            config['email_address'],
                            email_content['from'],
                            email_content['subject'],
                            ai_response
                        )
                        mark_as_read(service, email['id'])
                        logging.info(f"Created draft reply for email with ID: {email['id']}")
            
            time.sleep(config.get('check_frequency', 300))  # Check every 5 minutes by default
        except Exception as e:
            logging.error(f"An error occurred in the main loop: {e}")
            time.sleep(60)  # Wait a minute before trying again

if __name__ == "__main__":
    main()