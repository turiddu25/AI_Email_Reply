# AI Email Reply Bot for Artificial Intelligence Society

This Python program automatically detects incoming emails, drafts AI-generated replies, and saves them as drafts for manual review and sending. It's designed to run continuously and can be customized for the Artificial Intelligence Society's needs.

## Features

- Automatic email checking using IMAP protocol
- AI-powered response generation using Google's Gemini 1.5 Flash
- Customizable AI prompts with example replies
- Separate file for easily editable society information
- Creation of draft replies instead of automatic sending
- Configurable email checking frequency and processing limits
- Error handling and logging for improved reliability

## Setup

1. Clone this repository to your local machine or server.

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Configure the `config.yaml` file:
   - Enter your email credentials (address, password, IMAP server)
   - Add your Google API key for Gemini 1.5 Flash
   - Customize the AI prompt and example reply as needed
   - Adjust the `check_frequency` and `max_emails_per_cycle` as desired

4. Edit the `society_info.txt` file:
   - Add detailed information about your Artificial Intelligence Society
   - Include goals, activities, membership benefits, and contact information

5. Run the program:
   ```
   python email_replier.py
   ```

## Customization

You can customize the AI's behavior by modifying the following files:

1. `config.yaml`:
   - Adjust the `ai_prompt` to change how the AI generates responses
   - Modify the example reply to match your preferred style
   - Change `check_frequency` and `max_emails_per_cycle` to control email processing

2. `society_info.txt`:
   - Update this file with the latest information about your society
   - The AI will use this information when generating replies

## Manual Review and Sending

The program creates draft replies instead of sending them automatically. To review and send the drafts:

1. Log into your email account
2. Go to the Drafts folder
3. Review each draft, make any necessary edits
4. Send the emails manually when you're satisfied with the content

## Logging

The program logs its activities and any errors to `email_replier.log`. Check this file for debugging information if you encounter any issues.

## Security Note

Please ensure that your `config.yaml` file is kept secure and not shared publicly, as it contains sensitive information like email passwords and API keys.

## Continuous Running

To run this program continuously, you can use a process manager like `systemd` on Linux or create a Windows Service. Alternatively, you can set up a cron job or scheduled task to run the script at regular intervals.

## Disclaimer

This program interacts with email accounts and uses AI to generate responses. Please use it responsibly and in compliance with all relevant laws and regulations. Always review the AI-generated drafts before sending to ensure they meet your standards and accurately represent your society.

## Google API Key Setup

To use this program with Gemini 1.5 Flash, you need to set up a Google API key:

1. Go to the [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click on "Create API key" and copy the generated key
4. Paste the API key in the `config.yaml` file under `google_api_key`

Make sure to keep your API key confidential and never share it publicly.