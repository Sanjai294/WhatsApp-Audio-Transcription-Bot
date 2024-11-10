from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
from dotenv import load_dotenv
import librosa
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Fetch Twilio credentials and other configurations from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')  # Your Twilio Account SID
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')  # Your Twilio Auth Token
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')  # Your Twilio WhatsApp number

# Initialize Whisper model from Hugging Face transformers
processor = WhisperProcessor.from_pretrained("openai/whisper-large")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large")

# Handle incoming WhatsApp messages
@app.route('/sms', methods=['POST'])
def sms_reply():
    """
    Respond to incoming WhatsApp text messages.
    If the message mentions 'audio', instruct the user to send an audio file for transcription.
    """
    try:
        # Extract the sender's number and the message content from the request
        sender = request.form.get('From')
        message = request.form.get('Body')

        # Create a Twilio MessagingResponse object to send a reply
        response = MessagingResponse()

        # If the message contains the word "audio", prompt the user to send an audio file
        if 'audio' in message.lower():
            response.message('Please send an audio file for transcription.')
        else:
            response.message('Send an audio message, and I will transcribe it for you.')

        return str(response)  # Return the response to Twilio

    except Exception as e:
        # Log the error for debugging
        print(f"Error in sms_reply: {str(e)}")
        response = MessagingResponse()
        response.message("Sorry, there was an error processing your request.")
        return str(response), 500  # Return error message for any exceptions

# Handle incoming media (audio) messages
@app.route('/media', methods=['POST'])
def handle_media():
    """
    Handle audio messages sent via WhatsApp, download the media,
    and transcribe it using the Hugging Face Whisper model.
    """
    try:
        # Extract the media URL from the request (only 1 media file supported per message)
        media_url = request.form.get('MediaUrl0')
        sender = request.form.get('From')

        # If the media URL exists, proceed to download and transcribe the audio file
        if media_url:
            # Download the audio file
            audio_file = download_media(media_url)

            # Transcribe the audio using the Whisper model (Transformers + Torch)
            transcription = transcribe_audio(audio_file)

            # Respond with the transcription of the audio message
            response = MessagingResponse()
            response.message(f'Transcription: {transcription}')
            return str(response)
        
        # If no media was received, return an error response
        return "No audio file received", 400

    except Exception as e:
        # Log the error for debugging
        print(f"Error in handle_media: {str(e)}")
        return "Error processing media. Please try again later.", 500  # Return error message for any exceptions

def download_media(media_url):
    """
    Download the media file (audio) from the provided Twilio URL and save it locally.
    """
    try:
        # Send a GET request to Twilio to retrieve the media content
        media = requests.get(media_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))

        # Check if the media was successfully fetched
        if media.status_code != 200:
            raise Exception(f"Failed to download media. Status code: {media.status_code}")

        # Define the path where the audio file will be saved
        file_path = 'audio_file.mp3'

        # Write the media content to the file
        with open(file_path, 'wb') as f:
            f.write(media.content)

        return file_path  # Return the path to the saved file

    except requests.exceptions.RequestException as e:
        # Handle network-related issues
        print(f"Network error during media download: {str(e)}")
        raise Exception("Network error while downloading media. Please try again later.")
    
    except Exception as e:
        # Log and handle any other issues (file errors, etc.)
        print(f"Error downloading media: {str(e)}")
        raise Exception("Error downloading media. Please try again later.")

def transcribe_audio(audio_file_path):
    """
    Send the audio file to Hugging Face Whisper model for transcription.
    The transcription result is returned as a string.
    """
    try:
        # Load the audio file using librosa
        audio_input, _ = librosa.load(audio_file_path, sr=16000)  # Whisper model expects 16kHz audio input

        # Process the audio input for the Whisper model
        inputs = processor(audio_input, return_tensors="pt", sampling_rate=16000)

        # Generate transcription from the Whisper model
        with torch.no_grad():
            predicted_ids = model.generate(inputs.input_values)

        # Decode the predicted tokens to text
        transcription = processor.decode(predicted_ids[0], skip_special_tokens=True)

        return transcription

    except librosa.util.exceptions.LibrosaError as e:
        # Handle issues with librosa (e.g., invalid audio format or corrupted file)
        print(f"Librosa error: {str(e)}")
        return "Error loading audio file for transcription."

    except torch.errors.TimeoutError as e:
        # Handle issues with model inference (e.g., timeout or memory errors)
        print(f"Torch error during model inference: {str(e)}")
        return "Error during model inference. Please try again later."

    except Exception as e:
        # Log any other errors
        print(f"Error in transcribe_audio: {str(e)}")
        return "Error transcribing the audio. Please try again later."

if __name__ == '__main__':
    """
    Run the Flask app when this script is executed.
    The app will be available at http://127.0.0.1:5000/ for local testing.
    """
    try:
        app.run(debug=True)
    except Exception as e:
        # Log any errors during app startup
        print(f"Error starting Flask app: {str(e)}")
