# YouTube Comment Reply Bot 🤖

A Python-based automation tool that checks comments on a YouTube video, analyzes their sentiment, and automatically replies with an appropriate emoji.

Built with **Flask**, **Selenium**, and **TextBlob**.

## Features

- **Sentiment Analysis**: Uses `TextBlob` to detect if a comment is Positive, Negative, or Neutral.
- **Auto-Reply**: Automatically replies with:
    - 😊 for Positive comments
    - 👍 for Neutral comments
    - 🙏 for Negative comments
- **Smart Skipping**: Skips comments that you have arguably already replied to (basic checking).
- **Manual Login**: Launches a browser for you to safely log in to your Google Account (no credentials stored in code).
- **Web Interface**: Simple Flask UI to input video URLs.

## Prerequisites

- Python 3.8+
- Google Chrome Browser installed.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd youtube-auto-smart-replies
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This will install Flask, Selenium, webdriver-manager, and TextBlob.*

## Usage

1. **Start the Application**:
   ```bash
   python app.py
   ```

2. **Open the Web UI**:
   Open your browser and navigate to: `http://127.0.0.1:5000`

3. **Run the Bot**:
   - Enter the **YouTube Video URL** you want to manage.
   - Click **Fetch Comments**.

4. **Authenticate (Important)**:
   - A new Chrome window will open.
   - **Manually Log In** to your YouTube/Google account in this new window.
   - Once the video page is visible and you are logged in, return to your terminal.
   - You will see a prompt: `"Press Enter in this terminal ONLY after you have successfully logged in..."`.
   - **Press Enter** in the terminal.

5. **Watch**:
   - The bot will scroll through comments and reply automatically.
   - Check the terminal for progress logs.

## Disclaimer

This tool is for educational purposes. Automated actions on YouTube may violate their Terms of Service. Use responsibly and at your own risk.
