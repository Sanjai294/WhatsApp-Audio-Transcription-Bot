# WhatsApp-Audio-Transcription-Bot
This project provides an automated solution for transcribing audio messages sent via WhatsApp. It allows users to easily convert speech into text using advanced speech-to-text technology powered by Hugging Face’s Whisper model
# WhatsApp Audio Transcription Bot

This project is a WhatsApp bot that allows users to send audio messages, which are then transcribed using the Hugging Face Whisper model. The bot is built using Flask and integrated with Twilio to handle WhatsApp messages. The transcription is performed using the `Whisper` model, which is capable of converting speech to text with high accuracy.

## Features

- **Receive Audio Messages:** The bot receives audio messages sent to a WhatsApp number.
- **Audio Transcription:** The audio message is transcribed to text using the Hugging Face Whisper model.
- **Twilio Integration:** The bot is powered by Twilio for handling WhatsApp interactions.
- **Error Handling:** Robust error handling to ensure smooth interaction and proper error messages when issues occur.

## Requirements

This project uses the following technologies and libraries:
- **Flask:** A lightweight Python web framework used to create the server and handle incoming requests.
- **Twilio:** For sending and receiving WhatsApp messages.
- **Hugging Face Transformers:** For accessing the Whisper model for audio transcription.
- **Librosa:** For loading and processing audio files.
- **PyTorch:** Deep learning framework used for running the Whisper model.

## Setup

### Prerequisites
Make sure you have Python 3.8+ installed. You will also need a Twilio account and API credentials to run the bot.

### Install Dependencies

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/whatsapp-audio-transcription-bot.git
    cd whatsapp-audio-transcription-bot
    ```

2. Create a virtual environment and activate it (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables. You can use the `.env` file for this.

    Create a `.env` file in the root directory of the project with the following variables:

    ```env
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number
    HUGGINGFACE_API_KEY=your_huggingface_api_key
    NGROK_URL=your_ngrok_url  # If using ngrok for local testing
    ```

    - **Twilio:** You need to sign up for a Twilio account and obtain your `ACCOUNT_SID`, `AUTH_TOKEN`, and a WhatsApp-enabled Twilio number.
    - **Hugging Face:** Obtain an API key from [Hugging Face](https://huggingface.co/).
    - **Ngrok:** Optionally, if you're testing locally, use [Ngrok](https://ngrok.com/) to expose your Flask app.

### Running the App

1. Start the Flask application:

    ```bash
    python app.py
    ```

2. Your Flask app will run on `http://127.0.0.1:5000/` for local testing. If you are using Ngrok, it will provide a public URL to interact with your app via WhatsApp.

3. Set up a webhook in your Twilio console to point to the `/sms` and `/media` endpoints of your Flask app. You will need to use the Ngrok public URL or a deployed server URL to receive WhatsApp messages.

    - For the `/sms` endpoint, Twilio will send a request when a text message is received.
    - For the `/media` endpoint, Twilio will send a request when an audio message is received.

4. Test by sending an audio message to your Twilio WhatsApp number. The bot will transcribe the audio and reply with the text.

## Usage

- Send a text message to your Twilio WhatsApp number containing the word **"audio"** to prompt the bot to ask for an audio message.
- Send an audio message to the bot, and it will reply with the transcribed text.

## Error Handling

The bot has built-in error handling to address issues like:
- Missing audio files.
- Network or server errors when interacting with Twilio or the Hugging Face API.
- Invalid audio formats.

In case of an error, the bot will send a message to the user indicating what went wrong.
