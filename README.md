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
- Continuous running capability using GitHub Actions

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

5. Run the program locally:
   ```
   python email_replier.py
   ```

## Testing

To test the AI response generation without sending an actual email, you can use the built-in test function:

1. Make sure you have completed the setup steps above, including adding your Google API key to the `config.yaml` file.

2. Run the test command:
   ```
   python email_replier.py --test
   ```

3. The program will generate a response to a sample email inquiry and display it in the console. This allows you to verify that the AI is generating appropriate responses based on your configuration and society information.

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

Please ensure that your `config.yaml` file is kept secure and not shared publicly, as it contains sensitive information like email passwords and API keys. When using GitHub Actions, store sensitive information as GitHub Secrets.

## Continuous Running on GitHub Servers

To run this program continuously on GitHub servers, we use GitHub Actions. This allows the script to run at regular intervals without the need for a dedicated server. Here's how it's set up:

1. The GitHub Actions workflow is defined in `.github/workflows/run_email_replier.yml`.
2. The workflow is scheduled to run every 15 minutes (you can adjust this as needed).
3. Sensitive information (email credentials, API keys) is stored as GitHub Secrets and passed to the script securely.
4. The script runs for a limited time during each execution to avoid exceeding GitHub Actions time limits.

To set up continuous running on GitHub:

1. Fork or push this repository to your GitHub account.
2. Go to your repository's Settings > Secrets and add the following secrets:
   - EMAIL_ADDRESS
   - EMAIL_PASSWORD
   - GOOGLE_API_KEY
3. Update the `config.yaml` file to use these secrets (the workflow will handle this).
4. Commit and push your changes.
5. GitHub Actions will now run the script automatically according to the schedule.

You can monitor the execution in the "Actions" tab of your GitHub repository.

## Disclaimer

This program interacts with email accounts and uses AI to generate responses. Please use it responsibly and in compliance with all relevant laws and regulations. Always review the AI-generated drafts before sending to ensure they meet your standards and accurately represent your society.

## Google API Key Setup

To use this program with Gemini 1.5 Flash, you need to set up a Google API key:

1. Go to the [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click on "Create API key" and copy the generated key
4. Add the API key as a GitHub Secret named GOOGLE_API_KEY

Make sure to keep your API key confidential and never share it publicly.