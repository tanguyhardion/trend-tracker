# Trend Tracker

A simple Python script that fetches current trending topics from trends24.in (United States) and sends a summary via email.

## Features

- 🔍 Scrapes trending topics from trends24.in
- 📊 Extracts trend names, URLs, and tweet counts
- 📧 Sends formatted email summaries (HTML + plain text)
- ⏰ Includes timestamp information
- 🛡️ Uses environment variables for secure email configuration

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Set up the following environment variables:

- `GMAIL_EMAIL`: Your Gmail address
- `GMAIL_APP_PASSWORD`: Your Gmail app password (not regular password)
- `EMAIL_RECIPIENT`: Email address to send the summary to

#### Windows (Command Prompt):
```cmd
set GMAIL_EMAIL=your-email@gmail.com
set GMAIL_APP_PASSWORD=your-app-password
set EMAIL_RECIPIENT=recipient@example.com
```

#### Windows (PowerShell):
```powershell
$env:GMAIL_EMAIL="your-email@gmail.com"
$env:GMAIL_APP_PASSWORD="your-app-password"
$env:EMAIL_RECIPIENT="recipient@example.com"
```

### 3. Gmail App Password Setup

1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account Settings → Security → App passwords
3. Generate a new app password for "Mail"
4. Use this 16-character password as `GMAIL_APP_PASSWORD`

## Usage

Simply run the script:

```bash
python main.py
```

The script will:
1. Fetch current trends from trends24.in
2. Format them into a nice email summary
3. Send the email to the specified recipient

## Output

The email includes:
- Current timestamp from the trends data
- Top 20 trending topics with tweet counts
- Clickable links to Twitter searches
- Both HTML and plain text versions

## Example Output

```
🚀 Starting Trend Tracker...
📊 Fetching trends from trends24.in...
✅ Found 50 trends
📝 Formatting email content...
📧 Sending email...
✅ Email sent successfully to recipient@example.com
🎉 Trend summary sent successfully!
```

## Error Handling

The script handles common errors:
- Network connectivity issues
- Missing environment variables
- Email sending failures
- Website structure changes

## Dependencies

- `requests`: For web scraping
- `beautifulsoup4`: For HTML parsing
- `lxml`: For faster XML/HTML parsing
- `smtplib`: For sending emails (built-in)

## License

This project is for educational purposes. Please respect the terms of service of trends24.in.
