# AI Email Reply Bot for Artificial Intelligence Society

This Python program automatically detects incoming emails, drafts AI-generated replies, and saves them as drafts for manual review and sending. It's designed to run continuously using GitHub Actions and can be customized for the Artificial Intelligence Society's needs.

## Features

- Automatic email checking using Gmail API
- AI-powered response generation using Google's Generative AI
- Customizable AI prompts with example replies
- Separate file for easily editable society information
- Creation of draft replies instead of automatic sending
- Configurable email checking frequency and processing limits
- Error handling and logging for improved reliability
- Continuous running capability using GitHub Actions

## Setup

1. Clone this repository to your local machine or fork it to your GitHub account.

2. Set up a Google Cloud Project and enable the Gmail API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API for your project
   - Create OAuth 2.0 credentials (Desktop app) and download the client configuration as `credentials.json`

3. Install the required Python packages locally for testing:
   ```
   pip install -r requirements.txt
   ```

4. Configure the `config.yaml` file:
   - Update the `email_address` field with your Gmail address
   - Customize the `ai_prompt` as needed
   - Adjust the `check_frequency` and `max_emails_per_cycle` as desired

5. Edit the `society_info.txt` file:
   - Add detailed information about your Artificial Intelligence Society
   - Include goals, activities, membership benefits, and contact information

6. Set up GitHub Secrets:
   - In your GitHub repository, go to Settings > Secrets and variables > Actions
   - Add the following secrets:
     - `EMAIL_ADDRESS`: Your Gmail address
     - `GOOGLE_API_KEY`: Your Google API key for the Generative AI model
     - `GOOGLE_CREDENTIALS`: The contents of your `credentials.json` file, base64 encoded

7. Push your changes to GitHub:
   ```
   git add .
   git commit -m "Set up AI Email Reply Bot"
   git push
   ```

## Running the Bot

The bot is configured to run automatically every 15 minutes using GitHub Actions. You can also trigger it manually:

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. Select the "Run Email Replier" workflow
4. Click "Run workflow"

## Local Testing

To test the bot locally:

1. Ensure you have the `credentials.json` file in your project directory
2. Run the script:
   ```
   python email_replier.py
   ```

3. The first time you run the script, it will prompt you to authorize access to your Gmail account. Follow the instructions in the console.

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

1. Log into your Gmail account
2. Go to the Drafts folder
3. Review each draft, make any necessary edits
4. Send the emails manually when you're satisfied with the content

## Logging

The program logs its activities and any errors to `email_replier.log`. You can view these logs in the GitHub Actions run details.

## Security Note

Ensure that your `config.yaml` file and `credentials.json` are kept secure and not shared publicly, as they contain sensitive information. The GitHub Secrets feature is used to securely store and use these credentials in the GitHub Actions workflow.

## Disclaimer

This program interacts with email accounts and uses AI to generate responses. Please use it responsibly and in compliance with all relevant laws and regulations. Always review the AI-generated drafts before sending to ensure they meet your standards and accurately represent your society.