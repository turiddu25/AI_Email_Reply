import imaplib
import email
import time
import yaml
import google.generativeai as genai
import smtplib
import logging
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up logging
logging.basicConfig(filename='email_replier.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        
        # Override config with environment variables if available
        config['email_address'] = os.environ.get('EMAIL_ADDRESS', config['email_address'])
        config['email_password'] = os.environ.get('EMAIL_PASSWORD', config['email_password'])
        config['google_api_key'] = os.environ.get('GOOGLE_API_KEY', config['google_api_key'])
        
        return config
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

def test_ai_response():
    config = load_config()
    society_info = load_society_info(config['society_info_file'])
    
    # Configure Google Generative AI
    genai.configure(api_key=config['google_api_key'])
    
    test_email_content = {
        'body': "Hello, I'm interested in joining the AI Society. Can you tell me more about your upcoming events and how I can become a member?",
        'subject': "Inquiry about AI Society Membership",
        'from': "test@example.com"
    }
    
    ai_response = generate_ai_response(config['ai_prompt'], test_email_content['body'], society_info)
    
    if ai_response:
        print("Test AI Response:")
        print(f"Subject: Re: {test_email_content['subject']}")
        print(f"To: {test_email_content['from']}")
        print(f"Body:\n{ai_response}")
        return True
    else:
        print("Failed to generate AI response.")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = test_ai_response()
        sys.exit(0 if success else 1)
    
    config = load_config()
    society_info = load_society_info(config['society_info_file'])
    
    # Configure Google Generative AI
    genai.configure(api_key=config['google_api_key'])
    
    imap_server = imaplib.IMAP4_SSL(config['imap_server'])
    
    start_time = time.time()
    max_runtime = 540  # 9 minutes (to stay within GitHub Actions 10-minute limit)
    
    while time.time() - start_time < max_runtime:
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
    
    logging.info("Script reached maximum runtime, shutting down.")
    imap_server.logout()