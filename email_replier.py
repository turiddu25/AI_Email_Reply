import imaplib
import email
import time
import yaml
import google.generativeai as genai
import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up logging
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

def check_for_new_emails(imap_server, email_address, password):
    try:
        imap_server.login(email_address, password)
        imap_server.select('INBOX')
        _, message_numbers = imap_server.search(None, 'UNSEEN')
        return message_numbers[0].split()
    except Exception as e:
        logging.error(f"Error checking for new emails: {e}")
        return []

def get_email_content(imap_server, email_id):
    try:
        _, msg_data = imap_server.fetch(email_id, '(RFC822)')
        email_body = msg_data[0][1]
        email_message = email.message_from_bytes(email_body)
        
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    return {
                        'body': part.get_payload(decode=True).decode(),
                        'subject': email_message['Subject'],
                        'from': email_message['From']
                    }
        else:
            return {
                'body': email_message.get_payload(decode=True).decode(),
                'subject': email_message['Subject'],
                'from': email_message['From']
            }
    except Exception as e:
        logging.error(f"Error getting email content: {e}")
        return None

def generate_ai_response(prompt, email_content, society_info):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"{prompt}\n\nSociety Information:\n{society_info}\n\nEmail content:\n{email_content}\n\nReply:",
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=300,
                temperature=0.7,
            ),
        )
        return response.text
    except Exception as e:
        logging.error(f"Error generating AI response: {e}")
        return None

def create_draft(imap_server, sender_email, recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        draft_folder = "Drafts"
        imap_server.create(draft_folder)
        imap_server.append(draft_folder, '', imaplib.Time2Internaldate(time.time()), str(msg).encode('utf-8'))
        logging.info(f"Draft created for email to {recipient_email}")
    except Exception as e:
        logging.error(f"Error creating draft: {e}")

def mark_as_processed(imap_server, email_id):
    try:
        imap_server.store(email_id, '+FLAGS', '\\Seen')
        logging.info(f"Marked email {email_id} as processed")
    except Exception as e:
        logging.error(f"Error marking email as processed: {e}")

if __name__ == "__main__":
    config = load_config()
    society_info = load_society_info(config['society_info_file'])
    
    # Configure Google Generative AI
    genai.configure(api_key=config['google_api_key'])
    
    imap_server = imaplib.IMAP4_SSL(config['imap_server'])
    
    while True:
        try:
            new_emails = check_for_new_emails(imap_server, config['email_address'], config['email_password'])
            
            for email_id in new_emails[:config.get('max_emails_per_cycle', 5)]:
                email_content = get_email_content(imap_server, email_id)
                if email_content:
                    ai_response = generate_ai_response(config['ai_prompt'], email_content['body'], society_info)
                    if ai_response:
                        create_draft(
                            imap_server,
                            config['email_address'],
                            email_content['from'],
                            f"Re: {email_content['subject']}",
                            ai_response
                        )
                        mark_as_processed(imap_server, email_id)
                        logging.info(f"Created draft reply for email with ID: {email_id}")
            
            time.sleep(config.get('check_frequency', 60))  # Check frequency in seconds
        except Exception as e:
            logging.error(f"An error occurred in the main loop: {e}")
            time.sleep(60)  # Wait a minute before trying again