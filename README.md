# Trend Tracker

A modular Python application that fetches current trending topics from trends24.in (United States) and sends beautifully formatted email summaries with a dark theme.

## Features

- 🔍 Scrapes trending topics from trends24.in
- 📊 Extracts trend names, URLs, and tweet counts
- 📧 Sends beautifully formatted email summaries with dark theme
- ⏰ Includes timestamp information
- 🛡️ Uses environment variables for secure email configuration
- 🏗️ Modular architecture with separate services

## Project Structure

```
trend-tracker/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── src/
│   ├── __init__.py
│   ├── main.py            # Main application logic
│   ├── config.py          # Configuration management
│   ├── trend_fetcher.py   # Trend fetching service
│   ├── email_service.py   # Email sending service
│   └── html_generator.py  # HTML email generation
└── styles/
    └── email.css          # Dark theme email styling
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Then edit the `.env` file with your actual values:

```env
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@example.com
```

Alternatively, set up the following environment variables manually:

- `GMAIL_EMAIL`: Your Gmail address
- `GMAIL_APP_PASSWORD`: Your Gmail app password (not regular password)
- `RECIPIENT_EMAIL`: Email address to send the summary to

#### Windows (Command Prompt):
```cmd
set GMAIL_EMAIL=your-email@gmail.com
set GMAIL_APP_PASSWORD=your-app-password
set RECIPIENT_EMAIL=recipient@example.com
```

#### Windows (PowerShell):
```powershell
$env:GMAIL_EMAIL="your-email@gmail.com"
$env:GMAIL_APP_PASSWORD="your-app-password"
$env:RECIPIENT_EMAIL="recipient@example.com"
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

## Email Design

The email features a modern dark theme design inspired by professional dashboards:

- 🌙 **Dark Theme**: Black background with white text for better readability
- 🎨 **Color-coded Sections**: Different accent colors for different trend categories
- 📱 **Responsive Layout**: Works well on both desktop and mobile email clients
- 🔗 **Interactive Links**: Clickable trend names that open Twitter/X searches
- 📊 **Organized Data**: Clear separation between main trends and max tweets trends

## Dependencies

- `requests`: For web scraping
- `beautifulsoup4`: For HTML parsing
- `lxml`: For faster XML/HTML parsing
- `pytz`: For timezone handling
- `python-dotenv`: For environment variable management
- `smtplib`: For sending emails (built-in)

## License

This project is for educational purposes. Please respect the terms of service of trends24.in.
